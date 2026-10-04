from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from icm_audit import AUDIT_CONTRACT_VERSION, AUDIT_DIR, PROPOSAL_FILE, audit_repository
from icm_graph_render import render_projections, write_projections
from icm_graph_store import graph_root, load_graph, write_graph
from icm_graph_validate import graph_status, validate_graph
from icm_io import safe_repo_path
from icm_source_state import (
    SourceStateError,
    build_source_state,
    load_source_state,
    source_state_path,
    write_source_state,
)


class InitConflict(ValueError):
    pass


def _proposal_path(root: Path) -> Path:
    return safe_repo_path(root, AUDIT_DIR / PROPOSAL_FILE)


def load_candidate(root: Path) -> tuple[dict[str, Any], str, int, str]:
    proposal = _proposal_path(root)
    if proposal.is_file():
        value = json.loads(proposal.read_text(encoding="utf-8"))
        if not isinstance(value, dict) or not isinstance(value.get("graph"), dict):
            raise InitConflict(f"{proposal.relative_to(root)}: expected audit report with graph object")
        if value.get("audit_contract_version") != AUDIT_CONTRACT_VERSION:
            raise InitConflict(
                f"{proposal.relative_to(root)}: audit contract is missing or stale; rerun icm audit --write"
            )
        fresh = audit_repository(root)
        if value.get("input_fingerprint") != fresh.get("input_fingerprint"):
            raise InitConflict(
                f"{proposal.relative_to(root)}: audit inputs changed after proposal creation; rerun icm audit --write"
            )
        return (
            value["graph"],
            str(proposal.relative_to(root)),
            int(value["audit_contract_version"]),
            str(value["input_fingerprint"]),
        )

    report = audit_repository(root)
    if report["status"] == "FAIL":
        raise InitConflict("fresh repository audit failed; cannot initialize canonical graph")
    return (
        report["graph"],
        "fresh-audit",
        int(report["audit_contract_version"]),
        str(report["input_fingerprint"]),
    )


def _canonical_existing_files(root: Path) -> bool:
    base = graph_root(root)
    return any((base / name).exists() for name in ("nodes.jsonl", "edges.jsonl", "schema-version.json"))


def plan_init(root: Path) -> dict[str, Any]:
    graph, source, audit_contract_version, input_fingerprint = load_candidate(root)
    diagnostics = validate_graph(root, graph)
    status = graph_status(diagnostics)
    if status == "FAIL":
        failures = [item for item in diagnostics if item["severity"] == "FAIL"]
        detail = "; ".join(f"{item['code']}:{item['subject']}" for item in failures[:5])
        raise InitConflict(f"candidate graph is invalid: {detail}")

    projections = render_projections(root, graph)
    existing_present = _canonical_existing_files(root)
    existing = load_graph(root) if existing_present else {"schema_version": 1, "nodes": [], "edges": []}
    same_graph = existing_present and existing == graph

    if existing_present and not same_graph:
        raise InitConflict(
            "canonical graph already exists and differs from candidate; "
            "use a future explicit migration/update workflow rather than overwriting during init"
        )

    desired_source_state = build_source_state(
        audit_contract_version=audit_contract_version,
        input_fingerprint=input_fingerprint,
        graph=graph,
    )
    source_state_change = True
    source_path = source_state_path(root)
    if source_path.exists():
        try:
            source_state_change = load_source_state(root) != desired_source_state
        except SourceStateError:
            # Explicit init --write may repair a malformed receipt when the
            # canonical graph itself still matches the validated candidate.
            source_state_change = True

    projection_changes: list[str] = []
    for name, content in sorted(projections.items()):
        path = safe_repo_path(root, Path(".icm/generated") / name)
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            projection_changes.append(str(path.relative_to(root)))

    graph_changes = [] if same_graph else [
        ".icm/graph/nodes.jsonl",
        ".icm/graph/edges.jsonl",
        ".icm/graph/schema-version.json",
    ]

    source_changes = [str(source_path.relative_to(root.resolve()))] if source_state_change else []

    return {
        "status": status,
        "source": source,
        "graph": graph,
        "source_state": desired_source_state,
        "diagnostics": diagnostics,
        "changes": graph_changes + projection_changes + source_changes,
        "already_initialized": same_graph and not projection_changes and not source_state_change,
    }


def initialize_repository(root: Path, *, write: bool = False) -> dict[str, Any]:
    plan = plan_init(root)
    if not write:
        return {**plan, "written": []}

    graph = plan["graph"]
    written: list[str] = []
    if plan["changes"]:
        existing_present = _canonical_existing_files(root)
        existing = load_graph(root) if existing_present else None
        if existing is None:
            write_graph(root, nodes=graph["nodes"], edges=graph["edges"], schema_version=graph["schema_version"])
            written.extend([
                ".icm/graph/nodes.jsonl",
                ".icm/graph/edges.jsonl",
                ".icm/graph/schema-version.json",
            ])
        elif existing != graph:
            raise InitConflict("canonical graph changed between plan and write")

        written.extend(write_projections(root, graph))

        if write_source_state(root, plan["source_state"]):
            written.append(str(source_state_path(root).relative_to(root.resolve())))

    return {**plan, "written": sorted(set(written)), "already_initialized": not written}
