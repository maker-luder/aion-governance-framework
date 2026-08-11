import pytest

from aion_runtime_v2.provider import EndpointProfile, ModelResponse, ModelResponseKind, ProviderCapabilities, ProviderRegistry, ScriptedProviderAdapter


def test_local_profile_rejects_remote_endpoint():
    with pytest.raises(ValueError):
        EndpointProfile("p", "provider", "model", "https://example.com/v1", ProviderCapabilities(local_only=True))


def test_registry_fails_without_remote_fallback():
    registry = ProviderRegistry()
    remote = EndpointProfile("remote", "provider", "model", "https://example.com/v1", ProviderCapabilities(local_only=False, tools=True))
    registry.register(ScriptedProviderAdapter(remote, [ModelResponse(ModelResponseKind.FINAL, text="x")]))
    with pytest.raises(LookupError):
        registry.select(require_tools=True, local_only=True)


def test_builtin_local_profiles():
    assert EndpointProfile.vllm("m").base_url == "http://127.0.0.1:8000/v1"
    assert EndpointProfile.llama_cpp("m").base_url == "http://127.0.0.1:8080/v1"
    assert EndpointProfile.vllm("m").capabilities.tools is True
