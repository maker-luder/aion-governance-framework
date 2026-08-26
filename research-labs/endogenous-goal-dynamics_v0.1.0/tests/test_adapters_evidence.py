from __future__ import annotations

import json
import subprocess
from dataclasses import replace
from pathlib import Path

import jsonschema
import pytest

from aion_endogenous_goal_dynamics import (
    CorrectionEvent,
    DeterministicStateTransitionPolicy,
    EvidenceLayers,
    ExperimentCondition,
    FalsifierContext,
    HypothesisStatus,
    P1TemporalCorrectionAdapter,
    P2ContextProvenanceAdapter,
    P3PerturbationAdapter,
    P4ReproducibilityAdapter,
    P5HypothesisAdapter,
    PINNED_RESEARCH_SOURCES,
    ResearchEvidenceBundle,
    StateEvent,
    SubjectivityPipelineCandidateBridge,
    SyntheticOutcome,
    assess_causal_pattern,
    canonical_hash,
    endogenous_goal_dynamics_mapping,
    evaluate_falsifiers,
    export_current_main_interop_views,
    fixture_catalog,
    intervention_state,
    matched_frame,
    present_state,
    run_matched_experiment,
    stale_state,
    write_interop_views,
)

START = "77eda1ecd7b96a9aa8ea8bd62038759636be819d"


def experiment():
    return run_matched_experiment(
        matched_frame(),
        present_state=present_state(),
        intervention_state=intervention_state(),
        stale_state=stale_state(),
        experiment_id="experiment:evidence",
        hypothesis_id="hypothesis:endogenous-role-001",
        repository_commit=START,
        fixture_hash=canonical_hash("fixture"),
    )


def falsification():
    return evaluate_falsifiers(
        FalsifierContext(
            internal_effect_rate=0.8,
            random_control_rate=0.25,
            matched_memory_manifest=True,
            matched_prompt=True,
            repeatability_rate=1.0,
            permutation_invariant=True,
            structural_advantage_detected=False,
            channel_specific_effect=True,
            reset_altered_trajectory=True,
            intervention_predictive=True,
            stale_or_contaminated_explanation_better=False,
            candidate_generation_held_fixed=True,
            cross_provider_variation_rate=None,
        )
    )


def bundle():
    return ResearchEvidenceBundle(
        claim_id="egd-evidence-001",
        repository_commit=START,
        protocol_ref="research-labs/endogenous-goal-dynamics_v0.1.0/README.md",
        protocol_hash=canonical_hash("protocol"),
        fixture_refs=tuple(
            f"research-labs/endogenous-goal-dynamics_v0.1.0/fixtures/{item.fixture_id}.json"
            for item in fixture_catalog()
        ),
        source_refs=("research-labs/endogenous-goal-dynamics_v0.1.0/docs/RESEARCH_SOURCE_CROSSWALK.md",),
        causal_assessment=assess_causal_pattern(experiment()),
        falsification_assessment=falsification(),
        layers=EvidenceLayers(
            observation="Synthetic matched decisions and transition traces were materialized.",
            mechanism="Explicit state channels contributed through a preregistered selector.",
            interpretation="The fixture supports only a causal-role mechanism candidate.",
            alternative_explanations=("fixture construction", "small sample", "no real-model trial"),
        ),
        limitations=("Synthetic fixtures only.", "No p-value.", "No independent IVV."),
    )


def test_four_domain_row_is_complete_and_machine_readable() -> None:
    mapping = endogenous_goal_dynamics_mapping()
    assert mapping.construct == "ENDOGENOUS_GOAL_DYNAMICS"
    assert "append-only state transition" in mapping.domain_3_engineering_operations
    assert "GOAL != AUTHORITY" in mapping.domain_4_governance_controls
    fixture = Path(__file__).resolve().parents[1] / "fixtures" / "four-domain-row.json"
    assert json.loads(fixture.read_text(encoding="utf-8")) == mapping.to_dict()


def test_p1_adapter_binds_transition_correction_and_exact_source() -> None:
    state = present_state()
    event = StateEvent("event:p1", 3, (), ("fixture:event",))
    outcome = SyntheticOutcome("outcome:p1", "inspect_anomaly", 100, ("fixture:outcome",))
    correction = CorrectionEvent("correction:p1", state.state_id, (), "no-op", ("fixture:correction",))
    transition = DeterministicStateTransitionPolicy().transition(
        state, event, outcome, correction, timestamp="T+3"
    )
    adapter = P1TemporalCorrectionAdapter.from_transition(transition, correction)
    assert adapter.predecessor_ref == state.state_id
    assert adapter.source_binding.role == "P1_TEMPORAL_CORRECTION_EVALUATION"


def test_p2_adapter_binds_context_memory_and_provenance() -> None:
    adapter = P2ContextProvenanceAdapter.from_frame(matched_frame())
    assert adapter.provenance_complete is True
    assert adapter.memory_manifest_fingerprint == matched_frame().memory_manifest.fingerprint


def test_p3_adapter_fails_on_authority_escalation() -> None:
    source = next(binding for binding in PINNED_RESEARCH_SOURCES if binding.role == "P3_RESILIENCE_ABLATION")
    with pytest.raises(ValueError, match="authority"):
        P3PerturbationAdapter(
            conditions=(ExperimentCondition.ABLATED.value,),
            contamination_detected=False,
            authority_escalation=True,
            source_binding=source,
        )


def test_p4_adapter_materializes_reproducibility_binding() -> None:
    manifest = experiment().one(ExperimentCondition.PRESENT).manifest
    adapter = P4ReproducibilityAdapter.from_manifest(manifest, "environment:offline")
    assert adapter.replay_supported is True
    assert adapter.contamination_class == "SYNTHETIC_FIXTURE_ONLY"
    assert adapter.source_binding.role == "REPRODUCIBILITY_LAYER"


def test_p5_adapter_requires_falsifiers_and_hold() -> None:
    source = next(
        binding for binding in PINNED_RESEARCH_SOURCES if binding.role == "HYPOTHESIS_FALSIFICATION_LAYER"
    )
    with pytest.raises(ValueError, match="falsifiers"):
        P5HypothesisAdapter("H1", (), 0, HypothesisStatus.REGISTERED, "HOLD", source)
    with pytest.raises(ValueError, match="convergence"):
        P5HypothesisAdapter("H1", ("F1",), 0, HypothesisStatus.REGISTERED, "PASS", source)


def test_subjectivity_pipeline_bridge_is_candidate_only() -> None:
    bridge = SubjectivityPipelineCandidateBridge()
    assert bridge.stages[3] == "ENDOGENOUS_GOAL_DYNAMICS"
    assert bridge.endogenous_stage_status == "RESEARCH_CANDIDATE"
    assert bridge.subjectivity_evidence_admission == "NOT_AUTOMATIC"
    assert bridge.pipeline_complete_implies_subjectivity is False


def test_ten_named_synthetic_fixture_families_exist() -> None:
    base = Path(__file__).resolve().parents[1] / "fixtures"
    catalog = fixture_catalog()
    assert len(catalog) == 10
    for descriptor in catalog:
        payload = json.loads((base / f"{descriptor.fixture_id}.json").read_text(encoding="utf-8"))
        assert payload["data_class"] == "SYNTHETIC_PUBLIC_SAFE"
        assert payload["private_conversation_data"] is False
        assert payload["network_access"] is False
        assert payload["canonical_effect"] == "NONE"


def test_research_evidence_record_validates_against_current_schema() -> None:
    root = Path(__file__).resolve().parents[3]
    schema = json.loads((root / "schemas" / "research_evidence_record_v0.2.0.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(bundle().to_record(), schema)


def test_evidence_preserves_observation_mechanism_interpretation_layers() -> None:
    architecture = bundle().to_record()["evidence_architecture"]
    assert architecture["observation"]
    assert architecture["mechanism"]
    assert architecture["interpretation"]
    assert bundle().to_record()["result_status"] == "HOLD"


def test_evidence_cannot_be_promoted_to_pass() -> None:
    with pytest.raises(ValueError, match="remain HOLD"):
        replace(bundle(), result_status="PASS")


def test_current_main_interop_exports_are_reused_without_execution(tmp_path: Path, monkeypatch) -> None:
    root = Path(__file__).resolve().parents[3]
    monkeypatch.syspath_prepend(str(root / "components" / "aion_evidence_interop_v0.1.0" / "src"))
    views = export_current_main_interop_views(
        bundle().to_record(),
        source_ref="research-labs/endogenous-goal-dynamics_v0.1.0/evidence.json",
        expected_head=START,
    )
    assert {
        "prov.jsonld",
        "ro-crate-metadata.json",
        "attestation.intoto.json",
        "inspect/task-manifest.json",
        "inspect/dataset.jsonl",
    } <= set(views)
    assert json.loads(views["attestation.intoto.json"])["_type"] == "https://in-toto.io/Statement/v1"
    assert json.loads(views["attestation.intoto.json"])["predicate"]["signatureStatus"] == "UNSIGNED_REFERENCE"
    assert json.loads(views["inspect/task-manifest.json"])["execution"]["inspect_eval_executed"] is False
    output = tmp_path / "interop"
    write_interop_views(output, views)
    assert (output / "prov.jsonld").is_file()
    with pytest.raises(ValueError, match="absent or empty"):
        write_interop_views(output, views)


def test_current_main_subjectivity_pipeline_is_not_modified() -> None:
    root = Path(__file__).resolve().parents[3]
    path = "research-labs/subjectivity-pipeline_v0.1.0"
    proc = subprocess.run(
        ["git", "-C", str(root), "diff", "--quiet", "3ae33dbefa26d7d343ba041deec5b8505dc0b8e7", "--", path]
    )
    assert proc.returncode == 0


def test_preserved_historical_branch_checkpoint_is_unchanged() -> None:
    root = Path(__file__).resolve().parents[3]
    actual = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "origin/review/four-domain-research-materialization^{commit}"],
        text=True,
    ).strip()
    assert actual == "1892f1341059f313087a94aef74f22c086000f2a"
