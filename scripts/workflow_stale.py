from __future__ import annotations

import argparse
import json
import sys

from workflow_lib import load_json, repo_root, stage_staleness, state_files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    root = repo_root()
    payload = []
    any_stale = False

    for state_path in state_files(root):
        state = load_json(state_path)
        stale = stage_staleness(root, state)
        stages = []
        for stage in state.get("stages", []):
            item = {"id": stage["id"], **stale[stage["id"]]}
            stages.append(item)
            any_stale = any_stale or item["stale"]
        payload.append({"workflow_id": state.get("workflow_id"), "stages": stages})

    if args.as_json:
        print(json.dumps(payload, indent=2))
    else:
        if not payload:
            print("No active workflows.")
        for workflow in payload:
            print(f"workflow={workflow['workflow_id']}")
            for stage in workflow["stages"]:
                state = "STALE" if stage["stale"] else "CURRENT"
                extra = f" unpinned={len(stage['unpinned'])}" if stage["unpinned"] else ""
                print(f"  {stage['id']}: {state}{extra}")
                for path in stage["direct"]:
                    print(f"    changed: {path}")
                for upstream in stage["upstream"]:
                    print(f"    upstream_stale: {upstream}")

    return 1 if any_stale else 0


if __name__ == "__main__":
    sys.exit(main())
