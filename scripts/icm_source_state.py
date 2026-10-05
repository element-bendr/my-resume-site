from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from icm_io import atomic_write_text, safe_repo_path

SOURCE_STATE_PATH = Path(".icm/state/source.json")
SOURCE_STATE_SCHEMA_VERSION = 1
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class SourceStateError(ValueError):
    pass


def graph_fingerprint(graph: dict[str, Any]) -> str:
    canonical = json.dumps(
        graph,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def source_state_path(root: Path) -> Path:
    return safe_repo_path(root, SOURCE_STATE_PATH)


def build_source_state(
    *,
    audit_contract_version: int,
    input_fingerprint: str,
    graph: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": SOURCE_STATE_SCHEMA_VERSION,
        "audit_contract_version": audit_contract_version,
        "input_fingerprint": input_fingerprint,
        "graph_fingerprint": graph_fingerprint(graph),
    }


def load_source_state(root: Path) -> dict[str, Any]:
    path = source_state_path(root)
    if not path.is_file():
        raise SourceStateError(f"missing source state: {path.relative_to(root.resolve())}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SourceStateError(f"{path}: invalid JSON: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise SourceStateError(f"{path}: expected object")

    required = {
        "schema_version",
        "audit_contract_version",
        "input_fingerprint",
        "graph_fingerprint",
    }
    extra = set(value) - required
    missing = required - set(value)
    if missing:
        raise SourceStateError(f"{path}: missing fields: {', '.join(sorted(missing))}")
    if extra:
        raise SourceStateError(f"{path}: unsupported fields: {', '.join(sorted(extra))}")
    if value.get("schema_version") != SOURCE_STATE_SCHEMA_VERSION:
        raise SourceStateError(
            f"{path}: schema_version must be {SOURCE_STATE_SCHEMA_VERSION}"
        )
    if not isinstance(value.get("audit_contract_version"), int):
        raise SourceStateError(f"{path}: audit_contract_version must be integer")
    for key in ("input_fingerprint", "graph_fingerprint"):
        fingerprint = value.get(key)
        if not isinstance(fingerprint, str) or not SHA256_RE.fullmatch(fingerprint):
            raise SourceStateError(f"{path}: {key} must be a lowercase SHA-256 hex digest")
    return value


def write_source_state(root: Path, state: dict[str, Any]) -> bool:
    path = source_state_path(root)
    content = json.dumps(state, indent=2, sort_keys=True) + "\n"
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        return False
    atomic_write_text(path, content)
    return True
