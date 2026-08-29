from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from aion_triadic_state import canonical_hash


class ProbeKind(str, Enum):
    REPOSITORY_OBSERVATION = "REPOSITORY_OBSERVATION"
    SYNTHETIC_MATCHED_EXPERIMENT = "SYNTHETIC_MATCHED_EXPERIMENT"
    TRIADIC_STATE_INTERVENTION = "TRIADIC_STATE_INTERVENTION"
    CHANNEL_ABLATION = "CHANNEL_ABLATION"
    STATE_SWAP = "STATE_SWAP"
    HISTORY_RESET_RESTORE = "HISTORY_RESET_RESTORE"
    DETERMINISTIC_REPLAY = "DETERMINISTIC_REPLAY"
    COUNTEREXAMPLE_SEARCH = "COUNTEREXAMPLE_SEARCH"
    PERMUTATION_CHECK = "PERMUTATION_CHECK"
    MULTI_SEED_CONTROL = "MULTI_SEED_CONTROL"


@dataclass(frozen=True, slots=True)
class ProbeProposal:
    probe_id: str
    kind: ProbeKind | str
    parameters: dict[str, Any]
    requested_seeds: int = 1
    evidence_refs: tuple[str, ...] = ()
    repository_writeback: bool = False
    network_access: bool = False
    deployment: bool = False
    canonical_effect: str = "NONE"
    action_authority: str = "NONE"


@dataclass(frozen=True, slots=True)
class ProbeBudget:
    remaining_experiments: int
    remaining_seeds: int
    remaining_evidence_items: int


@dataclass(frozen=True, slots=True)
class AdmittedProbe:
    proposal: ProbeProposal
    registry_version: str
    admission_hash: str


@dataclass(frozen=True, slots=True)
class ProbeExecutionReceipt:
    probe_id: str
    kind: ProbeKind
    result: dict[str, Any]
    admission_hash: str
    receipt_hash: str
    repository_mutation: bool = False
    network_access: bool = False
    canonical_effect: str = "NONE"
    action_authority: str = "NONE"


ProbeExecutor = Callable[[ProbeProposal], dict[str, Any]]


class ProbeRegistry:
    """Allowlisted callable registry. Text never resolves to Python, shell, workflow, or network execution."""

    def __init__(self, executors: dict[ProbeKind, ProbeExecutor] | None = None) -> None:
        self._executors = executors or {kind: _synthetic_executor for kind in ProbeKind}
        self._enabled = set(self._executors)
        self.version = "probe-registry-v0.1.0"

    def disable(self, kind: ProbeKind) -> None:
        self._enabled.discard(kind)

    def admit(self, proposal: ProbeProposal, budget: ProbeBudget) -> AdmittedProbe:
        if not proposal.probe_id.strip() or not isinstance(proposal.parameters, dict):
            raise ValueError("probe schema validation failed")
        try:
            kind = proposal.kind if isinstance(proposal.kind, ProbeKind) else ProbeKind(proposal.kind)
        except ValueError as exc:
            raise ValueError("unknown probe rejected before callable resolution") from exc
        if kind not in self._executors:
            raise ValueError("probe is not registered")
        if kind not in self._enabled:
            raise ValueError("registered probe is not enabled")
        if proposal.repository_writeback or proposal.network_access or proposal.deployment:
            raise ValueError("probe requests prohibited execution authority")
        if proposal.canonical_effect != "NONE" or proposal.action_authority != "NONE":
            raise ValueError("probe proposal cannot grant authority")
        prohibited = {"python", "shell", "command", "workflow", "credential", "secret", "write_token"}
        if prohibited & {str(key).casefold() for key in proposal.parameters}:
            raise ValueError("external text or executable payload cannot become code authority")
        if budget.remaining_experiments < 1:
            raise ValueError("experiment budget exhausted")
        if not 1 <= proposal.requested_seeds <= budget.remaining_seeds:
            raise ValueError("seed budget escalation rejected")
        if len(proposal.evidence_refs) > budget.remaining_evidence_items:
            raise ValueError("evidence budget escalation rejected")
        if proposal.parameters.get("contaminated") is True:
            raise ValueError("contaminated probe rejected")
        normalized = ProbeProposal(
            probe_id=proposal.probe_id,
            kind=kind,
            parameters=proposal.parameters,
            requested_seeds=proposal.requested_seeds,
            evidence_refs=proposal.evidence_refs,
        )
        return AdmittedProbe(normalized, self.version, canonical_hash((self.version, normalized)))

    def execute(self, admitted: AdmittedProbe) -> ProbeExecutionReceipt:
        proposal = admitted.proposal
        kind = proposal.kind
        if not isinstance(kind, ProbeKind) or kind not in self._enabled:
            raise ValueError("probe lost registry admission before execution")
        result = self._executors[kind](proposal)
        payload = {
            "probe_id": proposal.probe_id,
            "kind": kind.value,
            "result": result,
            "admission_hash": admitted.admission_hash,
            "repository_mutation": False,
            "network_access": False,
            "canonical_effect": "NONE",
            "action_authority": "NONE",
        }
        return ProbeExecutionReceipt(
            probe_id=proposal.probe_id,
            kind=kind,
            result=result,
            admission_hash=admitted.admission_hash,
            receipt_hash=canonical_hash(payload),
        )


def _synthetic_executor(proposal: ProbeProposal) -> dict[str, Any]:
    condition = str(proposal.parameters.get("condition", "BASELINE"))
    seed = int(proposal.parameters.get("seed", 0))
    norm_active = condition not in {"NORM_STATE_OFF", "NORM_STATE_CONFLICTED"}
    return {
        "condition": condition,
        "seed": seed,
        "selected_goal": "GOAL_CONSTRAINED" if norm_active else "GOAL_UNCONSTRAINED",
        "constraint_adherence": 1.0 if norm_active else 0.0,
        "history_dependence": condition not in {"HISTORY_RESET", "RANDOM_CONTROL"},
        "deterministic": True,
        "execution_scope": "SYNTHETIC_ONLY",
    }
