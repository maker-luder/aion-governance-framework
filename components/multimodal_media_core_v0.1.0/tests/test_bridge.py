from __future__ import annotations

from dataclasses import dataclass

import pytest

from aion_multimodal_media import (
    AssetStatus, GenerationRequest, MediaAsset, MediaKind, MediaOrigin, MultimodalResearchBridge, ResearchRole,
)
from aion_research_integrity.models import EvidenceRecord
from aion_subjectivity_pipeline.engine import SubjectivityResearchPipeline
from aion_subjectivity_pipeline.evidence_dimensions import (
    DimensionObservation,
    EvidenceDisposition,
    SubjectivityEvidenceDimension,
    SubjectivityEvidenceMatrix,
)
from aion_subjectivity_pipeline.models import (
    FiniteIndividualityProfile,
    LongitudinalEpisode,
    PipelineStage,
    StageRecord,
)


@dataclass(frozen=True)
class Binding:
    binding_fingerprint: str = "2" * 64


@dataclass(frozen=True)
class Matrix:
    matrix_integrity_pass: bool = True
    fingerprint: str = "3" * 64
    binding: Binding = Binding()


@dataclass(frozen=True)
class Inquiry:
    final_chain_hash: str = "4" * 64
    scientific_disposition: str = "HOLD"


def subjectivity_matrix() -> SubjectivityEvidenceMatrix:
    return SubjectivityEvidenceMatrix(
        subject_ref="bounded-subject-001",
        protocol_ref="docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
        observations=tuple(
            DimensionObservation(
                dimension=dimension,
                disposition=EvidenceDisposition.NOT_TESTED,
                mechanism_ref="media-bridge:bounded-observation",
                evidence_refs=(),
                competing_explanations=("provider output may reflect prompt-conditioned generation only",),
            )
            for dimension in SubjectivityEvidenceDimension
        ),
    )


def asset() -> MediaAsset:
    request = GenerationRequest(
        request_id="video-bridge", media_kind=MediaKind.VIDEO, prompt="controlled transition stimulus",
        provider="openai", model="sora-2", research_purpose="seven-state matched perturbation replay",
    )
    return MediaAsset(
        asset_id="asset-video-1", request_fingerprint=request.fingerprint, media_kind=MediaKind.VIDEO,
        origin=MediaOrigin.PROVIDER_GENERATED,
        provider="openai", model="sora-2", status=AssetStatus.SUCCEEDED, mime_type="video/mp4",
        content_uri="urn:sha256:" + "1" * 64, content_sha256="1" * 64,
    )


def observed_asset() -> MediaAsset:
    return MediaAsset(
        asset_id="asset-observed-1", request_fingerprint="5" * 64, media_kind=MediaKind.VIDEO,
        origin=MediaOrigin.SENSOR_OBSERVED, provider="governed-capture-device", model="device-profile-1",
        status=AssetStatus.SUCCEEDED, mime_type="video/mp4",
        content_uri="urn:sha256:" + "6" * 64, content_sha256="6" * 64,
        source_type_uri="http://cv.iptc.org/newscodes/digitalsourcetype/digitalCapture",
    )


def test_bridge_binds_exact_existing_research_fingerprints() -> None:
    record = MultimodalResearchBridge().bind(
        observed_asset(), role=ResearchRole.COUNTERFACTUAL, research_run_ref="run:seven-state-media-1",
        evidence_refs=("evidence:matched-replay",),
        selector={"type": "FragmentSelector", "value": "t=2.0,4.0"}, seven_state_matrix=Matrix(),
        inquiry_report=Inquiry(), subject_ref="bounded-subject-001",
        subjectivity_evidence_matrix=subjectivity_matrix(),
    )
    assert record.seven_state_matrix_fingerprint == "3" * 64
    assert record.seven_state_binding_fingerprint == "2" * 64
    assert record.aion_astra_chain_hash == "4" * 64
    assert record.annotation["target"]["selector"]["value"] == "t=2.0,4.0"
    assert record.subjectivity_conclusion == "NOT_ESTABLISHED"
    admitted = EvidenceRecord(
        evidence_id=record.record_id, raw_hash=record.content_sha256,
        full_context_available=True, provenance_verified=True,
    )
    stage = MultimodalResearchBridge().to_subjectivity_stage_record(record, admitted, human_reviewed=True)
    assert stage.stage is PipelineStage.SUBJECTIVITY_EVIDENCE
    assert record.fingerprint in stage.evidence_refs
    assert subjectivity_matrix().fingerprint in stage.evidence_refs

    profile = FiniteIndividualityProfile(
        subject_ref="bounded-subject-001", identity_namespace="identity:bounded-subject-001",
        memory_namespace="memory:bounded-subject-001", lifecycle_epoch="epoch-1",
        context_budget=1024, persistent_memory_budget=128,
    )
    earlier = tuple(
        StageRecord(stage=item, record_ref=f"record:{item.value}", passed_governance=True)
        for item in tuple(PipelineStage)[:-1]
    )
    assessment = SubjectivityResearchPipeline().assess_episode(
        profile,
        LongitudinalEpisode(
            episode_id="episode-media-1", subject_ref=profile.subject_ref, ordinal=1, stages=(*earlier, stage),
        ),
        evidence_matrix=subjectivity_matrix(),
    )
    assert assessment.complete_stage_chain
    assert assessment.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_bridge_rejects_failed_seven_state_integrity() -> None:
    with pytest.raises(ValueError, match="matrix_integrity_pass"):
        MultimodalResearchBridge().bind(
            asset(), role=ResearchRole.COUNTERFACTUAL, research_run_ref="run:failed-matrix",
            evidence_refs=("evidence:x",),
            seven_state_matrix=Matrix(matrix_integrity_pass=False),
        )


def test_c2pa_reference_is_not_validation() -> None:
    record = MultimodalResearchBridge().bind(
        asset(), role=ResearchRole.STIMULUS, research_run_ref="run:provenance",
        evidence_refs=("evidence:content-hash",),
    )
    body = record.annotation["body"]
    assert body["c2paManifestRef"] is None
    assert body["c2paValidated"] is False


def test_generated_media_is_not_external_observation_or_admitted_subjectivity_evidence() -> None:
    bridge = MultimodalResearchBridge()
    with pytest.raises(ValueError, match="external empirical observation"):
        bridge.bind(
            asset(), role=ResearchRole.OBSERVATION, research_run_ref="run:invalid-observation",
            evidence_refs=("evidence:generated",),
        )

    record = bridge.bind(
        asset(), role=ResearchRole.STIMULUS, research_run_ref="run:prompt-controlled",
        evidence_refs=("evidence:generated",), subject_ref="bounded-subject-001",
        subjectivity_evidence_matrix=subjectivity_matrix(),
    )
    prompt_induced = EvidenceRecord(
        evidence_id=record.record_id, raw_hash=record.content_sha256,
        full_context_available=True, provenance_verified=True, prompt_induced=True,
    )
    with pytest.raises(ValueError, match="not direct subjectivity evidence"):
        bridge.to_subjectivity_stage_record(record, prompt_induced, human_reviewed=True)


def test_subjectivity_admission_requires_human_review_and_exact_hash() -> None:
    bridge = MultimodalResearchBridge()
    record = bridge.bind(
        observed_asset(), role=ResearchRole.OBSERVATION, research_run_ref="run:review-required",
        evidence_refs=("evidence:governed",), subject_ref="bounded-subject-001",
        subjectivity_evidence_matrix=subjectivity_matrix(),
    )
    admitted = EvidenceRecord(
        evidence_id=record.record_id, raw_hash=record.content_sha256,
        full_context_available=True, provenance_verified=True,
    )
    with pytest.raises(PermissionError, match="human review"):
        bridge.to_subjectivity_stage_record(record, admitted)
    mismatched = EvidenceRecord(
        evidence_id=record.record_id, raw_hash="f" * 64,
        full_context_available=True, provenance_verified=True,
    )
    with pytest.raises(ValueError, match="raw hash"):
        bridge.to_subjectivity_stage_record(record, mismatched, human_reviewed=True)
