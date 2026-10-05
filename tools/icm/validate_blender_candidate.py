#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


REQUIRED_FILES = (
    "art/blender/command-center/source/command-center.blend",
    "art/blender/command-center/previews/detail-runtime.png",
    "art/blender/command-center/previews/detail-top.png",
    "art/blender/command-center/previews/detail-side.png",
    "art/blender/command-center/validation.json",
    "art/blender/command-center/detail-review.md",
)

REQUIRED_REVIEW_HEADINGS = (
    "## Reference comparison",
    "## Source validation",
    "## Protected state",
    "## Known limitations",
)


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
    declared = Path(payload["execution"]["worktree"]).resolve()
    if Path.cwd().resolve() != declared:
        raise SystemExit("validator is not running in the declared worktree")
    if git("status", "--porcelain"):
        raise SystemExit("candidate worktree is not clean")

    missing = [path for path in REQUIRED_FILES if not Path(path).is_file()]
    if missing:
        raise SystemExit("missing required candidate files: " + ", ".join(missing))

    report = json.loads(Path("art/blender/command-center/validation.json").read_text(encoding="utf-8"))
    if report.get("status") != "PASS":
        raise SystemExit("committed Blender source validation is not PASS")
    metrics = report.get("metrics", {})
    if not isinstance(metrics.get("triangles"), int) or metrics["triangles"] <= 0:
        raise SystemExit("validation report has no positive triangle count")
    if not isinstance(metrics.get("material_count"), int) or metrics["material_count"] <= 0:
        raise SystemExit("validation report has no positive material count")

    for image in (
        "art/blender/command-center/previews/detail-runtime.png",
        "art/blender/command-center/previews/detail-top.png",
        "art/blender/command-center/previews/detail-side.png",
    ):
        if Path(image).stat().st_size < 50_000:
            raise SystemExit(f"candidate preview is implausibly small: {image}")

    review = Path("art/blender/command-center/detail-review.md").read_text(encoding="utf-8")
    missing_headings = [heading for heading in REQUIRED_REVIEW_HEADINGS if heading not in review]
    if missing_headings:
        raise SystemExit("detail review missing headings: " + ", ".join(missing_headings))

    changed = {
        path
        for path in git("diff", "--name-only", f"{task['base_sha']}..HEAD").splitlines()
        if path
    }
    required_changed = set(REQUIRED_FILES)
    absent = sorted(required_changed - changed)
    if absent:
        raise SystemExit("candidate did not commit required outputs: " + ", ".join(absent))

    forbidden = {
        "public/world/art/command-center.glb",
        "art/blender/command-center/previews/massing-v2-runtime.png",
        "art/blender/command-center/previews/massing-v2-top.png",
        "art/blender/command-center/previews/massing-v2-side.png",
        "art/blender/command-center/massing-v2-review.md",
        "art/blender/command-center/massing-v2-validation.json",
    }
    touched_forbidden = sorted(changed & forbidden)
    if touched_forbidden:
        raise SystemExit("candidate changed protected evidence/export: " + ", ".join(touched_forbidden))

    print(
        "BLENDER_CANDIDATE_VALIDATION: PASS "
        f"triangles={metrics['triangles']} materials={metrics['material_count']} changed={len(changed)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
