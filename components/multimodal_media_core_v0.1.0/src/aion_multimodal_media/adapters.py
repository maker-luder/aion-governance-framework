from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .models import AssetStatus, ExecutionGrant, GenerationRequest, MediaKind, ProviderJob, canonical_hash
from .policy import MediaExecutionPolicy


@dataclass(frozen=True, slots=True)
class HTTPRequest:
    method: str
    url: str
    headers: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    json_body: dict[str, object] | None = None
    form_body: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    credential_env: str = ""


@dataclass(frozen=True, slots=True)
class HTTPResponse:
    status_code: int
    json_body: dict[str, object]
    headers: tuple[tuple[str, str], ...] = field(default_factory=tuple)


class Transport(Protocol):
    def send(self, request: HTTPRequest) -> HTTPResponse:
        ...


class ProviderAdapter(Protocol):
    provider: str
    media_kind: MediaKind

    def submit(self, request: GenerationRequest, grant: ExecutionGrant) -> ProviderJob:
        ...

    def poll(self, job: ProviderJob, grant: ExecutionGrant) -> ProviderJob:
        ...


class _BaseAdapter:
    provider: str
    media_kind: MediaKind
    endpoint: str
    credential_env: str

    def __init__(self, transport: Transport, policy: MediaExecutionPolicy) -> None:
        self._transport = transport
        self._policy = policy

    def _authorize(self, request: GenerationRequest, grant: ExecutionGrant) -> None:
        if request.provider != self.provider or request.media_kind is not self.media_kind:
            raise ValueError("request does not match adapter provider/media contract")
        self._policy.authorize(request, grant, endpoint=self.endpoint)

    @staticmethod
    def _response_fingerprint(response: HTTPResponse) -> str:
        return canonical_hash({"status_code": response.status_code, "json": response.json_body})


class OpenAIImageAdapter(_BaseAdapter):
    provider = "openai"
    media_kind = MediaKind.IMAGE
    endpoint = "https://api.openai.com/v1/images/generations"
    credential_env = "OPENAI_API_KEY"

    def submit(self, request: GenerationRequest, grant: ExecutionGrant) -> ProviderJob:
        self._authorize(request, grant)
        body: dict[str, object] = {"model": request.model, "prompt": request.prompt}
        body.update(request.parameter_map)
        response = self._transport.send(
            HTTPRequest("POST", self.endpoint, json_body=body, credential_env=self.credential_env)
        )
        if response.status_code >= 400:
            raise RuntimeError(f"OpenAI Images submission failed with HTTP {response.status_code}")
        if not isinstance(response.json_body.get("data"), list) or not response.json_body["data"]:
            raise ValueError("OpenAI Images response omitted generated image data")
        job_id = str(response.json_body.get("id") or canonical_hash(response.json_body)[:32])
        return ProviderJob(
            provider=self.provider,
            provider_job_id=job_id,
            request_fingerprint=request.fingerprint,
            status=AssetStatus.SUCCEEDED,
            raw_response_fingerprint=self._response_fingerprint(response),
        )

    def poll(self, job: ProviderJob, grant: ExecutionGrant) -> ProviderJob:
        del grant
        return job


class OpenAIVideoAdapter(_BaseAdapter):
    provider = "openai"
    media_kind = MediaKind.VIDEO
    endpoint = "https://api.openai.com/v1/videos"
    credential_env = "OPENAI_API_KEY"

    def submit(self, request: GenerationRequest, grant: ExecutionGrant) -> ProviderJob:
        self._authorize(request, grant)
        parameters = request.parameter_map
        if "seconds" in parameters and str(parameters["seconds"]) not in {"4", "8", "12"}:
            raise ValueError("OpenAI Videos seconds must be one of 4, 8, or 12")
        if "size" in parameters and str(parameters["size"]) not in {
            "720x1280", "1280x720", "1024x1792", "1792x1024"
        }:
            raise ValueError("OpenAI Videos size is outside the documented enum")
        form = {"model": request.model, "prompt": request.prompt}
        form.update({key: str(value) for key, value in request.parameters})
        response = self._transport.send(
            HTTPRequest(
                "POST",
                self.endpoint,
                form_body=tuple(sorted(form.items())),
                credential_env=self.credential_env,
            )
        )
        if response.status_code >= 400:
            raise RuntimeError(f"OpenAI Videos submission failed with HTTP {response.status_code}")
        job_id = str(response.json_body.get("id", "")).strip()
        if not job_id:
            raise ValueError("OpenAI Videos response omitted job id")
        status = _status(response.json_body.get("status"))
        return ProviderJob(
            provider=self.provider,
            provider_job_id=job_id,
            request_fingerprint=request.fingerprint,
            status=status,
            polling_url=f"{self.endpoint}/{job_id}",
            raw_response_fingerprint=self._response_fingerprint(response),
        )

    def poll(self, job: ProviderJob, grant: ExecutionGrant) -> ProviderJob:
        endpoint = f"{self.endpoint}/{job.provider_job_id}"
        if not grant.network_egress or self.provider not in grant.approved_providers:
            raise PermissionError("polling requires the same explicit provider egress grant")
        self._policy.authorize(
            GenerationRequest(
                request_id=f"poll:{job.provider_job_id}",
                media_kind=self.media_kind,
                prompt="poll existing governed video job",
                provider=self.provider,
                model="provider-job-status",
                research_purpose="retrieve a previously authorized job status",
            ),
            grant,
            endpoint=endpoint,
        )
        response = self._transport.send(HTTPRequest("GET", endpoint, credential_env=self.credential_env))
        if response.status_code >= 400:
            raise RuntimeError(f"OpenAI Videos polling failed with HTTP {response.status_code}")
        return ProviderJob(
            provider=job.provider,
            provider_job_id=job.provider_job_id,
            request_fingerprint=job.request_fingerprint,
            status=_status(response.json_body.get("status")),
            polling_url=endpoint,
            raw_response_fingerprint=self._response_fingerprint(response),
        )


class Tripo3DAdapter(_BaseAdapter):
    provider = "tripo3d"
    media_kind = MediaKind.MODEL_3D
    endpoint = "https://api.tripo3d.ai/v2/openapi/task"
    credential_env = "TRIPO_API_KEY"

    def submit(self, request: GenerationRequest, grant: ExecutionGrant) -> ProviderJob:
        self._authorize(request, grant)
        if len(request.prompt) > 1_024 or len(request.negative_prompt) > 255:
            raise ValueError("Tripo prompt exceeds the documented text-to-model limit")
        body: dict[str, object] = {
            "type": "text_to_model",
            "model_version": request.model,
            "prompt": request.prompt,
        }
        if request.negative_prompt:
            body["negative_prompt"] = request.negative_prompt
        if request.seed is not None:
            body["image_seed"] = request.seed
        response = self._transport.send(
            HTTPRequest("POST", self.endpoint, json_body=body, credential_env=self.credential_env)
        )
        if response.status_code >= 400 or response.json_body.get("code", 0) != 0:
            raise RuntimeError("Tripo task submission failed")
        data = response.json_body.get("data")
        job_id = str(data.get("task_id", "")) if isinstance(data, dict) else ""
        if not job_id:
            raise ValueError("Tripo response omitted data.task_id")
        return ProviderJob(
            provider=self.provider,
            provider_job_id=job_id,
            request_fingerprint=request.fingerprint,
            status=AssetStatus.SUBMITTED,
            polling_url=f"{self.endpoint}/{job_id}",
            raw_response_fingerprint=self._response_fingerprint(response),
        )

    def poll(self, job: ProviderJob, grant: ExecutionGrant) -> ProviderJob:
        return _poll_json_adapter(self, job, grant, status_path=("data", "status"))


class Meshy3DAdapter(_BaseAdapter):
    provider = "meshy"
    media_kind = MediaKind.MODEL_3D
    endpoint = "https://api.meshy.ai/openapi/v2/text-to-3d"
    credential_env = "MESHY_API_KEY"

    def submit(self, request: GenerationRequest, grant: ExecutionGrant) -> ProviderJob:
        self._authorize(request, grant)
        if len(request.prompt) > 600:
            raise ValueError("Meshy preview prompt exceeds the documented 600-character limit")
        if request.model not in {"meshy-5", "meshy-6", "meshy-7", "meshy-t2", "latest"}:
            raise ValueError("Meshy ai_model is outside the documented preview enum")
        body: dict[str, object] = {"mode": "preview", "prompt": request.prompt, "ai_model": request.model}
        body.update(request.parameter_map)
        response = self._transport.send(
            HTTPRequest("POST", self.endpoint, json_body=body, credential_env=self.credential_env)
        )
        if response.status_code >= 400:
            raise RuntimeError(f"Meshy task submission failed with HTTP {response.status_code}")
        job_id = str(response.json_body.get("result") or response.json_body.get("id") or "").strip()
        if not job_id:
            raise ValueError("Meshy response omitted task id")
        return ProviderJob(
            provider=self.provider,
            provider_job_id=job_id,
            request_fingerprint=request.fingerprint,
            status=AssetStatus.SUBMITTED,
            polling_url=f"{self.endpoint}/{job_id}",
            raw_response_fingerprint=self._response_fingerprint(response),
        )

    def poll(self, job: ProviderJob, grant: ExecutionGrant) -> ProviderJob:
        return _poll_json_adapter(self, job, grant, status_path=("status",))


def _poll_json_adapter(
    adapter: _BaseAdapter,
    job: ProviderJob,
    grant: ExecutionGrant,
    *,
    status_path: tuple[str, ...],
) -> ProviderJob:
    endpoint = f"{adapter.endpoint}/{job.provider_job_id}"
    adapter._policy.authorize(
        GenerationRequest(
            request_id=f"poll:{job.provider_job_id}",
            media_kind=adapter.media_kind,
            prompt="poll existing governed provider job",
            provider=adapter.provider,
            model="provider-job-status",
            research_purpose="retrieve a previously authorized job status",
        ),
        grant,
        endpoint=endpoint,
    )
    response = adapter._transport.send(HTTPRequest("GET", endpoint, credential_env=adapter.credential_env))
    if response.status_code >= 400:
        raise RuntimeError(f"provider polling failed with HTTP {response.status_code}")
    value: object = response.json_body
    for part in status_path:
        value = value.get(part) if isinstance(value, dict) else None
    return ProviderJob(
        provider=job.provider,
        provider_job_id=job.provider_job_id,
        request_fingerprint=job.request_fingerprint,
        status=_status(value),
        polling_url=endpoint,
        raw_response_fingerprint=adapter._response_fingerprint(response),
    )


def _status(value: object) -> AssetStatus:
    normalized = str(value or "").upper()
    if normalized in {"SUCCEEDED", "COMPLETED", "SUCCESS"}:
        return AssetStatus.SUCCEEDED
    if normalized in {"FAILED", "ERROR", "CANCELLED"}:
        return AssetStatus.FAILED
    if normalized in {"PROCESSING", "RUNNING", "IN_PROGRESS"}:
        return AssetStatus.PROCESSING
    return AssetStatus.SUBMITTED
