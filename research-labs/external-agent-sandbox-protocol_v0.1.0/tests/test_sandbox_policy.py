from aion_external_agent_sandbox import CandidateState, SandboxPolicy, assess_policy, classify_candidate


def ready_policy(**overrides):
    values = dict(
        provider="KILO_CLOUD_AGENT",
        model="EXPLICIT_FREE_MODEL_TO_BE_PINNED_AT_ACTIVATION",
        free_status_verified_at_activation=True,
        explicit_model_lineage=True,
        auto_model_routing=False,
        separate_sandbox_repository=True,
        primary_repository_write=False,
        research_integration_write=False,
        main_write=False,
        auto_merge=False,
        public_safe_capsule_only=True,
        secret_access=False,
        private_memory_access=False,
        local_agent_configuration_access=False,
        scheduled_trigger_enabled=False,
        agent_count=1,
        research_question_count=1,
        human_review_required=True,
        local_agent_cloud_migration=False,
        local_agent_network_egress=False,
        local_agent_external_worker_role=False,
    )
    values.update(overrides)
    return SandboxPolicy(**values)


def test_minimal_first_run_can_pass_preflight_without_executing():
    result = assess_policy(ready_policy())
    assert result.ready is True
    assert result.external_agent_run == "NOT_EXECUTED"
    assert result.main_effect == "NONE"


def test_auto_model_routing_holds():
    result = assess_policy(ready_policy(auto_model_routing=True))
    assert result.ready is False
    assert "MODEL_ROUTING_NOT_EXPLICIT" in result.reasons


def test_primary_or_main_write_holds():
    assert assess_policy(ready_policy(primary_repository_write=True)).ready is False
    assert assess_policy(ready_policy(main_write=True)).ready is False


def test_scheduling_is_not_allowed_on_first_run():
    result = assess_policy(ready_policy(scheduled_trigger_enabled=True))
    assert result.ready is False
    assert "FIRST_RUN_MUST_BE_UNSCHEDULED" in result.reasons


def test_local_agent_boundary_cannot_be_weakened():
    result = assess_policy(ready_policy(local_agent_network_egress=True))
    assert result.ready is False
    assert "LOCAL_AGENT_BOUNDARY_WEAKENED" in result.reasons


def test_contaminated_or_incomplete_provenance_is_quarantined():
    assert classify_candidate(provenance_complete=True, contamination_suspected=True, nonconforming=False, potentially_useful=True) is CandidateState.QUARANTINE
    assert classify_candidate(provenance_complete=False, contamination_suspected=False, nonconforming=False, potentially_useful=True) is CandidateState.QUARANTINE


def test_valuable_not_adopted_stays_isolated():
    state = classify_candidate(provenance_complete=True, contamination_suspected=False, nonconforming=False, potentially_useful=True, adopted=False)
    assert state is CandidateState.RETAIN_ISOLATED


def test_unusable_nonconforming_candidate_is_rejected_not_auto_deleted():
    state = classify_candidate(provenance_complete=True, contamination_suspected=False, nonconforming=True, potentially_useful=False)
    assert state is CandidateState.REJECT
