from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Any

from aion_triadic_state import FourDomainOutput, canonical_hash, canonical_value


class CampaignStage(str, Enum):
    QUESTION_POOL = "QUESTION_POOL"
    QUESTION_SELECTION = "QUESTION_SELECTION"
    FOUR_DOMAIN_MAPPING = "FOUR_DOMAIN_MAPPING"
    HYPOTHESIS_REGISTRATION = "HYPOTHESIS_REGISTRATION"
    COMPETING_EXPLANATIONS = "COMPETING_EXPLANATIONS"
    EXPERIMENT_PLANNING = "EXPERIMENT_PLANNING"
    GOVERNANCE_ADMISSION = "GOVERNANCE_ADMISSION"
    BOUNDED_EXECUTION = "BOUNDED_EXECUTION"
    INDEPENDENT_AION_INTERPRETATION = "INDEPENDENT_AION_INTERPRETATION"
    INDEPENDENT_ASTRA_INTERPRETATION = "INDEPENDENT_ASTRA_INTERPRETATION"
    ADVERSARIAL_REVIEW = "ADVERSARIAL_REVIEW"
    COUNTERFACTUAL_OR_FALSIFIER = "COUNTERFACTUAL_OR_FALSIFIER"
    STATISTICAL_SUMMARY = "STATISTICAL_SUMMARY"
    FOUR_DOMAIN_INTERPRETATION = "FOUR_DOMAIN_INTERPRETATION"
    GOVERNANCE_DISPOSITION = "GOVERNANCE_DISPOSITION"
    FOLLOW_UP_GENERATION = "FOLLOW_UP_GENERATION"
    NEXT_BOUNDED_ITERATION = "NEXT_BOUNDED_ITERATION"


class AgendaKind(str, Enum):
    UNRESOLVED_GAP = "UNRESOLVED_GAP"
    CONTRADICTION = "CONTRADICTION"
    FAILED_REPLICATION = "FAILED_REPLICATION"
    UNTESTED_FALSIFIER = "UNTESTED_FALSIFIER"
    CONFOUND = "CONFOUND"
    FOLLOW_UP = "FOLLOW_UP"


class PeerRole(str, Enum):
    PROPOSER = "PROPOSER"
    FALSIFIER = "FALSIFIER"


class RunIntegrity(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    REJECT = "REJECT"


class MechanismStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    CHALLENGED = "CHALLENGED"
    INCONCLUSIVE = "INCONCLUSIVE"
    NOT_EVALUATED = "NOT_EVALUATED"


class ScientificDisposition(str, Enum):
    HOLD = "HOLD"
    REJECT = "REJECT"


@dataclass(frozen=True, slots=True)
class CampaignLimits:
    max_questions: int = 3
    max_experiments_per_question: int = 6
    max_peer_rounds: int = 2
    max_external_queries: int = 0
    max_evidence_items: int = 20
    max_seeds: int = 3
    max_follow_up_depth: int = 1
    max_total_campaign_steps: int = 200

    def __post_init__(self) -> None:
        bounds = {
            "max_questions": (self.max_questions, 1, 20),
            "max_experiments_per_question": (self.max_experiments_per_question, 1, 20),
            "max_peer_rounds": (self.max_peer_rounds, 1, 12),
            "max_external_queries": (self.max_external_queries, 0, 50),
            "max_evidence_items": (self.max_evidence_items, 1, 100),
            "max_seeds": (self.max_seeds, 1, 50),
            "max_follow_up_depth": (self.max_follow_up_depth, 0, 5),
            "max_total_campaign_steps": (self.max_total_campaign_steps, 1, 1_000),
        }
        for name, (value, minimum, maximum) in bounds.items():
            if not minimum <= value <= maximum:
                raise ValueError(f"{name} must be between {minimum} and {maximum}")


@dataclass(frozen=True, slots=True)
class AgendaScore:
    epistemic_value: int
    falsifiability: int
    expected_information_gain: int
    cost: int
    risk: int

    def __post_init__(self) -> None:
        if min(self.epistemic_value, self.falsifiability, self.expected_information_gain, self.cost, self.risk) <= 0:
            raise ValueError("agenda score components must be positive integers")

    @property
    def exact(self) -> Fraction:
        return Fraction(
            self.epistemic_value * self.falsifiability * self.expected_information_gain,
            self.cost * self.risk,
        )

    def to_record(self) -> dict[str, int | str]:
        return {
            "epistemic_value": self.epistemic_value,
            "falsifiability": self.falsifiability,
            "expected_information_gain": self.expected_information_gain,
            "cost": self.cost,
            "risk": self.risk,
            "score_numerator": self.exact.numerator,
            "score_denominator": self.exact.denominator,
            "score_exact": f"{self.exact.numerator}/{self.exact.denominator}",
        }


@dataclass(frozen=True, slots=True)
class AgendaEntry:
    question_id: str
    question: str
    kind: AgendaKind
    score: AgendaScore
    source_refs: tuple[str, ...]
    depth: int = 0

    def __post_init__(self) -> None:
        if not self.question_id.strip() or not self.question.strip():
            raise ValueError("agenda entry identifiers and question must not be empty")
        if self.depth < 0:
            raise ValueError("agenda depth must be non-negative")


@dataclass(frozen=True, slots=True)
class RoleAssignment:
    round_index: int
    aion_role: PeerRole
    astra_role: PeerRole
    aion_provider: str
    astra_provider: str
    shared_public_transcript: bool = True
    shared_admitted_evidence: bool = True
    shared_identity: bool = False

    def __post_init__(self) -> None:
        if self.round_index < 1:
            raise ValueError("round_index must be positive")
        if self.aion_role is self.astra_role:
            raise ValueError("AION and Astra must hold complementary roles")
        if not self.aion_provider.strip() or not self.astra_provider.strip():
            raise ValueError("both provider identities are required")
        if self.aion_provider == self.astra_provider:
            raise ValueError("AION_PROVIDER must differ from ASTRA_PROVIDER")
        if self.shared_identity:
            raise ValueError("AION and Astra may not share identity")


def rotating_roles(round_index: int) -> RoleAssignment:
    odd = round_index % 2 == 1
    return RoleAssignment(
        round_index=round_index,
        aion_role=PeerRole.PROPOSER if odd else PeerRole.FALSIFIER,
        astra_role=PeerRole.FALSIFIER if odd else PeerRole.PROPOSER,
        aion_provider="deterministic-provider:AION",
        astra_provider="deterministic-provider:ASTRA",
    )


@dataclass(frozen=True, slots=True)
class StageEvent:
    sequence: int
    stage: CampaignStage
    question_id: str
    detail: str
    previous_hash: str
    event_hash: str


def append_stage_event(
    events: list[StageEvent], stage: CampaignStage, question_id: str, detail: str
) -> StageEvent:
    previous = "GENESIS" if not events else events[-1].event_hash
    payload = {
        "sequence": len(events) + 1,
        "stage": stage.value,
        "question_id": question_id,
        "detail": detail,
        "previous_hash": previous,
    }
    event = StageEvent(len(events) + 1, stage, question_id, detail, previous, canonical_hash(payload))
    events.append(event)
    return event


def verify_stage_chain(events: tuple[StageEvent, ...]) -> bool:
    previous = "GENESIS"
    for index, event in enumerate(events, 1):
        payload = {
            "sequence": event.sequence,
            "stage": event.stage.value,
            "question_id": event.question_id,
            "detail": event.detail,
            "previous_hash": event.previous_hash,
        }
        if event.sequence != index or event.previous_hash != previous or event.event_hash != canonical_hash(payload):
            return False
        previous = event.event_hash
    return True


@dataclass(frozen=True, slots=True)
class PeerInterpretation:
    peer: str
    role: PeerRole
    opaque_condition_label: str
    observation: str
    mechanism_assessment: str
    challenge: str
    evidence_refs: tuple[str, ...]
    private_state_ref: str


@dataclass(frozen=True, slots=True)
class GovernanceDecision:
    run_integrity: RunIntegrity
    mechanism_status: MechanismStatus
    scientific_disposition: ScientificDisposition
    reasons: tuple[str, ...]
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.reasons:
            raise ValueError("governance decision requires reasons")
        if self.canonical_effect != "NONE":
            raise ValueError("autonomous governance cannot create canonical effect")
        if self.scientific_disposition not in {ScientificDisposition.HOLD, ScientificDisposition.REJECT}:
            raise ValueError("scientific truth promotion is not available")


@dataclass(frozen=True, slots=True)
class ResearchIterationReport:
    iteration_id: str
    question: AgendaEntry
    role_assignments: tuple[RoleAssignment, ...]
    blinded_mapping_hash: str
    mapping_revealed_after_interpretations: bool
    interpretations: tuple[PeerInterpretation, ...]
    experiment_manifest_fingerprints: tuple[str, ...]
    probe_receipt_hashes: tuple[str, ...]
    metrics: dict[str, Any]
    competing_explanations: tuple[dict[str, Any], ...]
    falsifier_results: tuple[dict[str, str], ...]
    four_domain: FourDomainOutput
    governance: GovernanceDecision
    evidence_refs: tuple[str, ...]
    follow_up_questions: tuple[str, ...]
    transcript_chain_hash: str


@dataclass(frozen=True, slots=True)
class CampaignReport:
    campaign_id: str
    repository_ref: str
    limits: CampaignLimits
    agenda: tuple[AgendaEntry, ...]
    iterations: tuple[ResearchIterationReport, ...]
    stage_events: tuple[StageEvent, ...]
    stop_reason: str
    external_web_enabled: bool
    external_queries_used: int
    run_integrity: RunIntegrity
    scientific_disposition: ScientificDisposition = ScientificDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False
    live_model_execution: bool = False
    autonomous_external_write: bool = False
    autonomous_authority_escalation: bool = False

    def __post_init__(self) -> None:
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("campaign cannot create canonical or deployment effect")
        if self.live_model_execution or self.autonomous_external_write or self.autonomous_authority_escalation:
            raise ValueError("campaign authority boundary violated")
        if len(self.iterations) > self.limits.max_questions:
            raise ValueError("campaign exceeded maximum questions")
        if len(self.stage_events) > self.limits.max_total_campaign_steps:
            raise ValueError("campaign exceeded total step budget")

    @property
    def final_chain_hash(self) -> str:
        return "GENESIS" if not self.stage_events else self.stage_events[-1].event_hash

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)

    def to_record(self) -> dict[str, Any]:
        record = canonical_value(self)
        record["schema_version"] = "0.1.0"
        record["agenda"] = [
            {
                **canonical_value(entry),
                "rank": rank,
                "score": entry.score.to_record(),
            }
            for rank, entry in enumerate(self.agenda, 1)
        ]
        record["final_chain_hash"] = self.final_chain_hash
        record["fingerprint"] = self.fingerprint
        record["boundaries"] = {
            "autonomous_canonical_truth": "NO",
            "autonomous_authority_escalation": "NO",
            "autonomous_secret_access": "NO",
            "autonomous_external_write": "NO",
            "autonomous_deployment": "NO",
            "autonomous_merge": "NO",
            "human_authority_boundary": "REQUIRED",
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "consciousness_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
        }
        return record
