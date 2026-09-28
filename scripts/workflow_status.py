from __future__ import annotations

import argparse
import json
import subprocess
import sys

from workflow_lib import load_json, repo_root, stage_staleness, state_files, validate_state


def current_commit(root) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def build_report(root):
    workflows = []
    for path in state_files(root):
        state = load_json(path)
        errors = validate_state(root, path)
        stale = stage_staleness(root, state)
        workflows.append(
            {
                "workflow_id": state.get("workflow_id"),
                "title": state.get("title"),
                "status": state.get("status"),
                "active_stage": state.get("active_stage"),
                "state_file": str(path.relative_to(root)),
                "errors": errors,
                "stages": [
                    {
                        "id": stage["id"],
                        "declared_status": stage.get("status"),
                        **stale[stage["id"]],
                    }
                    for stage in state.get("stages", [])
                ],
            }
        )
    return {
        "commit": current_commit(root),
        "active_workflows": workflows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    root = repo_root()
    report = build_report(root)

    if args.as_json:
        print(json.dumps(report, indent=2))
    else:
        print(f"commit={report['commit']}")
        if not report["active_workflows"]:
            print("active_workflows=0")
        for workflow in report["active_workflows"]:
            print(f"workflow={workflow['workflow_id']} status={workflow['status']}")
            print(f"active_stage={workflow['active_stage']}")
            for stage in workflow["stages"]:
                flags = []
                if stage["stale"]:
                    flags.append("STALE")
                if stage["unpinned"]:
                    flags.append(f"UNPINNED:{len(stage['unpinned'])}")
                if not flags:
                    flags.append("CURRENT")
                print(f"  {stage['id']}: {stage['declared_status']} [{' '.join(flags)}]")
                for path in stage["direct"]:
                    print(f"    changed: {path}")
                for upstream in stage["upstream"]:
                    print(f"    upstream_stale: {upstream}")
            for error in workflow["errors"]:
                print(f"  error: {error}")

    if not args.strict:
        return 0

    for workflow in report["active_workflows"]:
        if workflow["errors"]:
            return 1
        by_id = {stage["id"]: stage for stage in workflow["stages"]}
        for stage in workflow["stages"]:
            if stage["declared_status"] == "certified" and stage["stale"]:
                return 1
        active = by_id.get(workflow["active_stage"])
        if active and active["stale"]:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
