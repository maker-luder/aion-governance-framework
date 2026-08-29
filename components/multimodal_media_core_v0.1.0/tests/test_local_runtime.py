from __future__ import annotations

import json

import pytest

from aion_multimodal_media import (
    ExecutionGrant,
    GenerationRequest,
    INTERNAL_PROCEDURAL_MODEL,
    InternalProceduralGenerator,
    LOCAL_PROVIDER,
    LocalMediaExecutionPolicy,
    LocalRuntimeSpec,
    MediaKind,
    MediaOrigin,
)


def request(kind: MediaKind, *, suffix: str = "a") -> GenerationRequest:
    return GenerationRequest(
        request_id=f"local-{kind.value.lower()}-{suffix}",
        media_kind=kind,
        prompt=f"deterministic local {kind.value.lower()} fixture {suffix}",
        provider=LOCAL_PROVIDER,
        model=INTERNAL_PROCEDURAL_MODEL,
        seed=17,
        research_purpose="offline multimodal generation contract test",
    )


def grant(kind: MediaKind, *, network_egress: bool = False, human_approved: bool = True) -> ExecutionGrant:
    return ExecutionGrant(
        grant_id=f"local-grant-{kind.value.lower()}",
        approved_providers=(LOCAL_PROVIDER,),
        approved_media=(kind,),
        network_egress=network_egress,
        human_approved=human_approved,
    )


@pytest.mark.parametrize(
    ("kind", "mime_type"),
    [
        (MediaKind.IMAGE, "image/x-portable-pixmap"),
        (MediaKind.VIDEO, "video/x-yuv4mpeg"),
        (MediaKind.MODEL_3D, "model/gltf+json"),
    ],
)
def test_internal_generator_produces_completed_local_assets(kind: MediaKind, mime_type: str) -> None:
    result = InternalProceduralGenerator().generate(request(kind), grant(kind))
    assert result.asset.origin is MediaOrigin.LOCAL_GENERATED
    assert result.asset.provider == LOCAL_PROVIDER
    assert result.asset.model == INTERNAL_PROCEDURAL_MODEL
    assert result.asset.mime_type == mime_type
    assert result.asset.content_uri == "urn:sha256:" + result.asset.content_sha256
    assert result.asset.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert len(result.runtime_fingerprint) == 64


def test_internal_generation_is_byte_deterministic() -> None:
    generator = InternalProceduralGenerator()
    first = generator.generate(request(MediaKind.IMAGE), grant(MediaKind.IMAGE))
    second = generator.generate(request(MediaKind.IMAGE), grant(MediaKind.IMAGE))
    changed = generator.generate(request(MediaKind.IMAGE, suffix="b"), grant(MediaKind.IMAGE))
    assert first.content == second.content
    assert first.asset.content_sha256 == second.asset.content_sha256
    assert first.content != changed.content


def test_internal_video_is_a_real_bounded_y4m_sequence() -> None:
    result = InternalProceduralGenerator().generate(request(MediaKind.VIDEO), grant(MediaKind.VIDEO))
    assert result.content.startswith(b"YUV4MPEG2 W16 H16 F4:1")
    assert result.content.count(b"FRAME\n") == 4


def test_internal_3d_is_valid_json_gltf_with_geometry() -> None:
    result = InternalProceduralGenerator().generate(request(MediaKind.MODEL_3D), grant(MediaKind.MODEL_3D))
    document = json.loads(result.content)
    assert document["asset"]["version"] == "2.0"
    assert document["asset"]["generator"] == "AION_INTERNAL_PROCEDURAL"
    assert document["meshes"][0]["primitives"][0]["attributes"]["POSITION"] == 0
    assert document["buffers"][0]["uri"].startswith("data:application/octet-stream;base64,")


def test_local_policy_requires_network_to_remain_off() -> None:
    policy = LocalMediaExecutionPolicy()
    decision = policy.evaluate(request(MediaKind.IMAGE), grant(MediaKind.IMAGE, network_egress=True))
    assert not decision.allowed
    assert "LOCAL_RUNTIME_REQUIRES_NETWORK_EGRESS_FALSE" in decision.reasons


def test_local_policy_still_requires_explicit_human_approval() -> None:
    policy = LocalMediaExecutionPolicy()
    decision = policy.evaluate(request(MediaKind.IMAGE), grant(MediaKind.IMAGE, human_approved=False))
    assert not decision.allowed
    assert "HUMAN_APPROVAL_REQUIRED" in decision.reasons


def test_runtime_descriptor_is_language_neutral_but_network_closed() -> None:
    rust_runtime = LocalRuntimeSpec(
        runtime_id="example-rust-runtime",
        language="Rust",
        engine="CANDLE_COMPATIBLE_LOCAL_RUNTIME",
        supported_media=(MediaKind.IMAGE,),
        model_ref="local-model-ref",
        license_ref="model-license-ref",
        interface="JSON_STDIO",
    )
    assert rust_runtime.language == "Rust"
    assert not rust_runtime.network_access
    with pytest.raises(ValueError, match="LOCAL_RUNTIME_NETWORK_ACCESS"):
        LocalRuntimeSpec(
            runtime_id="bad-runtime",
            language="C++",
            engine="native",
            supported_media=(MediaKind.IMAGE,),
            model_ref="model",
            license_ref="license",
            interface="JSON_STDIO",
            network_access=True,
        )
