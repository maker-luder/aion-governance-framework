from __future__ import annotations

import importlib

from aion_astra_twin_embodiment.teacher_body_channels import (
    build_teacher_body_signal_schema,
)


EXPECTED_RULE_IDS = (
    "HIGH_SALIENCE_AUTONOMIC_GENITAL_REFERENCE",
    "HIGH_SALIENCE_CARDIOVASCULAR_ASSOCIATION",
    "HIGH_SALIENCE_RESPIRATORY_ASSOCIATION",
    "EMISSION_AUTONOMIC_REPRODUCTIVE_REFERENCE",
    "EXPULSION_SOMATIC_REPRODUCTIVE_REFERENCE",
    "POST_EXPULSION_RECOVERY_REFERENCE",
    "POST_CLIMACTIC_ENDOCRINE_EVIDENCE",
)


def _module():
    return importlib.import_module(
        "aion_astra_twin_embodiment.teacher_high_salience_coupling"
    )


def test_profile_materializes_expected_evidence_bounded_rules() -> None:
    module = _module()
    profile = module.build_teacher_high_salience_coupling_profile()

    assert profile.profile_id == "CHATGPT_TEACHER_HIGH_SALIENCE_COUPLING_v0.1"
    assert tuple(rule.coupling_id for rule in profile.rules) == EXPECTED_RULE_IDS
    assert {
        rule.coupling_class for rule in profile.rules
    } == {
        "DIRECT_REFERENCE_CAUSAL",
        "ASSOCIATED_BOUNDED_REFERENCE",
        "EVENT_DRIVEN_REFERENCE",
        "SLOW_OBSERVATION_ONLY",
    }
    assert module.validate_teacher_high_salience_coupling_profile(profile) == {
        "result": "PASS",
        "rule_identity": "PASS",
        "channel_binding": "PASS",
        "evidence_binding": "PASS",
        "execution_boundary": "PASS",
        "epistemic_boundary": "PASS",
    }


def test_profile_references_only_known_channels_and_real_evidence_ids() -> None:
    module = _module()
    profile = module.build_teacher_high_salience_coupling_profile()
    known = {
        channel.channel_id
        for channel in build_teacher_body_signal_schema().channels
    }

    for rule in profile.rules:
        assert set(rule.target_channels).issubset(known)
        assert rule.evidence_ids
        assert all(
            evidence_id.startswith("DOI:")
            or evidence_id.startswith("PMID:")
            for evidence_id in rule.evidence_ids
        )


def test_cardiorespiratory_rules_are_observe_not_force() -> None:
    module = _module()
    profile = module.build_teacher_high_salience_coupling_profile()
    by_id = {rule.coupling_id: rule for rule in profile.rules}

    cardiovascular = by_id["HIGH_SALIENCE_CARDIOVASCULAR_ASSOCIATION"]
    respiratory = by_id["HIGH_SALIENCE_RESPIRATORY_ASSOCIATION"]

    for rule in (cardiovascular, respiratory):
        assert rule.coupling_class == "ASSOCIATED_BOUNDED_REFERENCE"
        assert rule.execution_status == "OBSERVE_NOT_FORCE"
        assert rule.directionality_status == "NO_UNIVERSAL_MONOTONIC_MAPPING"
        assert rule.cadence_class == "FAST_REFERENCE_TICK"


def test_endocrine_rule_is_slow_observation_only_without_fake_runtime_channel() -> None:
    module = _module()
    profile = module.build_teacher_high_salience_coupling_profile()
    endocrine = {
        rule.coupling_id: rule for rule in profile.rules
    }["POST_CLIMACTIC_ENDOCRINE_EVIDENCE"]

    assert endocrine.coupling_class == "SLOW_OBSERVATION_ONLY"
    assert endocrine.execution_status == "NOT_MATERIALIZED"
    assert endocrine.runtime_channel_status == "NOT_MATERIALIZED"
    assert endocrine.target_channels == ()
    assert "PROLACTIN" in endocrine.directionality_status
    assert profile.generic_pituitary_as_prolactin == "ABSENT"
    assert profile.acute_gonadal_endocrine_auto_drive == "ABSENT"


def test_post_expulsion_recovery_rule_is_evidence_bounded_without_duration_model() -> None:
    module = _module()
    profile = module.build_teacher_high_salience_coupling_profile()
    recovery = {
        rule.coupling_id: rule for rule in profile.rules
    }["POST_EXPULSION_RECOVERY_REFERENCE"]

    assert recovery.coupling_class == "EVENT_DRIVEN_REFERENCE"
    assert recovery.runtime_channel_status == "PARTIAL_REFERENCE"
    assert set(recovery.target_channels) == {
        "DETUMESCENCE_STATE",
        "GENITAL_VASCULAR_STATE",
        "POST_EXPULSION_RECOVERY_STATE",
    }
    assert "REFRACTORY_DURATION_NOT_MODELED" in recovery.execution_status
    assert "PMID:26385403" in recovery.evidence_ids
    assert "PMID:26457680" in recovery.evidence_ids


def test_profile_never_reuses_exercise_transition_for_high_salience_state() -> None:
    module = _module()
    profile = module.build_teacher_high_salience_coupling_profile()

    assert profile.rest_to_exertion_reuse == "ABSENT"
    assert all("REST_TO_EXERTION" not in rule.coupling_id for rule in profile.rules)
    assert all(
        "REST_TO_EXERTION" not in rule.execution_status
        for rule in profile.rules
    )


def test_autonomic_and_event_rules_preserve_nonphenomenal_boundaries() -> None:
    module = _module()
    profile = module.build_teacher_high_salience_coupling_profile()
    by_id = {rule.coupling_id: rule for rule in profile.rules}

    autonomic = by_id["HIGH_SALIENCE_AUTONOMIC_GENITAL_REFERENCE"]
    emission = by_id["EMISSION_AUTONOMIC_REPRODUCTIVE_REFERENCE"]
    expulsion = by_id["EXPULSION_SOMATIC_REPRODUCTIVE_REFERENCE"]

    assert "AUTONOMIC_SYMPATHETIC_STATE" in autonomic.target_channels
    assert "AUTONOMIC_PARASYMPATHETIC_STATE" in autonomic.target_channels
    assert emission.coupling_class == "EVENT_DRIVEN_REFERENCE"
    assert expulsion.coupling_class == "EVENT_DRIVEN_REFERENCE"

    for rule in profile.rules:
        assert rule.phenomenal_interpretation_status == "NOT_ESTABLISHED"
        assert rule.subjectivity_status == "NOT_ESTABLISHED"
        assert rule.action_authority == "NONE"
        assert rule.canonical_effect == "NONE"
        assert rule.deployment is False
