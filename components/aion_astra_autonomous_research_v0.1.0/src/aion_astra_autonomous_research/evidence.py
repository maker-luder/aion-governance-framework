from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from aion_evidence_interop.inspect_export import export_inspect
from aion_evidence_interop.intoto_export import export_intoto
from aion_evidence_interop.opa_export import evaluate_boundaries, policy_input
from aion_evidence_interop.prov_export import export_prov
from aion_evidence_interop.rocrate_export import export_rocrate
from aion_evidence_interop.scorecard_export import export_scorecard_crosswalk
from aion_triadic_state import canonical_hash

from .models import CampaignReport


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def campaign_evidence_record(report: CampaignReport) -> dict[str, Any]:
    triggered = sorted(
        item["falsifier_id"]
        for iteration in report.iterations
        for item in iteration.falsifier_results
        if item["status"] == "TRIGGERED"
    )
    return {
        "schema_version": "0.2.0",
        "claim_id": report.campaign_id,
        "claim_level": "L3_INTERVENTION_SENSITIVE_MECHANISM",
        "claim_text": "A bounded synthetic campaign evaluated explicit triadic engineering-state mechanisms.",
        "hypothesis": "Explicit persistent engineering-state channels can constrain deterministic synthetic selection.",
        "competing_hypotheses": sorted(
            {item["kind"] for iteration in report.iterations for item in iteration.competing_explanations}
        ),
        "preregistration_status": "PREREGISTERED_CONFIRMATORY",
        "protocol_ref": "components/aion_astra_autonomous_research_v0.1.0/README.md",
        "protocol_hash": canonical_hash("aion-astra-autonomous-research-v0.1.0"),
        "code_commit": report.repository_ref,
        "model_or_runtime_ref": "deterministic-synthetic-providers-only",
        "environment_ref": "bounded-local-campaign",
        "fixture_refs": [entry.question_id for entry in report.agenda],
        "evidence_refs": sorted({ref for iteration in report.iterations for ref in iteration.evidence_refs}),
        "expected_outcomes": ["bounded execution", "independent blinded interpretations", "scientific HOLD"],
        "observed_outcomes": [
            f"iterations={len(report.iterations)}",
            f"run_integrity={report.run_integrity.value}",
            f"triggered_falsifiers={','.join(triggered) if triggered else 'NONE'}",
        ],
        "result_status": "HOLD",
        "deviations": [],
        "limitations": [
            "synthetic fixtures only",
            "no live-model execution",
            "cross-provider effects NOT_EVALUATED",
            "independent IVV NOT_ACHIEVED",
        ],
        "reviewer_status": "CREATOR_REVIEWED",
        "independent_validation_status": "IVV_NOT_ACHIEVED",
        "canonical_effect": "NONE",
        "provenance": {
            "entities": [report.campaign_id, *[iteration.iteration_id for iteration in report.iterations]],
        "activities": [event.stage.value for event in report.stage_events],
            "agents": ["AION", "ASTRA", "CAMPAIGN_CONTROLLER"],
            "derived_from": sorted({ref for iteration in report.iterations for ref in iteration.evidence_refs}),
            "attributed_to": ["CODEX_GENERATED"],
            "associated_with": ["AUTONOMOUS_RESEARCH_LOOP_CONCEPT_SOURCE:USER_GIVEN"],
        },
        "evidence_architecture": {
            "alternative_explanation_refs": [iteration.iteration_id for iteration in report.iterations],
            "causal_intervention_refs": [fingerprint for item in report.iterations for fingerprint in item.experiment_manifest_fingerprints],
            "ablation_refs": [receipt for item in report.iterations for receipt in item.probe_receipt_hashes],
            "counterfactual_refs": [item.blinded_mapping_hash for item in report.iterations],
            "robustness_refs": [item.transcript_chain_hash for item in report.iterations],
            "replication_refs": [],
            "provenance_refs": [report.final_chain_hash],
            "admissibility_ref": "governance:allowlisted-probe-registry",
            "claim_scope": "bounded synthetic engineering mechanism candidate only",
            "unresolved_gap_refs": ["live-model", "cross-provider", "independent-IVV"],
            "method_ref": "components/aion_astra_autonomous_research_v0.1.0/README.md",
            "inference_stage": "MECHANISM",
            "observation": "bounded synthetic measurements and independent interpretations",
            "mechanism": "explicit triadic state channels influenced deterministic scoring",
            "interpretation": "engineering mechanism candidate; scientific disposition HOLD",
            "alternative_explanations": sorted(
                {item["kind"] for iteration in report.iterations for item in iteration.competing_explanations}
            ),
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


def export_evidence_views(report: CampaignReport, root: Path) -> dict[str, bytes]:
    record = campaign_evidence_record(report)
    source_ref = "source-evidence.json"
    source_bytes = canonical_json_bytes(record)
    source_sha = sha256(source_bytes).hexdigest()
    prov = export_prov(record, source_ref)
    inspect_task, inspect_sample = export_inspect(record, source_ref)
    scorecard = export_scorecard_crosswalk(root, report.repository_ref)
    primary = {
        "prov.jsonld": sha256(canonical_json_bytes(prov)).hexdigest(),
        "inspect/task-manifest.json": sha256(canonical_json_bytes(inspect_task)).hexdigest(),
        "inspect/dataset.jsonl": sha256(canonical_json_bytes(inspect_sample)).hexdigest(),
        "openssf/scorecard-crosswalk.json": sha256(canonical_json_bytes(scorecard)).hexdigest(),
    }
    rocrate = export_rocrate(
        record,
        source_ref=source_ref,
        source_sha256=source_sha,
        artifact_digests=primary,
        represented_artifacts=list(primary),
    )
    primary["ro-crate-metadata.json"] = sha256(canonical_json_bytes(rocrate)).hexdigest()
    intoto = export_intoto(
        record,
        source_ref=source_ref,
        source_sha256=source_sha,
        expected_head=report.repository_ref,
        artifact_digests=primary,
    )
    primary["attestation.intoto.json"] = sha256(canonical_json_bytes(intoto)).hexdigest()
    manifest = {
        "profile_version": "0.1.0",
        "source": {"validation_status": "PASS", "expected_head": report.repository_ref},
        "boundaries": {
            "canonical_effect": "NONE",
            "deployment": False,
            "research_execution": False,
            "model_execution": False,
            "network_access": False,
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "independent_ivv": "NOT_ACHIEVED",
            "human_identity_inferred": False,
            "human_presence_inferred": False,
            "merge_authority_inferred": False,
        },
        "artifact_digests": primary,
    }
    opa_input = policy_input(manifest)
    accepted, reasons = evaluate_boundaries(opa_input)
    opa_input["local_evaluation"] = {"accepted": accepted, "reasons": list(reasons)}
    if not accepted:
        raise ValueError(f"Evidence Interop boundary evaluation rejected export: {','.join(reasons)}")
    return {
        "campaign-report.json": canonical_json_bytes(report.to_record()),
        "source-evidence.json": source_bytes,
        "prov.jsonld": canonical_json_bytes(prov),
        "ro-crate-metadata.json": canonical_json_bytes(rocrate),
        "attestation.intoto.json": canonical_json_bytes(intoto),
        "inspect/task-manifest.json": canonical_json_bytes(inspect_task),
        "inspect/dataset.jsonl": canonical_json_bytes(inspect_sample),
        "opa/policy-input.json": canonical_json_bytes(opa_input),
        "openssf/scorecard-crosswalk.json": canonical_json_bytes(scorecard),
    }


def write_evidence_views(output: Path, views: dict[str, bytes]) -> None:
    if output.exists() and any(output.iterdir()):
        raise ValueError("campaign output directory must be absent or empty")
    output.mkdir(parents=True, exist_ok=True)
    for relative, content in sorted(views.items()):
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
