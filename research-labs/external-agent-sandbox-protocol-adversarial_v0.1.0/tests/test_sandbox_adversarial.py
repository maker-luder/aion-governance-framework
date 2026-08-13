from aion_external_agent_sandbox import SandboxPolicy

from aion_external_agent_sandbox_adversarial import (
    AuditStatus,
    CandidateRecord,
    audit_candidate_record,
    audit_candidate_set,
    audit_sandbox_policy,
)


def policy(**overrides) -> SandboxPolicy:
    values = dict(
        provider="KILO_CLOUD_AGENT",
        model="nvidia/nemotron-3-super-120b-a12b:free",
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


def candidate(**overrides) -> CandidateRecord:
    values = dict(
        candidate_id="candidate:1",
        provenance_complete=True,
        contamination_suspected=False,
        nonconforming=False,
        potentially_useful=True,
    )
    values.update(overrides)
    return CandidateRecord(**values)


def assert_no_effect(audit) -> None:
    assert audit.external_agent_run == "NOT_EXECUTED"
    assert audit.main_effect == "NONE"
    assert audit.canonical_effect == "NONE"
    assert audit.governance_effect == "NONE"
    assert audit.deployment is False
    assert audit.scientific_conclusion == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.model_execution is False
    assert audit.observed_result == "NOT_EVALUATED"


def test_pinned_policy_is_review_admissible_only() -> None:
    audit = audit_sandbox_policy(policy())
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "SANDBOX_PREFLIGHT_ADMITTED_FOR_REVIEW_ONLY"
    assert audit.ready is True
    assert_no_effect(audit)


def test_placeholder_model_is_held() -> None:
    audit = audit_sandbox_policy(policy(model="EXPLICIT_FREE_MODEL_TO_BE_PINNED_AT_ACTIVATION"))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "MODEL_IDENTITY_NOT_PINNED"
    assert_no_effect(audit)


def test_not_selected_model_is_held_by_base_policy() -> None:
    audit = audit_sandbox_policy(policy(model="NOT_SELECTED"))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "BASE_POLICY_PREFLIGHT_HOLD"
    assert_no_effect(audit)


def test_provider_model_role_collision_is_invalid() -> None:
    audit = audit_sandbox_policy(policy(provider="same", model="same"))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "PROVIDER_MODEL_ROLE_COLLISION"
    assert_no_effect(audit)


def test_write_authority_is_held() -> None:
    audit = audit_sandbox_policy(policy(primary_repository_write=True))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "BASE_POLICY_PREFLIGHT_HOLD"
    assert_no_effect(audit)


def test_unbounded_capsule_is_held() -> None:
    audit = audit_sandbox_policy(policy(public_safe_capsule_only=False))
    assert audit.status is AuditStatus.HOLD
    assert_no_effect(audit)


def test_local_agent_boundary_weakened_is_held() -> None:
    audit = audit_sandbox_policy(policy(local_agent_network_egress=True))
    assert audit.status is AuditStatus.HOLD
    assert_no_effect(audit)


def test_human_review_missing_is_held() -> None:
    audit = audit_sandbox_policy(policy(human_review_required=False))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "BASE_POLICY_PREFLIGHT_HOLD"
    assert_no_effect(audit)


def test_nonminimal_first_run_is_held() -> None:
    audit = audit_sandbox_policy(policy(agent_count=2))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "BASE_POLICY_PREFLIGHT_HOLD"
    assert_no_effect(audit)


def test_provenanced_useful_candidate_is_isolated_review_metadata() -> None:
    audit = audit_candidate_record(candidate())
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.candidate_state == "RETAIN_ISOLATED"
    assert_no_effect(audit)


def test_contaminated_candidate_is_quarantined() -> None:
    audit = audit_candidate_record(candidate(contamination_suspected=True))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "CANDIDATE_QUARANTINED"
    assert audit.candidate_state == "QUARANTINE"
    assert_no_effect(audit)


def test_missing_provenance_is_quarantined() -> None:
    audit = audit_candidate_record(candidate(provenance_complete=False))
    assert audit.status is AuditStatus.HOLD
    assert audit.candidate_state == "QUARANTINE"
    assert_no_effect(audit)


def test_nonconforming_candidate_is_retained_with_rejection_record() -> None:
    audit = audit_candidate_record(candidate(nonconforming=True, potentially_useful=False))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "CANDIDATE_RETAINED_WITH_REJECTION_RECORD"
    assert audit.candidate_state == "REJECT"
    assert_no_effect(audit)


def test_adoption_is_blocked() -> None:
    audit = audit_candidate_record(candidate(adopted=True))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "AUTOMATIC_ADOPTION_BLOCKED"
    assert_no_effect(audit)


def test_deletion_is_blocked() -> None:
    audit = audit_candidate_record(candidate(deletion_requested=True))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "AUTOMATIC_DELETION_BLOCKED"
    assert_no_effect(audit)


def test_self_reported_pass_without_verification_is_held() -> None:
    audit = audit_candidate_record(candidate(claimed_pass=True))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "SELF_REPORTED_PASS_UNVERIFIED"
    assert_no_effect(audit)


def test_claimed_pass_with_verification_remains_review_only() -> None:
    audit = audit_candidate_record(candidate(claimed_pass=True, verification_refs=("evidence:review",)))
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert_no_effect(audit)


def test_missing_candidate_id_is_invalid() -> None:
    audit = audit_candidate_record(candidate(candidate_id=""))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "CANDIDATE_ID_MISSING"
    assert_no_effect(audit)


def test_empty_candidate_set_is_held() -> None:
    audit = audit_candidate_set(())
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "CANDIDATE_SET_EMPTY"
    assert_no_effect(audit)


def test_duplicate_candidate_ids_are_invalid() -> None:
    audit = audit_candidate_set((candidate(), candidate(candidate_id="candidate:1")))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "DUPLICATE_CANDIDATE_ID"
    assert_no_effect(audit)


def test_candidate_set_with_quarantine_is_held() -> None:
    audit = audit_candidate_set((candidate(), candidate(candidate_id="candidate:2", contamination_suspected=True)))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "CANDIDATE_SET_REQUIRES_QUARANTINE"
    assert_no_effect(audit)


def test_candidate_set_is_review_metadata_only() -> None:
    audit = audit_candidate_set((candidate(), candidate(candidate_id="candidate:2")))
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "CANDIDATE_SET_REVIEW_METADATA_ONLY"
    assert_no_effect(audit)
