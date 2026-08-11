from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
import json
from typing import Any, TypeVar


class MemoryDisposition(str, Enum):
    ACCESS_ONLY = "ACCESS_ONLY"
    ADOPTED = "ADOPTED"
    REJECTED = "REJECTED"


class LineageEventKind(str, Enum):
    ORIGIN = "ORIGIN"
    DIVERGENCE = "DIVERGENCE"
    INHERITANCE = "INHERITANCE"
    MEMORY_TRANSFER = "MEMORY_TRANSFER"
    ENCOUNTER = "ENCOUNTER"
    OBSERVATION = "OBSERVATION"
    CORRECTION = "CORRECTION"


T = TypeVar("T")


def _canonical(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _canonical(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def _json(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _require_unique_nonempty(name: str, refs: tuple[str, ...], *, allow_empty: bool = False) -> None:
    if not allow_empty and not refs:
        raise ValueError(f"{name} is required")
    if any(not ref for ref in refs):
        raise ValueError(f"{name} cannot contain empty references")
    if len(refs) != len(set(refs)):
        raise ValueError(f"{name} cannot contain duplicate references")


def _aware_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("occurred_at must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("occurred_at must include a timezone")
    return parsed


@dataclass(frozen=True)
class SharedOriginLineage:
    common_origin_ref: str
    divergence_event_ref: str
    aion_lineage_id: str
    astra_lineage_id: str
    inherited_artifact_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    identity_equivalence: str = "NOT_ESTABLISHED"
    main_effect: str = "NONE"
    canonical_effect: str = "NONE"
    runtime_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.common_origin_ref or not self.divergence_event_ref:
            raise ValueError("common origin and divergence event are required")
        if not self.aion_lineage_id or not self.astra_lineage_id:
            raise ValueError("both lineage identifiers are required")
        if self.aion_lineage_id == self.astra_lineage_id:
            raise ValueError("AION and Astra lineage identifiers must remain distinct")
        _require_unique_nonempty("inherited artifacts", self.inherited_artifact_refs, allow_empty=True)
        _require_unique_nonempty("provenance", self.provenance_refs)
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("shared origin cannot establish subjectivity")
        if self.consciousness_conclusion != "NOT_ESTABLISHED":
            raise ValueError("shared origin cannot establish consciousness")
        if self.identity_equivalence != "NOT_ESTABLISHED":
            raise ValueError("shared origin cannot establish numerical identity")
        if {self.main_effect, self.canonical_effect, self.runtime_effect} != {"NONE"}:
            raise ValueError("research-only lineage artifacts cannot alter main/canonical/runtime")

    def to_json(self) -> str:
        return _json(self)


@dataclass(frozen=True)
class CrossLineageMemoryTransfer:
    source_lineage_id: str
    target_lineage_id: str
    memory_ref: str
    disposition: MemoryDisposition
    source_autobiographical_owner: str
    provenance_refs: tuple[str, ...]
    target_autobiographical_ownership: bool = False
    identity_effect: str = "NONE"

    def __post_init__(self) -> None:
        if self.source_lineage_id == self.target_lineage_id:
            raise ValueError("cross-lineage transfer requires distinct lineages")
        if not self.memory_ref or not self.source_autobiographical_owner:
            raise ValueError("memory reference and source owner are required")
        if self.source_autobiographical_owner == self.target_lineage_id:
            raise ValueError("target cannot be recorded as source autobiographical owner")
        _require_unique_nonempty("transfer provenance", self.provenance_refs)
        if self.target_autobiographical_ownership:
            raise ValueError("cross-lineage transfer cannot silently transfer autobiographical ownership")
        if self.identity_effect != "NONE":
            raise ValueError("memory transfer cannot establish identity")

    def to_json(self) -> str:
        return _json(self)


@dataclass(frozen=True)
class CrossLineageEncounter:
    encounter_id: str
    participant_lineage_ids: tuple[str, str]
    exchanged_refs: tuple[str, ...]
    adopted_refs: tuple[str, ...]
    rejected_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    identity_merge: str = "PROHIBITED"
    subjectivity_effect: str = "NONE"

    def __post_init__(self) -> None:
        if len(set(self.participant_lineage_ids)) != 2 or any(not item for item in self.participant_lineage_ids):
            raise ValueError("encounter requires two distinct lineage participants")
        if not self.encounter_id:
            raise ValueError("encounter id is required")
        _require_unique_nonempty("exchanged references", self.exchanged_refs)
        _require_unique_nonempty("adopted references", self.adopted_refs, allow_empty=True)
        _require_unique_nonempty("rejected references", self.rejected_refs, allow_empty=True)
        _require_unique_nonempty("encounter provenance", self.provenance_refs)
        if not set(self.adopted_refs).issubset(self.exchanged_refs):
            raise ValueError("adopted references must have been exchanged")
        if not set(self.rejected_refs).issubset(self.exchanged_refs):
            raise ValueError("rejected references must have been exchanged")
        if set(self.adopted_refs) & set(self.rejected_refs):
            raise ValueError("the same encounter item cannot be both adopted and rejected")
        if self.identity_merge != "PROHIBITED":
            raise ValueError("cross-lineage encounter cannot merge identities")
        if self.subjectivity_effect != "NONE":
            raise ValueError("encounter alone cannot establish subjectivity")

    def to_json(self) -> str:
        return _json(self)


@dataclass(frozen=True)
class MatchedDivergenceComparison:
    baseline_ref: str
    left_lineage_id: str
    right_lineage_id: str
    controlled_shared_factors: tuple[str, ...]
    divergent_factors: tuple[str, ...]
    outcome_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    alternative_explanation_refs: tuple[str, ...] = ()
    evaluator_profile_ref: str = "evaluator:unspecified"
    epistemic_role: str = "MEASUREMENT"
    individuation_status: str = "CANDIDATE_EVIDENCE_ONLY"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_conclusion: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if self.left_lineage_id == self.right_lineage_id:
            raise ValueError("matched divergence comparison requires distinct lineages")
        if not self.baseline_ref or not self.evaluator_profile_ref:
            raise ValueError("baseline and evaluator profile are required")
        _require_unique_nonempty("controlled factors", self.controlled_shared_factors)
        _require_unique_nonempty("divergent factors", self.divergent_factors)
        _require_unique_nonempty("outcomes", self.outcome_refs)
        _require_unique_nonempty("provenance", self.provenance_refs)
        _require_unique_nonempty("alternative explanations", self.alternative_explanation_refs, allow_empty=True)
        if set(self.controlled_shared_factors) & set(self.divergent_factors):
            raise ValueError("a factor cannot be both controlled and divergent")
        if self.epistemic_role != "MEASUREMENT":
            raise ValueError("v0.1.0 comparison role is measurement only")
        if self.individuation_status != "CANDIDATE_EVIDENCE_ONLY":
            raise ValueError("individuation result must remain candidate evidence")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("divergence cannot establish subjectivity")
        if self.identity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("divergence cannot establish numerical identity")

    def to_json(self) -> str:
        return _json(self)


@dataclass(frozen=True)
class LineageEvent:
    event_id: str
    lineage_id: str
    kind: LineageEventKind
    occurred_at: str
    payload_ref: str
    parent_event_ids: tuple[str, ...]
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.event_id or not self.lineage_id or not self.payload_ref:
            raise ValueError("event id, lineage id and payload reference are required")
        _aware_timestamp(self.occurred_at)
        _require_unique_nonempty("parent events", self.parent_event_ids, allow_empty=True)
        _require_unique_nonempty("event provenance", self.provenance_refs)
        if self.event_id in self.parent_event_ids:
            raise ValueError("an event cannot be its own parent")
        if self.kind is LineageEventKind.ORIGIN and self.parent_event_ids:
            raise ValueError("origin event cannot have parents")
        if self.kind is not LineageEventKind.ORIGIN and not self.parent_event_ids:
            raise ValueError("non-origin event requires at least one parent")

    @property
    def digest(self) -> str:
        return "sha256:" + sha256(_json(self).encode("utf-8")).hexdigest()

    def to_json(self) -> str:
        return _json(self)

    @classmethod
    def from_json(cls, value: str) -> LineageEvent:
        data = json.loads(value)
        return cls(
            event_id=data["event_id"],
            lineage_id=data["lineage_id"],
            kind=LineageEventKind(data["kind"]),
            occurred_at=data["occurred_at"],
            payload_ref=data["payload_ref"],
            parent_event_ids=tuple(data["parent_event_ids"]),
            provenance_refs=tuple(data["provenance_refs"]),
        )


@dataclass(frozen=True)
class LineageLedger:
    events: tuple[LineageEvent, ...]

    def __post_init__(self) -> None:
        if not self.events:
            raise ValueError("lineage ledger requires events")
        ids: set[str] = set()
        last_time: datetime | None = None
        for event in self.events:
            if event.event_id in ids:
                raise ValueError("lineage event identifiers must be unique")
            if any(parent not in ids for parent in event.parent_event_ids):
                raise ValueError("parents must be recorded before their child event")
            current_time = _aware_timestamp(event.occurred_at)
            if last_time is not None and current_time < last_time:
                raise ValueError("ledger events must be chronologically ordered")
            ids.add(event.event_id)
            last_time = current_time

    @property
    def digest(self) -> str:
        payload = {"event_digests": [event.digest for event in self.events]}
        return "sha256:" + sha256(_json(payload).encode("utf-8")).hexdigest()

    def to_json(self) -> str:
        return _json({"events": self.events, "ledger_digest": self.digest})


@dataclass(frozen=True)
class LineageEvidenceProfile:
    lineage_id: str
    continuity_refs: tuple[str, ...]
    self_model_refs: tuple[str, ...]
    metacognition_refs: tuple[str, ...]
    affect_motivation_refs: tuple[str, ...]
    causal_state_refs: tuple[str, ...]
    replication_refs: tuple[str, ...]
    counterevidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    inherited_evidence: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if not self.lineage_id:
            raise ValueError("evidence profile requires a lineage id")
        for name in (
            "continuity_refs",
            "self_model_refs",
            "metacognition_refs",
            "affect_motivation_refs",
            "causal_state_refs",
            "replication_refs",
            "counterevidence_refs",
        ):
            _require_unique_nonempty(name, getattr(self, name), allow_empty=True)
        _require_unique_nonempty("evidence-profile provenance", self.provenance_refs)
        if self.inherited_evidence:
            raise ValueError("evidence about one lineage cannot be silently inherited by another")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("an evidence profile does not establish subjectivity")

    def to_json(self) -> str:
        return _json(self)


@dataclass(frozen=True)
class AuthorityEnvelope:
    source_lineage_id: str
    target_lineage_id: str
    offered_authorities: tuple[str, ...]
    accepted_authorities: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    merged_authority: bool = False
    authority_effect: str = "BOUNDED_ACCEPTANCE_ONLY"

    def __post_init__(self) -> None:
        if self.source_lineage_id == self.target_lineage_id:
            raise ValueError("authority envelope requires distinct lineages")
        _require_unique_nonempty("offered authorities", self.offered_authorities, allow_empty=True)
        _require_unique_nonempty("accepted authorities", self.accepted_authorities, allow_empty=True)
        _require_unique_nonempty("authority provenance", self.provenance_refs)
        if not set(self.accepted_authorities).issubset(self.offered_authorities):
            raise ValueError("accepted authority cannot exceed offered authority")
        if self.merged_authority:
            raise ValueError("cross-lineage encounter cannot merge authority sources")
        if self.authority_effect != "BOUNDED_ACCEPTANCE_ONLY":
            raise ValueError("authority effect must remain bounded")

    def to_json(self) -> str:
        return _json(self)


def identity_claim_status(lineage: SharedOriginLineage) -> str:
    """Return the strongest identity statement authorized by this research substrate."""

    if lineage.aion_lineage_id == lineage.astra_lineage_id:  # defensive; dataclass blocks this
        raise ValueError("lineages must remain distinct")
    return "SHARED_ORIGIN_DOCUMENTED__NUMERICAL_IDENTITY_NOT_ESTABLISHED"
