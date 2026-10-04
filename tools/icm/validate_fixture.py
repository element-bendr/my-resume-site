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
    parser.add_argument("--task-file", required=True)
    args = parser.parse_args()

    payload = json.loads(Path(args.task_file).read_text(encoding="utf-8"))
    task = payload["task"]
    task_id = task["task_id"]
    receipt = Path("workflow/local-execution/fixtures") / f"{task_id}.txt"
    expected = (
        f"task_id={task_id}\n"
        f"base_sha={task['base_sha']}\n"
        "executor=deterministic-fixture\n"
        "purpose=prove-local-execution-plumbing\n"
    )
    if not receipt.is_file() or receipt.read_text(encoding="utf-8") != expected:
        raise SystemExit("fixture receipt content mismatch")
    changed = [p for p in git("diff", "--name-only", f"{task['base_sha']}..HEAD").splitlines() if p]
    if changed != [receipt.as_posix()]:
        raise SystemExit(f"unexpected fixture changes: {changed!r}")
    if git("status", "--porcelain"):
        raise SystemExit("fixture validation found a dirty worktree")
    print("FIXTURE_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
