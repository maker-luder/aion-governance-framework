import pytest

from aion_runtime_v2.deployment import DeploymentEventType, DeploymentLedger


def test_deployment_chain_and_clone_new_lineage():
    ledger = DeploymentLedger()
    ledger.append(event_type=DeploymentEventType.FIRST_INSTANTIATION, deployment_id="D1", runtime_instance_id="R1", lineage_id="L1")
    ledger.append(event_type=DeploymentEventType.CLONE, deployment_id="D2", runtime_instance_id="R2", lineage_id="L2", source_checkpoint_id="CP1", source_lineage_id="L1")
    assert ledger.verify_chain() is True
    assert ledger.events()[1].lineage_id != ledger.events()[1].source_lineage_id


def test_clone_same_lineage_rejected():
    ledger = DeploymentLedger()
    with pytest.raises(ValueError):
        ledger.append(event_type=DeploymentEventType.CLONE, deployment_id="D2", runtime_instance_id="R2", lineage_id="L1", source_checkpoint_id="CP1", source_lineage_id="L1")


def test_restore_requires_checkpoint():
    ledger = DeploymentLedger()
    with pytest.raises(ValueError):
        ledger.append(event_type=DeploymentEventType.RESTORE, deployment_id="D1", runtime_instance_id="R1", lineage_id="L1")
