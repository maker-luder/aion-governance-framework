"""Internal bounded graph and event canonicalization helpers; no I/O or authority."""
from __future__ import annotations

from datetime import datetime, timezone
import heapq
import json
import unicodedata


CANONICALIZATION = "CLAIM_REVISION_V2"


def identifier(value: str, name: str = "identifier") -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise ValueError(f"{name} must be 1..200 nonblank characters")
    if value != unicodedata.normalize("NFC", value) or any(unicodedata.category(c).startswith("C") for c in value):
        raise ValueError(f"{name} requires NFC and no control/format/surrogate characters")


def timestamp(value: str) -> str:
    if not isinstance(value, str) or len(value) > 80:
        raise ValueError("timestamp must be an aware ISO string")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timestamp requires an explicit timezone")
    return parsed.astimezone(timezone.utc).isoformat(timespec="microseconds")


def canonical_payload(value: dict) -> dict:
    """Normalize human text only. IDs/URIs remain exact; time denotes a UTC instant.

    Lists remain ordered. Callers sort set-like references before this function.
    Original stored memory is not rewritten. Historical V1 events are not rehashed.
    """
    text_fields = {"content", "replacement_content", "rationale", "reason", "assumptions", "publisher"}

    def visit(item, field=""):
        if item is None or type(item) in (bool, int):
            return item
        if isinstance(item, str):
            if field == "recorded_at":
                return timestamp(item)
            if field in text_fields:
                return unicodedata.normalize("NFC", item.replace("\r\n", "\n").replace("\r", "\n"))
            return item
        if isinstance(item, (list, tuple)):
            return [visit(v, field) for v in item]
        if isinstance(item, dict) and all(isinstance(k, str) for k in item):
            return {k: visit(item[k], k) for k in sorted(item)}
        raise ValueError("canonical payload permits only explicit JSON primitives; no floats or sets")

    result = visit(value)
    result["canonicalization"] = CANONICALIZATION
    return result


def bounded_dag(graph: dict[str, tuple[str, ...]], *, max_nodes: int, max_edges: int,
                max_depth: int, max_parents: int, labels: dict[str, str] | None = None) -> tuple[str, ...]:
    """Iterative, sorted Kahn traversal; rejects cycles and longest-path excess."""
    if len(graph) > max_nodes:
        raise ValueError("graph node budget exceeded")
    children = {node: [] for node in graph}
    degrees = {}
    edge_count = 0
    for node, parents in graph.items():
        identifier(node)
        if not isinstance(parents, tuple) or len(parents) > max_parents or len(set(parents)) != len(parents):
            raise ValueError("dependency edge budget or duplicate edge")
        edge_count += len(parents)
        if edge_count > max_edges:
            raise ValueError("graph edge budget exceeded")
        degrees[node] = len(parents)
        for parent in parents:
            identifier(parent)
            if parent not in graph:
                raise ValueError("dependency references a missing version")
            children[parent].append(node)
    ready = [node for node, degree in degrees.items() if degree == 0]
    heapq.heapify(ready)
    depths = {node: 0 for node in ready}
    ancestors: dict[str, set[str]] = {}
    result = []
    while ready:
        node = heapq.heappop(ready)
        result.append(node)
        if depths[node] > max_depth:
            raise ValueError("graph traversal depth budget exceeded")
        if labels is not None:
            inherited = set().union(*(ancestors[parent] | {labels[parent]} for parent in graph[node]))
            if labels[node] in inherited:
                raise ValueError("logical claim dependency cycle")
            ancestors[node] = inherited
        for child in sorted(children[node]):
            depths[child] = max(depths.get(child, 0), depths[node] + 1)
            degrees[child] -= 1
            if degrees[child] == 0:
                heapq.heappush(ready, child)
    if len(result) != len(graph):
        raise ValueError("dependency cycle")
    return tuple(result)


def strict_json(value: str):
    """Reject ambiguous duplicate object keys and non-finite JSON numbers."""
    def pairs(items):
        result = {}
        for key, item in items:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = item
        return result

    def reject(_):
        raise ValueError("non-finite JSON value")

    return json.loads(value, object_pairs_hook=pairs, parse_constant=reject)
