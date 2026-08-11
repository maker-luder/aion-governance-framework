from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping, Protocol
from urllib.parse import urlparse


class ModelResponseKind(str, Enum):
    FINAL = "final"
    TOOL_CALLS = "tool_calls"
    RETRY = "retry"
    ERROR = "error"


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str = ""
    input_schema: Mapping[str, Any] = field(default_factory=dict)
    requires_sandbox: bool = False

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("tool name must be non-empty")


@dataclass(frozen=True)
class ToolCall:
    call_id: str
    name: str
    arguments: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.call_id.strip() or not self.name.strip():
            raise ValueError("tool call_id and name must be non-empty")


@dataclass(frozen=True)
class ModelRequest:
    messages: tuple[Mapping[str, Any], ...]
    tools: tuple[ToolSpec, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelResponse:
    kind: ModelResponseKind
    text: str = ""
    tool_calls: tuple[ToolCall, ...] = ()
    retry_reason: str | None = None
    usage: Mapping[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.kind is ModelResponseKind.TOOL_CALLS and not self.tool_calls:
            raise ValueError("tool_calls response requires at least one tool call")
        if self.kind is ModelResponseKind.FINAL and self.tool_calls:
            raise ValueError("final response cannot contain tool calls")


@dataclass(frozen=True)
class ProviderCapabilities:
    chat: bool = True
    tools: bool = False
    structured_output: bool = False
    streaming: bool = False
    cancellation: bool = False
    openai_compatible: bool = False
    local_only: bool = True
    context_window: int | None = None

    def __post_init__(self) -> None:
        if self.context_window is not None and self.context_window <= 0:
            raise ValueError("context_window must be positive")


_LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


@dataclass(frozen=True)
class EndpointProfile:
    profile_id: str
    provider_id: str
    model_id: str
    base_url: str
    capabilities: ProviderCapabilities
    api_style: str = "openai-compatible"

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.profile_id, self.provider_id, self.model_id, self.base_url)):
            raise ValueError("profile identifiers and base_url must be non-empty")
        parsed = urlparse(self.base_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("base_url must use http or https")
        host = parsed.hostname
        if self.capabilities.local_only and host not in _LOOPBACK_HOSTS:
            raise ValueError("local-only profile must use a loopback endpoint")

    @staticmethod
    def vllm(model_id: str, *, base_url: str = "http://127.0.0.1:8000/v1") -> "EndpointProfile":
        return EndpointProfile(
            profile_id=f"vllm:{model_id}",
            provider_id="vllm",
            model_id=model_id,
            base_url=base_url,
            capabilities=ProviderCapabilities(
                tools=True,
                structured_output=True,
                streaming=True,
                cancellation=True,
                openai_compatible=True,
                local_only=True,
            ),
        )

    @staticmethod
    def llama_cpp(model_id: str, *, base_url: str = "http://127.0.0.1:8080/v1") -> "EndpointProfile":
        return EndpointProfile(
            profile_id=f"llama.cpp:{model_id}",
            provider_id="llama.cpp",
            model_id=model_id,
            base_url=base_url,
            capabilities=ProviderCapabilities(
                tools=True,
                structured_output=True,
                streaming=True,
                cancellation=False,
                openai_compatible=True,
                local_only=True,
            ),
        )


class ProviderAdapter(Protocol):
    profile: EndpointProfile

    def complete(self, request: ModelRequest) -> ModelResponse:
        ...


class ScriptedProviderAdapter:
    """Offline deterministic provider used for tests and synthetic integration only."""

    def __init__(self, profile: EndpointProfile, responses: Iterable[ModelResponse]) -> None:
        self.profile = profile
        self._responses = list(responses)
        self.requests: list[ModelRequest] = []

    def complete(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        if not self._responses:
            return ModelResponse(ModelResponseKind.ERROR, text="script exhausted")
        return self._responses.pop(0)


@dataclass
class ProviderRegistry:
    _adapters: dict[str, ProviderAdapter] = field(default_factory=dict)

    def register(self, adapter: ProviderAdapter) -> None:
        profile_id = adapter.profile.profile_id
        if profile_id in self._adapters:
            raise ValueError(f"duplicate provider profile: {profile_id}")
        self._adapters[profile_id] = adapter

    def get(self, profile_id: str) -> ProviderAdapter:
        try:
            return self._adapters[profile_id]
        except KeyError as exc:
            raise KeyError(f"unknown provider profile: {profile_id}") from exc

    def select(self, *, require_tools: bool = False, require_structured_output: bool = False, local_only: bool = True) -> ProviderAdapter:
        for adapter in self._adapters.values():
            cap = adapter.profile.capabilities
            if local_only and not cap.local_only:
                continue
            if require_tools and not cap.tools:
                continue
            if require_structured_output and not cap.structured_output:
                continue
            return adapter
        raise LookupError("no provider profile satisfies the requested capabilities; no remote fallback is permitted")

    def profiles(self) -> tuple[EndpointProfile, ...]:
        return tuple(adapter.profile for adapter in self._adapters.values())
