from __future__ import annotations

import pytest

from aion_multimodal_media import (
    AssetStatus, ExecutionGrant, GenerationRequest, MediaAsset, MediaExecutionPolicy, MediaKind, MediaOrigin,
)


def request() -> GenerationRequest:
    return GenerationRequest(
        request_id="img-001", media_kind=MediaKind.IMAGE,
        prompt="A controlled diagram-like research stimulus", provider="openai", model="gpt-image-2",
        parameters=(("size", "1024x1024"),), research_purpose="matched multimodal stimulus experiment",
    )


def grant(*, human_approved: bool = True, network_egress: bool = True) -> ExecutionGrant:
    return ExecutionGrant(
        grant_id="grant-001", approved_providers=("openai",), approved_media=(MediaKind.IMAGE,),
        human_approved=human_approved, network_egress=network_egress,
    )


def test_request_is_deterministic_and_credential_free() -> None:
    assert request().fingerprint == request().fingerprint
    assert len(request().fingerprint) == 64
    with pytest.raises(ValueError, match="raw credentials"):
        GenerationRequest(
            request_id="bad", media_kind=MediaKind.IMAGE, prompt="x", provider="openai", model="gpt-image-2",
            parameters=(("api_key", "do-not-record"),), research_purpose="test",
        )


def test_policy_fails_closed_without_approval_or_egress() -> None:
    policy = MediaExecutionPolicy(("api.openai.com",))
    decision = policy.evaluate(
        request(), grant(human_approved=False, network_egress=False),
        endpoint="https://api.openai.com/v1/images/generations",
    )
    assert not decision.allowed
    assert set(decision.reasons) == {"NETWORK_EGRESS_NOT_GRANTED", "HUMAN_APPROVAL_REQUIRED"}


def test_asset_requires_completed_hashed_output_and_preserves_nonclaims() -> None:
    asset = MediaAsset(
        asset_id="asset-001", request_fingerprint=request().fingerprint, media_kind=MediaKind.IMAGE,
        origin=MediaOrigin.PROVIDER_GENERATED,
        provider="openai", model="gpt-image-2", status=AssetStatus.SUCCEEDED, mime_type="image/png",
        content_uri="urn:sha256:" + "b" * 64, content_sha256="b" * 64,
    )
    assert asset.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert len(asset.fingerprint) == 64
    with pytest.raises(ValueError, match="only completed"):
        MediaAsset(
            asset_id="asset-pending", request_fingerprint=request().fingerprint, media_kind=MediaKind.IMAGE,
            origin=MediaOrigin.PROVIDER_GENERATED,
            provider="openai", model="gpt-image-2", status=AssetStatus.PROCESSING, mime_type="image/png",
            content_uri="urn:job:pending", content_sha256="b" * 64,
        )
