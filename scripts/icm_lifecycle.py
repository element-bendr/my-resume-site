from __future__ import annotations

from typing import Any

WORKFLOW_STATUSES = {"planned", "active", "blocked", "certified", "completed"}
STAGE_STATUSES = {"pending", "active", "blocked", "certified", "stale"}
TASK_STATUSES = {"pending", "active", "blocked", "completed", "certified", "stale"}

ALLOWED_STATUSES = {
    "workflow": WORKFLOW_STATUSES,
    "stage": STAGE_STATUSES,
    "task": TASK_STATUSES,
}

TERMINAL_STATUSES = {
    "workflow": {"certified", "completed"},
    "stage": {"certified"},
    "task": {"completed", "certified"},
}


def _diag(code: str, subject: str, message: str) -> dict[str, str]:
    return {"severity": "FAIL", "code": code, "subject": subject, "message": message}


def _terminal(node: dict[str, Any]) -> bool:
    node_type = node.get("type")
    return node.get("status") in TERMINAL_STATUSES.get(node_type, set())


def validate_lifecycle(graph: dict[str, Any]) -> list[dict[str, str]]:
    nodes = {
        node.get("id"): node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    edges = [edge for edge in graph.get("edges", []) if isinstance(edge, dict)]
    diagnostics: list[dict[str, str]] = []

    execution = {
        node_id: node
        for node_id, node in nodes.items()
        if node.get("type") in ALLOWED_STATUSES
    }

    for node_id, node in sorted(execution.items()):
        node_type = node.get("type")
        status = node.get("status")
        if status not in ALLOWED_STATUSES[node_type]:
            diagnostics.append(
                _diag(
                    "lifecycle.invalid-status",
                    node_id,
                    f"{node_type} status {status!r} is not allowed",
                )
            )

    for edge in edges:
        edge_type = edge.get("type")
        source_id = edge.get("from")
        target_id = edge.get("to")
        source = execution.get(source_id)
        target = execution.get(target_id)

        if edge_type == "depends_on" and source is not None and target is not None:
            source_status = source.get("status")
            if source_status in {"active", "certified", "completed"} and not _terminal(target):
                diagnostics.append(
                    _diag(
                        "lifecycle.prerequisite-not-ready",
                        str(source_id),
                        f"{source_id} is {source_status!r} but prerequisite {target_id} is not terminal",
                    )
                )

        if edge_type == "blocks" and target is not None:
            blocker = nodes.get(source_id)
            if blocker is None:
                continue
            blocker_terminal = _terminal(blocker) if blocker.get("type") in ALLOWED_STATUSES else blocker.get("status") in {"resolved", "closed"}
            if _terminal(target) and not blocker_terminal:
                diagnostics.append(
                    _diag(
                        "lifecycle.terminal-while-blocked",
                        str(target_id),
                        f"{target_id} is terminal while blocker {source_id} remains unresolved",
                    )
                )

    contained: dict[str, list[dict[str, Any]]] = {}
    for edge in edges:
        if edge.get("type") != "contains":
            continue
        source = edge.get("from")
        target = edge.get("to")
        if source in execution and target in execution:
            contained.setdefault(str(source), []).append(execution[target])

    for parent_id, children in sorted(contained.items()):
        parent = execution[parent_id]
        parent_type = parent.get("type")
        if not _terminal(parent):
            continue
        for child in children:
            if not _terminal(child):
                diagnostics.append(
                    _diag(
                        "lifecycle.terminal-parent-has-open-child",
                        parent_id,
                        f"terminal {parent_type} contains non-terminal child {child.get('id')}",
                    )
                )

    satisfied: set[str] = set()
    for edge in edges:
        if edge.get("type") not in {"satisfies", "validates"}:
            continue
        source = nodes.get(edge.get("from"))
        target = nodes.get(edge.get("to"))
        if source and target and source.get("type") == "evidence" and target.get("type") == "acceptance_criterion":
            satisfied.add(str(target.get("id")))

    required_by: dict[str, list[str]] = {}
    for edge in edges:
        if edge.get("type") != "requires":
            continue
        source = edge.get("from")
        target = edge.get("to")
        if source in execution and target in nodes and nodes[target].get("type") == "acceptance_criterion":
            required_by.setdefault(str(source), []).append(str(target))

    for node_id, criteria in sorted(required_by.items()):
        node = execution[node_id]
        if not _terminal(node):
            continue
        missing = sorted(criterion for criterion in criteria if criterion not in satisfied)
        for criterion in missing:
            diagnostics.append(
                _diag(
                    "lifecycle.terminal-without-acceptance-evidence",
                    node_id,
                    f"terminal execution node lacks evidence for required acceptance criterion {criterion}",
                )
            )

    diagnostics.sort(key=lambda item: (item["code"], item["subject"], item["message"]))
    return diagnostics
