from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workflow_lib import load_json, safe_repo_path
from workflow_selection import active_workflows, select_workflow

ROOT_CONTEXT = ["AGENTS.md", "CONTEXT.md", "HANDOFF.md"]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def context_bundle(root: Path, workflow_id: str | None = None) -> dict:
    selected = select_workflow(root, workflow_id)
    state_path = active_workflows(root)[selected]
    state = load_json(state_path)
    active_stage = state.get("active_stage")
    stages = state.get("stages", [])
    stage = next((item for item in stages if isinstance(item, dict) and item.get("id") == active_stage), None)
    if stage is None:
        raise ValueError(f"active stage not found: {active_stage!r}")

    candidates = list(ROOT_CONTEXT)
    context = stage.get("context")
    if not isinstance(context, str):
        raise ValueError("active stage context path is required")
    candidates.append(context)

    dependencies = stage.get("depends_on", [])
    if not isinstance(dependencies, list):
        raise ValueError("active stage depends_on must be a list")
    for dep in dependencies:
        if not isinstance(dep, dict) or not isinstance(dep.get("path"), str):
            raise ValueError("invalid dependency record")
        candidates.append(dep["path"])

    paths: list[str] = []
    seen: set[str] = set()
    for relative in candidates:
        if relative in seen:
            continue
        path = safe_repo_path(root, relative)
        if not path.is_file():
            raise FileNotFoundError(relative)
        seen.add(relative)
        paths.append(relative)

    return {"workflow_id": selected, "stage": active_stage, "paths": paths}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        result = context_bundle(repo_root(), args.workflow)
    except Exception as exc:
        print(f"CONTEXT: FAIL: {exc}", file=sys.stderr)
        return 1
    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        for path in result["paths"]:
            print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
