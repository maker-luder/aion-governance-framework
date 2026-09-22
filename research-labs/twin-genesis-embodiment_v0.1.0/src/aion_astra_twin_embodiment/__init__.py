"""AION/Astra shared-genesis twin embodiment research candidate."""

from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .runtime import TwinGenesisRuntime, TwinRuntimeState
from .runtime_binding import TwinRuntimeContexts, build_runtime_contexts
from .sensorimotor import (
    BodyModelSnapshot,
    BodyRegionState,
    RegionCondition,
    SensorimotorDisposition,
    SensorimotorObservation,
    SensorimotorPrediction,
    SensorimotorTransitionAudit,
    audit_sensorimotor_transition,
    body_model_snapshot_hash,
    sensorimotor_observation_hash,
    sensorimotor_prediction_hash,
)
from .validation import ValidationError, validate_candidate

__all__ = [
    "EmbodimentInstance",
    "EmbodimentTemplate",
    "SharedGenesisEvent",
    "TwinGenesisRuntime",
    "TwinRuntimeState",
    "TwinRuntimeContexts",
    "build_runtime_contexts",
    "BodyModelSnapshot",
    "BodyRegionState",
    "RegionCondition",
    "SensorimotorDisposition",
    "SensorimotorObservation",
    "SensorimotorPrediction",
    "SensorimotorTransitionAudit",
    "audit_sensorimotor_transition",
    "body_model_snapshot_hash",
    "sensorimotor_observation_hash",
    "sensorimotor_prediction_hash",
    "ValidationError",
    "validate_candidate",
]