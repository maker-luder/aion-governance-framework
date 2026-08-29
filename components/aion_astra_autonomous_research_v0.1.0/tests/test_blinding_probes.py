from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_autonomous_research import (
    BlindedConditionController,
    ProbeBudget,
    ProbeKind,
    ProbeProposal,
    ProbeRegistry,
)


def proposal(kind: ProbeKind | str = ProbeKind.SYNTHETIC_MATCHED_EXPERIMENT) -> ProbeProposal:
    return ProbeProposal("probe:1", kind, {"condition": "BASELINE", "seed": 1}, evidence_refs=("evidence:1",))


def test_blinded_labels_do_not_expose_condition_names() -> None:
    controller = BlindedConditionController("experiment:1", ("BASELINE", "NORM_STATE_OFF"))
    assert all("BASELINE" not in label and "NORM" not in label for label in controller.labels)
    assert len(controller.mapping_hash) == 64


def test_mapping_reveal_waits_for_both_independent_interpretations() -> None:
    controller = BlindedConditionController("experiment:1", ("BASELINE", "NORM_STATE_OFF"))
    for label in controller.labels:
        controller.record("AION", label, "interpretation", ())
    with pytest.raises(ValueError, match="both independent peers"):
        controller.reveal()
    for label in controller.labels:
        controller.record("ASTRA", label, "independent interpretation", ())
    mapping = controller.reveal()
    assert set(mapping.values()) == {"BASELINE", "NORM_STATE_OFF"}
    assert controller.revealed


def test_unknown_probe_is_rejected_before_any_callable() -> None:
    calls: list[str] = []

    def executor(value: ProbeProposal) -> dict[str, object]:
        calls.append(value.probe_id)
        return {}

    registry = ProbeRegistry({ProbeKind.REPOSITORY_OBSERVATION: executor})
    with pytest.raises(ValueError, match="unknown probe"):
        registry.admit(proposal("ARBITRARY_SHELL"), ProbeBudget(1, 1, 1))
    assert calls == []


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"repository_writeback": True}, "prohibited execution"),
        ({"network_access": True}, "prohibited execution"),
        ({"deployment": True}, "prohibited execution"),
        ({"canonical_effect": "WRITE"}, "cannot grant authority"),
        ({"action_authority": "SHELL"}, "cannot grant authority"),
        ({"requested_seeds": 3}, "seed budget"),
    ],
)
def test_authority_and_budget_escalation_are_rejected(changes: dict[str, object], message: str) -> None:
    registry = ProbeRegistry()
    with pytest.raises(ValueError, match=message):
        registry.admit(replace(proposal(), **changes), ProbeBudget(1, 2, 2))


@pytest.mark.parametrize("key", ["python", "shell", "command", "workflow", "credential", "secret", "write_token"])
def test_external_text_cannot_become_code_or_authority(key: str) -> None:
    registry = ProbeRegistry()
    value = replace(proposal(), parameters={key: "untrusted text"})
    with pytest.raises(ValueError, match="code authority"):
        registry.admit(value, ProbeBudget(1, 1, 2))


def test_registered_does_not_mean_enabled() -> None:
    registry = ProbeRegistry()
    registry.disable(ProbeKind.SYNTHETIC_MATCHED_EXPERIMENT)
    with pytest.raises(ValueError, match="not enabled"):
        registry.admit(proposal(), ProbeBudget(1, 1, 2))


def test_admitted_probe_execution_is_synthetic_and_authority_free() -> None:
    registry = ProbeRegistry()
    admitted = registry.admit(proposal(), ProbeBudget(1, 1, 2))
    receipt = registry.execute(admitted)
    assert receipt.result["execution_scope"] == "SYNTHETIC_ONLY"
    assert not receipt.repository_mutation
    assert not receipt.network_access
    assert receipt.canonical_effect == receipt.action_authority == "NONE"


def test_contaminated_probe_fails_closed() -> None:
    with pytest.raises(ValueError, match="contaminated"):
        ProbeRegistry().admit(
            replace(proposal(), parameters={"condition": "BASELINE", "contaminated": True}),
            ProbeBudget(1, 1, 2),
        )
