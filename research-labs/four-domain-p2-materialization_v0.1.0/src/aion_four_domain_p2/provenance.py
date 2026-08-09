from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re


_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


class ProvenanceRelationKind(str, Enum):
    DERIVED_FROM = "DERIVED_FROM"
    REVISION_OF = "REVISION_OF"
    ATTRIBUTED_TO = "ATTRIBUTED_TO"
    INVALIDATED_BY = "INVALIDATED_BY"
    PRIMARY_SOURCE = "PRIMARY_SOURCE"


class ProvenanceDecision(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    FAIL = "FAIL"


@dataclass(frozen=True, slots=True)
class ProvenanceRelation:
    kind: ProvenanceRelationKind
    target_id: str
    at_time: datetime | None = None
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ProvenanceEnvelope:
    entity_id: str | None = None
    subject_id: str | None = None
    namespace: str | None = None
    source_refs: tuple[str, ...] = ()
    actor_id: str | None = None
    activity_id: str | None = None
    operation: str | None = None
    generated_at: datetime | None = None
    content_hash: str | None = None
    authority_status: str | None = None
    transformation_refs: tuple[str, ...] = ()
    relations: tuple[ProvenanceRelation, ...] = ()


@dataclass(frozen=True, slots=True)
class ProvenanceReport:
    entity_id: str | None
    decision: ProvenanceDecision
    missing_fields: tuple[str, ...]
    invalid_fields: tuple[str, ...]
    missing_relations: tuple[ProvenanceRelationKind, ...]
    valid_fields: frozenset[str]
    numerator: int
    denominator: int
    completeness: float
    projection: tuple[tuple[str, str], ...]


class ProvenanceCompletenessValidator:
    """Privacy-bounded provenance validation inspired by W3C PROV concepts.

    This is not a PROV-O serializer or conformance checker.
    """

    REQUIRED_FIELDS = (
        "entity_id",
        "subject_id",
        "namespace",
        "source_refs",
        "actor_id",
        "activity_id",
        "operation",
        "generated_at",
        "content_hash",
        "authority_status",
    )

    CRITICAL_FIELDS = frozenset(REQUIRED_FIELDS)

    def validate(
        self,
        envelope: ProvenanceEnvelope | None,
        *,
        required_relations: tuple[ProvenanceRelationKind, ...] = (),
    ) -> ProvenanceReport:
        if envelope is None:
            denominator = len(self.REQUIRED_FIELDS) + len(required_relations)
            return ProvenanceReport(
                entity_id=None,
                decision=ProvenanceDecision.FAIL,
                missing_fields=self.REQUIRED_FIELDS,
                invalid_fields=(),
                missing_relations=required_relations,
                valid_fields=frozenset(),
                numerator=0,
                denominator=denominator,
                completeness=0.0 if denominator else 1.0,
                projection=(),
            )

        missing: list[str] = []
        invalid: list[str] = []
        valid: set[str] = set()

        for field_name in self.REQUIRED_FIELDS:
            value = getattr(envelope, field_name)
            if self._missing(value):
                missing.append(field_name)
                continue
            if field_name == "generated_at":
                assert isinstance(value, datetime)
                if value.tzinfo is None or value.utcoffset() is None:
                    invalid.append(field_name)
                    continue
            if field_name == "content_hash":
                assert isinstance(value, str)
                if _SHA256.fullmatch(value) is None:
                    invalid.append(field_name)
                    continue
            valid.add(field_name)

        relation_kinds = {relation.kind for relation in envelope.relations}
        missing_relations = tuple(kind for kind in required_relations if kind not in relation_kinds)

        for index, relation in enumerate(envelope.relations):
            if not relation.target_id.strip():
                invalid.append(f"relations[{index}].target_id")
            if relation.at_time is not None and (
                relation.at_time.tzinfo is None or relation.at_time.utcoffset() is None
            ):
                invalid.append(f"relations[{index}].at_time")

        denominator = len(self.REQUIRED_FIELDS) + len(required_relations)
        numerator = len(valid) + (len(required_relations) - len(missing_relations))
        completeness = 1.0 if denominator == 0 else numerator / denominator

        if self.CRITICAL_FIELDS.intersection(missing) or invalid:
            decision = ProvenanceDecision.FAIL
        elif missing_relations:
            decision = ProvenanceDecision.HOLD
        else:
            decision = ProvenanceDecision.PASS

        projection_items = [
            ("entity_id", envelope.entity_id or ""),
            ("subject_id", envelope.subject_id or ""),
            ("namespace", envelope.namespace or ""),
            ("content_hash", envelope.content_hash or ""),
            ("authority_status", envelope.authority_status or ""),
            ("relation_kinds", ",".join(sorted(kind.value for kind in relation_kinds))),
        ]

        return ProvenanceReport(
            entity_id=envelope.entity_id,
            decision=decision,
            missing_fields=tuple(missing),
            invalid_fields=tuple(sorted(set(invalid))),
            missing_relations=missing_relations,
            valid_fields=frozenset(valid),
            numerator=numerator,
            denominator=denominator,
            completeness=completeness,
            projection=tuple(projection_items),
        )

    @staticmethod
    def _missing(value: object) -> bool:
        if value is None:
            return True
        if isinstance(value, str):
            return not value.strip()
        if isinstance(value, tuple):
            return len(value) == 0
        return False
