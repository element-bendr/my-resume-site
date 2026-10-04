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


def expected_receipt(task: dict) -> tuple[Path, str]:
    task_id = task["task_id"]
    path = Path("workflow/local-execution/fixtures") / f"{task_id}.txt"
    content = (
        f"task_id={task_id}\n"
        f"base_sha={task['base_sha']}\n"
        "executor=deterministic-fixture\n"
        "purpose=prove-local-execution-plumbing\n"
    )
    return path, content


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-file", required=True)
    args = parser.parse_args()

    payload = json.loads(Path(args.task_file).read_text(encoding="utf-8"))
    task = payload["task"]
    worktree = Path(payload["execution"]["worktree"]).resolve()
    if Path.cwd().resolve() != worktree:
        raise SystemExit("fixture executor is not running in the declared worktree")

    path, content = expected_receipt(task)
    if path.exists():
        raise SystemExit(f"fixture receipt already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    git("add", path.as_posix())
    git(
        "-c", "user.name=ICM Fixture Executor",
        "-c", "user.email=icm-fixture@local.invalid",
        "commit", "-m", f"test(icm): execute {task['task_id']}",
    )
    if git("status", "--porcelain"):
        raise SystemExit("fixture executor left a dirty worktree")
    print(f"FIXTURE_EXECUTOR: PASS path={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
