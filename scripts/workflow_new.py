from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from workflow_lib import current_branch, current_commit
from workflow_selection import active_workflows, load_index, validate_index

WORKFLOW_ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_template(root: Path, name: str) -> str:
    path = root / "templates" / "icm" / name
    if not path.is_file():
        raise FileNotFoundError(str(path.relative_to(root)))
    return path.read_text(encoding="utf-8")


def create_workflow(
    root: Path,
    workflow_id: str,
    title: str | None = None,
    make_primary: bool = False,
    mode: str = "implementation",
    owner: str = "coordinator",
    write_paths: list[str] | None = None,
) -> dict:
    if not WORKFLOW_ID_RE.fullmatch(workflow_id):
        raise ValueError("workflow id must use lowercase letters, digits, and internal hyphens only (1-63 chars)")
    if mode not in {"read-only-audit", "implementation", "certification", "research"}:
        raise ValueError(f"invalid execution mode: {mode}")
    if not owner.strip():
        raise ValueError("owner must be non-empty")
    if write_paths is None:
        write_paths = [] if mode == "read-only-audit" else ["*"]
    if mode == "read-only-audit" and write_paths:
        raise ValueError("read-only-audit workflows cannot declare write paths")

    active = active_workflows(root)
    index_errors = validate_index(root)
    if len(active) > 1 and index_errors:
        raise ValueError("existing active-workflow index is ambiguous: " + "; ".join(index_errors))

    target = root / "workflow" / "active" / workflow_id
    if target.exists():
        raise FileExistsError(f"workflow already exists: {workflow_id}")

    context_template = _load_template(root, "STAGE-CONTEXT.md")
    state_template = json.loads(_load_template(root, "STATE.json"))
    display_title = title or workflow_id.replace("-", " ").title()
    stage_id = "01-initial"
    context = context_template.replace("# <Stage Name>", f"# {display_title}", 1)

    state_template.update({
        "workflow_id": workflow_id,
        "title": display_title,
        "status": "blocked",
        "active_stage": stage_id,
        "provenance": {
            "started_from_commit": current_commit(root),
            "validated_commit": None,
        },
        "execution": {
            "mode": mode,
            "branch": current_branch(root) or "detached",
            "worktree": str(root.resolve()),
            "owner": owner,
            "write_paths": write_paths,
        },
    })

    stages = state_template.get("stages")
    if not isinstance(stages, list) or not stages:
        raise ValueError("STATE.json template must contain at least one stage")
    stage = stages[0]
    stage.update({
        "id": stage_id,
        "status": "blocked",
        "block_reason": "contract_incomplete",
        "context": f"workflow/active/{workflow_id}/CONTEXT.md",
        "depends_on_stages": [],
        "depends_on": [],
        "outputs": [],
        "completion_report": f"workflow/active/{workflow_id}/output/completion-report.md",
    })

    index_path = root / "workflow" / "index.json"
    index = load_index(root)
    existing_primary = index.get("primary")
    if make_primary or not active:
        new_primary = workflow_id
    elif len(active) == 1 and existing_primary is None:
        new_primary = next(iter(active))
    else:
        new_primary = existing_primary

    target.mkdir(parents=True)
    (target / "output").mkdir()
    (target / "CONTEXT.md").write_text(context, encoding="utf-8")
    (target / "state.json").write_text(json.dumps(state_template, indent=2) + "\n", encoding="utf-8")
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps({"schema_version": 1, "primary": new_primary}, indent=2) + "\n", encoding="utf-8")
    return {"workflow_id": workflow_id, "path": str(target.relative_to(root)), "primary": new_primary}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workflow_id")
    parser.add_argument("--title")
    parser.add_argument("--make-primary", action="store_true")
    parser.add_argument("--mode", default="implementation", choices=["read-only-audit", "implementation", "certification", "research"])
    parser.add_argument("--owner", default="coordinator")
    parser.add_argument("--write-path", action="append", dest="write_paths")
    args = parser.parse_args()
    try:
        result = create_workflow(repo_root(), args.workflow_id, args.title, args.make_primary, args.mode, args.owner, args.write_paths)
    except Exception as exc:
        print(f"NEW WORKFLOW: FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"NEW WORKFLOW: PASS id={result['workflow_id']} path={result['path']} primary={result['primary']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
