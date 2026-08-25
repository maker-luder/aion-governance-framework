"""Offline model-provider metadata and deterministic selection contract."""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


class ProviderRegistryError(ValueError):
    pass


_SECRET = re.compile(r"(token|secret|password|cookie|credential|api[_-]?key)", re.I)


@dataclass(frozen=True)
class ProviderSpec:
    provider_id: str
    capabilities: frozenset[str]
    locality: str = "local"
    priority: int = 100
    enabled: bool = True
    metadata: tuple[tuple[str, str], ...] = ()
    canonical_effect: str = "NONE"
    deployment: bool = False

    def validate(self) -> None:
        if not self.provider_id or any(char.isspace() for char in self.provider_id):
            raise ProviderRegistryError("provider_id must be symbolic")
        if self.locality not in {"local", "loopback", "offline"}:
            raise ProviderRegistryError("provider locality must remain local/loopback/offline")
        if self.priority < 0:
            raise ProviderRegistryError("priority must be non-negative")
        if any(_SECRET.search(key) or _SECRET.search(value) for key, value in self.metadata):
            raise ProviderRegistryError("secret-like metadata is prohibited")
        if self.canonical_effect != "NONE":
            raise ProviderRegistryError("canonical_effect must remain NONE")
        if self.deployment:
            raise ProviderRegistryError("deployment must remain false")


@dataclass(frozen=True)
class SelectionPolicy:
    required_capabilities: frozenset[str] = frozenset()
    allowed_localities: frozenset[str] = frozenset({"local", "loopback", "offline"})


class ProviderRegistry:
    def __init__(self, providers: Iterable[ProviderSpec] = ()) -> None:
        self._providers: dict[str, ProviderSpec] = {}
        for provider in providers:
            self.register(provider)

    def register(self, provider: ProviderSpec) -> None:
        provider.validate()
        if provider.provider_id in self._providers:
            raise ProviderRegistryError(f"duplicate provider: {provider.provider_id}")
        self._providers[provider.provider_id] = provider

    def list(self) -> tuple[ProviderSpec, ...]:
        return tuple(sorted(self._providers.values(), key=lambda item: (item.priority, item.provider_id)))

    def select(self, policy: SelectionPolicy) -> ProviderSpec:
        candidates = [
            provider for provider in self.list()
            if provider.enabled
            and provider.locality in policy.allowed_localities
            and policy.required_capabilities.issubset(provider.capabilities)
        ]
        if not candidates:
            raise ProviderRegistryError("no enabled provider satisfies policy")
        return candidates[0]

    def capabilities(self, provider_id: str) -> frozenset[str]:
        try:
            return self._providers[provider_id].capabilities
        except KeyError as exc:
            raise ProviderRegistryError(f"unknown provider: {provider_id}") from exc
