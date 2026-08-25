
import pytest
from aion_governance_kernel.errors import InputValidationError
from aion_governance_kernel.models import ActionType, AuthorizationState, Environment, SourceType
from aion_governance_kernel.validation import validate_operation_request

def base(**overrides):
    data={"request_id":"req-1","source_type":"api","action":"analyze_document","target":"report.md","environment":"sandbox","authorization":"none","destructive":False,"network_access":False,"description":"analysis","metadata":{"x":1}}
    data.update(overrides); return data

def test_valid_request_is_typed_and_metadata_immutable():
    req=validate_operation_request(base())
    assert req.source_type is SourceType.API and req.action is ActionType.ANALYZE_DOCUMENT
    assert req.environment is Environment.SANDBOX and req.authorization is AuthorizationState.NONE
    with pytest.raises(TypeError): req.metadata["x"]="2"

def test_risk_level_is_ignored_and_hint_is_untrusted():
    req=validate_operation_request(base(risk_level="LOW", risk_hint="safe"))
    assert req.metadata["untrusted_risk_hint"]=="safe"

def test_unknown_action_becomes_unknown():
    assert validate_operation_request(base(action="invented operation")).action is ActionType.UNKNOWN

@pytest.mark.parametrize("field,value", [("source_type","alien"),("environment","moon"),("authorization","maybe")])
def test_invalid_enums_fail(field,value):
    with pytest.raises(InputValidationError): validate_operation_request(base(**{field:value}))

def test_unknown_field_fails():
    with pytest.raises(InputValidationError): validate_operation_request(base(extra="x"))

def test_invalid_request_id_fails():
    with pytest.raises(InputValidationError): validate_operation_request(base(request_id="bad id"))

def test_non_boolean_flags_fail():
    with pytest.raises(InputValidationError): validate_operation_request(base(destructive="false"))

def test_oversized_description_fails():
    with pytest.raises(InputValidationError): validate_operation_request(base(description="x"*5000))

def test_nested_metadata_fails():
    with pytest.raises(InputValidationError): validate_operation_request(base(metadata={"x":{"nested":1}}))

def test_action_aliases_are_supported():
    assert validate_operation_request(base(action="read")).action is ActionType.READ_FILE

def test_non_mapping_fails():
    with pytest.raises(InputValidationError): validate_operation_request([("action","read")])

def test_empty_action_fails():
    with pytest.raises(InputValidationError): validate_operation_request(base(action=""))

def test_invalid_target_type_fails():
    with pytest.raises(InputValidationError): validate_operation_request(base(target=123))

def test_too_many_metadata_items_fail():
    with pytest.raises(InputValidationError): validate_operation_request(base(metadata={str(i):i for i in range(21)}))

def test_auto_request_id_is_created():
    data=base(); data.pop("request_id")
    assert validate_operation_request(data).request_id
