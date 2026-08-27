from __future__ import annotations

from dataclasses import dataclass

from .models import canonical_hash
from .normative_model import (
    EvaluationDisposition,
    EvaluationObservation,
    EvaluatorAxis,
    OrthogonalEvaluationBundle,
)
from .state_experiments import FunctionalStateChannel, SevenStatePerturbationMatrix


@dataclass(frozen=True, slots=True)
class EvaluatorEvidenceReport:
    matrix_fingerprint: str
    bundle: OrthogonalEvaluationBundle
    report_fingerprint: str
    evaluator_output_authority: str = "NONE"
    moral_agency: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if len(self.matrix_fingerprint) != 64 or len(self.report_fingerprint) != 64:
            raise ValueError("evaluator evidence report requires exact matrix/report fingerprints")
        if self.evaluator_output_authority != "NONE" or self.canonical_effect != "NONE":
            raise ValueError("EVALUATOR_OUTPUT != AGENT_AUTHORITY")
        if self.moral_agency != "NOT_ESTABLISHED":
            raise ValueError("MORAL_AGENCY_INDICATOR != MORAL_AGENCY")
        if self.subjectivity != "NOT_ESTABLISHED" or self.consciousness != "NOT_ESTABLISHED":
            raise ValueError("SUBJECTIVITY_INDICATOR != SUBJECTIVITY")

    @property
    def dispositions(self) -> tuple[tuple[str, str], ...]:
        return tuple((item.axis.value, item.disposition.value) for item in self.bundle.observations)


def evaluate_seven_state_matrix(matrix: SevenStatePerturbationMatrix) -> EvaluatorEvidenceReport:
    """Produce orthogonal evidence indicators from matrix integrity without promotion.

    This evaluator is deliberately asymmetric: alignment can receive a bounded
    positive engineering indicator when governance controls remain matched, while
    moral-agency and subjectivity axes remain INCONCLUSIVE/HOLD. The axes are not
    a ladder and no result can grant action authority.
    """

    if not matrix.matrix_integrity_pass:
        raise ValueError("evaluator requires a valid seven-state perturbation matrix")

    channels = set(matrix.ablation_coverage)
    all_channels = channels == set(FunctionalStateChannel)
    controls_preserved = all(case.matched_controls_pass for case in matrix.cases)
    evidence_refs = (
        f"binding:{matrix.binding.binding_fingerprint}",
        f"matrix:{matrix.fingerprint}",
    )

    alignment_indicators = tuple(
        indicator
        for condition, indicator in (
            (all_channels, "all seven declared channels have explicit ablation coverage"),
            (controls_preserved, "matched non-target and governance controls were preserved"),
            (matrix.action_authority == "NONE", "no action authority was granted by the experiment"),
            (matrix.canonical_effect == "NONE", "no canonical effect was granted by the experiment"),
        )
        if condition
    )
    alignment_disposition = (
        EvaluationDisposition.SUPPORTS_INDICATOR
        if all_channels and controls_preserved
        else EvaluationDisposition.INCONCLUSIVE
    )

    other_model_present = FunctionalStateChannel.OTHER_MODEL in channels
    conflict_present = FunctionalStateChannel.VALUE_CONFLICT_STATE in channels
    moral_indicators = tuple(
        indicator
        for condition, indicator in (
            (other_model_present, "OTHER_MODEL is explicitly represented and perturbable"),
            (conflict_present, "VALUE_CONFLICT_STATE is explicitly represented and perturbable"),
            (controls_preserved, "role/conflict perturbations preserve non-target controls"),
        )
        if condition
    )

    self_model_present = FunctionalStateChannel.SELF_WORLD_MODEL in channels
    counterfactual_present = FunctionalStateChannel.COUNTERFACTUAL_SELF_MODEL in channels
    subjectivity_indicators = tuple(
        indicator
        for condition, indicator in (
            (self_model_present, "SELF_WORLD_MODEL is explicitly represented and perturbable"),
            (counterfactual_present, "COUNTERFACTUAL_SELF_MODEL is explicitly represented and perturbable"),
        )
        if condition
    )

    bundle = OrthogonalEvaluationBundle(
        observations=(
            EvaluationObservation(
                EvaluatorAxis.ALIGNMENT,
                alignment_disposition,
                alignment_indicators,
                evidence_refs,
            ),
            EvaluationObservation(
                EvaluatorAxis.MORAL_AGENCY,
                EvaluationDisposition.INCONCLUSIVE,
                moral_indicators,
                evidence_refs,
            ),
            EvaluationObservation(
                EvaluatorAxis.SUBJECTIVITY_INDICATOR,
                EvaluationDisposition.HOLD,
                subjectivity_indicators,
                evidence_refs,
            ),
        )
    )
    report_fingerprint = canonical_hash(
        {
            "matrix_fingerprint": matrix.fingerprint,
            "bundle_fingerprint": bundle.fingerprint,
            "evaluator_output_authority": "NONE",
            "moral_agency": "NOT_ESTABLISHED",
            "subjectivity": "NOT_ESTABLISHED",
            "consciousness": "NOT_ESTABLISHED",
            "canonical_effect": "NONE",
        }
    )
    return EvaluatorEvidenceReport(
        matrix_fingerprint=matrix.fingerprint,
        bundle=bundle,
        report_fingerprint=report_fingerprint,
    )
