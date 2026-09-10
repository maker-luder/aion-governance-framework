from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from .models import ResearchLot
from .provenance import ContributionOrigin, EpistemicProvenanceLedger, ProvenanceError


class ClaimQualityError(ValueError):
    pass


class ClaimLevel(StrEnum):
    L0_OBSERVATION = "L0_OBSERVATION"
    L1_REPEATABLE_BEHAVIOR = "L1_REPEATABLE_BEHAVIOR"
    L2_STATE_ASSOCIATION = "L2_STATE_ASSOCIATION"
    L3_INTERVENTION_SENSITIVE_MECHANISM = "L3_INTERVENTION_SENSITIVE_MECHANISM"
    L4_ROBUST_REPLICATION = "L4_ROBUST_REPLICATION"
    L5_SUBJECTIVITY_NOT_AUTOMATICALLY_ESTABLISHED = "L5_SUBJECTIVITY_NOT_AUTOMATICALLY_ESTABLISHED"


class ClaimStatus(StrEnum):
    OBSERVED = "OBSERVED"
    WORKING_HYPOTHESIS = "WORKING_HYPOTHESIS"
    RETAINED = "RETAINED"
    REVISED = "REVISED"
    WITHDRAWN = "WITHDRAWN"
    HOLD = "HOLD"


class EvidenceRelation(StrEnum):
    SUPPORTS = "SUPPORTS"
    CHALLENGES = "CHALLENGES"


class PublicationClass(StrEnum):
    PUBLIC_SAFE = "PUBLIC_SAFE"
    SYNTHETIC = "SYNTHETIC"
    PRIVATE_TRANSCRIPT = "PRIVATE_TRANSCRIPT"
    UNKNOWN = "UNKNOWN"


class ClaimAdmissionDisposition(StrEnum):
    ADMISSIBLE_AS_BOUNDED_RESEARCH_RECORD = "ADMISSIBLE_AS_BOUNDED_RESEARCH_RECORD"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class EvidenceBinding:
    evidence_id: str
    provenance_record_id: str
    relation: EvidenceRelation
    publication_class: PublicationClass
    naturalistic_case_id: str = ""
    intervention_sensitive: bool = False
    transfer_candidate: bool = False
    held_out: bool = False
    repeated: bool = False
    comparison_control: bool = False
    independently_scored: bool = False

    def __post_init__(self) -> None:
        if not self.evidence_id.strip() or not self.provenance_record_id.strip():
            raise ClaimQualityError("evidence_id and provenance_record_id must be non-empty")


@dataclass(frozen=True, slots=True)
class ClaimDependency:
    claim_id: str
    version: int

    def __post_init__(self) -> None:
        if not self.claim_id.strip() or self.version < 1:
            raise ClaimQualityError("claim dependency requires a claim_id and positive version")


@dataclass(frozen=True, slots=True)
class ClaimRevision:
    previous_claim_id: str
    previous_version: int
    new_version: int
    changed_fields: tuple[str, ...]
    rationale_ref: str

    def __post_init__(self) -> None:
        if not self.previous_claim_id.strip() or not self.rationale_ref.strip():
            raise ClaimQualityError("revision requires previous_claim_id and rationale_ref")
        if self.previous_version < 1 or self.new_version <= self.previous_version:
            raise ClaimQualityError("revision versions must increase monotonically")
        if not self.changed_fields or any(not item.strip() for item in self.changed_fields):
            raise ClaimQualityError("revision must identify changed fields")


@dataclass(frozen=True, slots=True)
class ResearchClaimRecord:
    claim_id: str
    version: int
    statement: str
    provenance_record_id: str | None
    claim_level: ClaimLevel
    status: ClaimStatus
    observed_evidence_ids: tuple[str, ...]
    inferred_statements: tuple[str, ...]
    competing_explanations: tuple[str, ...]
    falsifier: str
    supporting_evidence_ids: tuple[str, ...]
    publication_class: PublicationClass = PublicationClass.PUBLIC_SAFE
    challenging_evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    resolved_challenge_ids: tuple[str, ...] = field(default_factory=tuple)
    dependencies: tuple[ClaimDependency, ...] = field(default_factory=tuple)
    revision: ClaimRevision | None = None
    population_scope: bool = False
    causal_learning_effect: bool = False
    subjectivity_claim: bool = False
    consciousness_claim: bool = False
    phenomenal_experience_claim: bool = False
    moral_agency_claim: bool = False
    moral_status_claim: bool = False
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.claim_id.strip() or not self.statement.strip():
            raise ClaimQualityError("claim_id and statement must be non-empty")
        if self.version < 1:
            raise ClaimQualityError("claim version must be positive")
        if self.canonical_effect != "NONE":
            raise ClaimQualityError("bounded research claims cannot create canonical effect")
        for values, name in (
            (self.observed_evidence_ids, "observed_evidence_ids"),
            (self.competing_explanations, "competing_explanations"),
            (self.supporting_evidence_ids, "supporting_evidence_ids"),
        ):
            if not values or any(not item.strip() for item in values):
                raise ClaimQualityError(f"{name} must contain non-empty values")
        if not self.falsifier.strip():
            raise ClaimQualityError("falsifier must be non-empty")
        if len(set(self.supporting_evidence_ids)) != len(self.supporting_evidence_ids):
            raise ClaimQualityError("supporting evidence ids must be unique")
        if len(set(self.challenging_evidence_ids)) != len(self.challenging_evidence_ids):
            raise ClaimQualityError("challenging evidence ids must be unique")
        if not set(self.resolved_challenge_ids).issubset(self.challenging_evidence_ids):
            raise ClaimQualityError("resolved challenges must refer to challenging evidence ids")


@dataclass(frozen=True, slots=True)
class ClaimQualityAssessment:
    claim_id: str
    version: int
    disposition: ClaimAdmissionDisposition
    reasons: tuple[str, ...]
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    moral_agency: str = "NOT_ESTABLISHED"
    moral_status: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"


class ProvenanceClaimQualityGate:
    """Connects provenance, evidence, revision and quality without judging truth.

    The gate admits only a bounded research record. It never promotes a claim to
    subjectivity, consciousness, phenomenal experience, moral agency or canonical
    repository state.
    """

    def assess(
        self,
        claim: ResearchClaimRecord,
        *,
        ledger: EpistemicProvenanceLedger,
        lot: ResearchLot,
        evidence_bindings: tuple[EvidenceBinding, ...],
        known_claims: tuple[ResearchClaimRecord, ...] = (),
    ) -> ClaimQualityAssessment:
        failures: list[str] = []
        binding_by_id = {item.evidence_id: item for item in evidence_bindings}
        if len(binding_by_id) != len(evidence_bindings):
            failures.append("DUPLICATE_EVIDENCE_BINDING")

        claim_provenance = self._get_provenance(claim.provenance_record_id, ledger, failures)
        if claim_provenance is not None and claim_provenance.origin is ContributionOrigin.UNKNOWN:
            failures.append("UNKNOWN_CLAIM_ORIGIN")
        if claim.publication_class is PublicationClass.PRIVATE_TRANSCRIPT:
            failures.append("PRIVATE_TRANSCRIPT_CLAIM_NOT_PUBLISHABLE")
        elif claim.publication_class is PublicationClass.UNKNOWN:
            failures.append("UNKNOWN_CLAIM_PUBLICATION_CLASS")

        lot_support_ids = {item.evidence_id for item in lot.evidence}
        lot_challenge_ids = {item.item_id for item in lot.counterevidence}
        required_ids = (
            set(claim.observed_evidence_ids) | set(claim.supporting_evidence_ids) | set(claim.challenging_evidence_ids)
        )
        for evidence_id in sorted(required_ids):
            binding = binding_by_id.get(evidence_id)
            if binding is None:
                failures.append(f"MISSING_EVIDENCE_BINDING:{evidence_id}")
                continue
            provenance = self._get_provenance(binding.provenance_record_id, ledger, failures)
            if provenance is not None and provenance.origin is ContributionOrigin.UNKNOWN:
                failures.append(f"UNKNOWN_EVIDENCE_ORIGIN:{evidence_id}")
            if binding.publication_class is PublicationClass.PRIVATE_TRANSCRIPT:
                failures.append(f"PRIVATE_TRANSCRIPT_NOT_PUBLISHABLE:{evidence_id}")
            elif binding.publication_class is PublicationClass.UNKNOWN:
                failures.append(f"UNKNOWN_PUBLICATION_CLASS:{evidence_id}")

        for evidence_id in claim.supporting_evidence_ids:
            binding = binding_by_id.get(evidence_id)
            if evidence_id not in lot_support_ids:
                failures.append(f"SUPPORT_NOT_IN_QUALITY_LOT:{evidence_id}")
            if binding is not None and binding.relation is not EvidenceRelation.SUPPORTS:
                failures.append(f"SUPPORT_RELATION_MISMATCH:{evidence_id}")

        for evidence_id in claim.observed_evidence_ids:
            if evidence_id not in claim.supporting_evidence_ids:
                failures.append(f"OBSERVATION_NOT_BOUND_AS_SUPPORT:{evidence_id}")

        for evidence_id in claim.challenging_evidence_ids:
            binding = binding_by_id.get(evidence_id)
            if evidence_id not in lot_challenge_ids:
                failures.append(f"CHALLENGE_NOT_IN_QUALITY_LOT:{evidence_id}")
            if binding is not None and binding.relation is not EvidenceRelation.CHALLENGES:
                failures.append(f"CHALLENGE_RELATION_MISMATCH:{evidence_id}")
            if evidence_id not in claim.resolved_challenge_ids:
                failures.append(f"UNRESOLVED_CONTRADICTORY_EVIDENCE:{evidence_id}")

        if lot.canonical_effect != "NONE" or lot.deployment:
            failures.append("QUALITY_LOT_CANNOT_GRANT_CANONICAL_OR_DEPLOYMENT_AUTHORITY")
        if not lot.final_qa_pass:
            failures.append("QUALITY_FACTORY_FINAL_QA_NOT_PASSED")

        self._check_claim_level(claim, binding_by_id, failures)
        self._check_scope_and_transfer(claim, binding_by_id, failures)
        self._check_dependencies_and_revision(claim, known_claims, failures)

        if claim.status in {ClaimStatus.WITHDRAWN, ClaimStatus.HOLD}:
            failures.append(f"CLAIM_STATUS_{claim.status.value}")
        if claim.subjectivity_claim:
            failures.append("SUBJECTIVITY_PROMOTION_PROHIBITED")
        if claim.consciousness_claim:
            failures.append("CONSCIOUSNESS_PROMOTION_PROHIBITED")
        if claim.phenomenal_experience_claim:
            failures.append("PHENOMENAL_EXPERIENCE_PROMOTION_PROHIBITED")
        if claim.moral_agency_claim:
            failures.append("MORAL_AGENCY_PROMOTION_PROHIBITED")
        if claim.moral_status_claim:
            failures.append("MORAL_STATUS_PROMOTION_PROHIBITED")

        reasons = (
            tuple(dict.fromkeys(failures))
            if failures
            else (
                "PROVENANCE_BOUND",
                "OBSERVATION_INFERENCE_HYPOTHESIS_SEPARATED",
                "COMPETING_EXPLANATIONS_AND_FALSIFIER_PRESENT",
                "QUALITY_FACTORY_FINAL_QA_PASSED",
                "ADMISSION_IS_NOT_SCIENTIFIC_VALIDATION",
            )
        )
        disposition = (
            ClaimAdmissionDisposition.HOLD
            if failures
            else ClaimAdmissionDisposition.ADMISSIBLE_AS_BOUNDED_RESEARCH_RECORD
        )
        return ClaimQualityAssessment(
            claim_id=claim.claim_id,
            version=claim.version,
            disposition=disposition,
            reasons=reasons,
        )

    @staticmethod
    def _get_provenance(
        record_id: str | None,
        ledger: EpistemicProvenanceLedger,
        failures: list[str],
    ):
        if record_id is None or not record_id.strip():
            failures.append("MISSING_PROVENANCE")
            return None
        try:
            record = ledger.get(record_id)
            ledger.audit(record_id)
            return record
        except ProvenanceError:
            failures.append(f"INVALID_PROVENANCE:{record_id}")
            return None

    @staticmethod
    def _check_claim_level(
        claim: ResearchClaimRecord,
        bindings: dict[str, EvidenceBinding],
        failures: list[str],
    ) -> None:
        ordered_levels = tuple(ClaimLevel)
        level_index = ordered_levels.index(claim.claim_level)
        supports = tuple(bindings[item] for item in claim.supporting_evidence_ids if item in bindings)
        if level_index >= ordered_levels.index(ClaimLevel.L3_INTERVENTION_SENSITIVE_MECHANISM):
            if not any(item.intervention_sensitive for item in supports):
                failures.append("MECHANISM_PROMOTION_REQUIRES_INTERVENTION_SENSITIVE_EVIDENCE")
        if level_index >= ordered_levels.index(ClaimLevel.L4_ROBUST_REPLICATION):
            qualifying = [item for item in supports if item.repeated and item.held_out]
            if len(qualifying) < 2:
                failures.append("ROBUST_REPLICATION_REQUIRES_REPEATED_HELD_OUT_EVIDENCE")

    @staticmethod
    def _check_scope_and_transfer(
        claim: ResearchClaimRecord,
        bindings: dict[str, EvidenceBinding],
        failures: list[str],
    ) -> None:
        supports = tuple(bindings[item] for item in claim.supporting_evidence_ids if item in bindings)
        if claim.population_scope:
            case_ids = {item.naturalistic_case_id for item in supports if item.naturalistic_case_id}
            if len(case_ids) < 2:
                failures.append("SINGLE_NATURALISTIC_CASE_CANNOT_SUPPORT_POPULATION_CLAIM")
        if claim.causal_learning_effect:
            transfer = [
                item
                for item in supports
                if item.transfer_candidate
                and item.held_out
                and item.repeated
                and item.comparison_control
                and item.independently_scored
            ]
            if len(transfer) < 2:
                failures.append("TRANSFER_OBSERVATION_CANNOT_ESTABLISH_CAUSAL_LEARNING_EFFECT")

    @staticmethod
    def _check_dependencies_and_revision(
        claim: ResearchClaimRecord,
        known_claims: tuple[ResearchClaimRecord, ...],
        failures: list[str],
    ) -> None:
        by_key = {(item.claim_id, item.version): item for item in known_claims}
        if len(by_key) != len(known_claims):
            failures.append("DUPLICATE_KNOWN_CLAIM_VERSION")
        latest_version: dict[str, int] = {}
        for item in known_claims:
            latest_version[item.claim_id] = max(latest_version.get(item.claim_id, 0), item.version)

        for dependency in claim.dependencies:
            upstream = by_key.get((dependency.claim_id, dependency.version))
            if upstream is None:
                failures.append(f"UNKNOWN_DEPENDENCY:{dependency.claim_id}@{dependency.version}")
                continue
            if latest_version[dependency.claim_id] != dependency.version:
                failures.append(f"STALE_DEPENDENCY:{dependency.claim_id}@{dependency.version}")
            if upstream.status in {ClaimStatus.HOLD, ClaimStatus.WITHDRAWN}:
                failures.append(f"DEPENDENCY_HOLD:{dependency.claim_id}@{dependency.version}")

        if claim.revision is None:
            if claim.status is ClaimStatus.REVISED:
                failures.append("REVISED_STATUS_REQUIRES_REVISION_LINK")
            return
        revision = claim.revision
        if claim.status is not ClaimStatus.REVISED:
            failures.append("REVISION_LINK_REQUIRES_REVISED_STATUS")
        if revision.previous_claim_id != claim.claim_id:
            failures.append("REVISION_MUST_PRESERVE_STABLE_CLAIM_ID")
        prior = by_key.get((revision.previous_claim_id, revision.previous_version))
        if prior is None:
            failures.append("STALE_OR_UNKNOWN_REVISION_BASE")
        elif latest_version[revision.previous_claim_id] != revision.previous_version:
            failures.append("STALE_REVISION_BASE")
        if revision.new_version != claim.version:
            failures.append("REVISION_VERSION_MISMATCH")
