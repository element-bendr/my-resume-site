from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workflow_lib import git_blob, load_json, safe_repo_path
from workflow_selection import active_workflows, select_workflow


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def pin_workflow(root: Path, workflow_id: str | None = None, write: bool = False) -> dict:
    selected = select_workflow(root, workflow_id)
    state_path = active_workflows(root)[selected]
    state = load_json(state_path)
    changes: list[dict[str, str | None | bool]] = []
    locked: list[str] = []
    for stage in state.get("stages", []):
        stage_id = stage.get("id")
        dependencies = stage.get("depends_on", [])
        if not isinstance(dependencies, list):
            raise ValueError(f"{stage_id}: depends_on must be a list")
        for dep in dependencies:
            if not isinstance(dep, dict) or not isinstance(dep.get("path"), str):
                raise ValueError(f"{stage_id}: invalid dependency record")
            relative = dep["path"]
            path = safe_repo_path(root, relative)
            if not path.is_file():
                raise FileNotFoundError(relative)
            current = git_blob(root, relative)
            previous = dep.get("blob")
            if previous != current:
                is_locked = stage.get("status") == "certified"
                changes.append({"stage": str(stage_id), "path": relative, "previous": previous if isinstance(previous, str) else None, "current": current, "locked": is_locked})
                if is_locked:
                    locked.append(str(stage_id))
                else:
                    dep["blob"] = current
    if write and locked:
        raise ValueError("certified stage dependencies changed; reopen/invalidate the stage before re-pinning: " + ", ".join(sorted(set(locked))))
    if write and changes:
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return {"workflow_id": selected, "state_file": str(state_path.relative_to(root)), "write": write, "changes": changes}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        result = pin_workflow(repo_root(), args.workflow, write=args.write)
    except Exception as exc:
        print(f"PIN: FAIL: {exc}", file=sys.stderr)
        return 1
    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        mode = "WRITE" if args.write else "DRY-RUN"
        print(f"PIN: {mode} workflow={result['workflow_id']} changes={len(result['changes'])}")
        for item in result["changes"]:
            lock = " LOCKED" if item.get("locked") else ""
            print(f"  {item['stage']}: {item['path']} {item['previous']} -> {item['current']}{lock}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
