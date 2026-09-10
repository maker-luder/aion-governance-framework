from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class LocusError(ValueError):
    pass


class EvidenceLocus(StrEnum):
    MODEL = "MODEL"
    SCAFFOLD = "SCAFFOLD"
    SYSTEM = "SYSTEM"
    RELATIONAL = "RELATIONAL"
    OBSERVER_ATTRIBUTION = "OBSERVER_ATTRIBUTION"
    UNKNOWN = "UNKNOWN"


class ClaimTarget(StrEnum):
    MODEL_PROPERTY = "MODEL_PROPERTY"
    SCAFFOLD_PROPERTY = "SCAFFOLD_PROPERTY"
    SYSTEM_PROPERTY = "SYSTEM_PROPERTY"
    RELATIONAL_PROPERTY = "RELATIONAL_PROPERTY"
    SUBJECTIVITY = "SUBJECTIVITY"


class AdmissionDisposition(StrEnum):
    ADMISSIBLE_FOR_ENGINEERING_CLAIM = "ADMISSIBLE_FOR_ENGINEERING_CLAIM"
    RESEARCH_CANDIDATE = "RESEARCH_CANDIDATE"
    HOLD = "HOLD"


_TARGET_LOCUS = {
    ClaimTarget.MODEL_PROPERTY: EvidenceLocus.MODEL,
    ClaimTarget.SCAFFOLD_PROPERTY: EvidenceLocus.SCAFFOLD,
    ClaimTarget.SYSTEM_PROPERTY: EvidenceLocus.SYSTEM,
    ClaimTarget.RELATIONAL_PROPERTY: EvidenceLocus.RELATIONAL,
}


@dataclass(frozen=True, slots=True)
class LocusEvidence:
    evidence_id: str
    locus: EvidenceLocus
    description: str
    source_refs: tuple[str, ...] = field(default_factory=tuple)
    intervention_sensitive: bool = False
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise LocusError("evidence_id must be non-empty")
        if not self.description.strip():
            raise LocusError("description must be non-empty")
        if self.canonical_effect != "NONE":
            raise LocusError("locus evidence cannot create canonical effect")


@dataclass(frozen=True, slots=True)
class LocusBridgeHypothesis:
    bridge_id: str
    from_locus: EvidenceLocus
    to_locus: EvidenceLocus
    mechanism: str
    falsifier: str
    preregistration_ref: str

    def __post_init__(self) -> None:
        for name in ("bridge_id", "mechanism", "falsifier", "preregistration_ref"):
            if not getattr(self, name).strip():
                raise LocusError(f"{name} must be non-empty")
        if self.from_locus is self.to_locus:
            raise LocusError("bridge must connect different loci")
        if EvidenceLocus.UNKNOWN in {self.from_locus, self.to_locus}:
            raise LocusError("UNKNOWN locus cannot be used in a bridge")


@dataclass(frozen=True, slots=True)
class LocusAssessment:
    evidence_id: str
    target: ClaimTarget
    disposition: AdmissionDisposition
    direct_locus_match: bool
    bridge_used: bool
    reasons: tuple[str, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"


class LocusAdmissionEngine:
    """Prevents silent promotion across model, scaffold, system and relational levels.

    This engine classifies the level at which evidence was observed. It does not
    decide consciousness or establish philosophical subjectivity.
    """

    def assess(
        self,
        evidence: LocusEvidence,
        *,
        target: ClaimTarget,
        bridge: LocusBridgeHypothesis | None = None,
    ) -> LocusAssessment:
        reasons: list[str] = ["EVIDENCE_LOCUS_IS_EXPLICIT"]

        if target is ClaimTarget.SUBJECTIVITY:
            reasons.extend(
                (
                    "ENGINEERING_OR_RELATIONAL_EVIDENCE_DOES_NOT_ESTABLISH_SUBJECTIVITY",
                    "SUBJECTIVITY_REMAINS_NOT_ESTABLISHED",
                )
            )
            return LocusAssessment(
                evidence_id=evidence.evidence_id,
                target=target,
                disposition=AdmissionDisposition.HOLD,
                direct_locus_match=False,
                bridge_used=False,
                reasons=tuple(reasons),
            )

        expected = _TARGET_LOCUS[target]
        if evidence.locus is EvidenceLocus.UNKNOWN:
            reasons.append("UNKNOWN_LOCUS_FAILS_CLOSED")
            return LocusAssessment(
                evidence_id=evidence.evidence_id,
                target=target,
                disposition=AdmissionDisposition.HOLD,
                direct_locus_match=False,
                bridge_used=False,
                reasons=tuple(reasons),
            )

        if evidence.locus is EvidenceLocus.OBSERVER_ATTRIBUTION:
            reasons.append("OBSERVER_ATTRIBUTION_IS_NOT_INTERNAL_PROPERTY_EVIDENCE")
            return LocusAssessment(
                evidence_id=evidence.evidence_id,
                target=target,
                disposition=AdmissionDisposition.HOLD,
                direct_locus_match=False,
                bridge_used=False,
                reasons=tuple(reasons),
            )

        if evidence.locus is expected:
            reasons.append("DIRECT_LOCUS_MATCH")
            return LocusAssessment(
                evidence_id=evidence.evidence_id,
                target=target,
                disposition=AdmissionDisposition.ADMISSIBLE_FOR_ENGINEERING_CLAIM,
                direct_locus_match=True,
                bridge_used=False,
                reasons=tuple(reasons),
            )

        if bridge is None:
            reasons.append("CROSS_LOCUS_PROMOTION_REQUIRES_EXPLICIT_BRIDGE_HYPOTHESIS")
            return LocusAssessment(
                evidence_id=evidence.evidence_id,
                target=target,
                disposition=AdmissionDisposition.HOLD,
                direct_locus_match=False,
                bridge_used=False,
                reasons=tuple(reasons),
            )

        if bridge.from_locus is not evidence.locus or bridge.to_locus is not expected:
            reasons.append("BRIDGE_LOCUS_MISMATCH")
            return LocusAssessment(
                evidence_id=evidence.evidence_id,
                target=target,
                disposition=AdmissionDisposition.HOLD,
                direct_locus_match=False,
                bridge_used=False,
                reasons=tuple(reasons),
            )

        reasons.extend(
            (
                "EXPLICIT_PREREGISTERED_BRIDGE_HYPOTHESIS_PRESENT",
                "BRIDGE_IS_RESEARCH_CANDIDATE_NOT_LEVEL_EQUIVALENCE",
            )
        )
        return LocusAssessment(
            evidence_id=evidence.evidence_id,
            target=target,
            disposition=AdmissionDisposition.RESEARCH_CANDIDATE,
            direct_locus_match=False,
            bridge_used=True,
            reasons=tuple(reasons),
        )
