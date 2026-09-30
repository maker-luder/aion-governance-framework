from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ProvenanceError(ValueError):
    pass


class ContributionOrigin(StrEnum):
    HUMAN_ORIGIN = "HUMAN_ORIGIN"
    AI_FORMALIZATION = "AI_FORMALIZATION"
    JOINT_SYNTHESIS = "JOINT_SYNTHESIS"
    EXTERNAL_SOURCE = "EXTERNAL_SOURCE"
    UNKNOWN = "UNKNOWN"


class ContributionActor(StrEnum):
    """Operational collaborator/source label, separate from epistemic origin."""

    HUMAN_OWNER = "HUMAN_OWNER"
    CHATGPT_TEACHER = "CHATGPT_TEACHER"
    CHATGPT_WORK = "CHATGPT_WORK"
    CODEX = "CODEX"
    MANUS = "MANUS"
    GITHUB_ACTIONS = "GITHUB_ACTIONS"
    AUTOMATED_TEST = "AUTOMATED_TEST"
    EXTERNAL_SOURCE = "EXTERNAL_SOURCE"
    SOURCE_UNVERIFIED = "SOURCE_UNVERIFIED"


_AI_FORMALIZATION_ACTORS = frozenset(
    {
        ContributionActor.CHATGPT_TEACHER,
        ContributionActor.CHATGPT_WORK,
        ContributionActor.CODEX,
        ContributionActor.MANUS,
    }
)


class AIInteractionSurface(StrEnum):
    """Observed user-facing or workflow surface for a bounded AI contribution."""

    CHATGPT_CHAT = "CHATGPT_CHAT"
    CHATGPT_WORK = "CHATGPT_WORK"
    CODEX = "CODEX"
    MANUS = "MANUS"
    UNKNOWN = "UNKNOWN"


class ActorClaimSource(StrEnum):
    """Evidence class for a returned actor label."""

    RUNTIME_SELF_REPORT = "RUNTIME_SELF_REPORT"
    EXTERNAL_METADATA = "EXTERNAL_METADATA"
    USER_OBSERVED_LABEL = "USER_OBSERVED_LABEL"
    UNKNOWN = "UNKNOWN"


class ContributionFunction(StrEnum):
    """Operational function of a bounded AI contribution."""

    FORMALIZATION = "FORMALIZATION"
    IMPLEMENTATION = "IMPLEMENTATION"
    REVIEW = "REVIEW"


@dataclass(frozen=True, slots=True)
class ActorExpectation:
    """Pre-delegation provenance expectation for a material AI task.

    Surface and actor are independent axes. A surface may be known while the
    execution actor remains SOURCE_UNVERIFIED.
    """

    task_id: str
    function: ContributionFunction
    expected_actor: ContributionActor
    expected_surface: AIInteractionSurface
    source_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ProvenanceError("task_id must be non-empty")
        if type(self.function) is not ContributionFunction:
            raise ProvenanceError("function must use an exact ContributionFunction value")
        if type(self.expected_actor) is not ContributionActor:
            raise ProvenanceError("expected_actor must use an exact ContributionActor value")
        if type(self.expected_surface) is not AIInteractionSurface:
            raise ProvenanceError("expected_surface must use an exact AIInteractionSurface value")
        if not self.source_refs:
            raise ProvenanceError("actor expectation requires at least one source reference")
        if (
            self.expected_actor is ContributionActor.SOURCE_UNVERIFIED
            and self.expected_surface is AIInteractionSurface.UNKNOWN
        ):
            raise ProvenanceError("actor expectation must bind at least actor or interaction surface")


@dataclass(frozen=True, slots=True)
class ActorClaim:
    """Returned actor claim, kept separate from surface and verified actor."""

    task_id: str
    function: ContributionFunction
    claimed_actor: ContributionActor
    surface: AIInteractionSurface
    claim_source: ActorClaimSource
    source_refs: tuple[str, ...] = field(default_factory=tuple)
    verified_actor: ContributionActor = ContributionActor.SOURCE_UNVERIFIED
    verification_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ProvenanceError("task_id must be non-empty")
        if type(self.function) is not ContributionFunction:
            raise ProvenanceError("function must use an exact ContributionFunction value")
        if type(self.claimed_actor) is not ContributionActor:
            raise ProvenanceError("claimed_actor must use an exact ContributionActor value")
        if type(self.surface) is not AIInteractionSurface:
            raise ProvenanceError("surface must use an exact AIInteractionSurface value")
        if type(self.claim_source) is not ActorClaimSource:
            raise ProvenanceError("claim_source must use an exact ActorClaimSource value")
        if type(self.verified_actor) is not ContributionActor:
            raise ProvenanceError("verified_actor must use an exact ContributionActor value")
        if not self.source_refs:
            raise ProvenanceError("actor claim requires at least one source reference")
        if (
            self.verified_actor is not ContributionActor.SOURCE_UNVERIFIED
            and not self.verification_refs
        ):
            raise ProvenanceError(
                "verified_actor requires independent verification_refs"
            )
        if (
            self.verified_actor is ContributionActor.SOURCE_UNVERIFIED
            and self.verification_refs
        ):
            raise ProvenanceError(
                "verification_refs require a specific verified_actor"
            )


def verify_actor_claim(expectation: ActorExpectation, claim: ActorClaim) -> None:
    """Fail closed on evidence conflict without equating surface with actor."""

    if expectation.task_id != claim.task_id:
        raise ProvenanceError("actor provenance task_id mismatch")
    if expectation.function is not claim.function:
        raise ProvenanceError("actor provenance contribution-function mismatch")

    if (
        expectation.expected_surface is not AIInteractionSurface.UNKNOWN
        and expectation.expected_surface is not claim.surface
    ):
        raise ProvenanceError(
            f"actor surface drift: expected {expectation.expected_surface.value}, got {claim.surface.value}"
        )

    if expectation.expected_actor is not ContributionActor.SOURCE_UNVERIFIED:
        if (
            claim.claimed_actor is not ContributionActor.SOURCE_UNVERIFIED
            and expectation.expected_actor is not claim.claimed_actor
        ):
            raise ProvenanceError(
                "actor claim conflict: "
                f"expected {expectation.expected_actor.value}, claimed {claim.claimed_actor.value}"
            )
        if (
            claim.verified_actor is not ContributionActor.SOURCE_UNVERIFIED
            and expectation.expected_actor is not claim.verified_actor
        ):
            raise ProvenanceError(
                "verified actor conflict: "
                f"expected {expectation.expected_actor.value}, verified {claim.verified_actor.value}"
            )

    if (
        claim.verified_actor is not ContributionActor.SOURCE_UNVERIFIED
        and claim.claimed_actor is not ContributionActor.SOURCE_UNVERIFIED
        and claim.verified_actor is not claim.claimed_actor
    ):
        raise ProvenanceError(
            "actor claim conflicts with independently verified actor: "
            f"claimed {claim.claimed_actor.value}, verified {claim.verified_actor.value}"
        )


class ClaimLayer(StrEnum):
    DIRECT_STATEMENT = "DIRECT_STATEMENT"
    OBSERVATION = "OBSERVATION"
    SOURCE_REPORT = "SOURCE_REPORT"
    ANALYSIS = "ANALYSIS"
    INFERENCE = "INFERENCE"
    HYPOTHESIS = "HYPOTHESIS"
    CORRECTION = "CORRECTION"


class StateAttribution(StrEnum):
    NOT_APPLICABLE = "NOT_APPLICABLE"
    SELF_REPORTED = "SELF_REPORTED"
    OBSERVED_SIGNAL_ONLY = "OBSERVED_SIGNAL_ONLY"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class ContributionRecord:
    """Immutable attribution record for a bounded research proposition.

    The record classifies where a proposition entered the collaboration and what
    epistemic layer it occupies. It does not establish that the proposition is true.
    """

    record_id: str
    proposition: str
    origin: ContributionOrigin
    layer: ClaimLayer
    actor: ContributionActor = ContributionActor.SOURCE_UNVERIFIED
    source_refs: tuple[str, ...] = field(default_factory=tuple)
    parent_ids: tuple[str, ...] = field(default_factory=tuple)
    state_attribution: StateAttribution = StateAttribution.NOT_APPLICABLE
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.record_id.strip():
            raise ProvenanceError("record_id must be non-empty")
        if not self.proposition.strip():
            raise ProvenanceError("proposition must be non-empty")
        if self.canonical_effect != "NONE":
            raise ProvenanceError("provenance records cannot create canonical effect")
        if type(self.actor) is not ContributionActor:
            raise ProvenanceError("actor must use an exact ContributionActor value")
        if self.origin is ContributionOrigin.AI_FORMALIZATION and self.actor not in _AI_FORMALIZATION_ACTORS:
            raise ProvenanceError(
                "AI_FORMALIZATION requires a specific AI collaborator actor; generic or unverified AI attribution is not admissible"
            )
        if self.actor in _AI_FORMALIZATION_ACTORS and self.origin is not ContributionOrigin.AI_FORMALIZATION:
            raise ProvenanceError("a specific AI collaborator actor requires AI_FORMALIZATION origin")
        if self.origin in {ContributionOrigin.HUMAN_ORIGIN, ContributionOrigin.EXTERNAL_SOURCE} and not self.source_refs:
            raise ProvenanceError(f"{self.origin.value} requires at least one source reference")
        if self.state_attribution is StateAttribution.SELF_REPORTED:
            if self.origin is not ContributionOrigin.HUMAN_ORIGIN:
                raise ProvenanceError("self-reported state must be attributed to HUMAN_ORIGIN")
            if self.layer is not ClaimLayer.DIRECT_STATEMENT:
                raise ProvenanceError("self-reported state requires DIRECT_STATEMENT layer")
        if self.state_attribution is StateAttribution.INFERRED and self.origin is ContributionOrigin.HUMAN_ORIGIN:
            raise ProvenanceError("an inferred state cannot be relabeled as HUMAN_ORIGIN")


@dataclass(frozen=True, slots=True)
class ProvenanceAudit:
    record_id: str
    actor: ContributionActor
    structurally_valid: bool
    human_origin_admissible: bool
    externally_sourced: bool
    joint_synthesis_admissible: bool
    reasons: tuple[str, ...]
    canonical_effect: str = "NONE"


class EpistemicProvenanceLedger:
    """Small append-only attribution ledger for human-AI research reconstruction.

    It guards source-role attribution only. It does not authenticate a person,
    validate external evidence, or decide scientific truth.
    """

    def __init__(self) -> None:
        self._records: dict[str, ContributionRecord] = {}

    def add(self, record: ContributionRecord) -> None:
        if record.record_id in self._records:
            raise ProvenanceError(f"duplicate record_id: {record.record_id}")
        missing = tuple(parent for parent in record.parent_ids if parent not in self._records)
        if missing:
            raise ProvenanceError(f"unknown parent_ids: {', '.join(missing)}")
        if record.origin is ContributionOrigin.JOINT_SYNTHESIS:
            if len(record.parent_ids) < 2:
                raise ProvenanceError("JOINT_SYNTHESIS requires at least two parent records")
            parent_origins = {self._records[parent].origin for parent in record.parent_ids}
            human_side = ContributionOrigin.HUMAN_ORIGIN in parent_origins or ContributionOrigin.JOINT_SYNTHESIS in parent_origins
            ai_side = ContributionOrigin.AI_FORMALIZATION in parent_origins or ContributionOrigin.JOINT_SYNTHESIS in parent_origins
            if not (human_side and ai_side):
                raise ProvenanceError("JOINT_SYNTHESIS requires traceable human and AI contribution parents")
        self._records[record.record_id] = record

    def get(self, record_id: str) -> ContributionRecord:
        try:
            return self._records[record_id]
        except KeyError as exc:
            raise ProvenanceError(f"unknown record_id: {record_id}") from exc

    def audit(self, record_id: str) -> ProvenanceAudit:
        record = self.get(record_id)
        reasons: list[str] = ["PROVENANCE_IS_NOT_TRUTH"]
        if record.actor is not ContributionActor.SOURCE_UNVERIFIED:
            reasons.append(f"CONTRIBUTOR_ACTOR:{record.actor.value}")
        if record.origin is ContributionOrigin.AI_FORMALIZATION:
            reasons.append("AI_FORMALIZATION_PRESERVES_SPECIFIC_ACTOR")
        human_origin_admissible = record.origin is ContributionOrigin.HUMAN_ORIGIN and bool(record.source_refs)
        externally_sourced = record.origin is ContributionOrigin.EXTERNAL_SOURCE and bool(record.source_refs)
        joint_synthesis_admissible = False

        if record.origin is ContributionOrigin.JOINT_SYNTHESIS:
            origins = {self._records[parent].origin for parent in record.parent_ids}
            joint_synthesis_admissible = (
                (ContributionOrigin.HUMAN_ORIGIN in origins or ContributionOrigin.JOINT_SYNTHESIS in origins)
                and (ContributionOrigin.AI_FORMALIZATION in origins or ContributionOrigin.JOINT_SYNTHESIS in origins)
            )
            reasons.append("JOINT_SYNTHESIS_PRESERVES_PARENT_ORIGINS")

        if record.origin is ContributionOrigin.UNKNOWN:
            reasons.append("UNKNOWN_ORIGIN_FAILS_CLOSED")
        if record.state_attribution is StateAttribution.INFERRED:
            reasons.append("INFERRED_STATE_IS_NOT_SELF_REPORT")
        if record.state_attribution is StateAttribution.OBSERVED_SIGNAL_ONLY:
            reasons.append("OBSERVED_SIGNAL_DOES_NOT_ESTABLISH_INTERNAL_STATE")
        if record.state_attribution is StateAttribution.SELF_REPORTED:
            reasons.append("SELF_REPORT_IS_ATTRIBUTED_REPORT_NOT_INDEPENDENT_MEASUREMENT")

        return ProvenanceAudit(
            record_id=record.record_id,
            actor=record.actor,
            structurally_valid=True,
            human_origin_admissible=human_origin_admissible,
            externally_sourced=externally_sourced,
            joint_synthesis_admissible=joint_synthesis_admissible,
            reasons=tuple(reasons),
        )

    def records(self) -> tuple[ContributionRecord, ...]:
        return tuple(self._records.values())
