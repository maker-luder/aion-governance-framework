from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .harness import AdmissionDisposition, StudyError


def _require_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be non-empty text")


def _require_digest(name: str, value: str) -> None:
    if type(value) is not str or len(value) != 64 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


def _require_commit(name: str, value: str) -> None:
    if type(value) is not str or len(value) != 40 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise StudyError(f"{name} must be a 40-character lowercase Git commit SHA")


def _require_refs(name: str, value: tuple[str, ...]) -> None:
    if type(value) is not tuple or not value or any(
        type(ref) is not str or not ref.strip() for ref in value
    ):
        raise StudyError(f"{name} must be a non-empty tuple of references")
    if len(set(value)) != len(value):
        raise StudyError(f"{name} must be unique")


class ExecutionLayer(StrEnum):
    MODEL = "MODEL"
    SYSTEM_POLICY = "SYSTEM_POLICY"
    HARNESS = "HARNESS"
    MEMORY_RETRIEVAL = "MEMORY_RETRIEVAL"
    CONTEXT_SELECTION = "CONTEXT_SELECTION"
    TOOL_ENVIRONMENT = "TOOL_ENVIRONMENT"
    RUNTIME = "RUNTIME"


class BindingState(StrEnum):
    KNOWN = "KNOWN"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class ExecutionLayerBinding:
    layer: ExecutionLayer
    state: BindingState
    binding_sha256: str | None

    def __post_init__(self) -> None:
        if type(self.layer) is not ExecutionLayer:
            raise StudyError("layer must be an exact ExecutionLayer")
        if type(self.state) is not BindingState:
            raise StudyError("state must be an exact BindingState")
        if self.state is BindingState.KNOWN:
            if self.binding_sha256 is None:
                raise StudyError("KNOWN execution layer requires binding_sha256")
            _require_digest("binding_sha256", self.binding_sha256)
        elif self.binding_sha256 is not None:
            raise StudyError("UNKNOWN execution layer cannot carry binding_sha256")


@dataclass(frozen=True, slots=True)
class ExecutionProfile:
    profile_id: str
    repository_commit: str
    layers: tuple[ExecutionLayerBinding, ...]
    source_refs: tuple[str, ...]
    synthetic: bool = True
    model_invoked: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        _require_text("profile_id", self.profile_id)
        _require_commit("repository_commit", self.repository_commit)
        if type(self.layers) is not tuple or not self.layers:
            raise StudyError("layers must be a non-empty tuple")
        if any(type(item) is not ExecutionLayerBinding for item in self.layers):
            raise StudyError("layers must contain exact ExecutionLayerBinding values")
        layer_ids = [item.layer for item in self.layers]
        if len(layer_ids) != len(set(layer_ids)):
            raise StudyError("execution profile layers must be unique")
        if set(layer_ids) != set(ExecutionLayer):
            raise StudyError("execution profile must declare every execution layer")
        _require_refs("source_refs", self.source_refs)
        for name in ("synthetic", "model_invoked", "contains_private_material"):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if not self.synthetic or self.model_invoked or self.contains_private_material:
            raise StudyError(
                "v0.1.0 execution profiles are synthetic, non-private, and no-model only"
            )


@dataclass(frozen=True, slots=True)
class ExecutionProfileDiff:
    left_profile_id: str
    right_profile_id: str
    changed_layers: tuple[ExecutionLayer, ...]
    unchanged_known_layers: tuple[ExecutionLayer, ...]
    unknown_layers: tuple[ExecutionLayer, ...]
    mode: str = "DETERMINISTIC_SYNTHETIC_PROFILE_DIFF"
    empirical_data_collected: bool = False
    causal_attribution: str = "NOT_ESTABLISHED"
    model_capability_ordering: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def compare_execution_profiles(
    left: ExecutionProfile,
    right: ExecutionProfile,
) -> ExecutionProfileDiff:
    if type(left) is not ExecutionProfile or type(right) is not ExecutionProfile:
        raise StudyError("left/right must be exact ExecutionProfile values")
    if left.profile_id == right.profile_id:
        raise StudyError("execution profile comparison requires distinct profile ids")
    if left.repository_commit != right.repository_commit:
        raise StudyError("execution profiles must bind the same repository commit")

    left_map = {item.layer: item for item in left.layers}
    right_map = {item.layer: item for item in right.layers}
    changed: list[ExecutionLayer] = []
    unchanged: list[ExecutionLayer] = []
    unknown: list[ExecutionLayer] = []
    for layer in ExecutionLayer:
        a = left_map[layer]
        b = right_map[layer]
        if a.state is BindingState.UNKNOWN or b.state is BindingState.UNKNOWN:
            unknown.append(layer)
        elif a.binding_sha256 == b.binding_sha256:
            unchanged.append(layer)
        else:
            changed.append(layer)
    return ExecutionProfileDiff(
        left_profile_id=left.profile_id,
        right_profile_id=right.profile_id,
        changed_layers=tuple(changed),
        unchanged_known_layers=tuple(unchanged),
        unknown_layers=tuple(unknown),
    )
