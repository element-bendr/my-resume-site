from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Iterable

from icm_io import atomic_write_text, fsync_directory, safe_repo_path

GRAPH_SCHEMA_VERSION = 1
GRAPH_ROOT = Path(".icm/graph")
NODES_FILE = "nodes.jsonl"
EDGES_FILE = "edges.jsonl"
VERSION_FILE = "schema-version.json"


class GraphStoreError(ValueError):
    pass


def graph_root(root: Path) -> Path:
    return safe_repo_path(root, GRAPH_ROOT)


def _replace_path(source: Path, target: Path) -> None:
    os.replace(source, target)


def _canonical_record(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _validate_record_list(records: Iterable[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
    values = list(records)
    seen: set[str] = set()
    for index, record in enumerate(values, start=1):
        if not isinstance(record, dict):
            raise GraphStoreError(f"{kind} record {index} must be an object")
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            raise GraphStoreError(f"{kind} record {index} requires non-empty id")
        if record_id in seen:
            raise GraphStoreError(f"duplicate {kind} id: {record_id}")
        seen.add(record_id)
    return sorted(values, key=lambda item: item["id"])


def _read_jsonl(path: Path, kind: str) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    if not path.is_file():
        raise GraphStoreError(f"{path}: expected file")
    records: list[dict[str, Any]] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise GraphStoreError(f"{path}:{number}: invalid JSON: {exc.msg}") from exc
        if not isinstance(value, dict):
            raise GraphStoreError(f"{path}:{number}: record must be object")
        records.append(value)
    return _validate_record_list(records, kind)


def _jsonl_content(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    return "".join(_canonical_record(record) + "\n" for record in records)


def load_graph(root: Path) -> dict[str, Any]:
    base = graph_root(root)
    required = [NODES_FILE, EDGES_FILE, VERSION_FILE]
    present = [name for name in required if (base / name).exists()]
    if present and len(present) != len(required):
        missing = sorted(set(required) - set(present))
        raise GraphStoreError(
            f"incomplete graph store under {base}: missing {', '.join(missing)}"
        )
    version_path = base / VERSION_FILE
    if version_path.exists():
        try:
            version = json.loads(version_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise GraphStoreError(f"{version_path}: invalid JSON: {exc.msg}") from exc
        if not isinstance(version, dict):
            raise GraphStoreError(f"{version_path}: expected object")
        schema_version = version.get("graph_schema_version")
        if schema_version != GRAPH_SCHEMA_VERSION:
            raise GraphStoreError(
                f"unsupported graph schema version {schema_version!r}; expected {GRAPH_SCHEMA_VERSION}"
            )
    else:
        schema_version = GRAPH_SCHEMA_VERSION

    return {
        "schema_version": schema_version,
        "nodes": _read_jsonl(base / NODES_FILE, "node"),
        "edges": _read_jsonl(base / EDGES_FILE, "edge"),
    }


def write_graph(
    root: Path,
    *,
    nodes: Iterable[dict[str, Any]],
    edges: Iterable[dict[str, Any]],
    schema_version: int = GRAPH_SCHEMA_VERSION,
) -> dict[str, Any]:
    if schema_version != GRAPH_SCHEMA_VERSION:
        raise GraphStoreError(
            f"unsupported graph schema version {schema_version!r}; expected {GRAPH_SCHEMA_VERSION}"
        )

    sorted_nodes = _validate_record_list(nodes, "node")
    sorted_edges = _validate_record_list(edges, "edge")
    desired = {
        "schema_version": GRAPH_SCHEMA_VERSION,
        "nodes": sorted_nodes,
        "edges": sorted_edges,
    }
    base = graph_root(root)

    if base.exists():
        required = [NODES_FILE, EDGES_FILE, VERSION_FILE]
        present = [name for name in required if (base / name).exists()]
        if not present:
            raise GraphStoreError(
                f"canonical graph directory already exists without a complete store: {base}"
            )
        existing = load_graph(root)
        if existing == desired:
            return desired
        raise GraphStoreError(
            "refusing to mutate existing canonical graph store through write_graph; "
            "use an explicit graph migration workflow"
        )

    version = {
        "graph_schema_version": GRAPH_SCHEMA_VERSION,
        "storage_contract_version": 1,
    }

    base.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".graph-stage-", dir=base.parent))
    try:
        atomic_write_text(stage / NODES_FILE, _jsonl_content(sorted_nodes))
        atomic_write_text(stage / EDGES_FILE, _jsonl_content(sorted_edges))
        atomic_write_text(
            stage / VERSION_FILE,
            json.dumps(version, indent=2, sort_keys=True) + "\n",
        )

        # Promotion is one same-filesystem directory rename. Canonical state is
        # untouched until every staged artifact exists and is fsynced.
        fsync_directory(stage)
        _replace_path(stage, base)
        fsync_directory(base.parent)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise

    return desired


def replace_graph(
    root: Path,
    *,
    nodes: Iterable[dict[str, Any]],
    edges: Iterable[dict[str, Any]],
    expected_current: dict[str, Any],
    schema_version: int = GRAPH_SCHEMA_VERSION,
) -> dict[str, Any]:
    if schema_version != GRAPH_SCHEMA_VERSION:
        raise GraphStoreError(
            f"unsupported graph schema version {schema_version!r}; expected {GRAPH_SCHEMA_VERSION}"
        )

    sorted_nodes = _validate_record_list(nodes, "node")
    sorted_edges = _validate_record_list(edges, "edge")
    desired = {
        "schema_version": GRAPH_SCHEMA_VERSION,
        "nodes": sorted_nodes,
        "edges": sorted_edges,
    }
    base = graph_root(root)
    if not base.is_dir():
        raise GraphStoreError("cannot refresh graph before canonical graph initialization")

    existing = load_graph(root)
    if existing != expected_current:
        raise GraphStoreError(
            "canonical graph changed after refresh planning; refusing replacement"
        )
    if existing == desired:
        return desired

    version = {
        "graph_schema_version": GRAPH_SCHEMA_VERSION,
        "storage_contract_version": 1,
    }

    parent = base.parent
    stage = Path(tempfile.mkdtemp(prefix=".graph-refresh-stage-", dir=parent))
    backup = Path(tempfile.mkdtemp(prefix=".graph-refresh-backup-", dir=parent))
    backup.rmdir()
    original_moved = False
    promoted = False
    try:
        atomic_write_text(stage / NODES_FILE, _jsonl_content(sorted_nodes))
        atomic_write_text(stage / EDGES_FILE, _jsonl_content(sorted_edges))
        atomic_write_text(
            stage / VERSION_FILE,
            json.dumps(version, indent=2, sort_keys=True) + "\n",
        )
        fsync_directory(stage)

        _replace_path(base, backup)
        original_moved = True
        fsync_directory(parent)

        try:
            _replace_path(stage, base)
            promoted = True
            fsync_directory(parent)
        except Exception:
            if backup.exists() and not base.exists():
                _replace_path(backup, base)
                original_moved = False
                fsync_directory(parent)
            raise

        shutil.rmtree(backup, ignore_errors=True)
        original_moved = False
        return desired
    except Exception:
        if original_moved and backup.exists() and not base.exists():
            try:
                _replace_path(backup, base)
                fsync_directory(parent)
                original_moved = False
            except Exception:
                pass
        raise
    finally:
        if stage.exists():
            shutil.rmtree(stage, ignore_errors=True)
        if backup.exists() and (promoted or not original_moved):
            shutil.rmtree(backup, ignore_errors=True)
