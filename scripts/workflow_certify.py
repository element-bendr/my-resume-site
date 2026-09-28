from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workflow_certify_check import certification_report
from workflow_lib import load_json
from workflow_selection import active_workflows, select_workflow


def certify_stage(root: Path, workflow_id: str | None = None, stage_id: str | None = None, write: bool = False, require_clean: bool = True) -> dict:
    report = certification_report(root, workflow_id, stage_id, require_clean=require_clean)
    if report["errors"]:
        raise ValueError("; ".join(report["errors"]))
    selected = select_workflow(root, workflow_id)
    state_path = active_workflows(root)[selected]
    state = load_json(state_path)
    sid = report["stage"]
    stage = next(item for item in state["stages"] if item.get("id") == sid)
    if write:
        stage["status"] = "certified"
        state.setdefault("provenance", {})["validated_commit"] = report["candidate_commit"]
        unresolved = [item for item in state["stages"] if item.get("status") != "certified"]
        if unresolved:
            next_stage = unresolved[0]
            next_stage["status"] = "blocked"
            next_stage["block_reason"] = "awaiting_activation"
            state["status"] = "blocked"
            state["active_stage"] = next_stage["id"]
        else:
            state["status"] = "certified"
            state["active_stage"] = None
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return {**report, "write": write}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow")
    parser.add_argument("--stage")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    args = parser.parse_args()
    try:
        result = certify_stage(Path(__file__).resolve().parents[1], args.workflow, args.stage, args.write, require_clean=not args.allow_dirty)
    except Exception as exc:
        print(f"CERTIFY: FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"CERTIFY: {'WRITE' if args.write else 'DRY-RUN'} workflow={result['workflow_id']} stage={result['stage']} candidate={result['candidate_commit']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
