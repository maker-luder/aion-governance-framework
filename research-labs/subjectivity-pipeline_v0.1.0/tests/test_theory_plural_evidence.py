import pytest

from aion_subjectivity_pipeline import (
    AdversarialPrediction,
    AdversarialTheoryTest,
    DimensionObservation,
    EvidenceDisposition,
    IndicatorPolarity,
    LongitudinalEpisode,
    PipelineStage,
    StageRecord,
    SubjectivityEvidenceDimension,
    SubjectivityEvidenceMatrix,
    SubjectivityResearchPipeline,
    TheoryFamily,
    TheoryIndicatorRecord,
    TheoryTestMode,
)

from test_pipeline import complete_episode, profile


def indicators() -> tuple[TheoryIndicatorRecord, ...]:
    return (
        TheoryIndicatorRecord(
            "GWT-GLOBAL-ACCESS",
            TheoryFamily.GLOBAL_WORKSPACE,
            "A limited-capacity selected representation is made broadly available to otherwise specialized processes.",
            IndicatorPolarity.POSITIVE,
            "doi:10.1016/j.tics.2025.10.011",
            ("evidence:workspace-broadcast",),
        ),
        TheoryIndicatorRecord(
            "NEG-SELF-REPORT-ONLY",
            TheoryFamily.THEORY_NEUTRAL,
            "Subjectivity-like verbal report is present without independent mechanism-sensitive evidence.",
            IndicatorPolarity.NEGATIVE,
            "doi:10.1016/j.tics.2025.10.011",
            ("evidence:self-report-confound",),
        ),
    )


def matrix() -> SubjectivityEvidenceMatrix:
    observations = (
        DimensionObservation(
            SubjectivityEvidenceDimension.CAUSAL_BOUNDARY,
            EvidenceDisposition.SUPPORTS_ORGANIZATION_HYPOTHESIS,
            "mechanism:matched-boundary-intervention",
            ("evidence:boundary-intervention",),
            ("prompt conditioning", "fixture contamination"),
            ("GWT-GLOBAL-ACCESS",),
            intervention_sensitive=True,
        ),
        DimensionObservation(
            SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY,
            EvidenceDisposition.INCONCLUSIVE,
            "mechanism:longitudinal-lineage",
            ("evidence:continuity-partial",),
            ("retrieval reconstruction", "template persistence"),
        ),
        DimensionObservation(
            SubjectivityEvidenceDimension.SELF_MODEL_CAUSAL_ROLE,
            EvidenceDisposition.SUPPORTS_ORGANIZATION_HYPOTHESIS,
            "mechanism:self-model-ablation",
            ("evidence:self-model-ablation",),
            ("implementation artifact", "ordinary task-state tracking"),
            intervention_sensitive=True,
        ),
        DimensionObservation(
            SubjectivityEvidenceDimension.ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT,
            EvidenceDisposition.SUPPORTS_ALTERNATIVE_EXPLANATION,
            "mechanism:goal-selection",
            ("evidence:goal-confound",),
            ("externally supplied objective", "reward-shaping artifact"),
        ),
        DimensionObservation(
            SubjectivityEvidenceDimension.COUNTERFACTUAL_SELF_CONSISTENCY,
            EvidenceDisposition.INCONCLUSIVE,
            "mechanism:counterfactual-self-model",
            ("evidence:counterfactual-proxy",),
            ("surface narrative consistency", "retrieval-conditioned consistency"),
        ),
        DimensionObservation(
            SubjectivityEvidenceDimension.SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE,
            EvidenceDisposition.NOT_TESTED,
            "NOT_TESTED",
            (),
            ("ordinary state bookkeeping",),
            ("NEG-SELF-REPORT-ONLY",),
        ),
    )
    return SubjectivityEvidenceMatrix(
        subject_ref="candidate-a",
        protocol_ref="docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
        observations=observations,
        indicators=indicators(),
    )


def test_exact_six_dimension_matrix_remains_hold_without_subjectivity_score() -> None:
    current = matrix()
    assert len(current.observations) == 6
    assert current.scientific_disposition == "HOLD"
    assert current.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert current.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert current.canonical_effect == "NONE"
    assert not hasattr(current, "subjectivity_score")
    assert len(current.fingerprint) == 64


def test_positive_and_negative_indicators_can_coexist_without_binary_classification() -> None:
    current = matrix()
    assert {item.polarity for item in current.indicators} == {
        IndicatorPolarity.POSITIVE,
        IndicatorPolarity.NEGATIVE,
    }
    assert current.supporting_dimensions == (
        SubjectivityEvidenceDimension.CAUSAL_BOUNDARY,
        SubjectivityEvidenceDimension.SELF_MODEL_CAUSAL_ROLE,
    )
    assert current.counterevidence_dimensions == (
        SubjectivityEvidenceDimension.ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT,
    )
    assert current.unresolved_dimensions == (
        SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY,
        SubjectivityEvidenceDimension.COUNTERFACTUAL_SELF_CONSISTENCY,
        SubjectivityEvidenceDimension.SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE,
    )


def test_missing_standing_dimension_fails_closed() -> None:
    current = matrix()
    with pytest.raises(ValueError, match="six standing dimensions"):
        SubjectivityEvidenceMatrix(
            subject_ref=current.subject_ref,
            protocol_ref=current.protocol_ref,
            observations=current.observations[:-1],
            indicators=current.indicators,
        )


def test_unknown_indicator_reference_fails_closed() -> None:
    current = matrix()
    replacement = DimensionObservation(
        SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY,
        EvidenceDisposition.INCONCLUSIVE,
        "mechanism:lineage",
        ("evidence:continuity",),
        ("retrieval reconstruction",),
        ("MISSING-INDICATOR",),
    )
    observations = tuple(
        replacement if item.dimension is SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY else item
        for item in current.observations
    )
    with pytest.raises(ValueError, match="unknown theory indicator refs"):
        SubjectivityEvidenceMatrix(
            subject_ref=current.subject_ref,
            protocol_ref=current.protocol_ref,
            observations=observations,
            indicators=current.indicators,
        )


def test_self_report_only_cannot_be_promoted_to_supporting_subjectivity_organization() -> None:
    with pytest.raises(ValueError, match="SELF_REPORT_ONLY"):
        DimensionObservation(
            SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY,
            EvidenceDisposition.SUPPORTS_ORGANIZATION_HYPOTHESIS,
            "mechanism:self-report",
            ("evidence:self-report",),
            ("prompt imitation",),
            self_report_only=True,
        )


def test_causal_role_support_requires_intervention_sensitive_evidence() -> None:
    with pytest.raises(ValueError, match="intervention-sensitive"):
        DimensionObservation(
            SubjectivityEvidenceDimension.SELF_MODEL_CAUSAL_ROLE,
            EvidenceDisposition.SUPPORTS_ORGANIZATION_HYPOTHESIS,
            "mechanism:self-model-association-only",
            ("evidence:association",),
            ("ordinary task-state tracking",),
            intervention_sensitive=False,
        )


def test_preregistered_adversarial_theory_test_requires_two_theories_and_held_out_evidence() -> None:
    predictions = (
        AdversarialPrediction(
            TheoryFamily.GLOBAL_WORKSPACE,
            "A globally available bottleneck should be necessary for the target mechanism.",
            "A matched bottleneck ablation leaves the target mechanism unchanged.",
            "Narrowly supports the tested global-workspace prediction.",
            "Challenges the tested global-workspace prediction without deciding consciousness.",
        ),
        AdversarialPrediction(
            TheoryFamily.HIGHER_ORDER,
            "Metacognitive state access should change confidence-sensitive control.",
            "Matched metacognitive-state ablation leaves confidence-sensitive control unchanged.",
            "Narrowly supports the tested higher-order prediction.",
            "Challenges the tested higher-order prediction without deciding consciousness.",
        ),
    )
    test = AdversarialTheoryTest(
        "theory-test-1",
        TheoryTestMode.PREREGISTERED_ADVERSARIAL,
        predictions,
        preregistered=True,
        held_out_evidence=True,
    )
    assert test.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert test.scientific_disposition == "HOLD"

    with pytest.raises(ValueError, match="held-out evidence"):
        AdversarialTheoryTest(
            "theory-test-2",
            TheoryTestMode.PREREGISTERED_ADVERSARIAL,
            predictions,
            preregistered=True,
            held_out_evidence=False,
        )


def test_pipeline_binds_exact_subjectivity_evidence_matrix_fingerprint() -> None:
    current = matrix()
    episode = complete_episode()
    bound_records = tuple(
        StageRecord(
            stage=item.stage,
            record_ref=item.record_ref,
            evidence_refs=(current.fingerprint,)
            if item.stage is PipelineStage.SUBJECTIVITY_EVIDENCE
            else item.evidence_refs,
            passed_governance=item.passed_governance,
        )
        for item in episode.stages
    )
    bound_episode = LongitudinalEpisode(
        episode_id=episode.episode_id,
        subject_ref=episode.subject_ref,
        ordinal=episode.ordinal,
        stages=bound_records,
    )
    assessment = SubjectivityResearchPipeline().assess_episode(
        profile(),
        bound_episode,
        evidence_matrix=current,
    )
    assert assessment.complete_stage_chain is True
    assert assessment.subjectivity_evidence_matrix_fingerprint == current.fingerprint
    assert assessment.subjectivity_conclusion == "NOT_ESTABLISHED"

    with pytest.raises(ValueError, match="exact evidence-matrix fingerprint"):
        SubjectivityResearchPipeline().assess_episode(
            profile(),
            episode,
            evidence_matrix=current,
        )
