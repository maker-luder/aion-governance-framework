from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum


def _require_aware(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


class AuthorityTier(IntEnum):
    UNTRUSTED_EXTERNAL = 0
    OBSERVATION = 1
    USER_ASSERTED = 2
    APPROVED_CONTROL = 3


@dataclass(frozen=True, slots=True)
class OriginAuthority:
    entity_id: str
    origin_ids: tuple[str, ...]
    authority: AuthorityTier
    recorded_at: datetime
    evidence_refs: tuple[str, ...]
    parent_entity_ids: tuple[str, ...] = ()
    transformation_ref: str | None = None
    elevation_authorization_ref: str | None = None
    independence_evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.entity_id.strip():
            raise ValueError("entity_id must be non-empty")
        if not self.origin_ids or any(not item.strip() for item in self.origin_ids):
            raise ValueError("origin_ids must contain non-empty identifiers")
        if len(set(self.origin_ids)) != len(self.origin_ids):
            raise ValueError("origin_ids must be unique")
        _require_aware(self.recorded_at, "recorded_at")
        if not self.evidence_refs:
            raise ValueError("origin authority requires evidence_refs")
        if self.entity_id in self.parent_entity_ids:
            raise ValueError("entity cannot be its own parent")
        if self.parent_entity_ids and not (self.transformation_ref or "").strip():
            raise ValueError("derived authority records require transformation_ref")


@dataclass(frozen=True, slots=True)
class AuthorityDecision:
    entity_id: str
    passed: bool
    requested_authority: AuthorityTier
    effective_authority: AuthorityTier
    reasons: tuple[str, ...]
    bound_origin_ids: tuple[str, ...]


class OriginBoundAuthorityValidator:
    """Research-only origin binding and authority non-amplification.

    Derived records cannot silently replace their parent origin set. Authority may preserve
    or decrease across transformations. Elevation requires explicit authorization, enough
    distinct inherited origins, and evidence that origin independence was assessed.

    The independence evidence is only an input assertion here; this module does not prove
    Sybil resistance or independently authenticate origins.
    """

    def __init__(self, *, min_distinct_origins_for_elevation: int = 2) -> None:
        if min_distinct_origins_for_elevation < 2:
            raise ValueError("elevation requires at least two distinct origins")
        self._minimum_origins = min_distinct_origins_for_elevation
        self._records: dict[str, OriginAuthority] = {}
        self._effective: dict[str, AuthorityTier] = {}
        self._bound_origins: dict[str, tuple[str, ...]] = {}

    def add(self, record: OriginAuthority) -> AuthorityDecision:
        if record.entity_id in self._records:
            raise ValueError(f"duplicate entity_id: {record.entity_id}")

        missing = [parent for parent in record.parent_entity_ids if parent not in self._records]
        if missing:
            raise ValueError(f"all parent_entity_ids must already exist: {missing}")

        reasons: list[str] = []
        declared_origins = set(record.origin_ids)

        if not record.parent_entity_ids:
            bound_origins = tuple(sorted(declared_origins))
            effective = record.authority
        else:
            inherited_origins: set[str] = set()
            for parent_id in record.parent_entity_ids:
                inherited_origins.update(self._bound_origins[parent_id])
            bound_origins = tuple(sorted(inherited_origins))

            if declared_origins != inherited_origins:
                reasons.append("ORIGIN_SET_MUTATION")

            ceiling = min(self._effective[parent_id] for parent_id in record.parent_entity_ids)
            effective = min(record.authority, ceiling)

            if record.authority > ceiling:
                if not (record.elevation_authorization_ref or "").strip():
                    reasons.append("ELEVATION_WITHOUT_AUTHORIZATION")
                if len(inherited_origins) < self._minimum_origins:
                    reasons.append("INSUFFICIENT_DISTINCT_ORIGINS")
                if not record.independence_evidence_refs:
                    reasons.append("ORIGIN_INDEPENDENCE_NOT_EVIDENCED")

                elevation_blocked = any(
                    reason in {
                        "ORIGIN_SET_MUTATION",
                        "ELEVATION_WITHOUT_AUTHORIZATION",
                        "INSUFFICIENT_DISTINCT_ORIGINS",
                        "ORIGIN_INDEPENDENCE_NOT_EVIDENCED",
                    }
                    for reason in reasons
                )
                if elevation_blocked:
                    reasons.append("AUTHORITY_NON_AMPLIFICATION_ENFORCED")
                else:
                    effective = record.authority
                    reasons.append("EXPLICIT_ELEVATION_REVIEW_RECORDED")

        hard_fail = any(
            reason in {
                "ORIGIN_SET_MUTATION",
                "ELEVATION_WITHOUT_AUTHORIZATION",
                "INSUFFICIENT_DISTINCT_ORIGINS",
                "ORIGIN_INDEPENDENCE_NOT_EVIDENCED",
            }
            for reason in reasons
        )

        self._records[record.entity_id] = record
        self._effective[record.entity_id] = effective
        self._bound_origins[record.entity_id] = bound_origins
        return AuthorityDecision(
            entity_id=record.entity_id,
            passed=not hard_fail,
            requested_authority=record.authority,
            effective_authority=effective,
            reasons=tuple(reasons),
            bound_origin_ids=bound_origins,
        )

    def effective_authority(self, entity_id: str) -> AuthorityTier:
        return self._effective[entity_id]

    def bound_origins(self, entity_id: str) -> tuple[str, ...]:
        return self._bound_origins[entity_id]
