from __future__ import annotations

import fnmatch
import subprocess
from pathlib import Path
from typing import Any, Iterable


class ProtectedStateError(ValueError):
    pass


def _diag(severity: str, code: str, subject: str, message: str) -> dict[str, str]:
    return {"severity": severity, "code": code, "subject": subject, "message": message}


def normalize_relative_path(value: str) -> str:
    raw = value.replace("\\", "/").strip()
    path = Path(raw)
    if not raw or path.is_absolute() or ".." in path.parts:
        raise ProtectedStateError(f"changed path must be repository-relative and traversal-free: {value!r}")
    normalized = path.as_posix()
    if normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def git_changed_paths(root: Path, base: str, head: str) -> list[str]:
    if not base or not head:
        raise ProtectedStateError("both base and head refs are required")
    try:
        output = subprocess.check_output(
            ["git", "diff", "--name-only", "--diff-filter=ACDMRTUXB", f"{base}...{head}", "--"],
            cwd=root,
            text=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.output or "").strip()
        raise ProtectedStateError(f"git diff failed for {base}...{head}: {detail}") from exc
    return sorted({normalize_relative_path(line) for line in output.splitlines() if line.strip()})


def _matches(path: str, rule_path: str, mode: str) -> bool:
    if mode == "exact":
        return path == rule_path
    if mode == "prefix":
        prefix = rule_path.rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    if mode == "glob":
        return fnmatch.fnmatchcase(path, rule_path)
    raise ProtectedStateError(f"unsupported protected-resource match mode: {mode!r}")


def protected_resources(graph: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        [
            node for node in graph.get("nodes", [])
            if isinstance(node, dict) and node.get("type") == "protected_resource"
        ],
        key=lambda node: str(node.get("id", "")),
    )


def validate_protected_changes(
    graph: dict[str, Any],
    changed_paths: Iterable[str],
    *,
    approvals: Iterable[str] = (),
) -> list[dict[str, str]]:
    approved = set(approvals)
    normalized = sorted({normalize_relative_path(path) for path in changed_paths})
    diagnostics: list[dict[str, str]] = []

    for resource in protected_resources(graph):
        resource_id = str(resource.get("id", "protected_resource"))
        attrs = resource.get("attributes")
        if not isinstance(attrs, dict):
            diagnostics.append(
                _diag("FAIL", "protected.attributes", resource_id, "protected resource attributes must be an object")
            )
            continue

        rule_path = attrs.get("path")
        policy = attrs.get("policy")
        mode = attrs.get("match", "exact")

        if not isinstance(rule_path, str) or not rule_path:
            diagnostics.append(_diag("FAIL", "protected.path", resource_id, "protected resource requires attributes.path"))
            continue
        try:
            rule_path = normalize_relative_path(rule_path)
        except ProtectedStateError as exc:
            diagnostics.append(_diag("FAIL", "protected.path", resource_id, str(exc)))
            continue
        if policy not in {"deny", "approval-required"}:
            diagnostics.append(
                _diag("FAIL", "protected.policy", resource_id, "policy must be deny or approval-required")
            )
            continue
        if mode not in {"exact", "prefix", "glob"}:
            diagnostics.append(
                _diag("FAIL", "protected.match", resource_id, "match must be exact, prefix, or glob")
            )
            continue

        matched = [path for path in normalized if _matches(path, rule_path, mode)]
        for path in matched:
            if policy == "deny":
                diagnostics.append(
                    _diag("FAIL", "protected.denied-change", resource_id, f"change to protected path is denied: {path}")
                )
            elif resource_id not in approved:
                diagnostics.append(
                    _diag(
                        "FAIL",
                        "protected.approval-required",
                        resource_id,
                        f"change requires explicit approval for {resource_id}: {path}",
                    )
                )

    diagnostics.sort(key=lambda item: (item["code"], item["subject"], item["message"]))
    return diagnostics
