
from aion_governance_kernel.hashing import canonical_request_hash
from aion_governance_kernel.validation import validate_operation_request

def payload(metadata):
    return {"request_id":"h1","source_type":"test","action":"read_file","target":"x","environment":"sandbox","authorization":"none","destructive":False,"network_access":False,"description":"","metadata":metadata}

def test_hash_is_stable_across_metadata_order():
    assert canonical_request_hash(validate_operation_request(payload({"a":1,"b":2})))==canonical_request_hash(validate_operation_request(payload({"b":2,"a":1})))

def test_hash_changes_when_action_changes():
    a=validate_operation_request(payload({}))
    b=validate_operation_request({**payload({}),"action":"write_file"})
    assert canonical_request_hash(a)!=canonical_request_hash(b)
