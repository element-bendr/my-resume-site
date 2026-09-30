from __future__ import annotations

import json
from pathlib import Path

from workflow_lib import safe_repo_path

ACTIVE_STATUSES = {"active", "blocked", "certified"}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def active_workflows(root: Path) -> dict[str, Path]:
    root = root.resolve()
    result: dict[str, Path] = {}
    safe_repo_path(root, "workflow/active")
    active_root = root / "workflow" / "active"
    if not active_root.exists():
        return result
    for state_path in sorted(active_root.glob("*/state.json")):
        relative_state = state_path.relative_to(root).as_posix()
        safe_repo_path(root, relative_state)
        state = load_json(state_path)
        workflow_id = state.get("workflow_id")
        status = state.get("status")
        if status not in ACTIVE_STATUSES:
            continue
        if not isinstance(workflow_id, str) or not workflow_id:
            raise ValueError(f"{state_path}: active workflow_id is required")
        if state_path.parent.name != workflow_id:
            raise ValueError(f"{state_path}: directory name must match workflow_id {workflow_id!r}")
        if workflow_id in result:
            raise ValueError(f"duplicate active workflow_id: {workflow_id}")
        result[workflow_id] = state_path
    return result


def load_index(root: Path) -> dict:
    root = root.resolve()
    safe_repo_path(root, "workflow/index.json")
    path = root / "workflow" / "index.json"
    if not path.exists():
        return {"schema_version": 1, "primary": None}
    value = load_json(path)
    if value.get("schema_version") != 1:
        raise ValueError("workflow/index.json schema_version must be 1")
    primary = value.get("primary")
    if primary is not None and (not isinstance(primary, str) or not primary):
        raise ValueError("workflow/index.json primary must be string or null")
    return value


def validate_index(root: Path) -> list[str]:
    try:
        active = active_workflows(root)
        index = load_index(root)
    except Exception as exc:
        return [str(exc)]
    errors: list[str] = []
    primary = index.get("primary")
    if primary is not None and primary not in active:
        errors.append(f"workflow/index.json primary is not active: {primary}")
    if len(active) > 1 and not primary:
        errors.append("multiple active workflows require workflow/index.json primary")
    return errors


def select_workflow(root: Path, explicit: str | None = None) -> str:
    active = active_workflows(root)
    if explicit is not None:
        if explicit not in active:
            raise ValueError(f"requested workflow is not active: {explicit}")
        return explicit
    if not active:
        raise ValueError("no active workflows")
    if len(active) == 1:
        errors = validate_index(root)
        if errors:
            raise ValueError("; ".join(errors))
        return next(iter(active))
    errors = validate_index(root)
    if errors:
        raise ValueError("; ".join(errors))
    primary = load_index(root).get("primary")
    if not primary:
        raise ValueError("multiple active workflows require a primary workflow")
    return primary
