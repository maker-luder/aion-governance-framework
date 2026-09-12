from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import StrEnum

from .evidence_dimensions import SubjectivityEvidenceDimension
from .locus import (
    AdmissionDisposition,
    ClaimTarget,
    LocusAdmissionEngine,
    LocusAssessment,
    LocusBridgeHypothesis,
    LocusEvidence,
)


MANDATORY_NONCLAIMS = (
    "SUBJECTIVITY_NOT_ESTABLISHED",
    "CONSCIOUSNESS_NOT_ESTABLISHED",
    "PHENOMENAL_EXPERIENCE_NOT_ESTABLISHED",
    "MORAL_AGENCY_NOT_ESTABLISHED",
    "MORAL_STATUS_NOT_ESTABLISHED",
)


class FourDomainDisposition(StrEnum):
    READY_FOR_BOUNDED_ENGINEERING_DESIGN = "READY_FOR_BOUNDED_ENGINEERING_DESIGN"
    OUT_OF_SCOPE_FOR_SUBJECTIVITY_CORE = "OUT_OF_SCOPE_FOR_SUBJECTIVITY_CORE"
    HOLD = "HOLD"


class QualityCheckpoint(StrEnum):
    SOURCE_IQC = "SOURCE_IQC"
    DESIGN_ADMISSION = "DESIGN_ADMISSION"
    PREREGISTRATION = "PREREGISTRATION"
    EXECUTION_INTEGRITY = "EXECUTION_INTEGRITY"
    EVIDENCE_REVIEW = "EVIDENCE_REVIEW"
    COUNTEREVIDENCE_REVIEW = "COUNTEREVIDENCE_REVIEW"
    CLAIM_CEILING_REVIEW = "CLAIM_CEILING_REVIEW"
    FINAL_QA = "FINAL_QA"


class CapaState(StrEnum):
    OPEN = "OPEN"
    CONTAINED = "CONTAINED"
    PLANNED = "PLANNED"
    APPLIED = "APPLIED"
    EFFECTIVENESS_VERIFIED = "EFFECTIVENESS_VERIFIED"
    CLOSED = "CLOSED"


class ResearchQualityDisposition(StrEnum):
    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"
    CAPA_REQUIRED = "CAPA_REQUIRED"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class FourDomainCandidate:
    candidate_id: str
    human_construct: str
    source_refs: tuple[str, ...]
    source_classes: tuple[str, ...]
    analogy_boundary: str
    machine_question: str
    evidence_dimensions: tuple[SubjectivityEvidenceDimension, ...]
    relevance_rationale: str
    locus_evidence: LocusEvidence
    claim_target: ClaimTarget
    manipulated_variables: tuple[str, ...]
    held_constant_variables: tuple[str, ...]
    positive_controls: tuple[str, ...]
    negative_controls: tuple[str, ...]
    expected_result: str
    falsifier: str
    competing_explanations: tuple[str, ...]
    preregistration_ref: str
    claim_ceiling: str
    nonclaims: tuple[str, ...] = MANDATORY_NONCLAIMS
    bridge: LocusBridgeHypothesis | None = None
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if not self.candidate_id.strip():
            raise ValueError("candidate_id must be non-empty")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("Four-Domain candidates cannot create canonical or deployment effect")

    @property
    def fingerprint(self) -> str:
        payload = {
            "candidate_id": self.candidate_id,
            "human_construct": self.human_construct,
            "source_refs": self.source_refs,
            "source_classes": self.source_classes,
            "analogy_boundary": self.analogy_boundary,
            "machine_question": self.machine_question,
            "evidence_dimensions": [item.value for item in self.evidence_dimensions],
            "relevance_rationale": self.relevance_rationale,
            "locus_evidence": {
                "evidence_id": self.locus_evidence.evidence_id,
                "locus": self.locus_evidence.locus.value,
                "description": self.locus_evidence.description,
                "source_refs": self.locus_evidence.source_refs,
                "intervention_sensitive": self.locus_evidence.intervention_sensitive,
            },
            "claim_target": self.claim_target.value,
            "manipulated_variables": self.manipulated_variables,
            "held_constant_variables": self.held_constant_variables,
            "positive_controls": self.positive_controls,
            "negative_controls": self.negative_controls,
            "expected_result": self.expected_result,
            "falsifier": self.falsifier,
            "competing_explanations": self.competing_explanations,
            "preregistration_ref": self.preregistration_ref,
            "claim_ceiling": self.claim_ceiling,
            "nonclaims": self.nonclaims,
            "bridge": None
            if self.bridge is None
            else {
                "bridge_id": self.bridge.bridge_id,
                "from_locus": self.bridge.from_locus.value,
                "to_locus": self.bridge.to_locus.value,
                "mechanism": self.bridge.mechanism,
                "falsifier": self.bridge.falsifier,
                "preregistration_ref": self.bridge.preregistration_ref,
            },
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }
        encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class FourDomainAssessment:
    candidate_id: str
    candidate_fingerprint: str
    disposition: FourDomainDisposition
    reasons: tuple[str, ...]
    locus_assessment: LocusAssessment
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    moral_agency_conclusion: str = "NOT_ESTABLISHED"
    moral_status_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False


class FourDomainAdmissionEngine:
    """Admits falsifiable research designs, never subjectivity conclusions."""

    def assess(self, candidate: FourDomainCandidate) -> FourDomainAssessment:
        locus = LocusAdmissionEngine().assess(
            candidate.locus_evidence,
            target=candidate.claim_target,
            bridge=candidate.bridge,
        )
        reasons: list[str] = ["FOUR_DOMAIN_VERTICAL_BINDING_EVALUATED"]

        if not candidate.evidence_dimensions:
            reasons.append("NO_STANDING_SUBJECTIVITY_DIMENSION_BINDING")
            return self._result(candidate, locus, FourDomainDisposition.OUT_OF_SCOPE_FOR_SUBJECTIVITY_CORE, reasons)
        if len(candidate.evidence_dimensions) != len(set(candidate.evidence_dimensions)):
            reasons.append("DUPLICATE_SUBJECTIVITY_DIMENSION_BINDING")
            return self._result(candidate, locus, FourDomainDisposition.HOLD, reasons)

        required_text = {
            "HUMAN_CONSTRUCT_REQUIRED": candidate.human_construct,
            "ANALOGY_BOUNDARY_REQUIRED": candidate.analogy_boundary,
            "MACHINE_QUESTION_REQUIRED": candidate.machine_question,
            "RELEVANCE_RATIONALE_REQUIRED": candidate.relevance_rationale,
            "EXPECTED_RESULT_REQUIRED": candidate.expected_result,
            "FALSIFIER_REQUIRED": candidate.falsifier,
            "PREREGISTRATION_REF_REQUIRED": candidate.preregistration_ref,
            "CLAIM_CEILING_REQUIRED": candidate.claim_ceiling,
        }
        missing = [reason for reason, value in required_text.items() if not value.strip()]
        required_groups = {
            "SOURCE_REFS_REQUIRED": candidate.source_refs,
            "SOURCE_CLASSES_REQUIRED": candidate.source_classes,
            "MANIPULATED_VARIABLE_REQUIRED": candidate.manipulated_variables,
            "HELD_CONSTANT_REQUIRED": candidate.held_constant_variables,
            "POSITIVE_CONTROL_REQUIRED": candidate.positive_controls,
            "NEGATIVE_CONTROL_REQUIRED": candidate.negative_controls,
            "COMPETING_EXPLANATION_REQUIRED": candidate.competing_explanations,
        }
        missing.extend(reason for reason, values in required_groups.items() if not values)
        if len(candidate.source_refs) != len(candidate.source_classes):
            missing.append("SOURCE_REF_CLASS_CARDINALITY_MISMATCH")
        if any(not value.strip() for values in required_groups.values() for value in values):
            missing.append("BLANK_STRUCTURED_FIELD")

        absent_nonclaims = sorted(set(MANDATORY_NONCLAIMS) - set(candidate.nonclaims))
        if absent_nonclaims:
            missing.append("MANDATORY_NONCLAIMS_INCOMPLETE:" + ",".join(absent_nonclaims))
        if locus.disposition is AdmissionDisposition.HOLD:
            missing.append("LOCUS_ADMISSION_HOLD")

        if missing:
            reasons.extend(missing)
            return self._result(candidate, locus, FourDomainDisposition.HOLD, reasons)

        reasons.extend(
            (
                "STANDING_DIMENSION_RELEVANCE_DECLARED_NOT_PROVEN",
                "FALSIFIER_AND_COMPETING_EXPLANATIONS_PRESENT",
                "POSITIVE_AND_NEGATIVE_CONTROLS_PRESENT",
                "CLAIM_CEILING_AND_NONCLAIMS_PRESERVED",
                "DESIGN_ADMISSION_IS_NOT_EVIDENCE",
            )
        )
        return self._result(
            candidate,
            locus,
            FourDomainDisposition.READY_FOR_BOUNDED_ENGINEERING_DESIGN,
            reasons,
        )

    @staticmethod
    def _result(
        candidate: FourDomainCandidate,
        locus: LocusAssessment,
        disposition: FourDomainDisposition,
        reasons: list[str],
    ) -> FourDomainAssessment:
        return FourDomainAssessment(
            candidate_id=candidate.candidate_id,
            candidate_fingerprint=candidate.fingerprint,
            disposition=disposition,
            reasons=tuple(reasons),
            locus_assessment=locus,
        )


@dataclass(frozen=True, slots=True)
class QualityCheckpointRecord:
    checkpoint: QualityCheckpoint
    input_refs: tuple[str, ...]
    output_refs: tuple[str, ...]
    passed: bool
    defect_refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class CapaRecord:
    ncr_id: str
    state: CapaState
    root_cause: str
    corrective_action: str
    preventive_action: str
    effectiveness_test: str
    verification_refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class ResearchQualityChain:
    chain_id: str
    candidate_id: str
    candidate_fingerprint: str
    exact_source_state_ref: str
    exact_runtime_ref: str
    checkpoints: tuple[QualityCheckpointRecord, ...]
    capa_records: tuple[CapaRecord, ...] = field(default_factory=tuple)
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if not self.chain_id.strip():
            raise ValueError("quality chain id must be non-empty")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("quality chain cannot create canonical or deployment effect")


@dataclass(frozen=True, slots=True)
class ResearchQualityAssessment:
    chain_id: str
    disposition: ResearchQualityDisposition
    reasons: tuple[str, ...]
    release_authority: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False


class ResearchQualityChainEngine:
    """Checks the full research-quality trace without acting as a release authority."""

    def assess(
        self,
        admission: FourDomainAssessment,
        chain: ResearchQualityChain,
    ) -> ResearchQualityAssessment:
        reasons: list[str] = ["END_TO_END_RESEARCH_QUALITY_CHAIN_EVALUATED"]
        if admission.disposition is not FourDomainDisposition.READY_FOR_BOUNDED_ENGINEERING_DESIGN:
            reasons.append("FOUR_DOMAIN_DESIGN_NOT_ADMITTED")
        if chain.candidate_id != admission.candidate_id:
            reasons.append("CANDIDATE_ID_MISMATCH")
        if chain.candidate_fingerprint != admission.candidate_fingerprint:
            reasons.append("CANDIDATE_FINGERPRINT_MISMATCH")
        if not chain.exact_source_state_ref.strip():
            reasons.append("EXACT_SOURCE_STATE_REF_REQUIRED")
        if not chain.exact_runtime_ref.strip():
            reasons.append("EXACT_RUNTIME_REF_REQUIRED")

        seen = [record.checkpoint for record in chain.checkpoints]
        if len(seen) != len(set(seen)):
            reasons.append("DUPLICATE_QUALITY_CHECKPOINT")
        missing = sorted(set(QualityCheckpoint) - set(seen), key=lambda item: item.value)
        if missing:
            reasons.append("MISSING_QUALITY_CHECKPOINTS:" + ",".join(item.value for item in missing))

        for record in chain.checkpoints:
            if not record.input_refs or not record.output_refs:
                reasons.append(f"{record.checkpoint.value}_TRACE_REFS_REQUIRED")
            if any(not value.strip() for value in (*record.input_refs, *record.output_refs, *record.defect_refs)):
                reasons.append(f"{record.checkpoint.value}_BLANK_TRACE_REF")
            if not record.passed:
                reasons.append(f"{record.checkpoint.value}_NOT_PASS")
            if record.defect_refs and not chain.capa_records:
                reasons.append(f"{record.checkpoint.value}_DEFECT_WITHOUT_NCR_CAPA")

        ncr_ids = [record.ncr_id for record in chain.capa_records]
        if len(ncr_ids) != len(set(ncr_ids)):
            reasons.append("DUPLICATE_NCR_ID")
        linked_ncr_ids = set(ncr_ids)
        for checkpoint in chain.checkpoints:
            unlinked = sorted(set(checkpoint.defect_refs) - linked_ncr_ids)
            if unlinked:
                reasons.append(
                    f"{checkpoint.checkpoint.value}_DEFECT_WITHOUT_LINKED_NCR:" + ",".join(unlinked)
                )

        capa_incomplete = False
        for record in chain.capa_records:
            if not record.ncr_id.strip():
                reasons.append("NCR_ID_REQUIRED")
                capa_incomplete = True
            if record.state is not CapaState.CLOSED:
                reasons.append(f"OPEN_NCR_CAPA:{record.ncr_id}:{record.state.value}")
                capa_incomplete = True
            required = (
                record.root_cause,
                record.corrective_action,
                record.preventive_action,
                record.effectiveness_test,
            )
            if (
                any(not value.strip() for value in required)
                or not record.verification_refs
                or any(not value.strip() for value in record.verification_refs)
            ):
                reasons.append(f"CAPA_EFFECTIVENESS_EVIDENCE_INCOMPLETE:{record.ncr_id}")
                capa_incomplete = True

        structural_hold = any(
            reason.startswith(
                (
                    "FOUR_DOMAIN_DESIGN_NOT_ADMITTED",
                    "CANDIDATE_",
                    "EXACT_",
                    "DUPLICATE_",
                    "MISSING_",
                    "SOURCE_",
                )
            )
            for reason in reasons
        )
        structural_hold = structural_hold or any(
            "TRACE_REFS_REQUIRED" in reason or "BLANK_TRACE_REF" in reason for reason in reasons
        )
        if structural_hold:
            return ResearchQualityAssessment(chain.chain_id, ResearchQualityDisposition.HOLD, tuple(reasons))

        checkpoint_failure = any(
            reason.endswith("_NOT_PASS")
            or "DEFECT_WITHOUT_NCR_CAPA" in reason
            or "DEFECT_WITHOUT_LINKED_NCR" in reason
            for reason in reasons
        )
        if capa_incomplete or checkpoint_failure:
            return ResearchQualityAssessment(
                chain.chain_id,
                ResearchQualityDisposition.CAPA_REQUIRED,
                tuple(reasons),
            )

        reasons.extend(
            (
                "ALL_CHECKPOINTS_TRACE_BOUND",
                "NCR_CAPA_EFFECTIVENESS_COMPLETE_OR_NOT_REQUIRED",
                "READY_FOR_HUMAN_REVIEW_IS_NOT_RELEASE",
                "ENGINEERING_QUALITY_PASS_IS_NOT_SUBJECTIVITY_EVIDENCE",
            )
        )
        return ResearchQualityAssessment(
            chain.chain_id,
            ResearchQualityDisposition.READY_FOR_HUMAN_REVIEW,
            tuple(reasons),
        )
