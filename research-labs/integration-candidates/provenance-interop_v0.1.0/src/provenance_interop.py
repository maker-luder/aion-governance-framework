"""Offline, deterministic provenance interoperability mapping.

This candidate is inspired by the W3C PROV-DM vocabulary but is not a
claim of full W3C conformance. It produces inspectable JSON only.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Iterable


class ProvenanceValidationError(ValueError):
    """Raised when a provenance document is structurally invalid."""


@dataclass(frozen=True)
class Entity:
    identifier: str
    kind: str = "entity"
    attributes: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Activity:
    identifier: str
    started_at: str
    ended_at: str | None = None
    attributes: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Agent:
    identifier: str
    kind: str = "agent"
    attributes: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Relation:
    relation: str
    subject: str
    object: str
    attributes: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ProvenanceDocument:
    entities: tuple[Entity, ...] = ()
    activities: tuple[Activity, ...] = ()
    agents: tuple[Agent, ...] = ()
    relations: tuple[Relation, ...] = ()
    canonical_effect: str = "NONE"
    deployment: bool = False
    independent_ivv: str = "NOT_ACHIEVED"

    def _validate_timestamp(self, value: str, label: str) -> None:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ProvenanceValidationError(f"invalid {label}: {value}") from exc
        if parsed.tzinfo is None:
            raise ProvenanceValidationError(f"{label} must include timezone: {value}")

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        entity_ids = [item.identifier for item in self.entities]
        activity_ids = [item.identifier for item in self.activities]
        agent_ids = [item.identifier for item in self.agents]
        all_ids = entity_ids + activity_ids + agent_ids
        if len(all_ids) != len(set(all_ids)):
            errors.append("identifiers must be globally unique")
        if any(not value or "://" in value or value.startswith("/") for value in all_ids):
            errors.append("identifiers must be non-empty symbolic identifiers")
        for activity in self.activities:
            try:
                self._validate_timestamp(activity.started_at, "activity.started_at")
                if activity.ended_at is not None:
                    self._validate_timestamp(activity.ended_at, "activity.ended_at")
                    start = datetime.fromisoformat(activity.started_at.replace("Z", "+00:00"))
                    end = datetime.fromisoformat(activity.ended_at.replace("Z", "+00:00"))
                    if end < start:
                        errors.append(f"activity ended before start: {activity.identifier}")
            except ProvenanceValidationError as exc:
                errors.append(str(exc))
        valid_relations = {
            "wasGeneratedBy": ("entity", "activity"),
            "used": ("activity", "entity"),
            "wasDerivedFrom": ("entity", "entity"),
            "wasAttributedTo": ("entity", "agent"),
            "wasAssociatedWith": ("activity", "agent"),
            "actedOnBehalfOf": ("agent", "agent"),
        }
        type_by_id = {**{x.identifier: "entity" for x in self.entities},
                      **{x.identifier: "activity" for x in self.activities},
                      **{x.identifier: "agent" for x in self.agents}}
        for relation in self.relations:
            expected = valid_relations.get(relation.relation)
            if expected is None:
                errors.append(f"unsupported relation: {relation.relation}")
                continue
            if relation.subject not in type_by_id or relation.object not in type_by_id:
                errors.append(f"relation references unknown identifier: {relation.relation}")
                continue
            if (type_by_id[relation.subject], type_by_id[relation.object]) != expected:
                errors.append(f"relation type mismatch: {relation.relation}")
        if self.canonical_effect != "NONE":
            errors.append("canonical_effect must remain NONE")
        if self.deployment:
            errors.append("deployment must remain false")
        if self.independent_ivv != "NOT_ACHIEVED":
            errors.append("independent_ivv must remain NOT_ACHIEVED")
        return tuple(sorted(set(errors)))

    def validate_or_raise(self) -> None:
        errors = self.validate()
        if errors:
            raise ProvenanceValidationError("; ".join(errors))

    def to_dict(self) -> dict[str, Any]:
        self.validate_or_raise()
        payload = asdict(self)
        payload["entities"] = sorted(payload["entities"], key=lambda item: item["identifier"])
        payload["activities"] = sorted(payload["activities"], key=lambda item: item["identifier"])
        payload["agents"] = sorted(payload["agents"], key=lambda item: item["identifier"])
        payload["relations"] = sorted(payload["relations"], key=lambda item: (item["relation"], item["subject"], item["object"]))
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    def digest(self) -> str:
        return hashlib.sha256(self.to_json().encode("utf-8")).hexdigest()


def build_document(*, entities: Iterable[Entity] = (), activities: Iterable[Activity] = (), agents: Iterable[Agent] = (), relations: Iterable[Relation] = ()) -> ProvenanceDocument:
    document = ProvenanceDocument(tuple(entities), tuple(activities), tuple(agents), tuple(relations))
    document.validate_or_raise()
    return document
