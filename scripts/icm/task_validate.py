from __future__ import annotations

import fnmatch
import json
import re
import subprocess
from pathlib import Path
from typing import Any

SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class TaskValidationError(ValueError):
    pass


def load_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise TaskValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise TaskValidationError(f"{path}: invalid JSON: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise TaskValidationError(f"{path}: expected JSON object")
    return value


def _type_matches(value: Any, expected: str) -> bool:
    return (
        (expected == "object" and isinstance(value, dict))
        or (expected == "array" and isinstance(value, list))
        or (expected == "string" and isinstance(value, str))
        or (expected == "integer" and isinstance(value, int) and not isinstance(value, bool))
        or (expected == "boolean" and isinstance(value, bool))
        or (expected == "null" and value is None)
    )


def validate_schema(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Validate the strict JSON-Schema subset used by local-execution contracts.

    The template intentionally stays standard-library-only. Unsupported schema keywords
    are not silently interpreted; the canonical schemas use only the subset below.
    """

    errors: list[str] = []
    if "const" in schema and instance != schema["const"]:
        return [f"{path}: expected const {schema['const']!r}"]
    if "enum" in schema and instance not in schema["enum"]:
        return [f"{path}: value {instance!r} not in enum"]

    expected = schema.get("type")
    if expected is not None:
        allowed = expected if isinstance(expected, list) else [expected]
        if not any(isinstance(kind, str) and _type_matches(instance, kind) for kind in allowed):
            return [f"{path}: wrong type"]

    if isinstance(instance, str):
        minimum = schema.get("minLength")
        maximum = schema.get("maxLength")
        if isinstance(minimum, int) and len(instance) < minimum:
            errors.append(f"{path}: shorter than minLength")
        if isinstance(maximum, int) and len(instance) > maximum:
            errors.append(f"{path}: longer than maxLength")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, instance) is None:
            errors.append(f"{path}: does not match pattern")

    if isinstance(instance, list):
        minimum = schema.get("minItems")
        maximum = schema.get("maxItems")
        if isinstance(minimum, int) and len(instance) < minimum:
            errors.append(f"{path}: fewer than minItems")
        if isinstance(maximum, int) and len(instance) > maximum:
            errors.append(f"{path}: more than maxItems")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in instance]
            if len(encoded) != len(set(encoded)):
                errors.append(f"{path}: duplicate items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                errors.extend(validate_schema(item, item_schema, f"{path}[{index}]"))

    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in instance:
                    errors.append(f"{path}: missing required field {key}")
        if schema.get("additionalProperties") is False and isinstance(properties, dict):
            for key in instance:
                if key not in properties:
                    errors.append(f"{path}: unsupported field {key}")
        if isinstance(properties, dict):
            for key, value in instance.items():
                child = properties.get(key)
                if isinstance(child, dict):
                    errors.extend(validate_schema(value, child, f"{path}.{key}"))
    return errors


def _git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "git command failed").strip()
        raise TaskValidationError(detail) from exc
    return result.stdout.strip()


def read_ref(root: Path, ref: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--verify", "--quiet", ref],
        capture_output=True,
        text=True,
    )
    if result.returncode == 1:
        return None
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "git rev-parse failed").strip()
        raise TaskValidationError(detail)
    value = result.stdout.strip()
    if not SHA_RE.fullmatch(value):
        raise TaskValidationError(f"ref {ref!r} resolved to invalid SHA: {value!r}")
    return value


def snapshot_refs(root: Path, refs: list[str]) -> dict[str, str | None]:
    return {ref: read_ref(root, ref) for ref in refs}


def changed_refs(root: Path, snapshot: dict[str, str | None]) -> list[str]:
    changes: list[str] = []
    for ref, before in snapshot.items():
        after = read_ref(root, ref)
        if after != before:
            changes.append(f"{ref}: {before or 'missing'} -> {after or 'missing'}")
    return changes


def _safe_pattern(pattern: str) -> bool:
    if not pattern or pattern.startswith("/"):
        return False
    parts = pattern.replace("\\", "/").split("/")
    return ".." not in parts and pattern not in {"*", "**"}


def path_matches(path: str, pattern: str) -> bool:
    normalized = path.replace("\\", "/").lstrip("./")
    candidate = pattern.replace("\\", "/").lstrip("./")
    if candidate.endswith("/**"):
        prefix = candidate[:-3].rstrip("/")
        return normalized == prefix or normalized.startswith(prefix + "/")
    return fnmatch.fnmatchcase(normalized, candidate)


def validate_changed_paths(task: dict[str, Any], changed_paths: list[str]) -> list[str]:
    errors: list[str] = []
    allowed = task.get("write_paths", [])
    protected = task.get("protected_paths", [])
    for path in sorted(set(changed_paths)):
        if not isinstance(path, str) or not _safe_pattern(path):
            errors.append(f"unsafe changed path: {path!r}")
            continue
        if not any(path_matches(path, pattern) for pattern in allowed):
            errors.append(f"changed path outside declared write scope: {path}")
        for pattern in protected:
            if path_matches(path, pattern):
                errors.append(f"changed path intersects protected state: {path} matches {pattern}")
    return errors


def validate_task(
    repo_root: Path,
    task: dict[str, Any],
    *,
    expected_repository: str,
    trusted_control_refs: set[str],
    allowed_validation_ids: set[str],
    trusted_ref_sha: str | None = None,
) -> list[str]:
    root = Path(repo_root).resolve()
    schema = load_json_object(root / "schemas/icm-task.schema.json")
    errors = validate_schema(task, schema)
    if errors:
        return sorted(set(errors))

    if task["repository"] != expected_repository:
        errors.append(
            f"repository mismatch: task={task['repository']!r} expected={expected_repository!r}"
        )

    origin_ref = task["origin"]["ref"]
    if origin_ref not in trusted_control_refs:
        errors.append(f"untrusted control ref: {origin_ref}")

    requested_validation = set(task["validation"])
    unknown_validation = sorted(requested_validation - allowed_validation_ids)
    if unknown_validation:
        errors.append(f"validation identifiers are not allowlisted: {', '.join(unknown_validation)}")

    for field in ("write_paths", "protected_paths"):
        for pattern in task[field]:
            if not _safe_pattern(pattern):
                errors.append(f"unsafe {field} pattern: {pattern!r}")

    for write_pattern in task["write_paths"]:
        for protected_pattern in task["protected_paths"]:
            # Exact/prefix overlap is rejected up front. Glob ambiguity is still enforced
            # against actual changed paths after execution.
            w = write_pattern.removesuffix("/**").rstrip("/")
            p = protected_pattern.removesuffix("/**").rstrip("/")
            if w == p or (w and p and (w.startswith(p + "/") or p.startswith(w + "/"))):
                errors.append(
                    f"declared write scope overlaps protected path: {write_pattern} vs {protected_pattern}"
                )

    base_sha = task["base_sha"]
    try:
        _git(root, "cat-file", "-e", f"{base_sha}^{{commit}}")
    except TaskValidationError:
        errors.append(f"base SHA does not exist locally: {base_sha}")

    resolved = trusted_ref_sha
    if resolved is None:
        try:
            resolved = _git(root, "rev-parse", task["trusted_ref"])
        except TaskValidationError:
            errors.append(f"trusted ref is unavailable locally: {task['trusted_ref']}")
            resolved = None
    if resolved is not None:
        if not SHA_RE.fullmatch(resolved):
            errors.append(f"trusted ref resolved to invalid SHA: {resolved!r}")
        elif resolved != base_sha:
            errors.append(
                f"stale base SHA: task={base_sha} trusted_ref={task['trusted_ref']} resolved={resolved}"
            )

    if task["claim"] != {
        "strategy": "atomic_git_ref",
        "ref_prefix": "refs/heads/icm/claims/",
        "allow_force_update": False,
        "stale_takeover": "coordinator_authorized_only",
    }:
        errors.append("claim policy does not match frozen V1 contract")

    return sorted(set(errors))


def require_valid_task(*args: Any, **kwargs: Any) -> None:
    errors = validate_task(*args, **kwargs)
    if errors:
        raise TaskValidationError("; ".join(errors))
