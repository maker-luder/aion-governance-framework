from __future__ import annotations

import base64
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import struct

from .models import (
    AssetStatus,
    ExecutionGrant,
    GenerationRequest,
    MediaAsset,
    MediaKind,
    MediaOrigin,
    canonical_hash,
)
from .policy import PolicyDecision


LOCAL_PROVIDER = "aion-local"
INTERNAL_PROCEDURAL_MODEL = "aion-internal-procedural-v0.1.0"


@dataclass(frozen=True, slots=True)
class LocalRuntimeSpec:
    runtime_id: str
    language: str
    engine: str
    supported_media: tuple[MediaKind, ...]
    model_ref: str
    license_ref: str
    interface: str = "DIRECT_PYTHON"
    network_access: bool = False
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        for name in ("runtime_id", "language", "engine", "model_ref", "license_ref", "interface"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if not self.supported_media or len(set(self.supported_media)) != len(self.supported_media):
            raise ValueError("local runtime requires a non-empty unique media capability set")
        if self.network_access:
            raise ValueError("LOCAL_RUNTIME_NETWORK_ACCESS = FALSE")
        if self.canonical_effect != "NONE":
            raise ValueError("LOCAL_RUNTIME != CANONICAL_AUTHORITY")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(asdict(self))


@dataclass(frozen=True, slots=True)
class LocalGenerationResult:
    asset: MediaAsset
    content: bytes
    runtime_fingerprint: str

    def __post_init__(self) -> None:
        if sha256(self.content).hexdigest() != self.asset.content_sha256:
            raise ValueError("local result bytes must match MediaAsset content_sha256")
        if len(self.runtime_fingerprint) != 64:
            raise ValueError("local result must bind an exact runtime fingerprint")


@dataclass(frozen=True, slots=True)
class LocalMediaExecutionPolicy:
    max_prompt_chars: int = 4_000
    require_human_approval: bool = True

    def evaluate(self, request: GenerationRequest, grant: ExecutionGrant) -> PolicyDecision:
        reasons: list[str] = []
        if request.provider != LOCAL_PROVIDER:
            reasons.append("LOCAL_PROVIDER_REQUIRED")
        if request.provider not in grant.approved_providers:
            reasons.append("PROVIDER_NOT_GRANTED")
        if request.media_kind not in grant.approved_media:
            reasons.append("MEDIA_KIND_NOT_GRANTED")
        if grant.network_egress:
            reasons.append("LOCAL_RUNTIME_REQUIRES_NETWORK_EGRESS_FALSE")
        if self.require_human_approval and not grant.human_approved:
            reasons.append("HUMAN_APPROVAL_REQUIRED")
        if len(request.prompt) > self.max_prompt_chars:
            reasons.append("PROMPT_LIMIT_EXCEEDED")
        return PolicyDecision(
            allowed=not reasons,
            reasons=tuple(reasons),
            request_fingerprint=request.fingerprint,
            grant_id=grant.grant_id,
        )

    def authorize(self, request: GenerationRequest, grant: ExecutionGrant) -> PolicyDecision:
        decision = self.evaluate(request, grant)
        if not decision.allowed:
            raise PermissionError("local media execution denied: " + ",".join(decision.reasons))
        return decision


class InternalProceduralGenerator:
    """Deterministic offline generator used as the executable local reference path.

    It intentionally produces tiny synthetic artifacts rather than photorealistic model output.
    The purpose is to prove that image/video/3D generation can occur entirely inside the
    governed local substrate with no provider, credential, model download, or network call.
    """

    provider = LOCAL_PROVIDER
    runtime = LocalRuntimeSpec(
        runtime_id="aion-local-procedural-runtime-v0.1.0",
        language="Python",
        engine="AION_INTERNAL_PROCEDURAL",
        supported_media=(MediaKind.IMAGE, MediaKind.VIDEO, MediaKind.MODEL_3D),
        model_ref=INTERNAL_PROCEDURAL_MODEL,
        license_ref="repository-license",
    )

    def __init__(self, policy: LocalMediaExecutionPolicy | None = None) -> None:
        self._policy = policy or LocalMediaExecutionPolicy()

    def generate(self, request: GenerationRequest, grant: ExecutionGrant) -> LocalGenerationResult:
        self._policy.authorize(request, grant)
        if request.model != self.runtime.model_ref:
            raise ValueError("request model must match the declared internal procedural runtime")
        if request.media_kind not in self.runtime.supported_media:
            raise ValueError("local runtime does not support requested media kind")

        if request.media_kind is MediaKind.IMAGE:
            content, mime_type = self._generate_ppm(request), "image/x-portable-pixmap"
        elif request.media_kind is MediaKind.VIDEO:
            content, mime_type = self._generate_y4m(request), "video/x-yuv4mpeg"
        else:
            content, mime_type = self._generate_gltf(request), "model/gltf+json"

        content_sha = sha256(content).hexdigest()
        asset = MediaAsset(
            asset_id=f"local:{request.request_id}:{content_sha[:16]}",
            request_fingerprint=request.fingerprint,
            media_kind=request.media_kind,
            origin=MediaOrigin.LOCAL_GENERATED,
            provider=self.provider,
            model=self.runtime.model_ref,
            status=AssetStatus.SUCCEEDED,
            mime_type=mime_type,
            content_uri=f"urn:sha256:{content_sha}",
            content_sha256=content_sha,
        )
        return LocalGenerationResult(asset=asset, content=content, runtime_fingerprint=self.runtime.fingerprint)

    @staticmethod
    def _seed_bytes(request: GenerationRequest) -> bytes:
        seed_suffix = "" if request.seed is None else f":{request.seed}"
        return sha256((request.fingerprint + seed_suffix).encode("utf-8")).digest()

    @classmethod
    def _generate_ppm(cls, request: GenerationRequest) -> bytes:
        width = 32
        height = 32
        seed = cls._seed_bytes(request)
        pixels = bytearray()
        for y in range(height):
            for x in range(width):
                base = seed[(x + y * 3) % len(seed)]
                pixels.extend(((base + x * 7) % 256, (base + y * 11) % 256, (base + x + y) % 256))
        return f"P6\n{width} {height}\n255\n".encode("ascii") + bytes(pixels)

    @classmethod
    def _generate_y4m(cls, request: GenerationRequest) -> bytes:
        width = 16
        height = 16
        frame_count = 4
        seed = cls._seed_bytes(request)
        out = bytearray(b"YUV4MPEG2 W16 H16 F4:1 Ip A1:1 C420jpeg\n")
        for frame in range(frame_count):
            out.extend(b"FRAME\n")
            y_value = (seed[frame] + frame * 23) % 256
            u_value = (seed[frame + 4] + 64) % 256
            v_value = (seed[frame + 8] + 128) % 256
            out.extend(bytes([y_value]) * (width * height))
            out.extend(bytes([u_value]) * (width * height // 4))
            out.extend(bytes([v_value]) * (width * height // 4))
        return bytes(out)

    @classmethod
    def _generate_gltf(cls, request: GenerationRequest) -> bytes:
        seed = cls._seed_bytes(request)
        scale = 0.5 + seed[0] / 510.0
        vertices = (
            (-scale, -scale, 0.0),
            (scale, -scale, 0.0),
            (0.0, scale, 0.0),
        )
        vertex_bytes = b"".join(struct.pack("<fff", *vertex) for vertex in vertices)
        index_bytes = struct.pack("<HHH", 0, 1, 2)
        payload = vertex_bytes + index_bytes
        encoded = base64.b64encode(payload).decode("ascii")
        gltf = {
            "asset": {"version": "2.0", "generator": "AION_INTERNAL_PROCEDURAL"},
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{"mesh": 0, "name": f"AION-{request.fingerprint[:8]}"}],
            "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1}]}],
            "buffers": [{"byteLength": len(payload), "uri": f"data:application/octet-stream;base64,{encoded}"}],
            "bufferViews": [
                {"buffer": 0, "byteOffset": 0, "byteLength": len(vertex_bytes), "target": 34962},
                {"buffer": 0, "byteOffset": len(vertex_bytes), "byteLength": len(index_bytes), "target": 34963},
            ],
            "accessors": [
                {
                    "bufferView": 0,
                    "componentType": 5126,
                    "count": 3,
                    "type": "VEC3",
                    "min": [-scale, -scale, 0.0],
                    "max": [scale, scale, 0.0],
                },
                {"bufferView": 1, "componentType": 5123, "count": 3, "type": "SCALAR"},
            ],
        }
        return (json.dumps(gltf, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
