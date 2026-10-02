from __future__ import annotations

from pathlib import Path
from typing import Any

from icm_audit import audit_repository
from icm_graph_render import ProjectionError, render_projections, write_projections
from icm_graph_store import GraphStoreError, load_graph, replace_graph
from icm_io import safe_repo_path
from icm_source_state import (
    SourceStateError,
    build_source_state,
    graph_fingerprint,
    load_source_state,
    source_state_path,
    write_source_state,
)


class RefreshConflict(ValueError):
    pass


def plan_refresh(root: Path) -> dict[str, Any]:
    root = root.resolve()
    try:
        current_graph = load_graph(root)
    except (GraphStoreError, OSError, ValueError) as exc:
        raise RefreshConflict(f"cannot load canonical graph: {exc}") from exc

    if not current_graph.get("nodes") and not current_graph.get("edges"):
        raise RefreshConflict("canonical graph is not initialized; use icm init first")

    try:
        current_source_state = load_source_state(root)
    except (SourceStateError, OSError, ValueError) as exc:
        raise RefreshConflict(
            f"cannot prove compiler ownership of canonical graph: {exc}; "
            "repair an unchanged graph with icm init --write first"
        ) from exc

    report = audit_repository(root)
    if report["status"] == "FAIL":
        raise RefreshConflict("fresh repository audit failed; refusing graph refresh")

    candidate_graph = report["graph"]
    try:
        rendered = render_projections(root, candidate_graph)
    except ProjectionError as exc:
        raise RefreshConflict(f"candidate graph cannot be rendered safely: {exc}") from exc

    current_fingerprint = graph_fingerprint(current_graph)
    candidate_fingerprint = graph_fingerprint(candidate_graph)
    recorded_fingerprint = current_source_state["graph_fingerprint"]

    recovery_mode = False
    if current_fingerprint != recorded_fingerprint:
        if current_fingerprint != candidate_fingerprint:
            raise RefreshConflict(
                "canonical graph has untracked changes and does not match the fresh audit candidate; "
                "refusing to overwrite it"
            )
        recovery_mode = True

    desired_source_state = build_source_state(
        audit_contract_version=int(report["audit_contract_version"]),
        input_fingerprint=str(report["input_fingerprint"]),
        graph=candidate_graph,
    )

    changes: list[str] = []
    graph_changed = current_graph != candidate_graph
    if graph_changed:
        changes.extend([
            ".icm/graph/nodes.jsonl",
            ".icm/graph/edges.jsonl",
            ".icm/graph/schema-version.json",
        ])

    for name, content in sorted(rendered.items()):
        path = safe_repo_path(root, Path(".icm/generated") / name)
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current != content:
            changes.append(str(path.relative_to(root)))

    source_path = source_state_path(root)
    if current_source_state != desired_source_state:
        changes.append(str(source_path.relative_to(root)))

    return {
        "status": report["status"],
        "current_graph": current_graph,
        "candidate_graph": candidate_graph,
        "source_state": desired_source_state,
        "changes": changes,
        "graph_changed": graph_changed,
        "recovery_mode": recovery_mode,
        "already_fresh": not changes,
        "written": [],
    }


def refresh_repository(root: Path, *, write: bool = False) -> dict[str, Any]:
    root = root.resolve()
    plan = plan_refresh(root)
    if not write:
        return plan

    # Recheck the graph immediately before mutation so a concurrent/manual
    # change cannot race the dry planning phase.
    try:
        live_graph = load_graph(root)
    except (GraphStoreError, OSError, ValueError) as exc:
        raise RefreshConflict(f"canonical graph changed before refresh write: {exc}") from exc
    if live_graph != plan["current_graph"]:
        raise RefreshConflict("canonical graph changed after refresh planning; refusing write")

    written: list[str] = []
    candidate = plan["candidate_graph"]

    if live_graph != candidate:
        try:
            replace_graph(
                root,
                nodes=candidate["nodes"],
                edges=candidate["edges"],
                schema_version=candidate["schema_version"],
                expected_current=live_graph,
            )
        except (GraphStoreError, OSError, ValueError) as exc:
            raise RefreshConflict(f"canonical graph replacement failed: {exc}") from exc
        written.extend([
            ".icm/graph/nodes.jsonl",
            ".icm/graph/edges.jsonl",
            ".icm/graph/schema-version.json",
        ])

    # If a process interruption occurs after graph promotion, the next refresh
    # may enter recovery_mode only when the graph exactly matches a fresh audit.
    written.extend(write_projections(root, candidate))
    if write_source_state(root, plan["source_state"]):
        written.append(str(source_state_path(root).relative_to(root)))

    return {
        **plan,
        "written": sorted(set(written)),
        "already_fresh": not written,
    }
