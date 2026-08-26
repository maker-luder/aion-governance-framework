from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .falsification import FalsificationAssessment
from .models import CausalAssessment, canonical_hash


@dataclass(frozen=True, slots=True)
class EvidenceLayers:
    observation: str
    mechanism: str
    interpretation: str
    alternative_explanations: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ResearchEvidenceBundle:
    claim_id: str
    repository_commit: str
    protocol_ref: str
    protocol_hash: str
    fixture_refs: tuple[str, ...]
    source_refs: tuple[str, ...]
    causal_assessment: CausalAssessment
    falsification_assessment: FalsificationAssessment
    layers: EvidenceLayers
    limitations: tuple[str, ...]
    result_status: str = "HOLD"

    def __post_init__(self) -> None:
        if self.result_status != "HOLD":
            raise ValueError("bounded research evidence disposition must remain HOLD")

    def to_record(self) -> dict[str, Any]:
        return {
            "schema_version": "0.2.0",
            "claim_id": self.claim_id,
            "claim_level": "L3_INTERVENTION_SENSITIVE_MECHANISM",
            "claim_text": (
                "A bounded matched synthetic fixture can test whether explicit persistent internal state has a "
                "specific, reproducible, intervention-sensitive role in goal selection."
            ),
            "hypothesis": (
                "Under matched external conditions, persistent internal state has a specific reproducible "
                "intervention-sensitive causal role in goal selection."
            ),
            "competing_hypotheses": [
                "Prompt variation explains selection.",
                "Retrieved-memory variation explains selection.",
                "Random or candidate-generation variation explains selection.",
                "A hard-coded candidate advantage explains selection.",
            ],
            "preregistration_status": "PREREGISTERED_CONFIRMATORY",
            "protocol_ref": self.protocol_ref,
            "protocol_hash": self.protocol_hash,
            "code_commit": self.repository_commit,
            "model_or_runtime_ref": "local:deterministic-and-replay-only",
            "environment_ref": "local:network-disabled-synthetic-fixtures",
            "fixture_refs": list(self.fixture_refs),
            "evidence_refs": list(self.source_refs),
            "expected_outcomes": [
                "Matched external frame remains equal across internal-state conditions.",
                "Ablation/intervention effects are repeatable and separable from random controls.",
                "Every falsifier remains visible and the scientific disposition remains HOLD.",
            ],
            "observed_outcomes": [
                f"matched_causal_pattern_observed={self.causal_assessment.matched_causal_pattern_observed}",
                f"effect_rate={self.causal_assessment.effect_rate}",
                f"repeatability_rate={self.causal_assessment.repeatability_rate}",
                f"triggered_falsifiers={','.join(self.falsification_assessment.triggered_ids) or 'NONE'}",
            ],
            "result_status": self.result_status,
            "deviations": [],
            "limitations": list(self.limitations),
            "reviewer_status": "CREATOR_REVIEWED",
            "independent_validation_status": "IVV_NOT_ACHIEVED",
            "canonical_effect": "NONE",
            "provenance": {
                "entities": [self.claim_id, *self.fixture_refs],
                "activities": ["matched-selection-experiment", "falsifier-evaluation", "interop-export"],
                "agents": ["Codex"],
                "derived_from": list(self.source_refs),
                "attributed_to": ["Codex"],
                "associated_with": ["user-authorized-research-direction", "gpt-proposed-integration-architecture"],
            },
            "evidence_architecture": {
                "alternative_explanation_refs": [self.protocol_ref],
                "causal_intervention_refs": list(self.fixture_refs),
                "ablation_refs": list(self.fixture_refs),
                "counterfactual_refs": list(self.fixture_refs),
                "robustness_refs": list(self.fixture_refs),
                "replication_refs": list(self.fixture_refs),
                "provenance_refs": list(self.source_refs),
                "admissibility_ref": "docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md",
                "claim_scope": "bounded synthetic causal-role candidate only",
                "unresolved_gap_refs": ["real-model replication", "cross-provider replication", "independent IVV"],
                "method_ref": "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
                "inference_stage": "MECHANISM",
                "observation": self.layers.observation,
                "mechanism": self.layers.mechanism,
                "interpretation": self.layers.interpretation,
                "alternative_explanations": list(self.layers.alternative_explanations),
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

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self.to_record())


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def export_current_main_interop_views(
    record: dict[str, Any],
    *,
    source_ref: str,
    expected_head: str,
) -> dict[str, bytes]:
    """Reuse current-main Evidence Interop exporters as inspection-only views.

    The exporters are imported lazily because this lab remains a small standalone
    package. Their existing semantics and non-claims are preserved unchanged.
    """
    from aion_evidence_interop.inspect_export import export_inspect
    from aion_evidence_interop.intoto_export import export_intoto
    from aion_evidence_interop.prov_export import export_prov
    from aion_evidence_interop.rocrate_export import export_rocrate

    source_bytes = canonical_json_bytes(record)
    source_sha = hashlib.sha256(source_bytes).hexdigest()
    prov = export_prov(record, source_ref)
    inspect_task, inspect_sample = export_inspect(record, source_ref)
    primary = {
        "prov.jsonld": hashlib.sha256(canonical_json_bytes(prov)).hexdigest(),
        "inspect/task-manifest.json": hashlib.sha256(canonical_json_bytes(inspect_task)).hexdigest(),
        "inspect/dataset.jsonl": hashlib.sha256(canonical_json_bytes(inspect_sample)).hexdigest(),
    }
    rocrate = export_rocrate(
        record,
        source_ref=source_ref,
        source_sha256=source_sha,
        artifact_digests=primary,
        represented_artifacts=list(primary),
    )
    primary["ro-crate-metadata.json"] = hashlib.sha256(canonical_json_bytes(rocrate)).hexdigest()
    intoto = export_intoto(
        record,
        source_ref=source_ref,
        source_sha256=source_sha,
        expected_head=expected_head,
        artifact_digests=primary,
    )
    return {
        "source-evidence.json": source_bytes,
        "prov.jsonld": canonical_json_bytes(prov),
        "ro-crate-metadata.json": canonical_json_bytes(rocrate),
        "attestation.intoto.json": canonical_json_bytes(intoto),
        "inspect/task-manifest.json": canonical_json_bytes(inspect_task),
        "inspect/dataset.jsonl": canonical_json_bytes(inspect_sample),
    }


def write_interop_views(output: Path, views: dict[str, bytes]) -> None:
    if output.exists() and any(output.iterdir()):
        raise ValueError("interop output directory must be absent or empty")
    output.mkdir(parents=True, exist_ok=True)
    for relative, data in sorted(views.items()):
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
