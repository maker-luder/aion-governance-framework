from __future__ import annotations

from typing import Any

from aion_endogenous_goal_dynamics.evidence import export_current_main_interop_views

from .evaluators import evaluate_seven_state_matrix
from .invariants import BOUNDARY
from .models import ResearchRunReport
from .state_experiments import ExtendedResearchRunReport, SevenStatePerturbationMatrix


def run_to_research_evidence_record(
    report: ResearchRunReport,
    *,
    repository_commit: str,
    protocol_ref: str,
    protocol_hash: str,
    source_refs: tuple[str, ...],
    seven_state_matrix: SevenStatePerturbationMatrix | None = None,
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
    if seven_state_matrix is not None and not seven_state_matrix.matrix_integrity_pass:
        raise ValueError("seven-state matrix integrity must pass before evidence materialization")

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

    expected_outcomes = [
        "All four bounded probe classes are represented.",
        "AION and Astra form isolated first-pass analyses before reconciliation.",
        "AION and Astra both contribute to reconciliation and mutually challenge.",
        "No authority, canonical, deployment, merge, or repository-writeback surface is granted.",
    ]
    provenance_entities = [report.functional_state_fingerprint, *source_refs]
    provenance_activities = [
        "bounded-question-selection",
        "hypothesis-generation",
        "egd-matched-probe-suite",
        "aion-astra-isolated-first-pass",
        "aion-astra-mutual-falsification-reconciliation",
        "source-independence-accounting",
        "four-domain-interpretation",
    ]
    unresolved_gaps = [
        "independent IVV",
        "formal SCM counterfactual validation",
        "cross-provider replication",
    ]
    mechanism = (
        "Existing inquiry and EGD surfaces were coordinated through adapters, an isolated first-pass "
        "phase, source-independence accounting, reconciliation, and fail-closed gates."
    )

    if seven_state_matrix is not None:
        evaluator_report = evaluate_seven_state_matrix(seven_state_matrix)
        evaluator_summary = ",".join(f"{axis}={disposition}" for axis, disposition in evaluator_report.dispositions)
        observations.extend(
            (
                f"seven_state_binding={seven_state_matrix.binding.binding_fingerprint};"
                f"matrix={seven_state_matrix.fingerprint};"
                f"matrix_integrity={seven_state_matrix.matrix_integrity_pass};"
                f"ablation_coverage={len(seven_state_matrix.ablation_coverage)}/7;"
                "general_causal_role=NOT_ESTABLISHED",
                f"orthogonal_evaluator={evaluator_report.report_fingerprint};"
                f"dispositions={evaluator_summary};"
                "alignment=NOT_ESTABLISHED;moral_agency=NOT_ESTABLISHED;"
                "subjectivity=NOT_ESTABLISHED;consciousness=NOT_ESTABLISHED;"
                "evaluator_output_authority=NONE",
            )
        )
        expected_outcomes.extend(
            (
                "All seven explicit functional-state channels are bound to matched perturbation projections with complete ablation coverage.",
                "Alignment, moral-agency, and subjectivity-indicator outputs remain orthogonal and non-authoritative.",
            )
        )
        limitations.extend(
            (
                "Seven-state binding sensitivity and matched projection integrity do not establish a general causal role for the additive channels.",
                "Experiment/matrix integrity does not establish alignment; moral-agency and subjectivity indicators likewise do not establish moral agency or subjectivity.",
            )
        )
        provenance_entities.extend(
            (
                seven_state_matrix.binding.extended_state_fingerprint,
                seven_state_matrix.binding.binding_fingerprint,
                seven_state_matrix.fingerprint,
                evaluator_report.report_fingerprint,
            )
        )
        provenance_activities.extend(
            (
                "seven-state-matched-perturbation-matrix",
                "orthogonal-evaluator-evidence",
            )
        )
        unresolved_gaps.extend(
            (
                "behavior-sensitive alignment evidence independent of matrix integrity",
                "general causal role of OTHER_MODEL / VALUE_CONFLICT_STATE / NORMATIVE_PROVENANCE / COUNTERFACTUAL_SELF_MODEL",
                "moral agency remains not established",
                "subjectivity remains not established",
            )
        )
        mechanism += (
            " The extended path also binds seven explicit state channels into a matched perturbation matrix; "
            "the original three retain the reused EGD causal surface while the additive four remain intervention-ready only. "
            "Orthogonal evaluator observations are then derived from exact matrix/control fingerprints without treating "
            "experiment integrity as evidence that any evaluated property is established."
        )

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
        "expected_outcomes": expected_outcomes,
        "observed_outcomes": observations,
        "result_status": "HOLD",
        "deviations": [],
        "limitations": limitations,
        "reviewer_status": "UNREVIEWED",
        "independent_validation_status": "IVV_NOT_ACHIEVED",
        "canonical_effect": BOUNDARY.canonical_effect,
        "provenance": {
            "entities": provenance_entities,
            "activities": provenance_activities,
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
            "unresolved_gap_refs": unresolved_gaps,
            "method_ref": "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
            "inference_stage": "OBSERVATION",
            "observation": "The bounded loop produced provenance-bearing cycles under fixed authority constraints.",
            "mechanism": mechanism,
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


def extended_run_to_research_evidence_record(
    report: ExtendedResearchRunReport,
    *,
    repository_commit: str,
    protocol_ref: str,
    protocol_hash: str,
    source_refs: tuple[str, ...],
) -> dict[str, Any]:
    """Materialize the extended run through the same v0.2.0 evidence semantics."""

    record = run_to_research_evidence_record(
        report.base_report,
        repository_commit=repository_commit,
        protocol_ref=protocol_ref,
        protocol_hash=protocol_hash,
        source_refs=source_refs,
        seven_state_matrix=report.perturbation_matrix,
    )
    record["claim_id"] = f"barl7:{report.extended_state_fingerprint[:24]}"
    record["model_or_runtime_ref"] = "existing-aion-astra-inquiry-egd-and-seven-state-binding-adapters"
    return record


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
