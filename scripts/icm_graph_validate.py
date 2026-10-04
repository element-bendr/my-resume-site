from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from icm_graph_store import GRAPH_SCHEMA_VERSION, GraphStoreError, load_graph
from icm_io import safe_repo_path

EXECUTION_TYPES = {"workflow", "stage", "task"}
SEVERITY_ORDER = {"FAIL": 0, "WARN": 1}


def _diag(severity: str, code: str, subject: str, message: str) -> dict[str, str]:
    return {"severity": severity, "code": code, "subject": subject, "message": message}


def _load_contract(root: Path, name: str) -> dict[str, Any]:
    path = safe_repo_path(root, Path(".icm") / "schema" / name)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GraphStoreError(f"missing graph schema contract: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GraphStoreError(f"{path}: invalid JSON: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise GraphStoreError(f"{path}: schema contract must be object")
    return value


def _validate_string_constraints(
    subject: str,
    field: str,
    value: Any,
    spec: dict[str, Any],
    *,
    allow_null: bool = False,
) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    if value is None and allow_null:
        return diagnostics
    if not isinstance(value, str):
        diagnostics.append(_diag("FAIL", "record.string-type", subject, f"{field} must be a string"))
        return diagnostics
    minimum = spec.get("minLength")
    maximum = spec.get("maxLength")
    if isinstance(minimum, int) and len(value) < minimum:
        diagnostics.append(
            _diag("FAIL", "record.string-length", subject, f"{field} must be at least {minimum} characters")
        )
    if isinstance(maximum, int) and len(value) > maximum:
        diagnostics.append(
            _diag("FAIL", "record.string-length", subject, f"{field} must be at most {maximum} characters")
        )
    return diagnostics


def _validate_origin(
    subject: str,
    origin: Any,
    schema: dict[str, Any],
) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    if not isinstance(origin, dict):
        return [_diag("FAIL", "record.origin-type", subject, "origin must be an object")]
    origin_schema = schema["properties"]["origin"]
    required = set(origin_schema.get("required", []))
    allowed = set(origin_schema.get("properties", {}))
    for key in sorted(required - set(origin)):
        diagnostics.append(_diag("FAIL", "record.origin-required", subject, f"origin missing required field {key}"))
    for key in sorted(set(origin) - allowed):
        diagnostics.append(_diag("FAIL", "record.origin-extra", subject, f"origin has unsupported field {key}"))
    kind = origin.get("kind")
    kinds = set(origin_schema["properties"]["kind"].get("enum", []))
    if kind not in kinds:
        diagnostics.append(_diag("FAIL", "record.origin-kind", subject, f"unsupported origin kind {kind!r}"))
    for key in ("path", "ref", "note"):
        spec = origin_schema["properties"][key]
        diagnostics.extend(
            _validate_string_constraints(
                subject,
                f"origin.{key}",
                origin.get(key),
                spec,
                allow_null=True,
            )
        )
    return diagnostics


def _validate_record(
    record: Any,
    schema: dict[str, Any],
    kind: str,
    index: int,
) -> list[dict[str, str]]:
    subject = f"{kind}[{index}]"
    if not isinstance(record, dict):
        return [_diag("FAIL", "record.object", subject, f"{kind} record must be an object")]

    record_id = record.get("id")
    if isinstance(record_id, str) and record_id:
        subject = record_id

    diagnostics: list[dict[str, str]] = []
    required = set(schema.get("required", []))
    allowed = set(schema.get("properties", {}))
    for key in sorted(required - set(record)):
        diagnostics.append(_diag("FAIL", "record.required", subject, f"missing required field {key}"))
    for key in sorted(set(record) - allowed):
        diagnostics.append(_diag("FAIL", "record.extra", subject, f"unsupported field {key}"))

    version = record.get("schema_version")
    expected_version = schema["properties"]["schema_version"].get("const")
    if version != expected_version:
        diagnostics.append(_diag("FAIL", "record.schema-version", subject, f"schema_version must be {expected_version}"))

    id_spec = schema["properties"]["id"]
    diagnostics.extend(_validate_string_constraints(subject, "id", record_id, id_spec))
    if isinstance(record_id, str):
        pattern = id_spec.get("pattern")
        if pattern and not re.fullmatch(pattern, record_id):
            diagnostics.append(_diag("FAIL", "record.id-format", subject, f"id does not match {pattern}"))

    record_type = record.get("type")
    allowed_types = set(schema["properties"]["type"].get("enum", []))
    if record_type not in allowed_types:
        diagnostics.append(_diag("FAIL", "record.type", subject, f"unsupported type {record_type!r}"))

    if kind == "node":
        diagnostics.extend(
            _validate_string_constraints(subject, "title", record.get("title"), schema["properties"]["title"])
        )
        diagnostics.extend(
            _validate_string_constraints(
                subject,
                "status",
                record.get("status"),
                schema["properties"]["status"],
                allow_null=True,
            )
        )
    else:
        for endpoint in ("from", "to"):
            value = record.get(endpoint)
            endpoint_spec = schema["properties"][endpoint]
            diagnostics.extend(_validate_string_constraints(subject, endpoint, value, endpoint_spec))
            pattern = endpoint_spec.get("pattern")
            if isinstance(value, str) and pattern and not re.fullmatch(pattern, value):
                diagnostics.append(_diag("FAIL", "edge.endpoint-format", subject, f"{endpoint} does not match node id format"))

    diagnostics.extend(_validate_origin(subject, record.get("origin"), schema))

    if not isinstance(record.get("attributes"), dict):
        diagnostics.append(_diag("FAIL", "record.attributes", subject, "attributes must be an object"))

    return diagnostics


def _find_cycles(nodes: set[str], arcs: list[tuple[str, str]]) -> list[list[str]]:
    adjacency: dict[str, list[str]] = {node: [] for node in nodes}
    for source, target in arcs:
        if source in adjacency and target in adjacency:
            adjacency[source].append(target)
    for source in adjacency:
        adjacency[source].sort()

    state = {node: 0 for node in nodes}
    stack: list[str] = []
    position: dict[str, int] = {}
    cycles: set[tuple[str, ...]] = set()

    def canonical(cycle: list[str]) -> tuple[str, ...]:
        body = cycle[:-1]
        rotations = [tuple(body[i:] + body[:i]) for i in range(len(body))]
        best = min(rotations)
        return best + (best[0],)

    def visit(node: str) -> None:
        state[node] = 1
        position[node] = len(stack)
        stack.append(node)
        for target in adjacency[node]:
            if state[target] == 0:
                visit(target)
            elif state[target] == 1:
                cycle = stack[position[target]:] + [target]
                cycles.add(canonical(cycle))
        stack.pop()
        position.pop(node, None)
        state[node] = 2

    for node in sorted(nodes):
        if state[node] == 0:
            visit(node)
    return [list(cycle) for cycle in sorted(cycles)]


def validate_graph(root: Path, graph: dict[str, Any] | None = None) -> list[dict[str, str]]:
    if graph is None:
        graph = load_graph(root)

    graph_schema = _load_contract(root, "graph.schema.json")
    node_schema = _load_contract(root, "node.schema.json")
    edge_schema = _load_contract(root, "edge.schema.json")
    edge_contract = _load_contract(root, "edge-rules.json")
    diagnostics: list[dict[str, str]] = []

    if not isinstance(graph, dict):
        return [_diag("FAIL", "graph.object", "graph", "graph must be an object")]

    graph_required = set(graph_schema.get("required", []))
    graph_allowed = set(graph_schema.get("properties", {}))
    for key in sorted(graph_required - set(graph)):
        diagnostics.append(_diag("FAIL", "graph.required", "graph", f"missing required field {key}"))
    if graph_schema.get("additionalProperties") is False:
        for key in sorted(set(graph) - graph_allowed):
            diagnostics.append(_diag("FAIL", "graph.extra", "graph", f"unsupported field {key}"))

    if graph.get("schema_version") != GRAPH_SCHEMA_VERSION:
        diagnostics.append(
            _diag("FAIL", "graph.schema-version", "graph", f"schema_version must be {GRAPH_SCHEMA_VERSION}")
        )

    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list):
        diagnostics.append(_diag("FAIL", "graph.nodes", "graph", "nodes must be a list"))
        nodes = []
    if not isinstance(edges, list):
        diagnostics.append(_diag("FAIL", "graph.edges", "graph", "edges must be a list"))
        edges = []

    for index, record in enumerate(nodes, start=1):
        diagnostics.extend(_validate_record(record, node_schema, "node", index))
    for index, record in enumerate(edges, start=1):
        diagnostics.extend(_validate_record(record, edge_schema, "edge", index))

    node_ids: dict[str, dict[str, Any]] = {}
    for record in nodes:
        if not isinstance(record, dict):
            continue
        node_id = record.get("id")
        if not isinstance(node_id, str) or not node_id:
            continue
        if node_id in node_ids:
            diagnostics.append(_diag("FAIL", "node.duplicate-id", node_id, "node id must be unique"))
        else:
            node_ids[node_id] = record
        node_type = record.get("type")
        if isinstance(node_type, str) and node_id.split(".", 1)[0] != node_type:
            diagnostics.append(
                _diag("FAIL", "node.id-prefix", node_id, f"id prefix must match node type {node_type!r}")
            )

    edge_ids: set[str] = set()
    rules_by_type = {
        item["type"]: item
        for item in edge_contract.get("rules", [])
        if isinstance(item, dict) and isinstance(item.get("type"), str)
    }
    degree = {node_id: 0 for node_id in node_ids}
    cycle_arcs: dict[str, list[tuple[str, str]]] = {"contains": [], "supersedes": [], "execution": []}

    for edge in edges:
        if not isinstance(edge, dict):
            continue
        edge_id = edge.get("id")
        edge_type = edge.get("type")
        source = edge.get("from")
        target = edge.get("to")
        subject = edge_id if isinstance(edge_id, str) and edge_id else "edge"

        if isinstance(edge_id, str) and edge_id:
            if edge_id in edge_ids:
                diagnostics.append(_diag("FAIL", "edge.duplicate-id", edge_id, "edge id must be unique"))
            edge_ids.add(edge_id)

        if not isinstance(source, str) or source not in node_ids:
            diagnostics.append(_diag("FAIL", "edge.missing-source", subject, f"source node does not exist: {source!r}"))
        if not isinstance(target, str) or target not in node_ids:
            diagnostics.append(_diag("FAIL", "edge.missing-target", subject, f"target node does not exist: {target!r}"))
        if source == target and isinstance(source, str):
            diagnostics.append(_diag("FAIL", "edge.self", subject, "self edges are forbidden"))

        if source in degree:
            degree[source] += 1
        if target in degree:
            degree[target] += 1

        rule = rules_by_type.get(edge_type)
        if rule is None:
            if isinstance(edge_type, str):
                diagnostics.append(_diag("FAIL", "edge.rule-missing", subject, f"no endpoint rule for edge type {edge_type!r}"))
            continue
        if source not in node_ids or target not in node_ids:
            continue
        source_type = node_ids[source].get("type")
        target_type = node_ids[target].get("type")
        if source_type not in set(rule.get("from", [])):
            diagnostics.append(
                _diag("FAIL", "edge.source-type", subject, f"{edge_type} cannot originate from {source_type!r}")
            )
        if target_type not in set(rule.get("to", [])):
            diagnostics.append(
                _diag("FAIL", "edge.target-type", subject, f"{edge_type} cannot target {target_type!r}")
            )

        if edge_type in {"contains", "supersedes"}:
            cycle_arcs[edge_type].append((source, target))
        if edge_type in {"depends_on", "blocks"} and source_type in EXECUTION_TYPES and target_type in EXECUTION_TYPES:
            cycle_arcs["execution"].append((source, target))

    for relation in ("contains", "supersedes"):
        for cycle in _find_cycles(set(node_ids), cycle_arcs[relation]):
            diagnostics.append(
                _diag("FAIL", f"graph.{relation}-cycle", cycle[0], f"{relation} cycle: {' -> '.join(cycle)}")
            )

    execution_nodes = {node_id for node_id, node in node_ids.items() if node.get("type") in EXECUTION_TYPES}
    for cycle in _find_cycles(execution_nodes, cycle_arcs["execution"]):
        diagnostics.append(
            _diag("FAIL", "graph.execution-cycle", cycle[0], f"execution dependency cycle: {' -> '.join(cycle)}")
        )

    for node_id, count in sorted(degree.items()):
        if count:
            continue
        node_type = node_ids[node_id].get("type")
        if node_type in EXECUTION_TYPES:
            diagnostics.append(
                _diag("FAIL", "graph.orphan-execution", node_id, "execution node must participate in the graph")
            )
        elif node_type != "project":
            diagnostics.append(
                _diag("WARN", "graph.orphan-knowledge", node_id, "knowledge node is not connected")
            )

    diagnostics.sort(
        key=lambda item: (
            SEVERITY_ORDER.get(item["severity"], 9),
            item["code"],
            item["subject"],
            item["message"],
        )
    )
    return diagnostics


def graph_status(diagnostics: list[dict[str, str]]) -> str:
    if any(item["severity"] == "FAIL" for item in diagnostics):
        return "FAIL"
    if any(item["severity"] == "WARN" for item in diagnostics):
        return "WARN"
    return "PASS"
