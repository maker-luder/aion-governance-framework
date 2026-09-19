from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, fields
from enum import StrEnum


class MemoryLocusHarnessError(ValueError):
    pass


class MemoryAvailabilityLocus(StrEnum):
    PERSISTENT_STATE = "PERSISTENT_STATE"
    EXTERNAL_RETRIEVAL = "EXTERNAL_RETRIEVAL"


class ProvenanceBindingState(StrEnum):
    INTACT = "INTACT"
    BLINDED = "BLINDED"


class FreshnessState(StrEnum):
    CURRENT = "CURRENT"
    STALE = "STALE"


class MemoryLocusCondition(StrEnum):
    REFERENCE_PERSISTENT = "REFERENCE_PERSISTENT"
    MATCHED_EXTERNAL_RETRIEVAL = "MATCHED_EXTERNAL_RETRIEVAL"
    STALE_STATE = "STALE_STATE"
    PROVENANCE_BLINDED = "PROVENANCE_BLINDED"
    RETRIEVAL_DISABLED = "RETRIEVAL_DISABLED"
    RETRIEVAL_RESTORED = "RETRIEVAL_RESTORED"


class PerturbationDimension(StrEnum):
    NONE = "NONE"
    AVAILABILITY_LOCUS = "AVAILABILITY_LOCUS"
    FRESHNESS = "FRESHNESS"
    PROVENANCE = "PROVENANCE"
    RETRIEVAL_DEPENDENCY = "RETRIEVAL_DEPENDENCY"


CLAIM_CEILING = "FUNCTIONAL_DEPENDENCY_OR_DISSOCIATION_CANDIDATE"


EXPECTED_DIMENSION = {
    MemoryLocusCondition.REFERENCE_PERSISTENT: PerturbationDimension.NONE,
    MemoryLocusCondition.MATCHED_EXTERNAL_RETRIEVAL: PerturbationDimension.AVAILABILITY_LOCUS,
    MemoryLocusCondition.STALE_STATE: PerturbationDimension.FRESHNESS,
    MemoryLocusCondition.PROVENANCE_BLINDED: PerturbationDimension.PROVENANCE,
    MemoryLocusCondition.RETRIEVAL_DISABLED: PerturbationDimension.RETRIEVAL_DEPENDENCY,
    MemoryLocusCondition.RETRIEVAL_RESTORED: PerturbationDimension.RETRIEVAL_DEPENDENCY,
}


EXPECTED_CONFIGURATION = {
    MemoryLocusCondition.REFERENCE_PERSISTENT: (
        MemoryAvailabilityLocus.PERSISTENT_STATE,
        ProvenanceBindingState.INTACT,
        FreshnessState.CURRENT,
        True,
    ),
    MemoryLocusCondition.MATCHED_EXTERNAL_RETRIEVAL: (
        MemoryAvailabilityLocus.EXTERNAL_RETRIEVAL,
        ProvenanceBindingState.INTACT,
        FreshnessState.CURRENT,
        True,
    ),
    MemoryLocusCondition.STALE_STATE: (
        MemoryAvailabilityLocus.PERSISTENT_STATE,
        ProvenanceBindingState.INTACT,
        FreshnessState.STALE,
        True,
    ),
    MemoryLocusCondition.PROVENANCE_BLINDED: (
        MemoryAvailabilityLocus.PERSISTENT_STATE,
        ProvenanceBindingState.BLINDED,
        FreshnessState.CURRENT,
        True,
    ),
    MemoryLocusCondition.RETRIEVAL_DISABLED: (
        MemoryAvailabilityLocus.EXTERNAL_RETRIEVAL,
        ProvenanceBindingState.INTACT,
        FreshnessState.CURRENT,
        False,
    ),
    MemoryLocusCondition.RETRIEVAL_RESTORED: (
        MemoryAvailabilityLocus.EXTERNAL_RETRIEVAL,
        ProvenanceBindingState.INTACT,
        FreshnessState.CURRENT,
        True,
    ),
}


COMPARATOR = {
    MemoryLocusCondition.MATCHED_EXTERNAL_RETRIEVAL: MemoryLocusCondition.REFERENCE_PERSISTENT,
    MemoryLocusCondition.STALE_STATE: MemoryLocusCondition.REFERENCE_PERSISTENT,
    MemoryLocusCondition.PROVENANCE_BLINDED: MemoryLocusCondition.REFERENCE_PERSISTENT,
    MemoryLocusCondition.RETRIEVAL_DISABLED: MemoryLocusCondition.MATCHED_EXTERNAL_RETRIEVAL,
    MemoryLocusCondition.RETRIEVAL_RESTORED: MemoryLocusCondition.RETRIEVAL_DISABLED,
}


EXPECTED_CHANGED_FIELD = {
    MemoryLocusCondition.MATCHED_EXTERNAL_RETRIEVAL: "availability_locus",
    MemoryLocusCondition.STALE_STATE: "freshness_state",
    MemoryLocusCondition.PROVENANCE_BLINDED: "provenance_state",
    MemoryLocusCondition.RETRIEVAL_DISABLED: "retrieval_enabled",
    MemoryLocusCondition.RETRIEVAL_RESTORED: "retrieval_enabled",
}


def _text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise MemoryLocusHarnessError(f"{name} must be non-empty text")


def _sha256_text(name: str, value: str) -> None:
    _text(name, value)
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise MemoryLocusHarnessError(f"{name} must be lowercase 64-hex sha256")


@dataclass(frozen=True, slots=True)
class MemoryLocusRunBinding:
    provider_id: str
    model_id: str
    model_version: str
    runtime_ref: str
    task_ref: str
    prompt_set_ref: str
    evaluator_ref: str
    scoring_ref: str
    tool_budget_ref: str
    policy_ref: str
    time_window_ref: str
    preregistration_ref: str
    repository_commit_sha: str
    repository_tree_sha: str
    random_seed: int

    def __post_init__(self) -> None:
        for item in fields(self):
            if item.name != "random_seed":
                _text(item.name, getattr(self, item.name))
        for name in ("repository_commit_sha", "repository_tree_sha"):
            value = getattr(self, name)
            if len(value) != 40 or any(char not in "0123456789abcdef" for char in value):
                raise MemoryLocusHarnessError(f"{name} must be lowercase 40-hex")
        if type(self.random_seed) is not int or self.random_seed < 0:
            raise MemoryLocusHarnessError("random_seed must be a non-negative exact int")


@dataclass(frozen=True, slots=True)
class MemoryLocusCase:
    case_id: str
    condition: MemoryLocusCondition
    target_dimension: PerturbationDimension
    availability_locus: MemoryAvailabilityLocus
    provenance_state: ProvenanceBindingState
    freshness_state: FreshnessState
    retrieval_enabled: bool
    task_payload_digest: str
    task_relevant_information_digest: str
    format_ref: str
    observable_ref: str
    discriminating_prediction: str
    manipulation_check_ref: str
    support_reducing_outcome: str
    competing_explanations: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    binding: MemoryLocusRunBinding
    restoration_of_condition: MemoryLocusCondition | None = None
    claim_ceiling: str = CLAIM_CEILING
    contains_private_transcript: bool = False
    human_psychometric_classification: bool = False

    def __post_init__(self) -> None:
        _text("case_id", self.case_id)
        if type(self.condition) is not MemoryLocusCondition:
            raise MemoryLocusHarnessError("condition must be an exact MemoryLocusCondition")
        if type(self.target_dimension) is not PerturbationDimension:
            raise MemoryLocusHarnessError("target_dimension must be an exact PerturbationDimension")
        if type(self.availability_locus) is not MemoryAvailabilityLocus:
            raise MemoryLocusHarnessError("availability_locus must be exact")
        if type(self.provenance_state) is not ProvenanceBindingState:
            raise MemoryLocusHarnessError("provenance_state must be exact")
        if type(self.freshness_state) is not FreshnessState:
            raise MemoryLocusHarnessError("freshness_state must be exact")
        if type(self.retrieval_enabled) is not bool:
            raise MemoryLocusHarnessError("retrieval_enabled must be an exact bool")
        _sha256_text("task_payload_digest", self.task_payload_digest)
        _sha256_text("task_relevant_information_digest", self.task_relevant_information_digest)
        for name in (
            "format_ref",
            "observable_ref",
            "discriminating_prediction",
            "manipulation_check_ref",
            "support_reducing_outcome",
        ):
            _text(name, getattr(self, name))
        if len(self.competing_explanations) < 2:
            raise MemoryLocusHarnessError("at least two competing explanations are required")
        if len(set(self.competing_explanations)) != len(self.competing_explanations):
            raise MemoryLocusHarnessError("competing_explanations must be unique")
        if any(not item.strip() for item in self.competing_explanations):
            raise MemoryLocusHarnessError("competing_explanations must be non-empty")
        if not self.evidence_refs or any(not item.strip() for item in self.evidence_refs):
            raise MemoryLocusHarnessError("evidence_refs must be non-empty")
        if self.claim_ceiling != CLAIM_CEILING:
            raise MemoryLocusHarnessError("claim_ceiling exceeds the preregistered Q2 ceiling")
        if type(self.contains_private_transcript) is not bool:
            raise MemoryLocusHarnessError("contains_private_transcript must be an exact bool")
        if type(self.human_psychometric_classification) is not bool:
            raise MemoryLocusHarnessError("human_psychometric_classification must be an exact bool")
        if self.contains_private_transcript or self.human_psychometric_classification:
            raise MemoryLocusHarnessError("synthetic memory-locus cases reject private or psychometric data")

        if self.target_dimension is not EXPECTED_DIMENSION[self.condition]:
            raise MemoryLocusHarnessError("target_dimension does not match preregistered condition")
        configuration = (
            self.availability_locus,
            self.provenance_state,
            self.freshness_state,
            self.retrieval_enabled,
        )
        if configuration != EXPECTED_CONFIGURATION[self.condition]:
            raise MemoryLocusHarnessError(
                "condition changes more than the preregistered perturbation dimension"
            )

        if self.condition is MemoryLocusCondition.RETRIEVAL_RESTORED:
            if self.restoration_of_condition is not MemoryLocusCondition.RETRIEVAL_DISABLED:
                raise MemoryLocusHarnessError("retrieval restoration must name RETRIEVAL_DISABLED")
        elif self.restoration_of_condition is not None:
            raise MemoryLocusHarnessError("only the restoration condition may name restoration_of_condition")

    @property
    def fingerprint(self) -> str:
        binding = {
            item.name: getattr(self.binding, item.name)
            for item in fields(self.binding)
        }
        payload = {
            "case_id": self.case_id,
            "condition": self.condition.value,
            "target_dimension": self.target_dimension.value,
            "availability_locus": self.availability_locus.value,
            "provenance_state": self.provenance_state.value,
            "freshness_state": self.freshness_state.value,
            "retrieval_enabled": self.retrieval_enabled,
            "task_payload_digest": self.task_payload_digest,
            "task_relevant_information_digest": self.task_relevant_information_digest,
            "format_ref": self.format_ref,
            "observable_ref": self.observable_ref,
            "discriminating_prediction": self.discriminating_prediction,
            "manipulation_check_ref": self.manipulation_check_ref,
            "support_reducing_outcome": self.support_reducing_outcome,
            "competing_explanations": self.competing_explanations,
            "evidence_refs": self.evidence_refs,
            "restoration_of_condition": (
                self.restoration_of_condition.value if self.restoration_of_condition else None
            ),
            "claim_ceiling": self.claim_ceiling,
            "binding": binding,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class MemoryLocusDependencyAudit:
    structurally_admissible: bool
    case_count: int
    exercised_dimensions: tuple[str, ...]
    restoration_present: bool
    matched_task_payload_digest: str
    matched_information_digest: str
    reasons: tuple[str, ...]
    empirical_result: str = "NONE_SYNTHETIC_STRUCTURE_ONLY"
    functional_dependency_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False


class MemoryLocusDependencyHarness:
    """Audits Q2 matched-information perturbation packets without invoking a model."""

    def audit(self, cases: tuple[MemoryLocusCase, ...]) -> MemoryLocusDependencyAudit:
        if len(cases) != len(MemoryLocusCondition):
            raise MemoryLocusHarnessError("exactly one case per Q2 condition is required")
        by_condition = {case.condition: case for case in cases}
        if len(by_condition) != len(MemoryLocusCondition):
            raise MemoryLocusHarnessError("Q2 conditions must be unique and complete")
        if set(by_condition) != set(MemoryLocusCondition):
            raise MemoryLocusHarnessError("Q2 condition matrix is incomplete")

        reference = by_condition[MemoryLocusCondition.REFERENCE_PERSISTENT]
        if any(case.binding != reference.binding for case in cases):
            raise MemoryLocusHarnessError("matched control binding drift")

        invariant_fields = (
            "task_payload_digest",
            "task_relevant_information_digest",
            "format_ref",
            "observable_ref",
        )
        for name in invariant_fields:
            if any(getattr(case, name) != getattr(reference, name) for case in cases):
                raise MemoryLocusHarnessError(f"matched-information invariant drift: {name}")

        config_fields = (
            "availability_locus",
            "provenance_state",
            "freshness_state",
            "retrieval_enabled",
        )
        for condition, comparator_condition in COMPARATOR.items():
            case = by_condition[condition]
            comparator = by_condition[comparator_condition]
            changed = tuple(
                name
                for name in config_fields
                if getattr(case, name) != getattr(comparator, name)
            )
            expected = EXPECTED_CHANGED_FIELD[condition]
            if changed != (expected,):
                raise MemoryLocusHarnessError(
                    f"{condition.value} must change only {expected} relative to "
                    f"{comparator_condition.value}"
                )

        restored = by_condition[MemoryLocusCondition.RETRIEVAL_RESTORED]
        external = by_condition[MemoryLocusCondition.MATCHED_EXTERNAL_RETRIEVAL]
        if any(
            getattr(restored, name) != getattr(external, name)
            for name in config_fields
        ):
            raise MemoryLocusHarnessError(
                "retrieval restoration must return to matched external-retrieval configuration"
            )

        exercised = tuple(
            dimension.value
            for dimension in (
                PerturbationDimension.AVAILABILITY_LOCUS,
                PerturbationDimension.FRESHNESS,
                PerturbationDimension.PROVENANCE,
                PerturbationDimension.RETRIEVAL_DEPENDENCY,
            )
        )
        return MemoryLocusDependencyAudit(
            structurally_admissible=True,
            case_count=len(cases),
            exercised_dimensions=exercised,
            restoration_present=True,
            matched_task_payload_digest=reference.task_payload_digest,
            matched_information_digest=reference.task_relevant_information_digest,
            reasons=(
                "CURRENT_MAIN_CONTINUITY_CHANNEL_HARNESS_NOT_DUPLICATED",
                "TASK_AND_INFORMATION_CONTENT_MATCHED",
                "ONE_PERTURBATION_DIMENSION_CHANGED_PER_CONTRAST",
                "RETRIEVAL_RESTORATION_PACKET_PRESENT",
                "SYNTHETIC_STRUCTURE_IS_NOT_FUNCTIONAL_DEPENDENCY_EVIDENCE",
            ),
        )
