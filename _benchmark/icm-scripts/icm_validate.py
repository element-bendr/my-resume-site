from __future__ import annotations

from pathlib import Path
from typing import Any

from icm_audit import AUDIT_CONTRACT_VERSION, audit_input_fingerprint
from icm_graph_render import ProjectionError, render_projections
from icm_graph_store import GraphStoreError, graph_root, load_graph
from icm_graph_validate import graph_status, validate_graph
from icm_protected import protected_resources, validate_protected_changes
from icm_lifecycle import validate_lifecycle
from icm_io import safe_repo_path
from workflow_lib import state_files, validate_state
from workflow_selection import validate_index
from icm_source_state import SourceStateError, graph_fingerprint, load_source_state


def _diag(severity: str, code: str, subject: str, message: str) -> dict[str, str]:
    return {"severity": severity, "code": code, "subject": subject, "message": message}


def _canonical_graph_state(root: Path) -> str:
    base = graph_root(root)
    names = ("nodes.jsonl", "edges.jsonl", "schema-version.json")
    present = [name for name in names if (base / name).exists()]
    if not present:
        return "absent"
    if len(present) == len(names):
        return "complete"
    return "partial"


def _folder_workflow_diagnostics(root: Path) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    try:
        paths = state_files(root, include_completed=True)
    except Exception as exc:
        return [_diag("FAIL", "workflow.discovery", "workflow", str(exc))]

    for path in paths:
        historical = "workflow/completed/" in path.as_posix()
        for error in validate_state(root, path, historical=historical):
            diagnostics.append(_diag("FAIL", "workflow.state", str(path.relative_to(root)), error))
    for error in validate_index(root):
        diagnostics.append(_diag("FAIL", "workflow.index", "workflow/index.json", error))
    return diagnostics




def _source_state_diagnostics(root: Path, graph: dict[str, Any]) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    try:
        state = load_source_state(root)
    except (SourceStateError, OSError, ValueError) as exc:
        return [_diag("FAIL", "graph.source-state", ".icm/state/source.json", str(exc))]

    if state.get("audit_contract_version") != AUDIT_CONTRACT_VERSION:
        diagnostics.append(
            _diag(
                "FAIL",
                "graph.source-contract-stale",
                ".icm/state/source.json",
                (
                    f"audit contract changed from {state.get('audit_contract_version')!r} "
                    f"to {AUDIT_CONTRACT_VERSION}; refresh graph state"
                ),
            )
        )

    actual_graph_fingerprint = graph_fingerprint(graph)
    if state.get("graph_fingerprint") != actual_graph_fingerprint:
        diagnostics.append(
            _diag(
                "FAIL",
                "graph.untracked-mutation",
                ".icm/graph",
                "canonical graph differs from the last compiler-written graph fingerprint",
            )
        )

    try:
        current_input_fingerprint, _ = audit_input_fingerprint(root)
    except (OSError, ValueError) as exc:
        diagnostics.append(
            _diag(
                "FAIL",
                "graph.source-check",
                ".icm/state/source.json",
                f"unable to fingerprint current audit inputs: {exc}",
            )
        )
    else:
        if state.get("input_fingerprint") != current_input_fingerprint:
            diagnostics.append(
                _diag(
                    "FAIL",
                    "graph.source-stale",
                    ".icm/graph",
                    "repository audit inputs changed after canonical graph initialization",
                )
            )

    return diagnostics

def _unresolved_diagnostics(graph: dict[str, Any]) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    for node in graph.get("nodes", []):
        if not isinstance(node, dict) or node.get("type") != "unresolved":
            continue
        node_id = str(node.get("id", "unresolved"))
        if node.get("status") == "blocking":
            diagnostics.append(
                _diag("FAIL", "graph.unresolved-blocking", node_id, "blocking unresolved project state")
            )
        else:
            diagnostics.append(
                _diag("WARN", "graph.unresolved", node_id, "unresolved project state remains")
            )
    return diagnostics


def _acceptance_diagnostics(graph: dict[str, Any]) -> list[dict[str, str]]:
    nodes = {
        node.get("id"): node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    evidence_sources: dict[str, list[str]] = {}
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict) or edge.get("type") not in {"satisfies", "validates"}:
            continue
        source = edge.get("from")
        target = edge.get("to")
        if source in nodes and target in nodes and nodes[source].get("type") == "evidence":
            evidence_sources.setdefault(target, []).append(source)

    diagnostics: list[dict[str, str]] = []
    for node_id, node in sorted(nodes.items()):
        if node.get("type") != "acceptance_criterion":
            continue
        status = node.get("status")
        if status in {"satisfied", "certified", "complete", "completed"} and not evidence_sources.get(node_id):
            diagnostics.append(
                _diag(
                    "FAIL",
                    "acceptance.claim-without-evidence",
                    node_id,
                    f"acceptance criterion claims status {status!r} without linked evidence",
                )
            )
    return diagnostics


def _projection_diagnostics(root: Path, graph: dict[str, Any]) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    try:
        expected = render_projections(root, graph)
    except ProjectionError as exc:
        return [_diag("FAIL", "projection.unrenderable", ".icm/generated", str(exc))]

    try:
        generated_root = safe_repo_path(root, ".icm/generated")
    except ValueError as exc:
        return [_diag("FAIL", "projection.path", ".icm/generated", str(exc))]

    for name, content in sorted(expected.items()):
        try:
            path = safe_repo_path(root, Path(".icm/generated") / name)
        except ValueError as exc:
            diagnostics.append(_diag("FAIL", "projection.path", f".icm/generated/{name}", str(exc)))
            continue
        relative = str(path.relative_to(root))
        if not path.is_file():
            diagnostics.append(_diag("FAIL", "projection.missing", relative, "generated projection is missing"))
            continue
        current = path.read_text(encoding="utf-8")
        if current != content:
            diagnostics.append(_diag("FAIL", "projection.drift", relative, "generated projection differs from canonical graph"))
    return diagnostics


def validate_repository(root: Path, *, changed_paths: list[str] | None = None, approvals: set[str] | None = None) -> dict[str, Any]:
    root = root.resolve()
    diagnostics: list[dict[str, str]] = []
    graph: dict[str, Any] | None = None

    graph_state = _canonical_graph_state(root)
    if graph_state == "absent":
        diagnostics.append(
            _diag(
                "FAIL",
                "graph.missing",
                ".icm/graph",
                "canonical graph is not initialized; run icm init --write first",
            )
        )
    else:
        try:
            graph = load_graph(root)
        except (GraphStoreError, OSError, ValueError) as exc:
            diagnostics.append(_diag("FAIL", "graph.load", ".icm/graph", str(exc)))

    if graph is not None:
        diagnostics.extend(validate_graph(root, graph))
        diagnostics.extend(_source_state_diagnostics(root, graph))
        diagnostics.extend(_unresolved_diagnostics(graph))
        diagnostics.extend(_acceptance_diagnostics(graph))
        diagnostics.extend(validate_lifecycle(graph))
        resources = protected_resources(graph)
        if resources and changed_paths is None:
            diagnostics.append(
                _diag(
                    "WARN",
                    "protected.diff-not-evaluated",
                    ".icm/graph",
                    "protected resources exist but no changed-path set was supplied",
                )
            )
        elif changed_paths is not None:
            diagnostics.extend(validate_protected_changes(graph, changed_paths, approvals=approvals or set()))
        if graph_status(diagnostics) != "FAIL":
            diagnostics.extend(_projection_diagnostics(root, graph))
        else:
            # Projection drift is meaningless when canonical graph itself is invalid.
            pass

    diagnostics.extend(_folder_workflow_diagnostics(root))
    diagnostics.sort(key=lambda item: (0 if item["severity"] == "FAIL" else 1, item["code"], item["subject"], item["message"]))

    status = "FAIL" if any(item["severity"] == "FAIL" for item in diagnostics) else (
        "WARN" if any(item["severity"] == "WARN" for item in diagnostics) else "PASS"
    )
    return {"status": status, "diagnostics": diagnostics}
