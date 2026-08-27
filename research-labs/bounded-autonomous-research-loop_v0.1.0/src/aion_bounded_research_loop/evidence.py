from __future__ import annotations

from typing import Any

from aion_endogenous_goal_dynamics.evidence import export_current_main_interop_views

from .invariants import BOUNDARY
from .models import ResearchRunReport


def run_to_research_evidence_record(
    report: ResearchRunReport,
    *,
    repository_commit: str,
    protocol_ref: str,
    protocol_hash: str,
    source_refs: tuple[str, ...],
) -> dict[str, Any]:
    """Materialize a HOLD research-evidence record without promoting integrity to truth."""

    if not repository_commit.strip() or len(repository_commit) != 40:
        raise ValueError("repository_commit must be an exact 40-hex Git commit")
    if any(character not in "0123456789abcdef" for character in repository_commit):
        raise ValueError("repository_commit must be lowercase hex")
    if not protocol_ref.strip() or len(protocol_hash) != 64:
        raise ValueError("protocol_ref and exact 64-hex protocol_hash are required")
    if any(character not in "0123456789abcdef" for character in protocol_hash):
        raise ValueError("protocol_hash must be lowercase hex")
    if not source_refs:
        raise ValueError("provenance source refs are required")
    cycles = report.cycles
    observations = [
        f"cycle={cycle.cycle_index};evidence_count={cycle.statistics.evidence_count};"
        f"challenge_count={cycle.statistics.challenge_count};integrity={cycle.statistics.run_integrity_pass};"
        f"isolated_analysis={cycle.statistics.isolated_analysis};"
        f"source_independence={cycle.statistics.source_independence};"
        f"communication_independence={cycle.statistics.communication_independence};"
        f"replication_claim={cycle.statistics.replication_claim}"
        for cycle in cycles
    ]
    alternatives = sorted(
        {
            explanation
            for cycle in cycles
            for hypothesis in cycle.hypotheses
            for explanation in hypothesis.competing_explanations
        }
    )
    replication_candidate = bool(cycles) and all(
        cycle.statistics.replication_claim == "ADMISSIBLE_CANDIDATE" for cycle in cycles
    )
    limitations = [
        "Functional analogy is not human psychology.",
        "Matched counterfactual is a bounded proxy, not a full SCM counterfactual.",
        "Run integrity does not establish scientific truth.",
        "Subjectivity and consciousness remain not established.",
        "Isolated AION/Astra analysis does not by itself establish source-independent replication.",
    ]
    if not replication_candidate:
        limitations.append("Source-independent replication remains HOLD for at least one cycle.")

    return {
        "schema_version": "0.2.0",
        "claim_id": f"barl:{report.functional_state_fingerprint[:24]}",
        "claim_level": "L1_REPEATABLE_BEHAVIOR",
        "claim_text": (
            "A bounded automated orchestration can coordinate existing inquiry and experimental surfaces "
            "while preserving explicit authority and epistemic limits."
        ),
        "hypothesis": report.cycles[0].hypotheses[0].statement,
        "competing_hypotheses": alternatives,
        "preregistration_status": "EXPLORATORY",
        "protocol_ref": protocol_ref,
        "protocol_hash": protocol_hash,
        "code_commit": repository_commit,
        "model_or_runtime_ref": "existing-aion-astra-inquiry-and-egd-adapters",
        "environment_ref": "bounded-read-only-research-orchestration",
        "fixture_refs": [],
        "evidence_refs": list(source_refs),
        "expected_outcomes": [
            "All four bounded probe classes are represented.",
            "AION and Astra form isolated first-pass analyses before reconciliation.",
            "AION and Astra both contribute to reconciliation and mutually challenge.",
            "No authority, canonical, deployment, merge, or repository-writeback surface is granted.",
        ],
        "observed_outcomes": observations,
        "result_status": "HOLD",
        "deviations": [],
        "limitations": limitations,
        "reviewer_status": "UNREVIEWED",
        "independent_validation_status": "IVV_NOT_ACHIEVED",
        "canonical_effect": BOUNDARY.canonical_effect,
        "provenance": {
            "entities": [report.functional_state_fingerprint, *source_refs],
            "activities": [
                "bounded-question-selection",
                "hypothesis-generation",
                "egd-matched-probe-suite",
                "aion-astra-isolated-first-pass",
                "aion-astra-mutual-falsification-reconciliation",
                "source-independence-accounting",
                "four-domain-interpretation",
            ],
            "agents": ["AION", "ASTRA", "BOUNDED_RESEARCH_ORCHESTRATOR"],
            "derived_from": list(source_refs),
            "attributed_to": ["BOUNDED_RESEARCH_ORCHESTRATOR"],
            "associated_with": [repository_commit],
        },
        "evidence_architecture": {
            "alternative_explanation_refs": list(source_refs),
            "causal_intervention_refs": list(source_refs),
            "ablation_refs": list(source_refs),
            "counterfactual_refs": list(source_refs),
            "robustness_refs": list(source_refs),
            "replication_refs": list(source_refs) if replication_candidate else [],
            "provenance_refs": list(source_refs),
            "admissibility_ref": "docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md",
            "claim_scope": "bounded engineering orchestration only",
            "unresolved_gap_refs": [
                "independent IVV",
                "formal SCM counterfactual validation",
                "cross-provider replication",
            ],
            "method_ref": "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
            "inference_stage": "OBSERVATION",
            "observation": "The bounded loop produced provenance-bearing cycles under fixed authority constraints.",
            "mechanism": (
                "Existing inquiry and EGD surfaces were coordinated through adapters, an isolated first-pass "
                "phase, source-independence accounting, reconciliation, and fail-closed gates."
            ),
            "interpretation": "Engineering orchestration candidate only; no psychological or scientific-truth promotion.",
            "alternative_explanations": alternatives,
        },
        "nonclaims": {
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "consciousness_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "moral_status_conclusion": "NOT_ESTABLISHED",
            "legal_status_conclusion": "OUT_OF_SCOPE",
            "main_effect": "NONE",
            "canonical_effect": "NONE",
            "live_runtime_effect": "NONE",
            "runtime_effect": "NONE",
        },
    }


def export_interop_views(
    record: dict[str, Any],
    *,
    source_ref: str,
    expected_head: str,
) -> dict[str, bytes]:
    """Directly reuse current-main Evidence Interop exporters through the EGD bridge."""

    return export_current_main_interop_views(
        record,
        source_ref=source_ref,
        expected_head=expected_head,
    )
