"""Read-only CSOMI × SLSH interface and consistency module."""

from .authority import CSOMI_SPEC, SLSH_SPEC, load_default_authorities
from .contract import build_integration_contract
from .validate import validate_file, validate_record

__all__ = [
    "CSOMI_SPEC",
    "SLSH_SPEC",
    "build_integration_contract",
    "load_default_authorities",
    "validate_file",
    "validate_record",
]
