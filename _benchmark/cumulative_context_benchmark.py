#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
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


def _safe_file(root: Path, relative: str) -> Path:
    root = root.resolve()
    path = (root / relative).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"path escapes repository: {relative!r}")
    if not path.is_file():
        raise FileNotFoundError(relative)
    return path


def _normalize_read(raw: Any, *, phase: int, read_index: int) -> dict[str, Any]:
    if isinstance(raw, str) and raw:
        return {"path": raw}
    if not isinstance(raw, dict):
        raise ValueError(f"phase {phase} read {read_index}: expected path string or object")
    path = raw.get("path")
    if not isinstance(path, str) or not path:
        raise ValueError(f"phase {phase} read {read_index}: non-empty path required")

    start = raw.get("start_line")
    end = raw.get("end_line")
    if start is None and end is None:
        return {"path": path}
    if not isinstance(start, int) or not isinstance(end, int):
        raise ValueError(f"phase {phase} read {read_index}: start_line/end_line must both be integers")
    if start < 1 or end < start:
        raise ValueError(f"phase {phase} read {read_index}: invalid line range {start}-{end}")
    return {"path": path, "start_line": start, "end_line": end}


def load_trace(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("phases"), list):
        raise ValueError("trace JSON requires phases[]")
    phases: list[dict[str, Any]] = []
    for index, raw in enumerate(payload["phases"], 1):
        if not isinstance(raw, dict):
            raise ValueError(f"phase {index}: expected object")
        name = raw.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError(f"phase {index}: non-empty name required")

        shared = raw.get("reads")
        if shared is None:
            shared = raw.get("paths")
        legacy_values = raw.get("legacy_reads", shared)
        graph_values = raw.get("graph_reads", shared)
        if not isinstance(legacy_values, list) or not isinstance(graph_values, list):
            raise ValueError(
                f"phase {index}: provide reads[]/paths[] or both legacy_reads[] and graph_reads[]"
            )

        legacy_reads = [
            _normalize_read(value, phase=index, read_index=read_index)
            for read_index, value in enumerate(legacy_values, 1)
        ]
        graph_reads = [
            _normalize_read(value, phase=index, read_index=read_index)
            for read_index, value in enumerate(graph_values, 1)
        ]
        phases.append(
            {
                "name": name,
                "legacy_reads": legacy_reads,
                "graph_reads": graph_reads,
            }
        )
    if not phases:
        raise ValueError("trace requires at least one phase")
    return phases


def _seed_state(root: Path, paths: list[str]) -> tuple[dict[str, None | set[int]], set[str]]:
    coverage: dict[str, None | set[int]] = {}
    hashes: set[str] = set()
    for relative in paths:
        path = _safe_file(root, relative)
        coverage[relative] = None
        hashes.add(str(source_metric(path)["sha256"]))
    return coverage, hashes


def _graph_seed_paths(graph: dict[str, Any], ambient: list[str]) -> list[str]:
    paths = list(dict.fromkeys(ambient))
    for source in graph.get("bootstrap_sources", []):
        if not isinstance(source, dict):
            continue
        path = source.get("path")
        if isinstance(path, str) and path:
            paths.append(path)
    return list(dict.fromkeys(paths))


def _read_delta(
    root: Path,
    read: dict[str, Any],
    *,
    coverage: dict[str, None | set[int]],
    seen_content_hashes: set[str],
) -> tuple[int, dict[str, Any]]:
    relative = read["path"]
    path = _safe_file(root, relative)
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    current = coverage.get(relative, set())

    if "start_line" not in read:
        if current is None:
            return 0, {"path": relative, "kind": "whole", "duplicate_or_preloaded": True}

        if not lines:
            content = ""
            new_line_numbers: list[int] = []
        else:
            covered = current if isinstance(current, set) else set()
            new_line_numbers = [idx for idx in range(1, len(lines) + 1) if idx not in covered]
            content = "".join(lines[idx - 1] for idx in new_line_numbers)

        full_digest = hashlib.sha256("".join(lines).encode()).hexdigest()
        coverage[relative] = None
        if full_digest in seen_content_hashes:
            return 0, {"path": relative, "kind": "whole", "duplicate_or_preloaded": True}
        seen_content_hashes.add(full_digest)

        tokens = (len(content) + 3) // 4
        return tokens, {
            "path": relative,
            "kind": "whole",
            "lines": len(new_line_numbers),
            "estimated_tokens": tokens,
            "duplicate_or_preloaded": False,
        }

    start = int(read["start_line"])
    end = int(read["end_line"])
    if end > len(lines):
        raise ValueError(f"{relative}: line range {start}-{end} exceeds {len(lines)} lines")
    if current is None:
        return 0, {
            "path": relative,
            "kind": "range",
            "start_line": start,
            "end_line": end,
            "duplicate_or_preloaded": True,
        }

    covered = current if isinstance(current, set) else set()
    new_line_numbers = [idx for idx in range(start, end + 1) if idx not in covered]
    content = "".join(lines[idx - 1] for idx in new_line_numbers)
    snippet_digest = hashlib.sha256(content.encode()).hexdigest()

    covered.update(range(start, end + 1))
    coverage[relative] = covered

    if not new_line_numbers or snippet_digest in seen_content_hashes:
        return 0, {
            "path": relative,
            "kind": "range",
            "start_line": start,
            "end_line": end,
            "duplicate_or_preloaded": True,
        }

    seen_content_hashes.add(snippet_digest)
    tokens = (len(content) + 3) // 4
    return tokens, {
        "path": relative,
        "kind": "range",
        "start_line": start,
        "end_line": end,
        "new_lines": len(new_line_numbers),
        "estimated_tokens": tokens,
        "duplicate_or_preloaded": False,
    }


def phase_additions(
    root: Path,
    phases: list[dict[str, Any]],
    *,
    seed_paths: list[str],
) -> tuple[list[dict[str, Any]], int]:
    coverage, hashes = _seed_state(root, seed_paths)
    results: list[dict[str, Any]] = []
    cumulative = 0

    for phase in phases:
        tokens = 0
        loaded_reads = 0
        duplicate_reads = 0
        details: list[dict[str, Any]] = []

        for read in phase["reads"]:
            added, detail = _read_delta(
                root,
                read,
                coverage=coverage,
                seen_content_hashes=hashes,
            )
            tokens += added
            if added:
                loaded_reads += 1
            else:
                duplicate_reads += 1
            details.append(detail)

        cumulative += tokens
        results.append(
            {
                "name": phase["name"],
                "new_reads": loaded_reads,
                "duplicate_or_preloaded_reads": duplicate_reads,
                "new_estimated_tokens": tokens,
                "cumulative_added_estimated_tokens": cumulative,
                "reads": details,
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

    legacy_phases = [
        {"name": phase["name"], "reads": phase["legacy_reads"]}
        for phase in phases
    ]
    graph_phases = [
        {"name": phase["name"], "reads": phase["graph_reads"]}
        for phase in phases
    ]

    legacy_phase_results, legacy_added = phase_additions(
        root,
        legacy_phases,
        seed_paths=legacy_paths,
    )
    graph_phase_results, graph_added = phase_additions(
        root,
        graph_phases,
        seed_paths=_graph_seed_paths(graph, ambient),
    )

    legacy_total = int(legacy_initial["estimated_tokens"]) + legacy_added
    graph_total = int(graph_initial["model_visible_estimated_tokens"]) + graph_added

    return {
        "schema_version": 2,
        "measurement": (
            "cumulative introduced model-visible context: initial context plus source deltas from an explicit "
            "task trace; each phase explicitly records legacy and graph-runtime reads; whole-file and exact line-range reads are supported; unchanged covered content is not re-injected"
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
            "Legacy and graph-runtime reads must represent the same task phase. Targeted line ranges must come from a real task retrieval plan and remain frozen with the result."
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
