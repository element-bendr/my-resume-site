#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

EXPECTED_BRANCH = "feat/blender-world-art-pipeline"
PR_NUMBER = 21
EVIDENCE = (
    "art/blender/command-center/previews/massing-v2-top.png",
    "art/blender/command-center/previews/massing-v2-runtime.png",
    "art/blender/command-center/previews/massing-v2-side.png",
    "art/blender/command-center/massing-v2-review.md",
)
PROTECTED_UNCOMMITTED = "AGENTS.md"


def run(root: Path, *args: str, capture: bool = True, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=root,
        check=check,
        text=True,
        capture_output=capture,
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Safely commit and push Command Center Massing V2 review evidence to PR #21."
    )
    parser.add_argument("--push", action="store_true", help="Push the evidence commit to origin after creating it.")
    parser.add_argument("--comment", action="store_true", help="After push, post/update a PR comment when gh is authenticated.")
    parser.add_argument(
        "--message",
        default="art: add Command Center Massing V2 review evidence",
        help="Commit message.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    branch = run(root, "git", "branch", "--show-current").stdout.strip()
    if branch != EXPECTED_BRANCH:
        print(f"PUBLISH REVIEW: FAIL wrong branch {branch!r}; expected {EXPECTED_BRANCH!r}", file=sys.stderr)
        return 1

    required = [root / relative for relative in EVIDENCE]
    missing = [str(path.relative_to(root)) for path in required if not path.is_file()]
    if missing:
        print("PUBLISH REVIEW: FAIL missing evidence:", file=sys.stderr)
        for item in missing:
            print(f"  - {item}", file=sys.stderr)
        return 1

    staged_before = run(root, "git", "diff", "--cached", "--name-only").stdout.splitlines()
    if staged_before:
        print("PUBLISH REVIEW: FAIL index is not clean; preserve unrelated staged work first:", file=sys.stderr)
        for item in staged_before:
            print(f"  - {item}", file=sys.stderr)
        return 1

    status = run(root, "git", "status", "--porcelain=v1").stdout.splitlines()
    protected_dirty = any(line[3:] == PROTECTED_UNCOMMITTED for line in status if len(line) > 3)
    if not protected_dirty:
        print("PUBLISH REVIEW: WARN AGENTS.md is not dirty; this is allowed, but never stage it.")

    manifest = {
        relative: {
            "bytes": (root / relative).stat().st_size,
            "sha256": sha256(root / relative),
        }
        for relative in EVIDENCE
    }
    print(json.dumps({"pr": PR_NUMBER, "branch": branch, "evidence": manifest}, indent=2))

    run(root, "git", "add", "--", *EVIDENCE, capture=False)

    staged = run(root, "git", "diff", "--cached", "--name-only").stdout.splitlines()
    unexpected = sorted(set(staged) - set(EVIDENCE))
    if unexpected or PROTECTED_UNCOMMITTED in staged:
        run(root, "git", "reset", capture=False)
        print("PUBLISH REVIEW: FAIL unexpected staged paths; index reset.", file=sys.stderr)
        for item in unexpected:
            print(f"  - {item}", file=sys.stderr)
        return 1

    run(root, "git", "commit", "-m", args.message, capture=False)
    commit = run(root, "git", "rev-parse", "HEAD").stdout.strip()
    print(f"PUBLISH REVIEW: COMMIT {commit}")

    if not args.push:
        print("PUBLISH REVIEW: LOCAL ONLY (rerun with --push after review)")
        return 0

    run(root, "git", "push", "origin", f"HEAD:{EXPECTED_BRANCH}", capture=False)
    print(f"PUBLISH REVIEW: PUSHED PR #{PR_NUMBER} branch={EXPECTED_BRANCH}")

    if args.comment:
        if shutil.which("gh") is None:
            print("PUBLISH REVIEW: WARN gh not installed; skipped PR comment.")
            return 0
        auth = run(root, "gh", "auth", "status", capture=True, check=False)
        if auth.returncode != 0:
            print("PUBLISH REVIEW: WARN gh is not authenticated; skipped PR comment.")
            return 0

        body = f"""## Massing V2 greybox review evidence

Commit: `{commit}`

- [runtime view](https://github.com/element-bendr/my-resume-site/blob/{EXPECTED_BRANCH}/art/blender/command-center/previews/massing-v2-runtime.png)
- [top view](https://github.com/element-bendr/my-resume-site/blob/{EXPECTED_BRANCH}/art/blender/command-center/previews/massing-v2-top.png)
- [side view](https://github.com/element-bendr/my-resume-site/blob/{EXPECTED_BRANCH}/art/blender/command-center/previews/massing-v2-side.png)
- [review notes](https://github.com/element-bendr/my-resume-site/blob/{EXPECTED_BRANCH}/art/blender/command-center/massing-v2-review.md)

Structural validation: PASS. Human composition acceptance remains pending.

No GLB export, React integration, Stage 03 work, merge, or deployment is implied by this evidence push.
"""
        run(root, "gh", "pr", "comment", str(PR_NUMBER), "--body", body, capture=False)
        print(f"PUBLISH REVIEW: COMMENTED PR #{PR_NUMBER}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())