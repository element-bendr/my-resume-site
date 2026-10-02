from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from icm_graph_validate import graph_status, validate_graph
from icm_io import atomic_write_text, safe_repo_path

AUDIT_DIR = Path(".icm/audit")
PROPOSAL_FILE = "proposal.json"
AUDIT_CONTRACT_VERSION = 1


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9_-]+", "-", value.lower()).strip("-_")
    return cleaned or "unnamed"


def _stable_path_id(prefix: str, relative: str) -> str:
    slug = _slug(relative.replace("/", "-"))
    digest = hashlib.sha1(relative.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}.{slug[:80]}-{digest}"


def _title_from_markdown(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip() or path.stem
    except (OSError, UnicodeError):
        pass
    return path.stem.replace("-", " ").replace("_", " ").title()


def _node(
    node_id: str,
    node_type: str,
    title: str,
    *,
    status: str | None = None,
    origin_kind: str,
    origin_path: str | None = None,
    origin_ref: str | None = None,
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": origin_kind}
    if origin_path is not None:
        origin["path"] = origin_path
    if origin_ref is not None:
        origin["ref"] = origin_ref
    value: dict[str, Any] = {
        "schema_version": 1,
        "id": node_id,
        "type": node_type,
        "title": title,
        "origin": origin,
        "attributes": attributes or {},
    }
    if status is not None:
        value["status"] = status
    return value


def _edge(
    edge_id: str,
    edge_type: str,
    source: str,
    target: str,
    *,
    origin_kind: str,
    origin_path: str | None = None,
) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": origin_kind}
    if origin_path is not None:
        origin["path"] = origin_path
    return {
        "schema_version": 1,
        "id": edge_id,
        "type": edge_type,
        "from": source,
        "to": target,
        "origin": origin,
        "attributes": {},
    }


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def _safe_repo_path(root: Path, value: str) -> tuple[str, Path]:
    raw = value.replace("\\", "/").strip()
    if not raw:
        raise ValueError(f"unsafe repository-relative path: {value!r}")
    relative = Path(raw).as_posix()
    return relative, safe_repo_path(root, relative)


def _project_title(root: Path) -> str:
    try:
        _, readme = _safe_repo_path(root, "README.md")
    except ValueError:
        return root.name
    if readme.is_file():
        return _title_from_markdown(readme)
    return root.name


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_input_manifest(root: Path) -> list[dict[str, Any]]:
    root = root.resolve()
    content_paths: set[str] = set()
    existence_paths: set[str] = set()
    unsafe_paths: set[str] = set()

    for relative in ("README.md", "AGENTS.md", "CONTEXT.md", "HANDOFF.md"):
        try:
            safe_relative, resolved = _safe_repo_path(root, relative)
        except ValueError:
            unsafe_paths.add(relative)
            continue
        if resolved.is_file():
            content_paths.add(safe_relative)

    for decision_root_relative in ("decisions", "docs/decisions"):
        try:
            _, decision_root = _safe_repo_path(root, decision_root_relative)
        except ValueError:
            unsafe_paths.add(decision_root_relative)
            continue
        if decision_root.is_dir():
            for path in sorted(decision_root.glob("*.md")):
                if path.name.lower() == "readme.md":
                    continue
                relative = path.relative_to(root).as_posix()
                try:
                    safe_relative, resolved = _safe_repo_path(root, relative)
                except ValueError:
                    unsafe_paths.add(relative)
                    continue
                if resolved.is_file():
                    content_paths.add(safe_relative)

    state_paths: list[tuple[str, Path]] = []
    for workflow_root_relative in ("workflow/active", "workflow/completed"):
        try:
            _, workflow_root = _safe_repo_path(root, workflow_root_relative)
        except ValueError:
            unsafe_paths.add(workflow_root_relative)
            continue
        if not workflow_root.is_dir():
            continue
        for candidate in sorted(workflow_root.glob("*/state.json")):
            relative_state = candidate.relative_to(root).as_posix()
            try:
                safe_state, resolved_state = _safe_repo_path(root, relative_state)
            except ValueError:
                unsafe_paths.add(relative_state)
                continue
            state_paths.append((safe_state, resolved_state))

    for relative_state, state_path in state_paths:
        content_paths.add(relative_state)
        try:
            state = _load_json(state_path)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        stages = state.get("stages")
        if not isinstance(stages, list):
            continue
        for stage in stages:
            if not isinstance(stage, dict):
                continue
            context_path = stage.get("context")
            if isinstance(context_path, str) and context_path:
                try:
                    safe_context, resolved_context = _safe_repo_path(root, context_path)
                except ValueError:
                    pass
                else:
                    if resolved_context.is_file():
                        content_paths.add(safe_context)
            dependencies = stage.get("depends_on")
            if isinstance(dependencies, list):
                for dependency in dependencies:
                    if isinstance(dependency, dict) and isinstance(dependency.get("path"), str):
                        try:
                            safe_dependency, _ = _safe_repo_path(root, dependency["path"])
                        except ValueError:
                            continue
                        existence_paths.add(safe_dependency)
            outputs = stage.get("outputs")
            if isinstance(outputs, list):
                for output in outputs:
                    if isinstance(output, str) and output:
                        try:
                            safe_output, _ = _safe_repo_path(root, output)
                        except ValueError:
                            continue
                        existence_paths.add(safe_output)

    manifest: list[dict[str, Any]] = []
    for relative in sorted(unsafe_paths):
        manifest.append({
            "path": relative,
            "kind": "unsafe",
            "exists": True,
        })
    for relative in sorted(content_paths):
        _, path = _safe_repo_path(root, relative)
        manifest.append({
            "path": relative,
            "kind": "content",
            "exists": path.is_file(),
            "sha256": _sha256_file(path) if path.is_file() else None,
        })
    for relative in sorted(existence_paths - content_paths):
        _, path = _safe_repo_path(root, relative)
        manifest.append({
            "path": relative,
            "kind": "existence",
            "exists": path.exists(),
        })
    return manifest


def audit_input_fingerprint(root: Path) -> tuple[str, list[dict[str, Any]]]:
    manifest = audit_input_manifest(root)
    canonical = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest(), manifest


def audit_repository(root: Path) -> dict[str, Any]:
    root = root.resolve()
    project_slug = _slug(root.name)
    project_id = f"project.{project_slug}"

    nodes: dict[str, dict[str, Any]] = {}
    edges: dict[str, dict[str, Any]] = {}
    unresolved: list[str] = []

    def add_node(value: dict[str, Any]) -> None:
        nodes.setdefault(value["id"], value)

    def add_edge(value: dict[str, Any]) -> None:
        edges.setdefault(value["id"], value)

    readme_origin: str | None = None
    readme_error: str | None = None
    try:
        _, readme_path = _safe_repo_path(root, "README.md")
    except ValueError as exc:
        readme_error = str(exc)
    else:
        if readme_path.is_file():
            readme_origin = "README.md"

    add_node(
        _node(
            project_id,
            "project",
            _project_title(root),
            status="observed",
            origin_kind="observed",
            origin_path=readme_origin,
            attributes={"repository_name": root.name},
        )
    )

    if readme_error is not None:
        unresolved_id = _stable_path_id("unresolved", "README.md:unsafe")
        add_node(
            _node(
                unresolved_id,
                "unresolved",
                "Unsafe README path",
                status="blocking",
                origin_kind="observed",
                origin_path=None,
                attributes={"path": "README.md", "reason": readme_error},
            )
        )
        add_edge(
            _edge(
                f"edge.project-contains-{unresolved_id.replace('.', '-')}",
                "contains",
                project_id,
                unresolved_id,
                origin_kind="derived",
            )
        )
        unresolved.append(unresolved_id)

    for decision_root_relative in ("decisions", "docs/decisions"):
        try:
            _, decisions_root = _safe_repo_path(root, decision_root_relative)
        except ValueError as exc:
            unresolved_id = _stable_path_id("unresolved", decision_root_relative + ":unsafe")
            add_node(
                _node(
                    unresolved_id,
                    "unresolved",
                    f"Unsafe decision directory: {decision_root_relative}",
                    status="blocking",
                    origin_kind="observed",
                    attributes={"path": decision_root_relative, "reason": str(exc)},
                )
            )
            add_edge(
                _edge(
                    f"edge.project-contains-{unresolved_id.replace('.', '-')}",
                    "contains",
                    project_id,
                    unresolved_id,
                    origin_kind="derived",
                )
            )
            unresolved.append(unresolved_id)
            continue
        if not decisions_root.is_dir():
            continue
        for decision_path in sorted(decisions_root.glob("*.md")):
            if decision_path.name.lower() == "readme.md":
                continue
            relative = decision_path.relative_to(root).as_posix()
            try:
                safe_relative, safe_decision_path = _safe_repo_path(root, relative)
            except ValueError as exc:
                unresolved_id = _stable_path_id("unresolved", relative + ":unsafe")
                add_node(
                    _node(
                        unresolved_id,
                        "unresolved",
                        f"Unsafe decision path: {relative}",
                        status="blocking",
                        origin_kind="observed",
                        attributes={"path": relative, "reason": str(exc)},
                    )
                )
                add_edge(
                    _edge(
                        f"edge.project-contains-{unresolved_id.replace('.', '-')}",
                        "contains",
                        project_id,
                        unresolved_id,
                        origin_kind="derived",
                    )
                )
                unresolved.append(unresolved_id)
                continue
            decision_id = _stable_path_id("decision", safe_relative)
            add_node(
                _node(
                    decision_id,
                    "decision",
                    _title_from_markdown(safe_decision_path).removeprefix("Decision: ").strip(),
                    status="observed",
                    origin_kind="authored",
                    origin_path=safe_relative,
                    attributes={"path": safe_relative},
                )
            )
            add_edge(
                _edge(
                    f"edge.project-contains-{decision_id.replace('.', '-')}",
                    "contains",
                    project_id,
                    decision_id,
                    origin_kind="derived",
                    origin_path=safe_relative,
                )
            )

    for workflow_root_relative in ("workflow/active", "workflow/completed"):
        try:
            _, workflow_root = _safe_repo_path(root, workflow_root_relative)
        except ValueError as exc:
            unresolved_id = _stable_path_id("unresolved", workflow_root_relative + ":unsafe")
            add_node(
                _node(
                    unresolved_id,
                    "unresolved",
                    f"Unsafe workflow directory: {workflow_root_relative}",
                    status="blocking",
                    origin_kind="observed",
                    attributes={"path": workflow_root_relative, "reason": str(exc)},
                )
            )
            add_edge(
                _edge(
                    f"edge.project-contains-{unresolved_id.replace('.', '-')}",
                    "contains",
                    project_id,
                    unresolved_id,
                    origin_kind="derived",
                )
            )
            unresolved.append(unresolved_id)
            continue
        if not workflow_root.is_dir():
            continue
        historical = workflow_root_relative == "workflow/completed"
        for candidate_state_path in sorted(workflow_root.glob("*/state.json")):
            relative_state = candidate_state_path.relative_to(root).as_posix()
            try:
                relative_state, state_path = _safe_repo_path(root, relative_state)
            except ValueError as exc:
                unresolved_id = _stable_path_id("unresolved", relative_state + ":unsafe")
                add_node(
                    _node(
                        unresolved_id,
                        "unresolved",
                        f"Unsafe workflow state path: {relative_state}",
                        status="blocking",
                        origin_kind="observed",
                        attributes={"path": relative_state, "reason": str(exc)},
                    )
                )
                add_edge(
                    _edge(
                        f"edge.project-contains-{unresolved_id.replace('.', '-')}",
                        "contains",
                        project_id,
                        unresolved_id,
                        origin_kind="derived",
                    )
                )
                unresolved.append(unresolved_id)
                continue
            try:
                state = _load_json(state_path)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                unresolved_id = _stable_path_id("unresolved", relative_state)
                add_node(
                    _node(
                        unresolved_id,
                        "unresolved",
                        f"Unreadable workflow state: {relative_state}",
                        status="blocking",
                        origin_kind="observed",
                        origin_path=relative_state,
                        attributes={"reason": str(exc)},
                    )
                )
                add_edge(
                    _edge(
                        f"edge.project-contains-{unresolved_id.replace('.', '-')}",
                        "contains",
                        project_id,
                        unresolved_id,
                        origin_kind="derived",
                        origin_path=relative_state,
                    )
                )
                unresolved.append(unresolved_id)
                continue

            workflow_id_raw = state.get("workflow_id")
            if not isinstance(workflow_id_raw, str) or not workflow_id_raw:
                workflow_id_raw = state_path.parent.name
                unresolved_id = _stable_path_id("unresolved", relative_state + ":workflow-id")
                add_node(
                    _node(
                        unresolved_id,
                        "unresolved",
                        f"Workflow id missing in {relative_state}",
                        status="blocking",
                        origin_kind="observed",
                        origin_path=relative_state,
                        attributes={"field": "workflow_id"},
                    )
                )
                add_edge(
                    _edge(
                        f"edge.project-contains-{unresolved_id.replace('.', '-')}",
                        "contains",
                        project_id,
                        unresolved_id,
                        origin_kind="derived",
                        origin_path=relative_state,
                    )
                )
                unresolved.append(unresolved_id)

            workflow_id = f"workflow.{_slug(workflow_id_raw)}"
            add_node(
                _node(
                    workflow_id,
                    "workflow",
                    str(state.get("title") or workflow_id_raw),
                    status=str(state.get("status") or ("completed" if historical else "unknown")),
                    origin_kind="observed",
                    origin_path=relative_state,
                    attributes={"historical": historical},
                )
            )
            add_edge(
                _edge(
                    f"edge.project-contains-{workflow_id.replace('.', '-')}",
                    "contains",
                    project_id,
                    workflow_id,
                    origin_kind="derived",
                    origin_path=relative_state,
                )
            )

            stage_id_map: dict[str, str] = {}
            stages = state.get("stages")
            if not isinstance(stages, list):
                stages = []
            for stage in stages:
                if not isinstance(stage, dict):
                    continue
                raw_stage_id = stage.get("id")
                if not isinstance(raw_stage_id, str) or not raw_stage_id:
                    continue
                stage_id = f"stage.{_slug(workflow_id_raw)}-{_slug(raw_stage_id)}"
                stage_id_map[raw_stage_id] = stage_id
                context_path = stage.get("context")
                title = raw_stage_id
                safe_context_path = context_path
                if isinstance(context_path, str):
                    try:
                        safe_context_path, resolved_context = _safe_repo_path(root, context_path)
                    except ValueError as exc:
                        unresolved_id = _stable_path_id("unresolved", relative_state + ":" + raw_stage_id + ":context")
                        add_node(
                            _node(
                                unresolved_id,
                                "unresolved",
                                f"Unsafe stage context path: {context_path}",
                                status="blocking",
                                origin_kind="observed",
                                origin_path=relative_state,
                                attributes={"reason": str(exc), "path": context_path},
                            )
                        )
                        add_edge(
                            _edge(
                                f"edge.{unresolved_id.replace('.', '-')}-blocks-{stage_id.replace('.', '-')}",
                                "blocks",
                                unresolved_id,
                                stage_id,
                                origin_kind="derived",
                                origin_path=relative_state,
                            )
                        )
                        unresolved.append(unresolved_id)
                        safe_context_path = None
                    else:
                        if resolved_context.is_file():
                            title = _title_from_markdown(resolved_context)

                add_node(
                    _node(
                        stage_id,
                        "stage",
                        title,
                        status=str(stage.get("status") or "unknown"),
                        origin_kind="observed",
                        origin_path=relative_state,
                        attributes={
                            "workflow_id": workflow_id_raw,
                            "stage_id": raw_stage_id,
                            "context": safe_context_path,
                        },
                    )
                )
                add_edge(
                    _edge(
                        f"edge.{workflow_id.replace('.', '-')}-contains-{stage_id.replace('.', '-')}",
                        "contains",
                        workflow_id,
                        stage_id,
                        origin_kind="derived",
                        origin_path=relative_state,
                    )
                )

                for dependency in stage.get("depends_on", []) if isinstance(stage.get("depends_on"), list) else []:
                    if not isinstance(dependency, dict) or not isinstance(dependency.get("path"), str):
                        continue
                    dep_path = dependency["path"]
                    try:
                        dep_path, dep_resolved = _safe_repo_path(root, dep_path)
                    except ValueError as exc:
                        unresolved_id = _stable_path_id("unresolved", relative_state + ":" + raw_stage_id + ":dependency:" + dependency["path"])
                        add_node(
                            _node(
                                unresolved_id,
                                "unresolved",
                                f"Unsafe declared dependency path: {dependency['path']}",
                                status="blocking",
                                origin_kind="observed",
                                origin_path=relative_state,
                                attributes={"reason": str(exc), "path": dependency["path"]},
                            )
                        )
                        add_edge(
                            _edge(
                                f"edge.{unresolved_id.replace('.', '-')}-blocks-{stage_id.replace('.', '-')}",
                                "blocks",
                                unresolved_id,
                                stage_id,
                                origin_kind="derived",
                                origin_path=relative_state,
                            )
                        )
                        unresolved.append(unresolved_id)
                        continue
                    dep_id = _stable_path_id("artifact", dep_path)
                    exists = dep_resolved.exists()
                    add_node(
                        _node(
                            dep_id,
                            "artifact",
                            dep_path,
                            status="present" if exists else "missing",
                            origin_kind="observed" if exists else "derived",
                            origin_path=dep_path if exists else relative_state,
                            attributes={"path": dep_path, "blob": dependency.get("blob")},
                        )
                    )
                    add_edge(
                        _edge(
                            f"edge.{stage_id.replace('.', '-')}-depends-{dep_id.replace('.', '-')}",
                            "depends_on",
                            stage_id,
                            dep_id,
                            origin_kind="observed",
                            origin_path=relative_state,
                        )
                    )
                    if not exists:
                        unresolved_id = _stable_path_id("unresolved", dep_path + ":missing")
                        add_node(
                            _node(
                                unresolved_id,
                                "unresolved",
                                f"Missing declared dependency: {dep_path}",
                                status="blocking",
                                origin_kind="observed",
                                origin_path=relative_state,
                                attributes={"path": dep_path},
                            )
                        )
                        add_edge(
                            _edge(
                                f"edge.{unresolved_id.replace('.', '-')}-blocks-{stage_id.replace('.', '-')}",
                                "blocks",
                                unresolved_id,
                                stage_id,
                                origin_kind="derived",
                                origin_path=relative_state,
                            )
                        )
                        unresolved.append(unresolved_id)

                for output in stage.get("outputs", []) if isinstance(stage.get("outputs"), list) else []:
                    if not isinstance(output, str) or not output:
                        continue
                    try:
                        output, output_resolved = _safe_repo_path(root, output)
                    except ValueError as exc:
                        unresolved_id = _stable_path_id("unresolved", relative_state + ":" + raw_stage_id + ":output:" + output)
                        add_node(
                            _node(
                                unresolved_id,
                                "unresolved",
                                f"Unsafe declared output path: {output}",
                                status="blocking",
                                origin_kind="observed",
                                origin_path=relative_state,
                                attributes={"reason": str(exc), "path": output},
                            )
                        )
                        add_edge(
                            _edge(
                                f"edge.{unresolved_id.replace('.', '-')}-blocks-{stage_id.replace('.', '-')}",
                                "blocks",
                                unresolved_id,
                                stage_id,
                                origin_kind="derived",
                                origin_path=relative_state,
                            )
                        )
                        unresolved.append(unresolved_id)
                        continue
                    output_id = _stable_path_id("artifact", output)
                    exists = output_resolved.exists()
                    add_node(
                        _node(
                            output_id,
                            "artifact",
                            output,
                            status="present" if exists else "planned",
                            origin_kind="observed" if exists else "authored",
                            origin_path=output if exists else relative_state,
                            attributes={"path": output},
                        )
                    )
                    add_edge(
                        _edge(
                            f"edge.{stage_id.replace('.', '-')}-produces-{output_id.replace('.', '-')}",
                            "produces",
                            stage_id,
                            output_id,
                            origin_kind="observed",
                            origin_path=relative_state,
                        )
                    )

            for stage in stages:
                if not isinstance(stage, dict):
                    continue
                raw_stage_id = stage.get("id")
                source = stage_id_map.get(raw_stage_id)
                if source is None:
                    continue
                upstream = stage.get("depends_on_stages", [])
                if not isinstance(upstream, list):
                    continue
                for raw_upstream in upstream:
                    target = stage_id_map.get(raw_upstream)
                    if target is None:
                        unresolved_id = _stable_path_id(
                            "unresolved",
                            f"{relative_state}:{raw_stage_id}:upstream:{raw_upstream}",
                        )
                        add_node(
                            _node(
                                unresolved_id,
                                "unresolved",
                                f"Unknown upstream stage {raw_upstream!r}",
                                status="blocking",
                                origin_kind="observed",
                                origin_path=relative_state,
                                attributes={"workflow": workflow_id_raw, "stage": raw_stage_id},
                            )
                        )
                        add_edge(
                            _edge(
                                f"edge.{unresolved_id.replace('.', '-')}-blocks-{source.replace('.', '-')}",
                                "blocks",
                                unresolved_id,
                                source,
                                origin_kind="derived",
                                origin_path=relative_state,
                            )
                        )
                        unresolved.append(unresolved_id)
                        continue
                    add_edge(
                        _edge(
                            f"edge.{source.replace('.', '-')}-depends-{target.replace('.', '-')}",
                            "depends_on",
                            source,
                            target,
                            origin_kind="observed",
                            origin_path=relative_state,
                        )
                    )

    graph = {
        "schema_version": 1,
        "nodes": sorted(nodes.values(), key=lambda item: item["id"]),
        "edges": sorted(edges.values(), key=lambda item: item["id"]),
    }
    diagnostics = validate_graph(root, graph)
    structural_status = graph_status(diagnostics)
    audit_status = "FAIL" if structural_status == "FAIL" else ("WARN" if unresolved or structural_status == "WARN" else "PASS")
    input_fingerprint, input_manifest = audit_input_fingerprint(root)
    return {
        "audit_contract_version": AUDIT_CONTRACT_VERSION,
        "input_fingerprint": input_fingerprint,
        "input_manifest": input_manifest,
        "status": audit_status,
        "graph": graph,
        "diagnostics": diagnostics,
        "unresolved": sorted(set(unresolved)),
    }


def write_audit_proposal(root: Path, report: dict[str, Any]) -> Path:
    target = safe_repo_path(root, AUDIT_DIR / PROPOSAL_FILE)
    target.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(report, indent=2, sort_keys=True) + "\n"
    current = target.read_text(encoding="utf-8") if target.exists() else None
    if current != content:
        atomic_write_text(target, content)
    return target
