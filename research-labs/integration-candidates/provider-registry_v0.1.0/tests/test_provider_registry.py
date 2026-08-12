import pytest

from provider_registry import ProviderRegistry, ProviderRegistryError, ProviderSpec, SelectionPolicy


def test_selects_lowest_priority_then_symbolic_id():
    registry = ProviderRegistry(
        [
            ProviderSpec("loopback-b", frozenset({"chat"}), priority=20),
            ProviderSpec("local-a", frozenset({"chat", "embedding"}), priority=10),
            ProviderSpec("offline-c", frozenset({"chat"}), priority=10),
        ]
    )
    assert registry.select(SelectionPolicy(frozenset({"chat"}))).provider_id == "local-a"
    assert registry.select(SelectionPolicy(frozenset({"embedding"}))).provider_id == "local-a"


def test_rejects_unsatisfied_capability():
    registry = ProviderRegistry([ProviderSpec("local", frozenset({"chat"}))])
    with pytest.raises(ProviderRegistryError, match="no enabled provider"):
        registry.select(SelectionPolicy(frozenset({"vision"})))


def test_disabled_provider_is_not_selected():
    registry = ProviderRegistry([ProviderSpec("local", frozenset({"chat"}), enabled=False)])
    with pytest.raises(ProviderRegistryError, match="no enabled provider"):
        registry.select(SelectionPolicy(frozenset({"chat"})))


def test_duplicate_and_secret_metadata_fail_closed():
    registry = ProviderRegistry([ProviderSpec("local", frozenset())])
    with pytest.raises(ProviderRegistryError, match="duplicate"):
        registry.register(ProviderSpec("local", frozenset()))
    with pytest.raises(ProviderRegistryError, match="secret-like"):
        ProviderSpec("offline", frozenset(), metadata=(("api_key", "redacted"),)).validate()


def test_remote_locality_and_promotion_are_rejected():
    with pytest.raises(ProviderRegistryError, match="local"):
        ProviderSpec("remote", frozenset(), locality="remote").validate()
    with pytest.raises(ProviderRegistryError, match="canonical_effect"):
        ProviderSpec("bad", frozenset(), canonical_effect="WRITE").validate()
