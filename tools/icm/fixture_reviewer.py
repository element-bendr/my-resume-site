#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit((result.stderr or result.stdout or "git failed").strip())
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    context = json.loads(Path(args.context).read_text(encoding="utf-8"))
    task = context["task"]
    result = context["result"]
    task_id = task["task_id"]
    receipt = Path("workflow/local-execution/fixtures") / f"{task_id}.txt"
    expected = (
        f"task_id={task_id}\n"
        f"base_sha={task['base_sha']}\n"
        "executor=deterministic-fixture\n"
        "purpose=prove-local-execution-plumbing\n"
    )

    if git("rev-parse", "HEAD") != result["candidate_sha"]:
        raise SystemExit("reviewer is not detached at the exact candidate SHA")
    changed = [p for p in git("diff", "--name-only", f"{task['base_sha']}..HEAD").splitlines() if p]
    if changed != [receipt.as_posix()]:
        raise SystemExit(f"review found unexpected changed paths: {changed!r}")
    if not receipt.is_file() or receipt.read_text(encoding="utf-8") != expected:
        raise SystemExit("review found an invalid fixture receipt")
    if git("status", "--porcelain"):
        raise SystemExit("review worktree is dirty")

    decision = {
        "verdict": "pass",
        "findings": [
            {
                "id": "fixture-scope",
                "severity": "info",
                "message": "Candidate contains only the deterministic local-execution fixture receipt.",
                "paths": [receipt.as_posix()],
            }
        ],
        "required_fixes": [],
        "validation_summary": "Exact candidate SHA, bounded path, deterministic receipt content and clean detached review worktree verified.",
    }
    Path(args.output).write_text(json.dumps(decision, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("FIXTURE_REVIEW: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
