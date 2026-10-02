#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def safe_path(root: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError(f"unsafe repository-relative path: {relative!r}")
    root = root.resolve()
    path = (root / relative).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"path escapes repository: {relative!r}")
    return path


def source_metric(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        estimated_tokens = None
        chars = None
    else:
        chars = len(text)
        estimated_tokens = (chars + 3) // 4
    return {
        "sha256": digest,
        "bytes": len(data),
        "text_chars": chars,
        "estimated_tokens": estimated_tokens,
    }


def baseline_paths(payload: Any) -> list[str]:
    if isinstance(payload, list):
        values = payload
    elif isinstance(payload, dict) and isinstance(payload.get("paths"), list):
        values = payload["paths"]
    else:
        raise ValueError("baseline JSON must be a path list or object with paths[]")
    if not all(isinstance(item, str) and item for item in values):
        raise ValueError("baseline paths must be non-empty strings")
    return list(dict.fromkeys(values))


def file_set_metrics(
    root: Path,
    paths: list[str],
    *,
    exclude_hashes: set[str] | None = None,
) -> dict[str, Any]:
    excluded = exclude_hashes or set()
    seen_hashes: set[str] = set()
    files = 0
    duplicate_files = 0
    excluded_duplicate_files = 0
    byte_count = 0
    estimated_tokens = 0
    unestimated_files = 0
    hashes: list[str] = []

    for relative in paths:
        path = safe_path(root, relative)
        if not path.is_file():
            raise FileNotFoundError(relative)
        metric = source_metric(path)
        digest = metric["sha256"]
        if digest in excluded:
            excluded_duplicate_files += 1
            continue
        if digest in seen_hashes:
            duplicate_files += 1
            continue
        seen_hashes.add(digest)
        hashes.append(digest)
        files += 1
        byte_count += int(metric["bytes"])
        value = metric["estimated_tokens"]
        if isinstance(value, int):
            estimated_tokens += value
        else:
            unestimated_files += 1

    return {
        "unique_files": files,
        "duplicate_files": duplicate_files,
        "excluded_duplicate_files": excluded_duplicate_files,
        "bytes": byte_count,
        "estimated_tokens": estimated_tokens,
        "unestimated_files": unestimated_files,
        "hashes": hashes,
        "measurement": "UTF-8 unicode_chars_div_4_heuristic; exact SHA-256 dedupe",
    }


def baseline_metrics(root: Path, paths: list[str]) -> dict[str, Any]:
    return file_set_metrics(root, paths)


def graph_runtime_metrics(
    root: Path,
    manifest: dict[str, Any],
    ambient_paths: list[str],
) -> dict[str, Any]:
    budget = manifest.get("budget")
    if not isinstance(budget, dict):
        raise ValueError("compact graph manifest requires budget object")

    required = (
        "bootstrap_source_files",
        "bootstrap_source_bytes",
        "estimated_tokens_if_bootstrap_sources_loaded",
        "compact_manifest_chars",
        "estimated_compact_manifest_tokens",
    )
    if any(not isinstance(budget.get(key), int) for key in required):
        raise ValueError("compact graph manifest budget is incomplete")

    bootstrap_sources = manifest.get("bootstrap_sources")
    if not isinstance(bootstrap_sources, list):
        raise ValueError("compact graph manifest requires bootstrap_sources[]")

    bootstrap_hashes = {
        item.get("sha256")
        for item in bootstrap_sources
        if isinstance(item, dict) and isinstance(item.get("sha256"), str)
    }
    ambient = file_set_metrics(
        root,
        list(dict.fromkeys(ambient_paths)),
        exclude_hashes=bootstrap_hashes,
    )

    bootstrap_tokens = int(budget["estimated_tokens_if_bootstrap_sources_loaded"])
    manifest_tokens = int(budget["estimated_compact_manifest_tokens"])
    ambient_tokens = int(ambient["estimated_tokens"])

    return {
        "bootstrap_source_files": int(budget["bootstrap_source_files"]),
        "bootstrap_source_bytes": int(budget["bootstrap_source_bytes"]),
        "bootstrap_source_estimated_tokens": bootstrap_tokens,
        "compact_manifest_chars": int(budget["compact_manifest_chars"]),
        "compact_manifest_estimated_tokens": manifest_tokens,
        "ambient": ambient,
        "model_visible_estimated_tokens": bootstrap_tokens + manifest_tokens + ambient_tokens,
        "measurement": (
            "model-visible estimate = compact manifest + bootstrap sources + ambient project instructions; "
            "UTF-8 text and serialized JSON use chars/4 heuristic"
        ),
    }


def reduction_percent(baseline: int, graph: int) -> float | None:
    if baseline <= 0:
        return None
    return round((1 - (graph / baseline)) * 100, 2)


def compare(
    root: Path,
    baseline: dict[str, Any],
    graph: dict[str, Any],
    *,
    ambient_paths: list[str] | None = None,
) -> dict[str, Any]:
    old = baseline_metrics(root, baseline_paths(baseline))
    new = graph_runtime_metrics(root, graph, ambient_paths or ["AGENTS.md"])
    reduction = reduction_percent(
        int(old["estimated_tokens"]),
        int(new["model_visible_estimated_tokens"]),
    )
    return {
        "schema_version": 2,
        "baseline": old,
        "graph_runtime_context": new,
        "estimated_token_reduction_percent": reduction,
        "graph_status": graph.get("status"),
        "graph_subject": graph.get("subject"),
        "graph_base_sha": graph.get("base_sha"),
        "ambient_paths": ambient_paths or ["AGENTS.md"],
        "note": (
            "This estimates initial model-visible context, not ChatGPT Plus quota. "
            "It counts the compact graph manifest, bootstrap source bodies, and shared ambient instructions. "
            "Correctness and validation evidence remain separate release gates."
        ),
    }


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare legacy ICM context with Bedrock graph-runtime context"
    )
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--baseline-json", required=True, type=Path)
    parser.add_argument("--graph-json", required=True, type=Path)
    parser.add_argument(
        "--ambient",
        action="append",
        default=None,
        help="repository-relative project instruction file visible in both modes; repeatable (default: AGENTS.md)",
    )
    parser.add_argument("--require-reduction", type=float)
    args = parser.parse_args()

    try:
        result = compare(
            args.repo,
            load_json(args.baseline_json),
            load_json(args.graph_json),
            ambient_paths=args.ambient,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, sort_keys=True))
        return 2

    reduction = result["estimated_token_reduction_percent"]
    status = "PASS"
    if args.require_reduction is not None:
        if reduction is None or reduction < args.require_reduction:
            status = "FAIL"
    result["status"] = status
    result["required_reduction_percent"] = args.require_reduction
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
