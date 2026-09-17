import pytest

from aion_human_ai_longitudinal.execution_profile import (
    BindingState,
    ExecutionLayer,
    ExecutionLayerBinding,
    ExecutionProfile,
    compare_execution_profiles,
)
from aion_human_ai_longitudinal.harness import StudyError


A = "a" * 64
B = "b" * 64
COMMIT = "1" * 40


def layer(layer_id, digest=A, state=BindingState.KNOWN):
    return ExecutionLayerBinding(
        layer=layer_id,
        state=state,
        binding_sha256=digest if state is BindingState.KNOWN else None,
    )


def profile(profile_id, overrides=None):
    overrides = overrides or {}
    layers = tuple(overrides.get(layer_id, layer(layer_id)) for layer_id in ExecutionLayer)
    return ExecutionProfile(
        profile_id=profile_id,
        repository_commit=COMMIT,
        layers=layers,
        source_refs=(f"fixture:{profile_id}",),
    )


def test_profile_diff_separates_changed_from_unknown_layers():
    right = profile(
        "right",
        {
            ExecutionLayer.HARNESS: layer(ExecutionLayer.HARNESS, digest=B),
            ExecutionLayer.MODEL: layer(ExecutionLayer.MODEL, state=BindingState.UNKNOWN),
        },
    )
    diff = compare_execution_profiles(profile("left"), right)
    assert diff.changed_layers == (ExecutionLayer.HARNESS,)
    assert diff.unknown_layers == (ExecutionLayer.MODEL,)
    assert diff.model_capability_ordering == "NOT_ESTABLISHED"


def test_unknown_layer_requires_no_binding_digest():
    with pytest.raises(StudyError, match="UNKNOWN execution layer cannot carry"):
        ExecutionLayerBinding(
            layer=ExecutionLayer.MODEL,
            state=BindingState.UNKNOWN,
            binding_sha256=A,
        )


def test_known_layer_requires_binding_digest():
    with pytest.raises(StudyError, match="KNOWN execution layer requires"):
        ExecutionLayerBinding(
            layer=ExecutionLayer.MODEL,
            state=BindingState.KNOWN,
            binding_sha256=None,
        )


def test_profile_requires_every_layer():
    with pytest.raises(StudyError, match="must declare every execution layer"):
        ExecutionProfile(
            profile_id="partial",
            repository_commit=COMMIT,
            layers=(layer(ExecutionLayer.MODEL),),
            source_refs=("fixture:partial",),
        )


def test_profile_comparison_requires_same_repository_state():
    left = profile("left")
    right = ExecutionProfile(
        profile_id="right",
        repository_commit="2" * 40,
        layers=tuple(layer(layer_id) for layer_id in ExecutionLayer),
        source_refs=("fixture:right",),
    )
    with pytest.raises(StudyError, match="same repository commit"):
        compare_execution_profiles(left, right)
