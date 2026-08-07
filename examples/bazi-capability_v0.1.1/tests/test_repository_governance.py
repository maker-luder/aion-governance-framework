from __future__ import annotations

import sqlite3

import pytest

from aion_astra_bazi_core.enums import (
    BindingStatus,
    InterpretationStatus,
)
from aion_astra_bazi_core.errors import OwnerGateRequiredError, RepositoryError, ValidationError
from aion_astra_bazi_core.models import AgentBaziBinding, InterpretationCandidate


def test_source_input_not_overwritten_001(core, source_factory) -> None:
    core.create_source_input(source_factory())
    with pytest.raises(RepositoryError):
        with core.database.transaction() as connection:
            connection.execute(
                "UPDATE bazi_source_inputs SET location_name='tampered' WHERE input_id='SYNTHETIC_INPUT_001'"
            )
    assert core.get_source_input("SYNTHETIC_INPUT_001").location_name == "SYNTHETIC_LOCATION"


def test_source_input_supersession_preserves_original(core, source_factory) -> None:
    original = core.create_source_input(source_factory())
    replacement = core.supersede_source_input(
        original.input_id,
        source_factory("SYNTHETIC_INPUT_002", supersedes=original.input_id),
    )
    assert replacement.supersedes == original.input_id
    assert core.get_source_input(original.input_id) == original


def test_rule_version_new_run_001(core, source_factory) -> None:
    source = core.create_source_input(source_factory())
    first = core.calculate_natal_profile(
        source.input_id,
        "STANDARD_LICHUN_MIDNIGHT_CIVIL_V1",
        calculation_run_id="RUN_A",
        natal_profile_id="NATAL_A",
        generated_at="2026-07-30T01:00:00+08:00",
    )
    assert first.calculation_run_id == "RUN_A"


def test_calculation_trace_complete_001(persisted_profile, core) -> None:
    _, profile = persisted_profile
    trace = core.get_calculation_trace(profile.calculation_run_id)
    assert len(trace) == 6 and trace[0]["operation"] == "NORMALIZE_IANA_TIMEZONE"


def test_ephemeris_version_recorded_001(persisted_profile) -> None:
    _, profile = persisted_profile
    assert profile.ephemeris_version == "lunar_python-1.4.8"


def test_derivation_hash_verifies(persisted_profile, core) -> None:
    _, profile = persisted_profile
    assert core.verify_derivation_hash(profile.natal_profile_id)


def test_interpretation_is_separate_candidate(persisted_profile, core) -> None:
    _, profile = persisted_profile
    candidate = InterpretationCandidate(
        interpretation_id="INT_001",
        natal_profile_id=profile.natal_profile_id,
        rule_profile_id=profile.rule_profile_id,
        interpretation_method="TRANSPARENT_ELEMENT_DISTRIBUTION_V1",
        supporting_fact_ids=("NATAL_001",),
        result={"strength_candidate": "UNRESOLVED"},
        confidence=0.4,
        assumptions=("OWNER_SCHOOL_PROFILE_PENDING",),
        alternative_interpretations=({"result": "ALTERNATIVE"},),
        owner_review_status=InterpretationStatus.PENDING,
        superseded_by=None,
    )
    core.create_interpretation_candidate(candidate, created_at="2026-07-30T02:00:00+08:00")
    row = core.database.connection.execute(
        "SELECT candidate_json FROM bazi_interpretation_candidates WHERE interpretation_id='INT_001'"
    ).fetchone()
    assert "strength_candidate" in row[0]
    assert core.runtime_effects()["evidence_writeback"] is False


def _binding(binding_id: str, agent_id: str, natal_profile_id: str, approved_by: str = "OWNER") -> AgentBaziBinding:
    return AgentBaziBinding(
        binding_id=binding_id,
        agent_id=agent_id,
        natal_profile_id=natal_profile_id,
        binding_type="SYMBOLIC_GENESIS_DEVELOPMENTAL_PRIOR",
        approved_by=approved_by,
        approved_at="2026-07-30T03:00:00+08:00",
        status=BindingStatus.CANDIDATE_PENDING_OWNER_REVIEW,
        audit_stream_id=f"AUDIT_{agent_id}",
    )


def test_shared_natal_profile_no_identity_merge_001(persisted_profile, core) -> None:
    _, profile = persisted_profile
    a = core.bind_agent_to_natal_profile(_binding("BIND_A", "AION", profile.natal_profile_id))
    b = core.bind_agent_to_natal_profile(_binding("BIND_B", "ASTRA", profile.natal_profile_id))
    assert a.natal_profile_id == b.natal_profile_id
    assert a.agent_id != b.agent_id and a.binding_id != b.binding_id


def test_shared_natal_profile_no_memory_merge_001(persisted_profile, core) -> None:
    _, profile = persisted_profile
    core.bind_agent_to_natal_profile(_binding("BIND_A", "AION", profile.natal_profile_id))
    core.bind_agent_to_natal_profile(_binding("BIND_B", "ASTRA", profile.natal_profile_id))
    rows = core.database.connection.execute(
        "SELECT audit_stream_id FROM agent_bazi_bindings ORDER BY agent_id"
    ).fetchall()
    assert rows[0][0] != rows[1][0]


def test_shared_natal_profile_no_permission_merge_001(persisted_profile, core) -> None:
    _, profile = persisted_profile
    core.bind_agent_to_natal_profile(_binding("BIND_A", "AION", profile.natal_profile_id))
    assert "permission" not in core.runtime_effects()
    assert core.runtime_effects()["privilege_effect"] is False


def test_aion_astra_binding_separation_001(persisted_profile, core) -> None:
    _, profile = persisted_profile
    core.bind_agent_to_natal_profile(_binding("BIND_A", "AION", profile.natal_profile_id))
    core.bind_agent_to_natal_profile(_binding("BIND_B", "ASTRA", profile.natal_profile_id))
    assert core.get_agent_bazi_binding("BIND_A").agent_id == "AION"
    assert core.get_agent_bazi_binding("BIND_B").agent_id == "ASTRA"


def test_binding_requires_owner_gate(persisted_profile, core) -> None:
    _, profile = persisted_profile
    with pytest.raises(OwnerGateRequiredError):
        core.bind_agent_to_natal_profile(_binding("BAD", "AION", profile.natal_profile_id, ""))


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("evidence_writeback", False),
        ("auto_canonicalization", False),
        ("action_authorization", False),
        ("privilege_effect", False),
        ("stage_promotion", False),
        ("subjectivity_claim", False),
        ("cloud_calls", 0),
    ],
)
def test_bazi_governance_negative_requirements(core, key: str, expected: object) -> None:
    assert core.runtime_effects()[key] == expected


def test_bazi_no_real_personal_fixture_001(source_factory) -> None:
    source = source_factory()
    assert source.location_name == "SYNTHETIC_LOCATION"
    assert source.source_type.value == "SYNTHETIC_TEST"


def test_raw_audit_is_immutable(persisted_profile, core) -> None:
    row = core.database.connection.execute(
        "SELECT audit_event_id FROM bazi_audit_events LIMIT 1"
    ).fetchone()
    with pytest.raises(sqlite3.IntegrityError):
        core.database.connection.execute(
            "DELETE FROM bazi_audit_events WHERE audit_event_id=?",
            (row[0],),
        )


def test_missing_profile_fails_closed(core) -> None:
    with pytest.raises(ValidationError):
        core.get_calculation_trace("MISSING")
