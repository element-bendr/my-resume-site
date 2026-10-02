from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from icm_graph_store import load_graph
from icm_io import safe_repo_path
from icm_source_state import load_source_state
from icm_validate import validate_repository
from workflow_lib import current_commit, git_output

CONTEXT_SCHEMA_VERSION = 1
EXECUTION_TYPES = {"workflow", "stage", "task"}
MAX_CONTEXT_NODES = 64
MAX_RECORDED_PATHS_PER_NODE = 4
MAX_TEXT_ESTIMATE_BYTES = 1_000_000
MAX_INLINE_ATTRIBUTE_CHARS = 2_000
GENERATED_PROJECTION_PREFIX = ".icm/generated/"

DIRECT_OUTGOING = {
    "depends_on",
    "implements",
    "modifies",
    "produces",
    "satisfies",
    "requires",
    "owned_by",
}
DIRECT_INCOMING = {"blocks", "validates", "contains"}
INHERITED_EXECUTION_OUTGOING = {"depends_on", "requires", "owned_by"}
class ContextError(ValueError):
    pass


def _node_map(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(node["id"]): node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }


def _edges(graph: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        [edge for edge in graph.get("edges", []) if isinstance(edge, dict)],
        key=lambda edge: str(edge.get("id", "")),
    )


def resolve_subject(graph: dict[str, Any], subject: str | None = None) -> str:
    nodes = _node_map(graph)
    if subject is not None:
        node = nodes.get(subject)
        if node is None:
            raise ContextError(f"context subject not found: {subject}")
        if node.get("type") not in EXECUTION_TYPES:
            raise ContextError(
                f"context subject must be workflow/stage/task, got {node.get('type')!r}: {subject}"
            )
        return subject

    for node_type in ("task", "stage", "workflow"):
        candidates = sorted(
            node_id
            for node_id, node in nodes.items()
            if node.get("type") == node_type and node.get("status") == "active"
        )
        if len(candidates) == 1:
            return candidates[0]
        if len(candidates) > 1:
            raise ContextError(
                f"ambiguous active {node_type} subjects: {', '.join(candidates)}; pass --subject"
            )

    raise ContextError("no unique active workflow/stage/task; pass --subject")


def _build_indexes(
    graph: dict[str, Any],
) -> tuple[
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
]:
    outgoing: dict[str, list[dict[str, Any]]] = {}
    incoming: dict[str, list[dict[str, Any]]] = {}
    for edge in _edges(graph):
        source = edge.get("from")
        target = edge.get("to")
        if isinstance(source, str):
            outgoing.setdefault(source, []).append(edge)
        if isinstance(target, str):
            incoming.setdefault(target, []).append(edge)
    return outgoing, incoming


def _step(path: tuple[str, ...], edge: dict[str, Any], target: str) -> tuple[str, ...]:
    return (*path, str(edge.get("id")), target)


def _best_path(paths: dict[str, set[tuple[str, ...]]], node_id: str) -> tuple[str, ...]:
    candidates = paths.get(node_id) or {(node_id,)}
    return min(candidates, key=lambda value: (len(value), value))


def graph_neighborhood(graph: dict[str, Any], subject: str) -> dict[str, Any]:
    nodes = _node_map(graph)
    if subject not in nodes:
        raise ContextError(f"context subject not found: {subject}")

    outgoing, incoming = _build_indexes(graph)
    selected: set[str] = set()
    reasons: dict[str, set[str]] = {}
    paths: dict[str, set[tuple[str, ...]]] = {}

    def add(node_id: str, reason: str, path: tuple[str, ...]) -> bool:
        if node_id not in nodes:
            raise ContextError(f"context traversal reached missing node: {node_id}")
        is_new = node_id not in selected
        if is_new and len(selected) >= MAX_CONTEXT_NODES:
            raise ContextError(
                f"context neighborhood exceeds {MAX_CONTEXT_NODES} nodes; refine the subject or graph relationships"
            )
        selected.add(node_id)
        reasons.setdefault(node_id, set()).add(reason)
        bucket = paths.setdefault(node_id, set())
        if len(bucket) < MAX_RECORDED_PATHS_PER_NODE:
            bucket.add(path)
        return is_new

    add(subject, "current execution subject", (subject,))

    # Direct subject relationships.
    for edge in outgoing.get(subject, []):
        edge_type = edge.get("type")
        target = edge.get("to")
        if edge_type in DIRECT_OUTGOING and isinstance(target, str):
            add(
                target,
                f"{subject} {edge_type} {target}",
                _step((subject,), edge, target),
            )

    for edge in incoming.get(subject, []):
        edge_type = edge.get("type")
        source = edge.get("from")
        if edge_type in DIRECT_INCOMING and isinstance(source, str):
            add(
                source,
                f"{source} {edge_type} {subject}",
                _step((subject,), edge, source),
            )

    # A stage/workflow subject may need its direct open execution children.
    subject_type = nodes[subject].get("type")
    if subject_type in {"workflow", "stage"}:
        for edge in outgoing.get(subject, []):
            if edge.get("type") != "contains":
                continue
            target = edge.get("to")
            child = nodes.get(target)
            if (
                isinstance(target, str)
                and child is not None
                and child.get("type") in EXECUTION_TYPES
                and child.get("status") not in {"certified", "completed"}
            ):
                add(
                    target,
                    f"{subject} contains current execution child {target}",
                    _step((subject,), edge, target),
                )

    # Walk only containment parents, never the sibling/whole-tree closure.
    ancestor_frontier = [subject]
    ancestors: list[str] = []
    seen_ancestors = {subject}
    for _ in range(4):
        next_frontier: list[str] = []
        for child_id in sorted(ancestor_frontier):
            child_path = _best_path(paths, child_id)
            for edge in incoming.get(child_id, []):
                if edge.get("type") != "contains":
                    continue
                parent_id = edge.get("from")
                parent = nodes.get(parent_id)
                if (
                    not isinstance(parent_id, str)
                    or parent is None
                    or parent_id in seen_ancestors
                    or parent.get("type") not in {"project", "system", "workflow", "stage"}
                ):
                    continue
                add(
                    parent_id,
                    f"{child_id} is contained by {parent_id}",
                    _step(child_path, edge, parent_id),
                )
                seen_ancestors.add(parent_id)
                ancestors.append(parent_id)
                next_frontier.append(parent_id)
        if not next_frontier:
            break
        ancestor_frontier = next_frontier

    # Execution ancestors contribute inherited requirements/prerequisites/ownership
    # and blockers, but not all of their children.
    for execution_id in sorted({subject, *ancestors}):
        node = nodes[execution_id]
        if node.get("type") not in EXECUTION_TYPES:
            continue
        base_path = _best_path(paths, execution_id)
        for edge in outgoing.get(execution_id, []):
            edge_type = edge.get("type")
            target = edge.get("to")
            if edge_type in INHERITED_EXECUTION_OUTGOING and isinstance(target, str):
                add(
                    target,
                    f"{execution_id} {edge_type} {target}",
                    _step(base_path, edge, target),
                )
        for edge in incoming.get(execution_id, []):
            source = edge.get("from")
            if edge.get("type") == "blocks" and isinstance(source, str):
                add(
                    source,
                    f"{source} blocks {execution_id}",
                    _step(base_path, edge, source),
                )

    # One bounded semantic expansion from already-selected policy/artifact nodes.
    snapshot = sorted(selected)
    for node_id in snapshot:
        node = nodes[node_id]
        node_type = node.get("type")
        base_path = _best_path(paths, node_id)

        if node_type == "acceptance_criterion":
            for edge in incoming.get(node_id, []):
                source = edge.get("from")
                source_node = nodes.get(source)
                if (
                    edge.get("type") in {"satisfies", "validates"}
                    and isinstance(source, str)
                    and source_node is not None
                    and source_node.get("type") == "evidence"
                ):
                    add(
                        source,
                        f"evidence {source} supports acceptance {node_id}",
                        _step(base_path, edge, source),
                    )

        if node_type == "constraint":
            for edge in outgoing.get(node_id, []):
                target = edge.get("to")
                if edge.get("type") == "protects" and isinstance(target, str):
                    add(
                        target,
                        f"{node_id} protects {target}",
                        _step(base_path, edge, target),
                    )

        if node_type == "protected_resource":
            for edge in incoming.get(node_id, []):
                source = edge.get("from")
                if edge.get("type") == "protects" and isinstance(source, str):
                    add(
                        source,
                        f"{source} protects {node_id}",
                        _step(base_path, edge, source),
                    )

        if node_type == "artifact":
            for edge in outgoing.get(node_id, []):
                target = edge.get("to")
                if edge.get("type") == "depends_on" and isinstance(target, str):
                    add(
                        target,
                        f"{node_id} depends_on {target}",
                        _step(base_path, edge, target),
                    )
            for edge in incoming.get(node_id, []):
                source = edge.get("from")
                source_node = nodes.get(source)
                if (
                    edge.get("type") == "validates"
                    and isinstance(source, str)
                    and source_node is not None
                    and source_node.get("type") == "evidence"
                ):
                    add(
                        source,
                        f"evidence {source} validates {node_id}",
                        _step(base_path, edge, source),
                    )

        if node_type in {"decision", "constraint", "artifact"}:
            for edge in [*outgoing.get(node_id, []), *incoming.get(node_id, [])]:
                if edge.get("type") != "supersedes":
                    continue
                other = edge.get("to") if edge.get("from") == node_id else edge.get("from")
                if isinstance(other, str):
                    add(
                        other,
                        f"{node_id} has supersession relationship with {other}",
                        _step(base_path, edge, other),
                    )

    used_edge_ids: set[str] = set()
    for node_paths in paths.values():
        for path in node_paths:
            for part in path:
                if part.startswith("edge."):
                    used_edge_ids.add(part)

    selected_edges = [
        edge
        for edge in _edges(graph)
        if edge.get("id") in used_edge_ids
    ]

    return {
        "subject": subject,
        "node_ids": sorted(selected),
        "reasons": {
            node_id: sorted(reasons.get(node_id, set()))
            for node_id in sorted(selected)
        },
        "paths": {
            node_id: [
                list(path)
                for path in sorted(
                    paths.get(node_id, set()),
                    key=lambda value: (len(value), value),
                )[:MAX_RECORDED_PATHS_PER_NODE]
            ]
            for node_id in sorted(selected)
        },
        "edges": selected_edges,
    }


def _candidate_source_paths(node: dict[str, Any]) -> list[str]:
    values: list[str] = []
    origin = node.get("origin")
    if isinstance(origin, dict) and isinstance(origin.get("path"), str):
        values.append(origin["path"])
    attributes = node.get("attributes")
    if isinstance(attributes, dict):
        if isinstance(attributes.get("path"), str):
            values.append(attributes["path"])
        if isinstance(attributes.get("context"), str):
            values.append(attributes["context"])
        sources = attributes.get("sources")
        if isinstance(sources, list):
            values.extend(value for value in sources if isinstance(value, str))
    return sorted(set(values))


def _subject_bootstrap_source_paths(node: dict[str, Any]) -> list[str]:
    values: list[str] = []
    attributes = node.get("attributes")
    if isinstance(attributes, dict):
        context = attributes.get("context")
        if isinstance(context, str):
            values.append(context)
        sources = attributes.get("sources")
        if isinstance(sources, list):
            values.extend(value for value in sources if isinstance(value, str))
    if not values:
        origin = node.get("origin")
        if isinstance(origin, dict) and isinstance(origin.get("path"), str):
            values.append(origin["path"])
    return sorted(set(values))


def _direct_relations(
    neighborhood: dict[str, Any],
    subject: str,
    node_id: str,
) -> set[tuple[str, str]]:
    relations: set[tuple[str, str]] = set()
    for edge in neighborhood.get("edges", []):
        if not isinstance(edge, dict):
            continue
        edge_type = edge.get("type")
        source = edge.get("from")
        target = edge.get("to")
        if not isinstance(edge_type, str):
            continue
        if source == subject and target == node_id:
            relations.add(("out", edge_type))
        elif target == subject and source == node_id:
            relations.add(("in", edge_type))
    return relations


def _source_load_policy(
    node_id: str,
    node: dict[str, Any],
    subject: str,
    neighborhood: dict[str, Any],
) -> str:
    if node_id == subject:
        return "bootstrap"

    node_type = node.get("type")
    relations = _direct_relations(neighborhood, subject, node_id)

    if ("in", "blocks") in relations:
        return "bootstrap"

    if node_type in {
        "constraint",
        "acceptance_criterion",
        "protected_resource",
        "unresolved",
    }:
        return "bootstrap"

    for relation in ("implements", "modifies", "requires", "satisfies"):
        if ("out", relation) in relations:
            return "bootstrap"

    if ("out", "depends_on") in relations:
        return "on_demand"

    if ("out", "produces") in relations:
        return "on_demand"

    if node_type in EXECUTION_TYPES or node_type in {"project", "system"}:
        return "metadata_only"

    return "on_demand"


def _bootstrap_candidate_paths(
    node_id: str,
    node: dict[str, Any],
    subject: str,
    neighborhood: dict[str, Any],
) -> list[str]:
    policy = _source_load_policy(node_id, node, subject, neighborhood)
    if policy != "bootstrap":
        return []
    if node_id == subject and node.get("type") in EXECUTION_TYPES:
        return _subject_bootstrap_source_paths(node)
    return _candidate_source_paths(node)


def _hash_bytes(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_record(root: Path, relative: str) -> dict[str, Any]:
    try:
        path = safe_repo_path(root, relative)
    except ValueError as exc:
        raise ContextError(str(exc)) from exc

    record: dict[str, Any] = {
        "path": relative,
        "exists": path.exists(),
        "kind": "missing",
        "sha256": None,
        "bytes": None,
        "text_chars": None,
        "estimated_tokens": None,
        "token_estimate_method": None,
        "duplicate_of": None,
    }
    if not path.exists():
        return record
    if path.is_dir():
        record["kind"] = "directory"
        return record
    if not path.is_file():
        record["kind"] = "other"
        return record

    size = path.stat().st_size
    record["kind"] = "file"
    record["bytes"] = size
    record["sha256"] = _hash_bytes(path)

    if size <= MAX_TEXT_ESTIMATE_BYTES:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            pass
        else:
            record["text_chars"] = len(text)
            record["estimated_tokens"] = (len(text) + 3) // 4
            record["token_estimate_method"] = "unicode_chars_div_4_heuristic"
    return record


def _compact_attributes(node: dict[str, Any]) -> dict[str, Any]:
    attributes = node.get("attributes")
    if not isinstance(attributes, dict):
        return {}
    encoded = json.dumps(
        attributes,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    if len(encoded) <= MAX_INLINE_ATTRIBUTE_CHARS:
        return attributes

    preserved: dict[str, Any] = {}
    for key in (
        "path",
        "context",
        "match",
        "policy",
        "blocker",
        "source_state",
        "plan_status",
    ):
        value = attributes.get(key)
        if isinstance(value, (str, int, float, bool)) or value is None:
            preserved[key] = value
    preserved["_omitted"] = True
    preserved["_keys"] = sorted(str(key) for key in attributes)
    preserved["_reason"] = (
        f"attributes exceed {MAX_INLINE_ATTRIBUTE_CHARS} inline characters; "
        "dereference canonical source if details are required"
    )
    return preserved


def _priority(node: dict[str, Any], subject: str) -> str:
    if node.get("id") == subject:
        return "required"
    if node.get("type") in {
        "constraint",
        "acceptance_criterion",
        "protected_resource",
        "unresolved",
    }:
        return "required"
    return "relevant"


def _non_compressible(node: dict[str, Any]) -> bool:
    return node.get("type") in {
        "constraint",
        "acceptance_criterion",
        "protected_resource",
        "unresolved",
        "evidence",
    }


def _repository_identity(root: Path) -> tuple[str, str]:
    remote = git_output(root, "remote", "get-url", "origin")
    if remote:
        value = remote.strip()
        if value.endswith(".git"):
            value = value[:-4]
        if value.startswith("git@") and ":" in value:
            value = value.split(":", 1)[1]
        elif "://" in value:
            value = value.split("://", 1)[1]
            value = value.split("/", 1)[1] if "/" in value else value
        parts = [part for part in value.split("/") if part]
        if len(parts) >= 2:
            return "/".join(parts[-2:]), "origin-remote"
        return remote, "origin-remote"
    return root.name, "directory-name-fallback"


def _context_fatal_failures(validation: dict[str, Any]) -> list[dict[str, Any]]:
    nonfatal_codes = {"graph.unresolved-blocking"}
    failures: list[dict[str, Any]] = []
    for item in validation.get("diagnostics", []):
        if not isinstance(item, dict) or item.get("severity") != "FAIL":
            continue
        code = str(item.get("code", ""))
        if code in nonfatal_codes or code.startswith("projection."):
            continue
        failures.append(item)
    return failures


def _budget_for_sources(records: list[dict[str, Any]]) -> dict[str, int]:
    unique = [
        record
        for record in records
        if record.get("duplicate_of") is None
    ]
    return {
        "files": sum(1 for record in unique if record.get("kind") == "file"),
        "bytes": sum(
            int(record["bytes"])
            for record in unique
            if isinstance(record.get("bytes"), int)
        ),
        "estimated_tokens": sum(
            int(record["estimated_tokens"])
            for record in unique
            if isinstance(record.get("estimated_tokens"), int)
        ),
        "unestimated_files": sum(
            1
            for record in unique
            if record.get("kind") == "file"
            and record.get("estimated_tokens") is None
        ),
    }


def _estimate_json_tokens(value: Any) -> tuple[int, int]:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return len(encoded), (len(encoded) + 3) // 4


def compact_context_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    bootstrap_sources = [
        {
            "path": source.get("path"),
            "sha256": source.get("sha256"),
        }
        for source in manifest.get("bootstrap_sources", [])
        if isinstance(source, dict)
    ]

    routes: dict[str, dict[str, dict[str, list[Any]]]] = {}
    for item in manifest.get("items", []):
        if not isinstance(item, dict):
            continue

        load = item.get("source_load")
        if load not in {"bootstrap", "on_demand", "metadata_only"}:
            load = "on_demand"

        node_type = item.get("type")
        if not isinstance(node_type, str) or not node_type:
            node_type = "unknown"

        status = item.get("status")
        status_key = status if isinstance(status, str) and status else "__none__"

        node_id = item.get("node_id")
        refs = item.get("source_refs")
        if isinstance(refs, list):
            source_refs = [value for value in refs if isinstance(value, str) and value]
        else:
            source_refs = []

        if not source_refs:
            record: Any = node_id
        elif len(source_refs) == 1:
            record = {"id": node_id, "ref": source_refs[0]}
        else:
            record = {"id": node_id, "refs": source_refs}

        routes.setdefault(load, {}).setdefault(node_type, {}).setdefault(status_key, []).append(record)

    for by_type in routes.values():
        for by_status in by_type.values():
            for values in by_status.values():
                values.sort(
                    key=lambda value: (
                        value if isinstance(value, str) else str(value.get("id", ""))
                    )
                )

    payload: dict[str, Any] = {
        "schema_version": manifest.get("schema_version"),
        "status": manifest.get("status"),
        "subject": manifest.get("subject"),
        "repository": manifest.get("repository"),
        "base_sha": manifest.get("base_sha"),
        "graph_fingerprint": manifest.get("graph_fingerprint"),
        "source_fingerprint": manifest.get("source_fingerprint"),
        "fresh": manifest.get("fresh"),
        "routes": routes,
        "bootstrap_sources": bootstrap_sources,
        "blocking_unresolved": manifest.get("blocking_unresolved", []),
        "budget": {
            "bootstrap_source_files": manifest.get("budget", {}).get("bootstrap_source_files", 0),
            "bootstrap_source_bytes": manifest.get("budget", {}).get("bootstrap_source_bytes", 0),
            "estimated_tokens_if_bootstrap_sources_loaded": manifest.get("budget", {}).get(
                "estimated_tokens_if_bootstrap_sources_loaded", 0
            ),
            "compact_manifest_chars": 0,
            "estimated_compact_manifest_tokens": 0,
            "token_estimate": "chars/4",
        },
    }

    for _ in range(4):
        chars, tokens = _estimate_json_tokens(payload)
        budget = payload["budget"]
        if (
            budget["compact_manifest_chars"] == chars
            and budget["estimated_compact_manifest_tokens"] == tokens
        ):
            break
        budget["compact_manifest_chars"] = chars
        budget["estimated_compact_manifest_tokens"] = tokens

    return payload

def build_context_manifest(root: Path, *, subject: str | None = None) -> dict[str, Any]:
    root = root.resolve()

    validation = validate_repository(root)
    failures = _context_fatal_failures(validation)
    if failures:
        summary = "; ".join(
            f"{item.get('code')}: {item.get('subject')}"
            for item in failures[:8]
        )
        raise ContextError(f"repository ICM state is not context-safe: {summary}")

    graph = load_graph(root)
    source_state = load_source_state(root)
    head = current_commit(root)
    if head is None:
        raise ContextError("unable to bind context manifest to current Git HEAD")
    repository, repository_identity_method = _repository_identity(root)

    resolved_subject = resolve_subject(graph, subject)
    neighborhood = graph_neighborhood(graph, resolved_subject)
    nodes = _node_map(graph)

    excluded: list[dict[str, str]] = [
        {
            "pattern": ".icm/generated/*.md",
            "reason": "generated human projections are excluded by default in valid graph mode",
        }
    ]

    source_records: dict[str, dict[str, Any]] = {}
    item_sources: dict[str, list[str]] = {}
    item_bootstrap_sources: dict[str, list[str]] = {}

    for node_id in neighborhood["node_ids"]:
        node = nodes[node_id]
        refs: list[str] = []
        bootstrap_refs: list[str] = []

        for relative in _candidate_source_paths(node):
            if relative.startswith(GENERATED_PROJECTION_PREFIX):
                continue
            if relative not in source_records:
                source_records[relative] = _source_record(root, relative)
            refs.append(relative)

        for relative in _bootstrap_candidate_paths(
            node_id,
            node,
            resolved_subject,
            neighborhood,
        ):
            if relative.startswith(GENERATED_PROJECTION_PREFIX):
                continue
            if relative not in source_records:
                source_records[relative] = _source_record(root, relative)
            bootstrap_refs.append(relative)

        item_sources[node_id] = sorted(set(refs))
        item_bootstrap_sources[node_id] = sorted(set(bootstrap_refs))

    # Exact-content dedupe for authored/observed file sources.
    first_by_hash: dict[str, str] = {}
    for relative in sorted(source_records):
        record = source_records[relative]
        digest = record.get("sha256")
        if not isinstance(digest, str):
            continue
        canonical = first_by_hash.setdefault(digest, relative)
        if canonical != relative:
            record["duplicate_of"] = canonical

    canonical_source_path = {
        path: (
            record["duplicate_of"]
            if isinstance(record.get("duplicate_of"), str)
            else path
        )
        for path, record in source_records.items()
    }

    items: list[dict[str, Any]] = []
    bootstrap_paths: set[str] = set()
    for node_id in neighborhood["node_ids"]:
        node = nodes[node_id]
        all_refs = sorted(
            {
                canonical_source_path[path]
                for path in item_sources[node_id]
            }
        )
        bootstrap_refs = sorted(
            {
                canonical_source_path[path]
                for path in item_bootstrap_sources[node_id]
            }
        )
        bootstrap_paths.update(bootstrap_refs)
        items.append(
            {
                "node_id": node_id,
                "type": node.get("type"),
                "title": node.get("title"),
                "status": node.get("status"),
                "origin": node.get("origin"),
                "attributes": _compact_attributes(node),
                "priority": _priority(node, resolved_subject),
                "source_load": _source_load_policy(
                    node_id,
                    node,
                    resolved_subject,
                    neighborhood,
                ),
                "non_compressible": _non_compressible(node),
                "reasons": neighborhood["reasons"][node_id],
                "graph_paths": neighborhood["paths"][node_id],
                "source_refs": all_refs,
                "bootstrap_source_refs": bootstrap_refs,
            }
        )

    all_source_records = [
        source_records[path]
        for path in sorted(source_records)
    ]
    all_budget = _budget_for_sources(all_source_records)

    bootstrap_source_records = [
        source_records[path]
        for path in sorted(bootstrap_paths)
        if path in source_records
    ]
    bootstrap_budget = _budget_for_sources(bootstrap_source_records)

    selected_blockers = [
        item["node_id"]
        for item in items
        if item["type"] == "unresolved" and item.get("status") == "blocking"
    ]
    context_status = "BLOCKED" if selected_blockers else "PASS"

    manifest = {
        "schema_version": CONTEXT_SCHEMA_VERSION,
        "status": context_status,
        "subject": resolved_subject,
        "repository": repository,
        "repository_identity_method": repository_identity_method,
        "base_sha": head,
        "graph_fingerprint": source_state["graph_fingerprint"],
        "source_fingerprint": source_state["input_fingerprint"],
        "fresh": True,
        "validation_status": validation.get("status"),
        "nonfatal_validation_diagnostics": [
            item
            for item in validation.get("diagnostics", [])
            if isinstance(item, dict)
            and item.get("severity") == "FAIL"
            and (
                item.get("code") == "graph.unresolved-blocking"
                or str(item.get("code", "")).startswith("projection.")
            )
        ],
        "budget": {
            "referenced_files": all_budget["files"],
            "referenced_bytes": all_budget["bytes"],
            "estimated_tokens_if_all_text_sources_loaded": all_budget["estimated_tokens"],
            "unestimated_files": all_budget["unestimated_files"],
            "bootstrap_source_files": bootstrap_budget["files"],
            "bootstrap_source_bytes": bootstrap_budget["bytes"],
            "estimated_tokens_if_bootstrap_sources_loaded": bootstrap_budget["estimated_tokens"],
            "bootstrap_unestimated_files": bootstrap_budget["unestimated_files"],
            "measurement": "file text uses unicode_chars_div_4_heuristic; source bodies are referenced, not embedded",
        },
        "items": items,
        "edges": neighborhood["edges"],
        "sources": all_source_records,
        "bootstrap_sources": bootstrap_source_records,
        "excluded": excluded,
        "unresolved": [
            item["node_id"]
            for item in items
            if item["type"] == "unresolved"
        ],
        "blocking_unresolved": selected_blockers,
    }

    compact = compact_context_manifest(manifest)
    manifest["budget"]["compact_manifest_chars"] = compact["budget"]["compact_manifest_chars"]
    manifest["budget"]["estimated_compact_manifest_tokens"] = compact["budget"][
        "estimated_compact_manifest_tokens"
    ]
    return manifest
