import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aion_astra_runtime.interop import (
    ErrorEnvelope,
    InteropError,
    canonical_json_text,
    parse_strict_json,
    sha256_canonical,
    validate_timestamp,
    validate_version,
)


ROOT = Path(__file__).resolve().parents[3]
PROFILE_SCHEMA = json.loads(
    (ROOT / "schemas/aion_serialization_profile_v0.1.0.schema.json").read_text(encoding="utf-8")
)
ERROR_SCHEMA = json.loads(
    (ROOT / "schemas/aion_error_envelope_v0.1.0.schema.json").read_text(encoding="utf-8")
)
VECTORS = json.loads(
    (ROOT / "conformance/aion_interoperability_primitives_v0.1.0.json").read_text(encoding="utf-8")
)["vectors"]


def test_profile_schema_is_strict_and_self_validating():
    profile = {
        "profile_id": "AION-JCS-COMPATIBLE-0.1.0",
        "schema_version": "0.1.0",
        "encoding": "UTF-8",
        "unicode_policy": "NFC_INPUT_PRESERVED",
        "timestamp_profile": "RFC3339_UTC_MICROS_Z",
        "object_member_order": "UTF16_CODE_UNIT_LEXICOGRAPHIC",
        "array_order": "PRESERVE",
        "whitespace": "NONE",
        "numbers": "SAFE_INTEGERS_ONLY",
        "duplicate_keys": "REJECT",
        "non_finite_numbers": "REJECT",
        "hash_algorithm": "SHA-256",
        "canonical_effect": "NONE",
    }
    Draft202012Validator(PROFILE_SCHEMA).validate(profile)
    with pytest.raises(Exception):
        Draft202012Validator(PROFILE_SCHEMA).validate({**profile, "authority": "OWNER"})


def test_error_envelope_schema_is_strict_and_self_validating():
    vector = next(item for item in VECTORS if item["contract"] == "ErrorEnvelope" and item["expected_acceptance"])
    Draft202012Validator(ERROR_SCHEMA).validate(vector["input"])
    with pytest.raises(Exception):
        Draft202012Validator(ERROR_SCHEMA).validate({**vector["input"], "authority": "OWNER"})


def test_interoperability_vectors_match_reference_behavior():
    for vector in VECTORS:
        contract = vector["contract"]
        accepted = True
        output = None
        error_code = None
        try:
            if contract == "SerializationProfile":
                if isinstance(vector["input"], str):
                    output = parse_strict_json(vector["input"])
                    output = canonical_json_text(output)
                else:
                    output = canonical_json_text(vector["input"])
            elif contract == "Timestamp":
                output = validate_timestamp(vector["input"])
            elif contract == "Version":
                output = validate_version(vector["input"])
            elif contract == "ErrorEnvelope":
                output = ErrorEnvelope.from_dict(vector["input"]).to_dict()
            else:
                raise AssertionError(f"unhandled vector contract: {contract}")
        except InteropError as exc:
            accepted = False
            error_code = exc.error_code

        assert accepted is vector["expected_acceptance"], vector["vector_id"]
        assert error_code == vector["expected_error_code"], vector["vector_id"]
        if accepted and contract in {"SerializationProfile", "Timestamp", "Version"}:
            assert output == vector["expected_output"], vector["vector_id"]
        if accepted and contract == "ErrorEnvelope":
            assert output == vector["expected_output"], vector["vector_id"]
        if accepted and vector["expected_canonical_serialization"] is not None:
            if contract == "ErrorEnvelope":
                canonical = canonical_json_text(output)
            else:
                canonical = output
            assert canonical == vector["expected_canonical_serialization"], vector["vector_id"]
        if accepted and vector["expected_hash"] is not None:
            if contract == "ErrorEnvelope":
                assert sha256_canonical(output) == vector["expected_hash"], vector["vector_id"]
            else:
                assert sha256_canonical(vector["input"]) == vector["expected_hash"], vector["vector_id"]


def test_identifier_and_version_errors_fail_closed():
    with pytest.raises(InteropError) as identifier_error:
        from aion_astra_runtime.interop import validate_identifier

        validate_identifier(" AION")
    assert identifier_error.value.error_code == "MALFORMED_INPUT"

    with pytest.raises(InteropError) as version_error:
        validate_version("0.2.0")
    assert version_error.value.error_code == "UNSUPPORTED_VERSION"
