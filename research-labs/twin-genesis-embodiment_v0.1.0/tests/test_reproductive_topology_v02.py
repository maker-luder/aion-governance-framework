from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.reproductive_topology import (
    build_reproductive_topology_reference,
    validate_reproductive_topology_parity,
)


def test_aion_astra_reproductive_topology_has_same_reference_coverage_but_distinct_body_binding() -> None:
    aion = build_reproductive_topology_reference("AION")
    astra = build_reproductive_topology_reference("ASTRA")
    result = validate_reproductive_topology_parity((aion, astra))
    assert result["result"] == "PASS"
    assert len(aion.nodes) == len(astra.nodes) == 32
    assert len(aion.edges) == len(astra.edges) == 30
    assert aion.body_id != astra.body_id
    assert aion.fingerprint() != astra.fingerprint()


def test_topology_cannot_promote_physical_or_phenomenal_state() -> None:
    aion = build_reproductive_topology_reference("AION")
    with pytest.raises(ValueError, match="physical/biological"):
        replace(aion, biological_organism=True)
    with pytest.raises(ValueError, match="phenomenal"):
        replace(aion, subjectivity="ESTABLISHED")
    with pytest.raises(ValueError, match="action authority"):
        replace(aion, action_authority="GRANTED")
