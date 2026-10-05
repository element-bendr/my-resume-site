#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

REQUIRED = (
    Path("art/blender/command-center/source/command-center.blend"),
    Path("art/blender/command-center/previews/reference-runtime.png"),
    Path("art/blender/command-center/previews/reference-top.png"),
    Path("art/blender/command-center/previews/reference-side.png"),
    Path("art/blender/command-center/reference-rebuild-review.md"),
    Path("art/blender/command-center/reference-rebuild-validation.json"),
    Path("art/blender/command-center/reference-comparison.json"),
)

REFERENCE = Path("art/blender/command-center/references/command-center-concept.png")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    if result.returncode:
        raise SystemExit((result.stderr or result.stdout).strip())
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-file", required=True)
    args = parser.parse_args()

    envelope = json.loads(Path(args.task_file).read_text(encoding="utf-8"))
    task = envelope["task"]

    missing = [str(path) for path in REQUIRED if not path.is_file()]
    if missing:
        raise SystemExit("REFERENCE REBUILD EVIDENCE: FAIL missing " + ", ".join(missing))

    if not REFERENCE.is_file():
        raise SystemExit("REFERENCE REBUILD EVIDENCE: FAIL primary reference missing")

    for render in REQUIRED[1:4]:
        if render.stat().st_size < 100_000:
            raise SystemExit(f"REFERENCE REBUILD EVIDENCE: FAIL implausibly small render {render}")

    validation = json.loads(REQUIRED[5].read_text(encoding="utf-8"))
    if validation.get("status") != "PASS":
        raise SystemExit("REFERENCE REBUILD EVIDENCE: FAIL source validation not PASS")
    if validation.get("protected_anchors") != "unchanged":
        raise SystemExit("REFERENCE REBUILD EVIDENCE: FAIL protected anchors not unchanged")

    comparison = json.loads(REQUIRED[6].read_text(encoding="utf-8"))
    expected_ref_sha = sha256(REFERENCE)
    if comparison.get("primary_reference") != REFERENCE.as_posix():
        raise SystemExit("REFERENCE REBUILD EVIDENCE: FAIL wrong primary reference")
    if comparison.get("primary_reference_sha256") != expected_ref_sha:
        raise SystemExit("REFERENCE REBUILD EVIDENCE: FAIL reference SHA mismatch")

    iterations = comparison.get("iterations")
    if not isinstance(iterations, list) or len(iterations) < 3:
        raise SystemExit("REFERENCE REBUILD EVIDENCE: FAIL fewer than 3 visual compare iterations")

    required_axes = {
        "silhouette",
        "depth",
        "curvature",
        "facade_depth",
        "materials",
        "landscape",
        "human_scale",
        "floating_platform",
        "lighting",
    }
    final_axes = comparison.get("final_axes")
    if not isinstance(final_axes, dict) or set(final_axes) != required_axes:
        raise SystemExit("REFERENCE REBUILD EVIDENCE: FAIL final_axes incomplete")
    if any(final_axes[name] not in {"close", "minor_gap"} for name in required_axes):
        raise SystemExit("REFERENCE REBUILD EVIDENCE: FAIL major visual mismatch remains")

    changed = [
        p for p in git("diff", "--name-only", f"{task['base_sha']}..HEAD").splitlines() if p
    ]
    if not changed:
        raise SystemExit("REFERENCE REBUILD EVIDENCE: FAIL empty candidate")

    review = REQUIRED[4].read_text(encoding="utf-8")
    for heading in (
        "## Primary reference",
        "## Largest mismatches corrected",
        "## Remaining visible differences",
        "## Protected anchors",
        "## Human visual gate",
    ):
        if heading not in review:
            raise SystemExit(f"REFERENCE REBUILD EVIDENCE: FAIL review missing {heading}")

    print(
        "REFERENCE_REBUILD_EVIDENCE: PASS "
        f"iterations={len(iterations)} reference_sha256={expected_ref_sha}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
