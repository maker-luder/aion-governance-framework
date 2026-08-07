"""Immutable workbench domain records."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .enums import (
    AdoptionStatus,
    ApprovalDecision,
    ChangeCategory,
    EvidenceValidity,
    KernelDecision,
    PermissionLevel,
    RiskLevel,
    SourceType,
    TaskStatus,
)


@dataclass(frozen=True, slots=True)
class OwnerConstraint:
    constraint_id: str
    statement: str
    source_type: SourceType = SourceType.OWNER_STATEMENT


@dataclass(frozen=True, slots=True)
class AcceptanceCriterion:
    criterion_id: str
    statement: str
    blocking: bool = True


@dataclass(frozen=True, slots=True)
class RiskClassification:
    level: RiskLevel
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TaskScope:
    goal: str
    current_state: str
    requested_change: str
    in_scope: tuple[str, ...]
    out_of_scope: tuple[str, ...]
    constraints: tuple[OwnerConstraint, ...]
    assumptions: tuple[str, ...]
    unresolved_questions: tuple[str, ...]
    acceptance_criteria: tuple[AcceptanceCriterion, ...]
    blocking_conditions: tuple[str, ...]
    affected_components: tuple[str, ...]
    revalidation_scope: tuple[str, ...]
    rollback_plan: str
    stop_condition: str


@dataclass(frozen=True, slots=True)
class EngineeringTask:
    task_id: str
    scope: TaskScope
    risk: RiskClassification
    status: TaskStatus
    created_at: str


@dataclass(frozen=True, slots=True)
class ApprovalRequest:
    approval_request_id: str
    task_id: str
    operation_type: PermissionLevel
    reason: str
    affected_paths: tuple[str, ...]
    proposed_commands: tuple[tuple[str, ...], ...]
    expected_effect: str
    risk_level: RiskLevel
    data_exposure: str
    rollback_plan: str
    requested_at: str
    expires_at: str
    request_hash: str
    status: ApprovalDecision = ApprovalDecision.DEFERRED


@dataclass(frozen=True, slots=True)
class ApprovalGrant:
    grant_id: str
    approval_request_id: str
    task_id: str
    operation_type: PermissionLevel
    decision: ApprovalDecision
    conditions: tuple[str, ...]
    approved_by: str
    approved_at: str
    expires_at: str
    request_hash: str


@dataclass(frozen=True, slots=True)
class CandidateWorkspace:
    task_id: str
    baseline_root: str
    candidate_root: str
    output_root: str
    baseline_hash: str
    created_at: str


@dataclass(frozen=True, slots=True)
class ChangeSet:
    change_id: str
    requirement_ids: tuple[str, ...]
    affected_files: tuple[str, ...]
    symbols: tuple[str, ...]
    change_reason: str
    risk: RiskLevel
    expected_behavior: str
    tests_required: tuple[str, ...]
    rollback_method: str
    owner_approval_reference: str
    files_added: tuple[str, ...] = ()
    files_modified: tuple[str, ...] = ()
    files_deleted: tuple[str, ...] = ()
    baseline_hash: str = ""
    candidate_hash: str = ""
    diff_summary: str = ""
    rollback_status: str = "NOT_REQUIRED"


@dataclass(frozen=True, slots=True)
class CommandRequest:
    command_id: str
    task_id: str
    argv: tuple[str, ...]
    working_directory: str
    timeout_seconds: int
    output_limit_bytes: int
    approval_reference: str


@dataclass(frozen=True, slots=True)
class CommandResult:
    command_id: str
    argv: tuple[str, ...]
    return_code: int | None
    stdout: str
    stderr: str
    timed_out: bool
    truncated: bool
    result_hash: str
    status: str


@dataclass(frozen=True, slots=True)
class ValidationPlan:
    change_category: ChangeCategory
    tests_to_run: tuple[str, ...]
    static_checks_to_run: tuple[str, ...]
    builds_to_run: tuple[str, ...]
    integration_checks_to_run: tuple[str, ...]
    evidence_reused: tuple[str, ...]
    evidence_invalidated: tuple[str, ...]
    full_rerun_justification: str | None


@dataclass(frozen=True, slots=True)
class ValidationResult:
    validation_id: str
    plan: ValidationPlan
    command_results: tuple[CommandResult, ...]
    passed: bool
    evidence_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    evidence_id: str
    artifact_version: str
    source_commit_or_hash: str
    environment_fingerprint: str
    test_scope: tuple[str, ...]
    dependency_scope: tuple[str, ...]
    generated_at: str
    validity_status: EvidenceValidity
    invalidation_conditions: tuple[str, ...]
    reused_by_versions: tuple[str, ...] = ()
    owner_review_status: str = "PENDING_OWNER_REVIEW"


@dataclass(frozen=True, slots=True)
class ReviewFinding:
    finding_id: str
    severity: RiskLevel
    summary: str
    blocking: bool
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReviewPacket:
    packet_id: str
    task_id: str
    blocking_issue: str
    current_state: str
    expected_result: str
    actual_result: str
    attempts_made: tuple[str, ...]
    relevant_files: tuple[str, ...]
    minimal_code_excerpt: str
    logs: str
    environment: dict[str, str]
    privacy_classification: str
    redactions_applied: tuple[str, ...]
    questions_for_reviewer: tuple[str, ...]
    excluded_material: tuple[str, ...]
    manifest: tuple[str, ...]
    hashes: dict[str, str]
    owner_submission_status: str


@dataclass(frozen=True, slots=True)
class ExternalTeacherInput:
    input_id: str
    task_id: str
    source_type: SourceType
    source_actor_id: str
    content_hash: str
    received_at: str
    adoption_status: AdoptionStatus = AdoptionStatus.PENDING_OWNER_REVIEW


@dataclass(frozen=True, slots=True)
class PackageCandidate:
    package_id: str
    task_id: str
    path: str
    manifest_hash: str
    package_hash: str
    canonical_effect: str = "NONE_PENDING_OWNER_REVIEW"
    deployed: bool = False


@dataclass(frozen=True, slots=True)
class OwnerHandoff:
    task_id: str
    overall_result: str
    package_candidates: tuple[PackageCandidate, ...]
    findings: tuple[ReviewFinding, ...]
    owner_decisions_required: tuple[str, ...]
    canonical_effect: str = "NONE_PENDING_OWNER_REVIEW"


@dataclass(frozen=True, slots=True)
class KernelEvaluation:
    decision: KernelDecision
    reason: str
    evidence_required: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AuditEvent:
    sequence: int
    occurred_at: str
    task_id: str
    action: str
    details: dict[str, Any] = field(default_factory=dict)
    previous_hash: str = ""
    event_hash: str = ""
