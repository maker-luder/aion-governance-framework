from __future__ import annotations

import pytest

from aion_astra_agent_substrate import (
    AdapterRegistryError,
    NATIVE_ADAPTER_ID,
    build_default_registry,
    dsh_profile,
)


def test_default_registry_enables_native_and_holds_live_dsh() -> None:
    registry = build_default_registry()

    native = registry.resolve(NATIVE_ADAPTER_ID)
    assert native.enabled is True
    assert native.live_execution is True
    assert native.execution_kind == "NATIVE_BOUNDED"

    dsh = registry.get(dsh_profile().adapter_id)
    assert dsh.enabled is False
    assert dsh.live_execution is False
    assert dsh.execution_kind == "INSPECTION_ONLY"

    with pytest.raises(AdapterRegistryError):
        registry.resolve(dsh.adapter_id)


def test_registry_snapshot_is_deterministic_and_sorted() -> None:
    registry = build_default_registry()
    first = registry.snapshot()
    second = registry.snapshot()

    assert first == second
    assert [item["adapter_id"] for item in first] == sorted(registry.adapter_ids())
