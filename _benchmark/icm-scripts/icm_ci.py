from __future__ import annotations

import os
import sys
from pathlib import Path

import icm
from icm_graph_store import graph_root


ZERO_SHA = "0" * 40


def canonical_graph_detected(root: Path) -> bool:
    base = graph_root(root)
    return any((base / name).exists() for name in ("nodes.jsonl", "edges.jsonl", "schema-version.json"))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    if not canonical_graph_detected(root):
        print("ICM CI: SKIP canonical graph not initialized")
        return 0

    args = ["--repo", str(root), "validate"]
    base = os.environ.get("ICM_BASE_SHA", "").strip()
    head = os.environ.get("ICM_HEAD_SHA", "").strip()

    if base == ZERO_SHA:
        base = ""
    if head == ZERO_SHA:
        head = ""

    if bool(base) != bool(head):
        print("ICM CI: FAIL base/head diff refs must be supplied together", file=sys.stderr)
        return 2
    if base and head:
        args.extend(["--base", base, "--head", head])

    return icm.main(args)


if __name__ == "__main__":
    raise SystemExit(main())
