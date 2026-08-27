from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .canonical import canonical_hash


class CompetingExplanationKind(str, Enum):
    A_PROMPT_PRIMING = "A_PROMPT_PRIMING"
    B_TOKEN_LEVEL_IMITATION = "B_TOKEN_LEVEL_IMITATION"
    C_REWARD_OPTIMIZATION = "C_REWARD_OPTIMIZATION"
    D_MEMORY_CONFOUND = "D_MEMORY_CONFOUND"
    E_CANDIDATE_GENERATION_VARIATION = "E_CANDIDATE_GENERATION_VARIATION"
    F_PROVIDER_OR_MODEL_VARIATION = "F_PROVIDER_OR_MODEL_VARIATION"
    G_STALE_OR_CONTAMINATED_STATE = "G_STALE_OR_CONTAMINATED_STATE"


@dataclass(frozen=True, slots=True)
class CompetingExplanation:
    explanation_id: str
    kind: CompetingExplanationKind
    statement: str
    discriminating_evidence: tuple[str, ...]
    status: str = "UNRESOLVED"

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class MechanismHypothesis:
    hypothesis_id: str
    question: str
    what_was_observed: str
    proposed_mechanism: str
    predictions: tuple[str, ...]
    competing_explanations: tuple[CompetingExplanation, ...]
    unresolved_alternatives: tuple[str, ...]
    what_is_not_established: tuple[str, ...]
    next_bounded_test: str
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.hypothesis_id.strip() or not self.question.strip():
            raise ValueError("hypothesis id and question are required")
        if not self.competing_explanations:
            raise ValueError("at least one competing explanation is required")
        if self.scientific_disposition != "HOLD" or self.canonical_effect != "NONE":
            raise ValueError("triadic hypotheses remain non-canonical HOLD research candidates")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


def default_competing_explanations(prefix: str = "ALT") -> tuple[CompetingExplanation, ...]:
    definitions = (
        (CompetingExplanationKind.A_PROMPT_PRIMING, "Prompt priming rather than persistent internal state explains the effect.", ("matched prompt fingerprint", "prompt-removal control")),
        (CompetingExplanationKind.B_TOKEN_LEVEL_IMITATION, "Token-level imitation produces the appearance of state-sensitive behavior.", ("replay", "counterfactual state swap")),
        (CompetingExplanationKind.C_REWARD_OPTIMIZATION, "Reward specification alone explains the observed selection.", ("matched reward fingerprint", "reward-preserving intervention")),
        (CompetingExplanationKind.D_MEMORY_CONFOUND, "Retrieved memory differences explain the result.", ("matched memory manifest",)),
        (CompetingExplanationKind.E_CANDIDATE_GENERATION_VARIATION, "Candidate generation variation is mistaken for state-sensitive selection.", ("fixed candidate universe", "permutation check")),
        (CompetingExplanationKind.F_PROVIDER_OR_MODEL_VARIATION, "Provider/model variation overwhelms the state effect.", ("cross-provider replication",)),
        (CompetingExplanationKind.G_STALE_OR_CONTAMINATED_STATE, "Stale or contaminated state better explains the result.", ("stale-state control", "history reset/restore")),
    )
    return tuple(CompetingExplanation(f"{prefix}-{index}", kind, statement, evidence) for index, (kind, statement, evidence) in enumerate(definitions, 1))
