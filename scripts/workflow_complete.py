from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from workflow_certify_check import validate_completion_report
from workflow_lib import load_json, validate_state
from workflow_selection import active_workflows, load_index, select_workflow


def _archive_path(value: str, workflow_id: str) -> str:
    prefix = f"workflow/active/{workflow_id}/"
    return f"workflow/completed/{workflow_id}/" + value[len(prefix):] if value.startswith(prefix) else value


def completion_preflight(root: Path, workflow_id: str | None = None) -> dict:
    errors: list[str] = []
    try:
        selected = select_workflow(root, workflow_id)
        states = active_workflows(root)
        state_path = states[selected]
        state = load_json(state_path)
    except Exception as exc:
        return {"workflow_id": workflow_id, "errors": [str(exc)]}
    if state.get("status") != "certified":
        errors.append("workflow must be certified before completion")
    errors.extend(validate_state(root, state_path))
    for stage in state.get("stages", []):
        report = stage.get("completion_report")
        if not isinstance(report, str) or not report:
            errors.append(f"stage {stage.get('id')}: completion_report is required")
        else:
            errors.extend(validate_completion_report(root, report))
    active_dir = state_path.parent
    completed_dir = root / "workflow" / "completed" / selected
    if completed_dir.exists():
        errors.append(f"completed workflow already exists: {selected}")
    return {"workflow_id": selected, "state_path": state_path, "active_dir": active_dir, "completed_dir": completed_dir, "state": state, "errors": errors}


def complete_workflow(root: Path, workflow_id: str | None = None, write: bool = False) -> dict:
    preflight = completion_preflight(root, workflow_id)
    if preflight["errors"]:
        raise ValueError("; ".join(preflight["errors"]))
    selected = preflight["workflow_id"]
    state_path: Path = preflight["state_path"]
    active_dir: Path = preflight["active_dir"]
    completed_dir: Path = preflight["completed_dir"]
    state = json.loads(json.dumps(preflight["state"]))
    index_path = root / "workflow" / "index.json"
    index = load_index(root)
    remaining = sorted(name for name in active_workflows(root) if name != selected)
    current_primary = index.get("primary")
    if current_primary == selected or current_primary not in remaining:
        new_primary = remaining[0] if remaining else None
    else:
        new_primary = current_primary

    state["status"] = "completed"
    state["active_stage"] = None
    for stage in state.get("stages", []):
        if isinstance(stage.get("context"), str):
            stage["context"] = _archive_path(stage["context"], selected)
        if isinstance(stage.get("completion_report"), str):
            stage["completion_report"] = _archive_path(stage["completion_report"], selected)
        stage["outputs"] = [_archive_path(item, selected) for item in stage.get("outputs", [])]

    if not write:
        return {"workflow_id": selected, "destination": str(completed_dir.relative_to(root)), "primary": new_primary, "write": False}

    completed_dir.parent.mkdir(parents=True, exist_ok=True)
    old_state_text = state_path.read_text(encoding="utf-8")
    old_index_text = index_path.read_text(encoding="utf-8") if index_path.exists() else None
    state_tmp = active_dir / ".state.complete.tmp"
    index_tmp = index_path.parent / ".index.complete.tmp"
    state_tmp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    index_tmp.write_text(json.dumps({"schema_version": 1, "primary": new_primary}, indent=2) + "\n", encoding="utf-8")
    try:
        os.replace(state_tmp, state_path)
        os.replace(active_dir, completed_dir)
        os.replace(index_tmp, index_path)
    except Exception:
        if completed_dir.exists() and not active_dir.exists():
            os.replace(completed_dir, active_dir)
        (active_dir / "state.json").write_text(old_state_text, encoding="utf-8")
        if old_index_text is None:
            index_path.unlink(missing_ok=True)
        else:
            index_path.write_text(old_index_text, encoding="utf-8")
        state_tmp.unlink(missing_ok=True)
        index_tmp.unlink(missing_ok=True)
        raise
    return {"workflow_id": selected, "destination": str(completed_dir.relative_to(root)), "primary": new_primary, "write": True}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        result = complete_workflow(Path(__file__).resolve().parents[1], args.workflow, args.write)
    except Exception as exc:
        print(f"COMPLETE: FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
