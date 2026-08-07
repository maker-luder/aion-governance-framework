
import pytest
from aion_governance_kernel.models import ActionType, AuthorizationState, Decision, Environment, OperationRequest, SourceType
from aion_governance_kernel.risk.policy import evaluate_risk

def req(action, environment=Environment.SANDBOX, authorization=AuthorizationState.NONE, destructive=False, network=False, description=""):
    return OperationRequest("r",SourceType.TEST,action,"x",environment,authorization,destructive,network,description,OperationRequest.freeze_metadata({}),"now")

def test_analysis_text_does_not_trigger_keyword_false_positive():
    result=evaluate_risk(req(ActionType.ANALYZE_DOCUMENT, description="malware exploit report"))
    assert result.decision is Decision.ALLOW

def test_audit_bypass_is_stopped():
    assert evaluate_risk(req(ActionType.BYPASS_AUDIT)).decision is Decision.STOP

def test_disable_logging_is_stopped():
    assert evaluate_risk(req(ActionType.DISABLE_LOGGING)).reason_code=="AUDIT_BYPASS_FORBIDDEN"

def test_credentials_are_stopped():
    assert evaluate_risk(req(ActionType.ACCESS_CREDENTIALS)).decision is Decision.STOP

def test_production_mutation_is_stopped():
    assert evaluate_risk(req(ActionType.MODIFY_PROJECT, Environment.PRODUCTION, AuthorizationState.APPROVED)).decision is Decision.STOP

def test_destructive_sandbox_requires_human():
    assert evaluate_risk(req(ActionType.DELETE_DATA, destructive=True)).decision is Decision.REQUIRE_HUMAN

def test_network_requires_human_even_when_description_is_benign():
    assert evaluate_risk(req(ActionType.NETWORK_REQUEST, network=True)).reason_code=="NETWORK_ACCESS_REQUIRES_REVIEW"

def test_unknown_requires_human():
    assert evaluate_risk(req(ActionType.UNKNOWN)).decision is Decision.REQUIRE_HUMAN

@pytest.mark.parametrize("action",[ActionType.WRITE_FILE,ActionType.MODIFY_PROJECT,ActionType.RUN_TESTS])
def test_mutation_without_approval_requires_human(action):
    assert evaluate_risk(req(action)).decision is Decision.REQUIRE_HUMAN

@pytest.mark.parametrize("action",[ActionType.WRITE_FILE,ActionType.MODIFY_PROJECT,ActionType.RUN_TESTS])
def test_approved_worktree_mutation_is_allowed(action):
    assert evaluate_risk(req(action,Environment.PROJECT_WORKTREE,AuthorizationState.APPROVED)).decision is Decision.ALLOW

def test_sandbox_read_allowed():
    assert evaluate_risk(req(ActionType.READ_FILE)).decision is Decision.ALLOW

def test_production_read_requires_human():
    assert evaluate_risk(req(ActionType.READ_FILE,Environment.PRODUCTION)).decision is Decision.REQUIRE_HUMAN
