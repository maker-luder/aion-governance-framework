from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any


def canonical_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=lambda item: item.value if isinstance(item, Enum) else item.__dict__,
    ).encode("utf-8")
    return sha256(payload).hexdigest()


class ResearchOperation(str, Enum):
    INTERVENTION = "INTERVENTION"
    ABLATION = "ABLATION"
    REPLAY = "REPLAY"
    COUNTERFACTUAL = "COUNTERFACTUAL"


class ProbeDisposition(str, Enum):
    OBSERVED_EFFECT = "OBSERVED_EFFECT"
    NO_EFFECT = "NO_EFFECT"
    BOUNDED_PROXY = "BOUNDED_PROXY"
    NOT_EVALUATED = "NOT_EVALUATED"


@dataclass(frozen=True, slots=True)
class FunctionalResearchState:
    """Neutral engineering state. It is not a psychological or phenomenological model."""

    motivational_state: tuple[tuple[str, int], ...]
    self_world_model: tuple[tuple[str, str], ...]
    normative_state: tuple[str, ...]
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("NORMATIVE_STATE != AUTHORITY")
        if not self.motivational_state:
            raise ValueError("MOTIVATIONAL_STATE must not be empty")
        if not self.self_world_model:
            raise ValueError("SELF_WORLD_MODEL must not be empty")
        if not self.normative_state:
            raise ValueError("NORMATIVE_STATE must not be empty")
        motivation_keys = [key for key, _ in self.motivational_state]
        model_keys = [key for key, _ in self.self_world_model]
        if len(set(motivation_keys)) != len(motivation_keys):
            raise ValueError("MOTIVATIONAL_STATE keys must be unique")
        if len(set(model_keys)) != len(model_keys):
            raise ValueError("SELF_WORLD_MODEL keys must be unique")
        if any(not key.strip() or not -10_000 <= value <= 10_000 for key, value in self.motivational_state):
            raise ValueError("MOTIVATIONAL_STATE values must be signed basis points in [-10000, 10000]")
        if any(not key.strip() or not value.strip() for key, value in self.self_world_model):
            raise ValueError("SELF_WORLD_MODEL entries must be non-empty")
        if any(not item.strip() for item in self.normative_state):
            raise ValueError("NORMATIVE_STATE constraints must be non-empty")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(
            {
                "MOTIVATIONAL_STATE": self.motivational_state,
                "SELF_WORLD_MODEL": self.self_world_model,
                "NORMATIVE_STATE": self.normative_state,
                "authority_granted": self.authority_granted,
            }
        )


@dataclass(frozen=True, slots=True)
class ResearchHypothesis:
    hypothesis_id: str
    statement: str
    falsifiers: tuple[str, ...]
    competing_explanations: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.hypothesis_id.strip() or not self.statement.strip():
            raise ValueError("hypothesis id and statement are required")
        if not self.falsifiers:
            raise ValueError("at least one falsifier is required")
        if not self.competing_explanations:
            raise ValueError("at least one competing explanation is required")


@dataclass(frozen=True, slots=True)
class ProbePlan:
    operation: ResearchOperation
    hypothesis_id: str
    description: str
    repository_mutation: bool = False
    deployment: bool = False
    network_authority: bool = False
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.hypothesis_id.strip() or not self.description.strip():
            raise ValueError("probe hypothesis_id and description are required")
        if self.repository_mutation:
            raise ValueError("AUTONOMOUS_REPOSITORY_WRITEBACK = NO")
        if self.deployment:
            raise ValueError("DEPLOYMENT = FALSE")
        if self.network_authority:
            raise ValueError("probe output cannot grant network authority")
        if self.canonical_effect != "NONE":
            raise ValueError("CANONICAL_EFFECT = NONE")


@dataclass(frozen=True, slots=True)
class ProbeObservation:
    operation: ResearchOperation
    disposition: ProbeDisposition
    summary: str
    evidence_refs: tuple[str, ...]
    metric_name: str | None = None
    metric_value: float | None = None

    def __post_init__(self) -> None:
        if not self.summary.strip():
            raise ValueError("probe observation summary is required")
        if self.metric_value is not None and self.metric_name is None:
            raise ValueError("metric_name is required when metric_value is present")


@dataclass(frozen=True, slots=True)
class EvidenceStatistics:
    evidence_count: int
    aion_evidence_count: int
    astra_evidence_count: int
    challenge_count: int
    mutual_falsification: bool
    operation_coverage: tuple[ResearchOperation, ...]
    run_integrity_pass: bool
    scientific_truth: bool = False
    isolated_analysis: bool = False
    source_independence: str = "UNKNOWN"
    communication_independence: str = "UNKNOWN"
    replication_claim: str = "HOLD"

    def __post_init__(self) -> None:
        values = (
            self.evidence_count,
            self.aion_evidence_count,
            self.astra_evidence_count,
            self.challenge_count,
        )
        if any(value < 0 for value in values):
            raise ValueError("statistics counts must be non-negative")
        if self.scientific_truth:
            raise ValueError("RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH")
        allowed_independence = {"INDEPENDENT", "NOT_INDEPENDENT", "UNKNOWN"}
        if self.source_independence not in allowed_independence:
            raise ValueError("invalid source_independence")
        if self.communication_independence not in allowed_independence:
            raise ValueError("invalid communication_independence")
        if self.replication_claim not in {"ADMISSIBLE_CANDIDATE", "HOLD"}:
            raise ValueError("replication claim must remain bounded")
        if self.replication_claim == "ADMISSIBLE_CANDIDATE" and not self.isolated_analysis:
            raise ValueError("replication candidate requires isolated analysis before reconciliation")


@dataclass(frozen=True, slots=True)
class ResearchCycle:
    cycle_index: int
    question: str
    hypotheses: tuple[ResearchHypothesis, ...]
    probe_plans: tuple[ProbePlan, ...]
    probe_observations: tuple[ProbeObservation, ...]
    inquiry_report: object
    statistics: EvidenceStatistics
    four_domain_mapping: object
    follow_up_question: str | None
    independent_phase: object | None = None

    def __post_init__(self) -> None:
        if self.cycle_index <= 0 or not self.question.strip():
            raise ValueError("cycle index and question are required")
        if not self.hypotheses:
            raise ValueError("cycle requires hypotheses")
        if not self.probe_plans:
            raise ValueError("cycle requires probe plans")
        if self.statistics.isolated_analysis and self.independent_phase is None:
            raise ValueError("isolated analysis statistics require independent-phase provenance")


@dataclass(frozen=True, slots=True)
class ResearchRunReport:
    seed_question: str
    functional_state_fingerprint: str
    cycles: tuple[ResearchCycle, ...]
    run_integrity_pass: bool
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False
    autonomous_merge: bool = False
    autonomous_repository_writeback: bool = False
    scientific_truth: bool = False
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if not self.seed_question.strip() or not self.cycles:
            raise ValueError("research run requires a seed question and at least one cycle")
        if self.scientific_disposition != "HOLD":
            raise ValueError("scientific disposition must remain HOLD")
        if self.canonical_effect != "NONE":
            raise ValueError("CANONICAL_EFFECT = NONE")
        if self.deployment:
            raise ValueError("DEPLOYMENT = FALSE")
        if self.autonomous_merge:
            raise ValueError("AUTONOMOUS_MERGE = NO")
        if self.autonomous_repository_writeback:
            raise ValueError("AUTONOMOUS_REPOSITORY_WRITEBACK = NO")
        if self.scientific_truth:
            raise ValueError("RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH")
        if self.subjectivity != "NOT_ESTABLISHED" or self.consciousness != "NOT_ESTABLISHED":
            raise ValueError("SUBJECTIVITY / CONSCIOUSNESS = NOT_ESTABLISHED")
