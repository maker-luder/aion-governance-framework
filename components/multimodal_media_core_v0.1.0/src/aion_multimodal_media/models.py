from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from hashlib import sha256
import json
from urllib.parse import urlparse


class MediaKind(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    MODEL_3D = "MODEL_3D"


class AssetStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    PROCESSING = "PROCESSING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class MediaOrigin(str, Enum):
    PROVIDER_GENERATED = "PROVIDER_GENERATED"
    SENSOR_OBSERVED = "SENSOR_OBSERVED"
    IMPORTED = "IMPORTED"


class ResearchRole(str, Enum):
    OBSERVATION = "OBSERVATION"
    STIMULUS = "STIMULUS"
    INTERVENTION = "INTERVENTION"
    CONTROL = "CONTROL"
    COUNTERFACTUAL = "COUNTERFACTUAL"


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()


def _require_nonempty(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)


@dataclass(frozen=True, slots=True)
class ExecutionGrant:
    grant_id: str
    approved_providers: tuple[str, ...]
    approved_media: tuple[MediaKind, ...]
    max_submissions: int = 1
    network_egress: bool = False
    human_approved: bool = False
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        _require_nonempty("grant_id", self.grant_id)
        if not self.approved_providers or not self.approved_media:
            raise ValueError("execution grant requires explicit provider and media allowlists")
        if self.max_submissions <= 0:
            raise ValueError("max_submissions must be positive")
        if self.canonical_effect != "NONE":
            raise ValueError("MEDIA_EXECUTION_GRANT != CANONICAL_AUTHORITY")


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    request_id: str
    media_kind: MediaKind
    prompt: str
    provider: str
    model: str
    parameters: tuple[tuple[str, str | int | float | bool], ...] = field(default_factory=tuple)
    input_asset_uris: tuple[str, ...] = field(default_factory=tuple)
    negative_prompt: str = ""
    seed: int | None = None
    research_purpose: str = ""
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        for name in ("request_id", "prompt", "provider", "model", "research_purpose"):
            _require_nonempty(name, getattr(self, name))
        keys = tuple(item[0] for item in self.parameters)
        if len(keys) != len(set(keys)) or any(not key.strip() for key in keys):
            raise ValueError("request parameters require unique non-empty keys")
        if any(key.lower() in {"api_key", "authorization", "token", "secret"} for key in keys):
            raise ValueError("raw credentials must not enter the research request or evidence record")
        for uri in self.input_asset_uris:
            parsed = urlparse(uri)
            if parsed.scheme not in {"https", "urn"}:
                raise ValueError("input assets require https or immutable urn references")
        if self.action_authority != "NONE" or self.canonical_effect != "NONE":
            raise ValueError("MEDIA_REQUEST != ACTION_OR_CANONICAL_AUTHORITY")

    @property
    def parameter_map(self) -> dict[str, str | int | float | bool]:
        return dict(self.parameters)

    @property
    def fingerprint(self) -> str:
        return canonical_hash(asdict(self))


@dataclass(frozen=True, slots=True)
class ProviderJob:
    provider: str
    provider_job_id: str
    request_fingerprint: str
    status: AssetStatus
    polling_url: str = ""
    retry_after_seconds: int | None = None
    raw_response_fingerprint: str = ""

    def __post_init__(self) -> None:
        for name in ("provider", "provider_job_id", "request_fingerprint"):
            _require_nonempty(name, getattr(self, name))
        if not _is_sha256(self.request_fingerprint):
            raise ValueError("provider job must bind the exact request fingerprint")
        if self.retry_after_seconds is not None and self.retry_after_seconds < 0:
            raise ValueError("retry_after_seconds cannot be negative")


@dataclass(frozen=True, slots=True)
class MediaAsset:
    asset_id: str
    request_fingerprint: str
    media_kind: MediaKind
    origin: MediaOrigin
    provider: str
    model: str
    status: AssetStatus
    mime_type: str
    content_uri: str
    content_sha256: str
    provider_job_id: str = ""
    source_type_uri: str = "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"
    c2pa_manifest_ref: str = ""
    c2pa_validated: bool = False
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        for name in ("asset_id", "request_fingerprint", "provider", "model", "mime_type", "content_uri"):
            _require_nonempty(name, getattr(self, name))
        if self.status is not AssetStatus.SUCCEEDED:
            raise ValueError("only completed media can become MediaAsset evidence")
        if not _is_sha256(self.request_fingerprint) or not _is_sha256(self.content_sha256):
            raise ValueError("media evidence requires 64-hex request and content digests")
        if urlparse(self.content_uri).scheme not in {"https", "urn"}:
            raise ValueError("media evidence content URI requires https or an immutable urn")
        if self.media_kind is MediaKind.IMAGE and not self.mime_type.startswith("image/"):
            raise ValueError("image asset requires an image MIME type")
        if self.media_kind is MediaKind.VIDEO and not self.mime_type.startswith("video/"):
            raise ValueError("video asset requires a video MIME type")
        if self.media_kind is MediaKind.MODEL_3D and self.mime_type not in {
            "model/gltf+json",
            "model/gltf-binary",
            "model/vnd.usdz+zip",
            "application/octet-stream",
        }:
            raise ValueError("3D evidence must use a declared interoperable model media type")
        if self.c2pa_validated and not self.c2pa_manifest_ref.strip():
            raise ValueError("validated C2PA provenance requires an exact manifest reference")
        if self.c2pa_manifest_ref and urlparse(self.c2pa_manifest_ref).scheme not in {"https", "urn"}:
            raise ValueError("C2PA manifest reference requires https or an immutable urn")
        if self.action_authority != "NONE" or self.canonical_effect != "NONE":
            raise ValueError("MEDIA_ASSET != ACTION_OR_CANONICAL_AUTHORITY")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("GENERATED_MEDIA != SUBJECTIVITY_EVIDENCE_CONCLUSION")
        synthetic_source = self.source_type_uri.endswith("/trainedAlgorithmicMedia")
        if self.origin is MediaOrigin.PROVIDER_GENERATED and not synthetic_source:
            raise ValueError("provider-generated media requires an explicit synthetic source type")
        if self.origin is MediaOrigin.SENSOR_OBSERVED and synthetic_source:
            raise ValueError("sensor-observed media cannot declare a generated source type")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(asdict(self))
