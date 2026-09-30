from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workflow_lib import current_commit, load_json
from workflow_selection import active_workflows, select_workflow


def _downstream(stages: list[dict], target: str) -> set[str]:
    result: set[str] = set()
    changed = True
    while changed:
        changed = False
        for stage in stages:
            sid = stage.get("id")
            deps = stage.get("depends_on_stages", [])
            if sid != target and sid not in result and any(dep == target or dep in result for dep in deps):
                result.add(sid)
                changed = True
    return result


def reopen_stage(root: Path, stage_id: str, reason: str, workflow_id: str | None = None, write: bool = False) -> dict:
    if not reason.strip():
        raise ValueError("reopen reason is required")
    selected = select_workflow(root, workflow_id)
    state_path = active_workflows(root)[selected]
    state = load_json(state_path)
    stages = state.get("stages", [])
    stage = next((item for item in stages if item.get("id") == stage_id), None)
    if not stage:
        raise ValueError(f"unknown stage: {stage_id}")
    if stage.get("status") not in {"certified", "stale"}:
        raise ValueError("only certified or stale stages can be reopened")
    downstream = _downstream(stages, stage_id)
    if write:
        prior = stage.get("status")
        stage["status"] = "active"
        stage.pop("block_reason", None)
        for item in stages:
            if item.get("id") in downstream and item.get("status") in {"active", "blocked", "certified"}:
                item["status"] = "stale"
        state["status"] = "active"
        state["active_stage"] = stage_id
        state.setdefault("provenance", {})["validated_commit"] = None
        state.setdefault("reopen_history", []).append({"stage": stage_id, "from_status": prior, "reason": reason.strip(), "at_commit": current_commit(root)})
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return {"workflow_id": selected, "stage": stage_id, "downstream_invalidated": sorted(downstream), "write": write}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage_id")
    parser.add_argument("--workflow")
    parser.add_argument("--reason", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        result = reopen_stage(Path(__file__).resolve().parents[1], args.stage_id, args.reason, args.workflow, args.write)
    except Exception as exc:
        print(f"REOPEN: FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
