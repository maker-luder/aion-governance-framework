"""Local reasoning-provider boundaries. No provider may apply changes."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Protocol
from urllib.parse import urlparse

from .errors import ValidationError


class ReasoningProvider(Protocol):
    def reason(self, prompt: str) -> str:
        """Return advisory text only."""


@dataclass(frozen=True)
class DeterministicTestProvider:
    response: str

    def reason(self, prompt: str) -> str:
        return self.response


@dataclass(frozen=True)
class OwnerSuppliedResponseProvider:
    response: str

    def reason(self, prompt: str) -> str:
        if not self.response:
            raise ValidationError("Owner-supplied response is empty")
        return self.response


@dataclass(frozen=True)
class LocalhostModelProvider:
    endpoint: str = "http://127.0.0.1:11434"
    enabled: bool = False

    def __post_init__(self) -> None:
        parsed = urlparse(self.endpoint)
        if parsed.hostname not in {"127.0.0.1", "::1", "localhost"}:
            raise ValidationError("local model endpoint must be loopback-only")

    def reason(self, prompt: str) -> str:
        if not self.enabled:
            raise ValidationError("localhost model provider is disabled")
        raise ValidationError("live local reasoning validation was not executed")


def external_input_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
