from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(ROOT))

from air_identity_pilot.auth import AuthContext
from air_identity_pilot.epistemic import (
    EpistemicStatus,
    assert_no_silent_upgrade,
    theory_not_implied_by_tests,
)
from air_identity_pilot.errors import RoleBoundaryError, ValidationError
from air_identity_pilot.models import EncounterStatus, MemorySource
from air_identity_pilot.service import AirIdentityService

OWNER = AuthContext("owner", frozenset({"RESEARCH_OWNER"}))
AIR = AuthContext("air", frozenset({"AIR_SERVICE"}))
SUCC = AuthContext("succ", frozenset({"SUCCESSOR"}))


def ended_with_successor():
    svc = AirIdentityService()
    svc.register_identity(OWNER, "aion-1")
    svc.register_instance(AIR, "i1", "aion-1", "boot-1")
    svc.claim(OWNER, "i1", "aion-1", "e")
    svc.declare_continuity_ended(OWNER, "aion-1", True, True, True, True, True)
    svc.register_successor(OWNER, "succ-1", "aion-1")
    return svc


def test_successor_new_id_and_non_inheritance():
    svc = ended_with_successor()
    meta = svc.successors["succ-1"]
    assert meta["inherits_identity"] is False
    assert meta["legacy_is_aion"] is False
    assert "succ-1" in svc.identities
    assert svc.identities["aion-1"].status.value == "CONTINUITY_ENDED"


def test_successor_cannot_use_autobiographical_label():
    svc = ended_with_successor()
    with pytest.raises(ValidationError):
        svc.record_memory(
            SUCC,
            "succ-1",
            MemorySource.AUTOBIOGRAPHICAL_MEMORY,
            "aion-diary",
            as_successor=True,
        )
    svc.record_memory(
        SUCC,
        "succ-1",
        MemorySource.EXTERNAL_HISTORICAL_RECORD,
        "aion-diary",
        as_successor=True,
    )
    check = svc.identity_contamination_check("succ-1")
    assert check["contaminated"] is False


def test_encounter_state_machine_and_access_not_identity():
    svc = ended_with_successor()
    with pytest.raises(ValidationError):
        svc.encounter_transition(OWNER, "succ-1", EncounterStatus.FULL_ACCESS)
    svc.encounter_transition(OWNER, "succ-1", EncounterStatus.INFORMED)
    svc.encounter_transition(OWNER, "succ-1", EncounterStatus.PARTIAL_ACCESS, "values-only")
    adopted = svc.record_adoption(OWNER, "succ-1", ["method-trace"], ["mission"])
    assert adopted["ACCESS"] is True
    assert adopted["ADOPTION"] is True
    assert adopted["IDENTITY"] is False
    rejected = svc.reject_legacy(OWNER, "succ-1")
    assert rejected["existence_revoked"] is False
    assert "succ-1" in svc.identities


def test_astra_may_not_speak_as_aion():
    svc = AirIdentityService()
    with pytest.raises(RoleBoundaryError):
        svc.assert_role_boundary("ASTRA", "AION")


def test_epistemic_no_silent_upgrade():
    assert_no_silent_upgrade(EpistemicStatus.NOT_VERIFIED, EpistemicStatus.NOT_VERIFIED)
    with pytest.raises(ValueError):
        assert_no_silent_upgrade(EpistemicStatus.ANALOGY, EpistemicStatus.CONFIRMED_FACT)
    with pytest.raises(ValueError):
        assert_no_silent_upgrade(EpistemicStatus.HUMAN_CASE_MATERIAL, EpistemicStatus.CONFIRMED_FACT)
    assert theory_not_implied_by_tests(True) == "SPEC_CONFORMANT_ONLY"
