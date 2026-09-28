from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

VALID_WORKFLOW_STATUS = {"active", "blocked", "certified", "completed"}
VALID_STAGE_STATUS = {"pending", "active", "blocked", "certified", "stale"}
VALID_EXECUTION_MODES = {"read-only-audit", "implementation", "certification", "research"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")
REQUIRED_STAGE_SECTIONS = (
    "## Authority / ownership",
    "## Inputs",
    "## Objective",
    "## In Scope",
    "## Out of Scope",
    "## Dependencies",
    "## Process",
    "## Outputs",
    "## Acceptance",
    "## Verify",
    "## Protected State",
    "## Known closed decisions",
    "## Stop Conditions",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def safe_repo_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f"invalid repository-relative path: {relative!r}")
    root = root.resolve()
    candidate = (root / relative).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"path escapes repository root: {relative}")
    return candidate


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def git_output(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    value = result.stdout.strip()
    return value or None


def current_commit(root: Path) -> str | None:
    value = git_output(root, "rev-parse", "HEAD")
    return value if value and SHA_RE.fullmatch(value) else None


def current_branch(root: Path) -> str | None:
    return git_output(root, "branch", "--show-current")


def git_blob(root: Path, relative: str) -> str:
    path = safe_repo_path(root, relative)
    if not path.is_file():
        raise FileNotFoundError(relative)
    result = subprocess.run(
        ["git", "-C", str(root), "hash-object", "--", relative],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def sha256_file(root: Path, relative: str) -> str:
    path = safe_repo_path(root, relative)
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def state_files(root: Path, include_completed: bool = False) -> list[Path]:
    root = root.resolve()
    result: list[Path] = []
    locations = ["workflow/active"]
    if include_completed:
        locations.append("workflow/completed")

    for relative_root in locations:
        # Validate the resolved directory but preserve lexical paths so active /
        # completed location semantics remain stable for safe in-repo symlinks.
        safe_repo_path(root, relative_root)
        folder = root / relative_root
        if not folder.exists():
            continue
        for state_path in sorted(folder.glob("*/state.json")):
            relative_state = state_path.relative_to(root).as_posix()
            safe_repo_path(root, relative_state)
            result.append(state_path)
    return result


def find_placeholders(text: str) -> list[str]:
    return sorted(set(PLACEHOLDER_RE.findall(text)))


def validate_stage_contract(root: Path, relative: str, *, require_complete: bool = True, historical: bool = False) -> list[str]:
    errors: list[str] = []
    try:
        path = safe_repo_path(root, relative)
    except ValueError as exc:
        return [str(exc)]
    if historical and not path.is_file():
        return []
    if not path.is_file():
        return [f"missing stage context {relative}"]
    text = path.read_text(encoding="utf-8")
    for section in REQUIRED_STAGE_SECTIONS:
        if section not in text:
            errors.append(f"{relative}: missing required stage section: {section}")
    if require_complete:
        for placeholder in find_placeholders(text):
            errors.append(f"{relative}: unresolved placeholder: {placeholder}")
    return errors


def validate_execution(execution: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(execution, dict):
        return ["execution object is required"]
    mode = execution.get("mode")
    if mode not in VALID_EXECUTION_MODES:
        errors.append(f"invalid execution mode {mode!r}")
    for key in ("branch", "worktree", "owner"):
        value = execution.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"execution.{key} must be a non-empty string")
    write_paths = execution.get("write_paths")
    if not isinstance(write_paths, list) or not all(isinstance(item, str) and item for item in write_paths):
        errors.append("execution.write_paths must be a string list")
    elif mode == "read-only-audit" and write_paths:
        errors.append("read-only-audit execution must have empty write_paths")
    return errors


def stage_dependency_cycles(stages: list[dict[str, Any]]) -> list[list[str]]:
    graph: dict[str, list[str]] = {}
    for stage in stages:
        if not isinstance(stage, dict):
            continue
        stage_id = stage.get("id")
        if not isinstance(stage_id, str) or not stage_id:
            continue
        deps = stage.get("depends_on_stages", [])
        graph[stage_id] = [dep for dep in deps if isinstance(dep, str)] if isinstance(deps, list) else []

    state: dict[str, int] = {node: 0 for node in graph}
    stack: list[str] = []
    position: dict[str, int] = {}
    cycles: list[list[str]] = []
    seen: set[tuple[str, ...]] = set()

    def canonical(cycle: list[str]) -> tuple[str, ...]:
        body = cycle[:-1]
        if not body:
            return tuple(cycle)
        rotations = [tuple(body[i:] + body[:i]) for i in range(len(body))]
        best = min(rotations)
        return best + (best[0],)

    def visit(node: str) -> None:
        state[node] = 1
        position[node] = len(stack)
        stack.append(node)
        for dep in graph.get(node, []):
            if dep not in graph:
                continue
            if state[dep] == 0:
                visit(dep)
            elif state[dep] == 1:
                cycle = stack[position[dep]:] + [dep]
                key = canonical(cycle)
                if key not in seen:
                    seen.add(key)
                    cycles.append(list(key))
        stack.pop()
        position.pop(node, None)
        state[node] = 2

    for node in graph:
        if state[node] == 0:
            visit(node)
    return cycles


def _validate_location(state_path: Path, workflow_id: str | None, status: str | None) -> list[str]:
    errors: list[str] = []
    parent = state_path.parent.name
    if workflow_id and parent != workflow_id:
        errors.append(f"{state_path}: directory name {parent!r} must match workflow_id {workflow_id!r}")
    if "/workflow/active/" in f"/{state_path.as_posix()}" and status == "completed":
        errors.append(f"{state_path}: completed workflow cannot remain under workflow/active")
    if "/workflow/completed/" in f"/{state_path.as_posix()}" and status != "completed":
        errors.append(f"{state_path}: workflow under workflow/completed must have status completed")
    return errors


def validate_state(root: Path, state_path: Path, historical: bool = False) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    try:
        relative_state = state_path.relative_to(root).as_posix()
        safe_repo_path(root, relative_state)
        state = load_json(state_path)
    except Exception as exc:
        return [f"{state_path}: {exc}"]

    if state.get("schema_version") != 1:
        errors.append(f"{state_path}: schema_version must be 1")

    workflow_id = state.get("workflow_id")
    if not isinstance(workflow_id, str) or not workflow_id:
        errors.append(f"{state_path}: workflow_id is required")
        workflow_id = None

    status = state.get("status")
    if status not in VALID_WORKFLOW_STATUS:
        errors.append(f"{state_path}: invalid workflow status {status!r}")

    errors.extend(_validate_location(state_path, workflow_id, status))

    provenance = state.get("provenance")
    if not isinstance(provenance, dict):
        errors.append(f"{state_path}: provenance object is required")
    else:
        started = provenance.get("started_from_commit")
        validated = provenance.get("validated_commit")
        if started is not None and (not isinstance(started, str) or not SHA_RE.fullmatch(started)):
            errors.append(f"{state_path}: started_from_commit must be a 40-char lowercase Git SHA or null")
        if validated is not None and (not isinstance(validated, str) or not SHA_RE.fullmatch(validated)):
            errors.append(f"{state_path}: validated_commit must be a 40-char lowercase Git SHA or null")
        if status == "completed" and not (isinstance(started, str) and SHA_RE.fullmatch(started)):
            errors.append(f"{state_path}: completed workflow requires started_from_commit")
        if status == "completed" and not (isinstance(validated, str) and SHA_RE.fullmatch(validated)):
            errors.append(f"{state_path}: completed workflow requires validated_commit")

    if not historical:
        errors.extend(f"{state_path}: {error}" for error in validate_execution(state.get("execution")))

    stages = state.get("stages")
    if not isinstance(stages, list) or not stages:
        errors.append(f"{state_path}: stages must be a non-empty list")
        return errors

    stage_ids: list[str] = []
    active_like: list[str] = []
    for stage in stages:
        if not isinstance(stage, dict):
            errors.append(f"{state_path}: every stage must be an object")
            continue
        stage_id = stage.get("id")
        if not isinstance(stage_id, str) or not stage_id:
            errors.append(f"{state_path}: stage id is required")
            continue
        stage_ids.append(stage_id)
        stage_status = stage.get("status")
        if stage_status not in VALID_STAGE_STATUS:
            errors.append(f"{state_path}: {stage_id}: invalid status {stage_status!r}")
        if stage_status in {"active", "blocked"}:
            active_like.append(stage_id)

        context = stage.get("context")
        if not isinstance(context, str):
            errors.append(f"{state_path}: {stage_id}: context path is required")
        else:
            try:
                safe_repo_path(root, context)
            except ValueError as exc:
                errors.append(f"{state_path}: {stage_id}: {exc}")
            else:
                require_complete = stage_status in {"active", "certified"}
                for error in validate_stage_contract(root, context, require_complete=require_complete, historical=historical):
                    errors.append(f"{state_path}: {stage_id}: {error}")

        upstream = stage.get("depends_on_stages", [])
        if not isinstance(upstream, list) or not all(isinstance(item, str) for item in upstream):
            errors.append(f"{state_path}: {stage_id}: depends_on_stages must be a string list")

        dependencies = stage.get("depends_on", [])
        if not isinstance(dependencies, list):
            errors.append(f"{state_path}: {stage_id}: depends_on must be a list")
            continue
        for dep in dependencies:
            if not isinstance(dep, dict) or not isinstance(dep.get("path"), str):
                errors.append(f"{state_path}: {stage_id}: invalid dependency record")
                continue
            relative = dep["path"]
            try:
                path = safe_repo_path(root, relative)
                if not historical and not path.is_file():
                    errors.append(f"{state_path}: {stage_id}: missing dependency {relative}")
            except ValueError as exc:
                errors.append(f"{state_path}: {stage_id}: {exc}")
            blob = dep.get("blob")
            if blob is not None and (not isinstance(blob, str) or not SHA_RE.fullmatch(blob)):
                errors.append(f"{state_path}: {stage_id}: blob must be a 40-char lowercase Git SHA or null")
            if stage_status == "certified" and not blob:
                errors.append(f"{state_path}: {stage_id}: certified dependency {relative} is unpinned")

        outputs = stage.get("outputs", [])
        if not isinstance(outputs, list) or not all(isinstance(item, str) for item in outputs):
            errors.append(f"{state_path}: {stage_id}: outputs must be a string list")
        elif stage_status == "certified" and not historical:
            for output in outputs:
                try:
                    if not safe_repo_path(root, output).exists():
                        errors.append(f"{state_path}: {stage_id}: missing certified output {output}")
                except ValueError as exc:
                    errors.append(f"{state_path}: {stage_id}: {exc}")

        report = stage.get("completion_report")
        if report is not None and not isinstance(report, str):
            errors.append(f"{state_path}: {stage_id}: completion_report must be string or null")
        elif isinstance(report, str):
            try:
                safe_repo_path(root, report)
            except ValueError as exc:
                errors.append(f"{state_path}: {stage_id}: {exc}")

    if len(stage_ids) != len(set(stage_ids)):
        errors.append(f"{state_path}: stage ids must be unique")

    known = set(stage_ids)
    for stage in stages:
        if not isinstance(stage, dict):
            continue
        for upstream_id in stage.get("depends_on_stages", []):
            if upstream_id not in known:
                errors.append(f"{state_path}: {stage.get('id')}: unknown upstream stage {upstream_id}")

    for cycle in stage_dependency_cycles(stages):
        errors.append(f"{state_path}: stage dependency cycle: {' -> '.join(cycle)}")

    active_stage = state.get("active_stage")
    if status in {"active", "blocked"}:
        if active_stage not in known:
            errors.append(f"{state_path}: active_stage must name a stage")
        else:
            selected = next(stage for stage in stages if stage.get("id") == active_stage)
            expected_status = "active" if status == "active" else "blocked"
            if selected.get("status") != expected_status:
                errors.append(f"{state_path}: active_stage status must be {expected_status}")
        if len(active_like) != 1:
            errors.append(f"{state_path}: active/blocked workflow must have exactly one active-like stage")
    elif status in {"certified", "completed"}:
        if active_stage is not None:
            errors.append(f"{state_path}: {status} workflow must have active_stage null")
        unfinished = [stage.get("id") for stage in stages if isinstance(stage, dict) and stage.get("status") != "certified"]
        if unfinished:
            errors.append(f"{state_path}: {status} workflow has non-certified stages: {', '.join(map(str, unfinished))}")

    return errors


def stage_staleness(root: Path, state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    stages = state.get("stages", [])
    report: dict[str, dict[str, Any]] = {}
    for stage in stages:
        stage_id = stage["id"]
        direct: list[str] = []
        unpinned: list[str] = []
        for dep in stage.get("depends_on", []):
            relative = dep["path"]
            expected = dep.get("blob")
            if not expected:
                unpinned.append(relative)
                continue
            try:
                actual = git_blob(root, relative)
            except Exception:
                direct.append(relative)
                continue
            if actual != expected:
                direct.append(relative)
        report[stage_id] = {"stale": bool(direct), "direct": direct, "upstream": [], "unpinned": unpinned}
    changed = True
    while changed:
        changed = False
        for stage in stages:
            stage_id = stage["id"]
            upstream_stale = [upstream for upstream in stage.get("depends_on_stages", []) if report.get(upstream, {}).get("stale")]
            if upstream_stale != report[stage_id]["upstream"]:
                report[stage_id]["upstream"] = upstream_stale
            new_value = bool(report[stage_id]["direct"] or upstream_stale)
            if new_value != report[stage_id]["stale"]:
                report[stage_id]["stale"] = new_value
                changed = True
    return report
