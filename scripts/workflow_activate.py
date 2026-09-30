from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workflow_lib import load_json, validate_execution, validate_stage_contract
from workflow_selection import active_workflows, select_workflow


def activate_workflow(root: Path, workflow_id: str | None = None, write: bool = False) -> dict:
    selected = select_workflow(root, workflow_id)
    state_path = active_workflows(root)[selected]
    state = load_json(state_path)
    if state.get("status") != "blocked":
        raise ValueError("workflow activation requires status blocked")
    stage_id = state.get("active_stage")
    stage = next((item for item in state.get("stages", []) if item.get("id") == stage_id), None)
    if not stage or stage.get("status") != "blocked":
        raise ValueError("active stage must be blocked before activation")
    errors = validate_execution(state.get("execution"))
    context = stage.get("context")
    if not isinstance(context, str):
        errors.append("active stage context is required")
    else:
        errors.extend(validate_stage_contract(root, context, require_complete=True))
    if errors:
        raise ValueError("; ".join(errors))
    if write:
        state["status"] = "active"
        stage["status"] = "active"
        stage.pop("block_reason", None)
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return {"workflow_id": selected, "stage": stage_id, "write": write}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        result = activate_workflow(Path(__file__).resolve().parents[1], args.workflow, args.write)
    except Exception as exc:
        print(f"ACTIVATE: FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"ACTIVATE: {'WRITE' if args.write else 'DRY-RUN'} workflow={result['workflow_id']} stage={result['stage']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
