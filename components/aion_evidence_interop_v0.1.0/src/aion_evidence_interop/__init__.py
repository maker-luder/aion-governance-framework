"""AION evidence interoperability profile.

This package is inspection-only. It transforms already-valid AION evidence
records into deterministic, non-canonical interoperability views.
"""

from .canonical import InteropError, validate_source_record
from .manifest import build_bundle

__all__ = ["InteropError", "validate_source_record", "build_bundle"]
__version__ = "0.1.0"
