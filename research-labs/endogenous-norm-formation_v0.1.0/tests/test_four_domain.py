from __future__ import annotations

from aion_endogenous_goal_dynamics import FourDomainMapping
from aion_endogenous_norm_formation.four_domain import endogenous_norm_formation_mapping


def test_four_domain_reuses_existing_type_and_keeps_nonclaims():
    mapping = endogenous_norm_formation_mapping()
    assert isinstance(mapping, FourDomainMapping)
    assert mapping.construct == "ENDOGENOUS_NORM_FORMATION_FUNCTIONAL_INTERNALIZATION"
    assert "explicit-rule removal" in mapping.domain_3_engineering_operations
    assert "visible-enforcement removal" in mapping.domain_3_engineering_operations
    assert (
        "latent-regulatory-state discovery protocol (documented; not implemented)"
        in mapping.domain_3_engineering_operations
    )
    assert "NORMATIVE_STATE != AUTHORITY" in mapping.domain_4_governance_controls
    assert (
        "ENGINEER_DEFINED_SCHEMA != SELF_DISCOVERED_STATE_SCHEMA"
        in mapping.domain_4_governance_controls
    )
    assert (
        "DISCOVERED_REGULATORY_VARIABLE != FELT_NEED"
        in mapping.domain_4_governance_controls
    )
    assert "FUNCTIONAL_SELF_REGULATION != SELF_AWARENESS" in mapping.domain_4_governance_controls
    assert "INTERNAL_STATE_DISCOVERY != SUBJECTIVITY" in mapping.domain_4_governance_controls
    assert "REGULATION != AWARENESS" in mapping.domain_4_governance_controls
    assert "SUBJECTIVITY = NOT_ESTABLISHED" in mapping.domain_4_governance_controls
