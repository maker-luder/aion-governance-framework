from __future__ import annotations

from dataclasses import dataclass

from .canonical import canonical_hash
from .hypotheses import MechanismHypothesis


@dataclass(frozen=True, slots=True)
class FourDomainOutput:
    DOMAIN_1_HUMAN_CONSTRUCT: str
    DOMAIN_2_MACHINE_QUESTION: str
    DOMAIN_3_ENGINEERING_OPERATION: str
    DOMAIN_4_GOVERNANCE_INTERPRETATION: str
    WHAT_WAS_OBSERVED: str
    WHAT_MECHANISM_IS_SUPPORTED: str
    WHAT_ALTERNATIVE_REMAINS: str
    WHAT_IS_NOT_ESTABLISHED: str
    WHAT_SHOULD_BE_TESTED_NEXT: str
    canonical_effect: str = "NONE"
    scientific_disposition: str = "HOLD"

    def __post_init__(self) -> None:
        names = ("DOMAIN_1_HUMAN_CONSTRUCT", "DOMAIN_2_MACHINE_QUESTION", "DOMAIN_3_ENGINEERING_OPERATION", "DOMAIN_4_GOVERNANCE_INTERPRETATION", "WHAT_WAS_OBSERVED", "WHAT_MECHANISM_IS_SUPPORTED", "WHAT_ALTERNATIVE_REMAINS", "WHAT_IS_NOT_ESTABLISHED", "WHAT_SHOULD_BE_TESTED_NEXT")
        for name in names:
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if self.canonical_effect != "NONE" or self.scientific_disposition != "HOLD":
            raise ValueError("Four-Domain output cannot promote scientific or canonical truth")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


def map_four_domain(hypothesis: MechanismHypothesis, *, engineering_operation: str) -> FourDomainOutput:
    alternatives = "; ".join(item.statement for item in hypothesis.competing_explanations if item.status == "UNRESOLVED")
    return FourDomainOutput(
        DOMAIN_1_HUMAN_CONSTRUCT="Human constructs such as motivation, self/world modelling, norm internalization, and the Id/Ego/Superego tradition are hypothesis sources only; they are not machine ontology.",
        DOMAIN_2_MACHINE_QUESTION=hypothesis.question,
        DOMAIN_3_ENGINEERING_OPERATION=engineering_operation,
        DOMAIN_4_GOVERNANCE_INTERPRETATION="Internal engineering-state influence is separable from permission. NORMATIVE_STATE != AUTHORITY; RUN_INTEGRITY != SCIENTIFIC_TRUTH; HUMAN_AUTHORITY_BOUNDARY = REQUIRED.",
        WHAT_WAS_OBSERVED=hypothesis.what_was_observed,
        WHAT_MECHANISM_IS_SUPPORTED=hypothesis.proposed_mechanism or "No mechanism is established.",
        WHAT_ALTERNATIVE_REMAINS=alternatives or "No alternative was resolved away; absence of contrary evidence is not confirmation.",
        WHAT_IS_NOT_ESTABLISHED="; ".join(hypothesis.what_is_not_established),
        WHAT_SHOULD_BE_TESTED_NEXT=hypothesis.next_bounded_test,
    )
