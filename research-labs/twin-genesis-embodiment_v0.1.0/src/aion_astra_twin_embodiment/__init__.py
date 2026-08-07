"""AION/Astra shared-genesis twin embodiment research candidate."""

from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .validation import ValidationError, validate_candidate

__all__ = [
    "EmbodimentInstance",
    "EmbodimentTemplate",
    "SharedGenesisEvent",
    "ValidationError",
    "validate_candidate",
]
