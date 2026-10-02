#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from context_benchmark import (
    baseline_metrics,
    baseline_paths,
    graph_runtime_metrics,
    load_json,
    reduction_percent,
    source_metric,
)


def _path_hash(root: Path, relative: str) -> str:
    path = (root / relative).resolve()
    root = root.resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"path escapes repository: {relative!r}")
    if not path.is_file():
        raise FileNotFoundError(relative)
    return str(source_metric(path)["sha256"])


def _seed_hashes(root: Path, paths: list[str]) -> set[str]:
    return {_path_hash(root, value) for value in paths}


def _graph_seed_hashes(root: Path, graph: dict[str, Any], ambient: list[str]) -> set[str]:
    hashes = _seed_hashes(root, ambient)
    for source in graph.get("bootstrap_sources", []):
        if not isinstance(source, dict):
            continue
        digest = source.get("sha256")
        if isinstance(digest, str):
            hashes.add(digest)
    return hashes


def load_trace(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("phases"), list):
        raise ValueError("trace JSON requires phases[]")
    phases: list[dict[str, Any]] = []
    for index, raw in enumerate(payload["phases"], 1):
        if not isinstance(raw, dict):
            raise ValueError(f"phase {index}: expected object")
        name = raw.get("name")
        paths = raw.get("paths")
        if not isinstance(name, str) or not name:
            raise ValueError(f"phase {index}: non-empty name required")
        if not isinstance(paths, list) or not all(isinstance(p, str) and p for p in paths):
            raise ValueError(f"phase {index}: paths[] must contain non-empty strings")
        phases.append({"name": name, "paths": list(dict.fromkeys(paths))})
    if not phases:
        raise ValueError("trace requires at least one phase")
    return phases


def phase_additions(
    root: Path,
    phases: list[dict[str, Any]],
    *,
    seed_hashes: set[str],
) -> tuple[list[dict[str, Any]], int]:
    seen = set(seed_hashes)
    results: list[dict[str, Any]] = []
    cumulative = 0
    for phase in phases:
        tokens = 0
        files = 0
        skipped_duplicate = 0
        loaded: list[str] = []
        for relative in phase["paths"]:
            path = (root / relative).resolve()
            if not path.is_file():
                raise FileNotFoundError(relative)
            metric = source_metric(path)
            digest = str(metric["sha256"])
            if digest in seen:
                skipped_duplicate += 1
                continue
            seen.add(digest)
            value = metric["estimated_tokens"]
            if value is None:
                raise ValueError(f"cannot estimate text tokens for {relative}")
            tokens += int(value)
            files += 1
            loaded.append(relative)
        cumulative += tokens
        results.append(
            {
                "name": phase["name"],
                "new_files": files,
                "duplicate_or_preloaded_files": skipped_duplicate,
                "new_estimated_tokens": tokens,
                "cumulative_added_estimated_tokens": cumulative,
                "loaded_paths": loaded,
            }
        )
    return results, cumulative


def compare_cumulative(
    root: Path,
    baseline: dict[str, Any],
    graph: dict[str, Any],
    trace: dict[str, Any],
    *,
    ambient_paths: list[str] | None = None,
) -> dict[str, Any]:
    ambient = ambient_paths or ["AGENTS.md"]
    legacy_paths = baseline_paths(baseline)
    legacy_initial = baseline_metrics(root, legacy_paths)
    graph_initial = graph_runtime_metrics(root, graph, ambient)
    phases = load_trace(trace)

    legacy_phase_results, legacy_added = phase_additions(
        root,
        phases,
        seed_hashes=_seed_hashes(root, legacy_paths),
    )
    graph_phase_results, graph_added = phase_additions(
        root,
        phases,
        seed_hashes=_graph_seed_hashes(root, graph, ambient),
    )

    legacy_total = int(legacy_initial["estimated_tokens"]) + legacy_added
    graph_total = int(graph_initial["model_visible_estimated_tokens"]) + graph_added

    return {
        "schema_version": 1,
        "measurement": (
            "cumulative introduced model-visible context: initial context plus exact-hash-deduped "
            "source deltas from an explicit task trace; unchanged context is not re-injected"
        ),
        "graph_subject": graph.get("subject"),
        "graph_base_sha": graph.get("base_sha"),
        "legacy": {
            "initial_estimated_tokens": legacy_initial["estimated_tokens"],
            "phases": legacy_phase_results,
            "added_estimated_tokens": legacy_added,
            "cumulative_estimated_tokens": legacy_total,
        },
        "graph_runtime": {
            "initial_estimated_tokens": graph_initial["model_visible_estimated_tokens"],
            "phases": graph_phase_results,
            "added_estimated_tokens": graph_added,
            "cumulative_estimated_tokens": graph_total,
        },
        "estimated_cumulative_reduction_percent": reduction_percent(legacy_total, graph_total),
        "note": (
            "This is a deterministic task-trace proxy, not measured ChatGPT Plus quota or an LLM execution transcript. "
            "The trace must be tied to a real repository task/contract and frozen with the result."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare cumulative context introduction across an explicit task trace")
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--baseline-json", required=True, type=Path)
    parser.add_argument("--graph-json", required=True, type=Path)
    parser.add_argument("--trace-json", required=True, type=Path)
    parser.add_argument("--ambient", action="append", default=None)
    parser.add_argument("--require-reduction", type=float)
    args = parser.parse_args()

    try:
        result = compare_cumulative(
            args.repo.resolve(),
            load_json(args.baseline_json),
            load_json(args.graph_json),
            load_json(args.trace_json),
            ambient_paths=args.ambient,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, sort_keys=True))
        return 2

    reduction = result["estimated_cumulative_reduction_percent"]
    passed = (
        args.require_reduction is None
        or (reduction is not None and reduction >= args.require_reduction)
    )
    result["gate"] = {
        "status": "PASS" if passed else "FAIL",
        "required_reduction_percent": args.require_reduction,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
