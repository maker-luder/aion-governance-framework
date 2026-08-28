from __future__ import annotations

from dataclasses import dataclass, field

from aion_multimodal_media import (
    AssetStatus, ExecutionGrant, GenerationRequest, HTTPRequest, HTTPResponse, MediaExecutionPolicy, MediaKind,
    Meshy3DAdapter, OpenAIImageAdapter, OpenAIVideoAdapter, Tripo3DAdapter,
)


@dataclass
class RecordingTransport:
    responses: list[HTTPResponse]
    requests: list[HTTPRequest] = field(default_factory=list)

    def send(self, request: HTTPRequest) -> HTTPResponse:
        self.requests.append(request)
        return self.responses.pop(0)


def grant(provider: str, kind: MediaKind) -> ExecutionGrant:
    return ExecutionGrant(
        grant_id=f"grant:{provider}:{kind.value}", approved_providers=(provider,), approved_media=(kind,),
        network_egress=True, human_approved=True,
    )


def request(provider: str, kind: MediaKind, model: str) -> GenerationRequest:
    return GenerationRequest(
        request_id=f"request:{provider}:{kind.value}", media_kind=kind, prompt="a low-poly research object",
        provider=provider, model=model, parameters=(("size", "1280x720"),) if kind is MediaKind.VIDEO else (),
        negative_prompt="text artifacts", seed=17, research_purpose="adapter contract test",
    )


def test_openai_image_request_contract() -> None:
    transport = RecordingTransport([HTTPResponse(200, {"created": 1, "data": [{"b64_json": "..."}]})])
    adapter = OpenAIImageAdapter(transport, MediaExecutionPolicy(("api.openai.com",)))
    job = adapter.submit(request("openai", MediaKind.IMAGE, "gpt-image-2"), grant("openai", MediaKind.IMAGE))
    sent = transport.requests[0]
    assert sent.url.endswith("/v1/images/generations")
    assert sent.json_body == {"model": "gpt-image-2", "prompt": "a low-poly research object"}
    assert sent.credential_env == "OPENAI_API_KEY"
    assert job.status is AssetStatus.SUCCEEDED


def test_openai_video_submission_and_poll_contract() -> None:
    transport = RecordingTransport([
        HTTPResponse(200, {"id": "video_123", "status": "queued"}),
        HTTPResponse(200, {"id": "video_123", "status": "completed"}),
    ])
    adapter = OpenAIVideoAdapter(transport, MediaExecutionPolicy(("api.openai.com",)))
    media_grant = grant("openai", MediaKind.VIDEO)
    job = adapter.submit(request("openai", MediaKind.VIDEO, "sora-2"), media_grant)
    assert dict(transport.requests[0].form_body) == {
        "model": "sora-2", "prompt": "a low-poly research object", "size": "1280x720",
    }
    completed = adapter.poll(job, media_grant)
    assert completed.status is AssetStatus.SUCCEEDED
    assert transport.requests[1].method == "GET"


def test_tripo_and_meshy_keep_distinct_3d_workflows() -> None:
    tripo_transport = RecordingTransport([HTTPResponse(200, {"code": 0, "data": {"task_id": "tripo-1"}})])
    tripo = Tripo3DAdapter(tripo_transport, MediaExecutionPolicy(("api.tripo3d.ai",)))
    tripo_job = tripo.submit(request("tripo3d", MediaKind.MODEL_3D, "P1-20260311"), grant("tripo3d", MediaKind.MODEL_3D))
    assert tripo_transport.requests[0].json_body == {
        "type": "text_to_model", "model_version": "P1-20260311", "prompt": "a low-poly research object",
        "negative_prompt": "text artifacts", "image_seed": 17,
    }
    assert tripo_job.provider_job_id == "tripo-1"

    meshy_transport = RecordingTransport([HTTPResponse(200, {"result": "meshy-1"})])
    meshy = Meshy3DAdapter(meshy_transport, MediaExecutionPolicy(("api.meshy.ai",)))
    meshy_job = meshy.submit(request("meshy", MediaKind.MODEL_3D, "latest"), grant("meshy", MediaKind.MODEL_3D))
    assert meshy_transport.requests[0].json_body == {
        "mode": "preview", "prompt": "a low-poly research object", "ai_model": "latest",
    }
    assert meshy_job.provider_job_id == "meshy-1"
