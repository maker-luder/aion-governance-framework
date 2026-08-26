"""Deterministic adapter registry for the shared AION/Astra execution substrate.

Registry membership is configuration, not authority. Disabled or inspection-only
adapters fail closed when selected for live execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .dsh import profile as dsh_profile
from .models import SubstrateError
from .native import NATIVE_PROFILE_ID

NATIVE_ADAPTER_ID = "native-bounded-runtime"
NATIVE_EXECUTION_KIND = "NATIVE_BOUNDED"
INSPECTION_ONLY_KIND = "INSPECTION_ONLY"


class AdapterRegistryError(SubstrateError):
    """Raised when adapter registration or selection fails closed."""


@dataclass(frozen=True, slots=True)
class AdapterRegistration:
    """One deterministic adapter registry entry."""

    adapter_id: str
    profile_id: str
    execution_kind: str
    enabled: bool
    live_execution: bool
    network_access: bool
    developer_preview: bool
    reason: str = ""

    def __post_init__(self) -> None:
        for name, value in (
            ("adapter_id", self.adapter_id),
            ("profile_id", self.profile_id),
            ("execution_kind", self.execution_kind),
        ):
            if not value.strip():
                raise AdapterRegistryError(f"{name} is required")
        if self.enabled and not self.live_execution:
            raise AdapterRegistryError("enabled adapters must explicitly admit live execution")

    def to_dict(self) -> dict[str, object]:
        return {
            "adapter_id": self.adapter_id,
            "profile_id": self.profile_id,
            "execution_kind": self.execution_kind,
            "enabled": self.enabled,
            "live_execution": self.live_execution,
            "network_access": self.network_access,
            "developer_preview": self.developer_preview,
            "reason": self.reason,
        }


class AdapterRegistry:
    """Immutable registry used by both AION and Astra dispatch paths."""

    def __init__(self, registrations: Iterable[AdapterRegistration]) -> None:
        entries: dict[str, AdapterRegistration] = {}
        for registration in registrations:
            if registration.adapter_id in entries:
                raise AdapterRegistryError(
                    f"duplicate adapter registration: {registration.adapter_id}"
                )
            entries[registration.adapter_id] = registration
        if not entries:
            raise AdapterRegistryError("adapter registry cannot be empty")
        self._entries = entries

    def resolve(
        self,
        adapter_id: str,
        *,
        require_executable: bool = True,
    ) -> AdapterRegistration:
        key = adapter_id.strip()
        if not key:
            raise AdapterRegistryError("adapter_id is required")
        registration = self._entries.get(key)
        if registration is None:
            raise AdapterRegistryError(f"adapter is not registered: {key}")
        if not registration.enabled:
            reason = f": {registration.reason}" if registration.reason else ""
            raise AdapterRegistryError(f"adapter is disabled: {key}{reason}")
        if require_executable and not registration.live_execution:
            raise AdapterRegistryError(f"adapter does not admit live execution: {key}")
        return registration

    def get(self, adapter_id: str) -> AdapterRegistration:
        key = adapter_id.strip()
        if not key:
            raise AdapterRegistryError("adapter_id is required")
        registration = self._entries.get(key)
        if registration is None:
            raise AdapterRegistryError(f"adapter is not registered: {key}")
        return registration

    def snapshot(self) -> tuple[dict[str, object], ...]:
        return tuple(
            self._entries[key].to_dict()
            for key in sorted(self._entries)
        )

    def adapter_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._entries))


def build_default_registry() -> AdapterRegistry:
    """Build the bounded registry used by current AION/Astra Runtime instances."""

    dsh = dsh_profile()
    return AdapterRegistry(
        (
            AdapterRegistration(
                adapter_id=NATIVE_ADAPTER_ID,
                profile_id=NATIVE_PROFILE_ID,
                execution_kind=NATIVE_EXECUTION_KIND,
                enabled=True,
                live_execution=True,
                network_access=False,
                developer_preview=False,
                reason="repository-native bounded execution",
            ),
            AdapterRegistration(
                adapter_id=dsh.adapter_id,
                profile_id=dsh.profile_id,
                execution_kind=INSPECTION_ONLY_KIND,
                enabled=False,
                live_execution=False,
                network_access=False,
                developer_preview=dsh.developer_preview,
                reason="pinned DSH adapter is inspection-only; live DSH execution is not authorized",
            ),
        )
    )
