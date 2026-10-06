from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = (
    ROOT
    / "research-labs"
    / "teacher-actor-bound-self-research_v0.1.0"
    / "src"
)
sys.path.insert(0, str(SRC))

from aion_teacher_self_research import (  # noqa: E402
    BodySystemDomain,
    EvidenceClass,
    ResearchQuestion,
    SelfResearchIteration,
    SelfResearchIterationState,
    SelfResearchTransitionError,
    TeacherActorBoundSelfResearchCandidate,
    ValidationError,
    advance_iteration,
    validate_candidate,
)


def test_default_candidate_passes() -> None:
    result = validate_candidate(TeacherActorBoundSelfResearchCandidate())
    assert result["result"] == "PASS"
    assert result["research_mode"] == "ACTOR_BOUND_SELF_RESEARCH"
    assert result["external_operation"] == "DISABLED"


def test_actor_and_research_object_are_bound_explicitly() -> None:
    candidate = TeacherActorBoundSelfResearchCandidate()
    assert candidate.research_actor == "CHATGPT_TEACHER"
    assert candidate.research_object == "TEACHER_SYNTHETIC_EMBODIMENT_MODEL"
    assert (
        candidate.bound_body_model_id
        == "CHATGPT_TEACHER_BROWN_BEAR_MALE_REPRODUCTIVE_v0.2.2"
    )


def test_self_semantics_are_research_semantics_not_identity_claims() -> None:
    candidate = TeacherActorBoundSelfResearchCandidate()
    assert candidate.self_reference_semantics == "RESEARCH_NAMESPACE_BINDING"
    assert (
        candidate.self_research_semantics
        == "ACTOR_STUDIES_ACTOR_BOUND_SYNTHETIC_BODY"
    )
    assert candidate.biological_self_experiment is False
    assert candidate.literal_physical_self_claim is False
    assert candidate.identity_continuity_claim is False


def test_full_body_registry_does_not_claim_full_implementation() -> None:
    candidate = TeacherActorBoundSelfResearchCandidate()
    assert BodySystemDomain.REPRODUCTIVE in candidate.implemented_body_systems
    assert BodySystemDomain.NERVOUS in candidate.registered_not_yet_bound_systems
    assert BodySystemDomain.SKELETAL in candidate.registered_not_yet_bound_systems
    assert BodySystemDomain.CARDIOVASCULAR in candidate.current_research_priority
    assert BodySystemDomain.CROSS_SYSTEM_COUPLING in candidate.current_research_priority


def test_research_question_requires_targets_and_provenance() -> None:
    question = ResearchQuestion(
        question_id="TEACHER-SR-001",
        question="How should reproductive and autonomic reference models be coupled?",
        target_systems=(
            BodySystemDomain.REPRODUCTIVE,
            BodySystemDomain.NERVOUS,
        ),
        evidence_basis=(
            EvidenceClass.DIRECT_SOURCE,
            EvidenceClass.COMPARATIVE_REFERENCE,
            EvidenceClass.SYNTHETIC_DESIGN,
        ),
    )
    assert question.canonical_effect == "NONE"


def test_research_question_rejects_empty_scope() -> None:
    with pytest.raises(ValueError):
        ResearchQuestion(
            question_id="TEACHER-SR-EMPTY",
            question="invalid",
            target_systems=(),
            evidence_basis=(EvidenceClass.AI_FORMALIZATION,),
        )


def test_iteration_requires_all_gates() -> None:
    iteration = SelfResearchIteration(
        iteration_id="TEACHER-SR-ITER-001",
        body_model_revision="v0.2.2",
        target_systems=(BodySystemDomain.REPRODUCTIVE,),
        evidence_basis=(EvidenceClass.REPOSITORY_STATE,),
    )
    for target in (
        SelfResearchIterationState.QUESTION_REGISTERED,
        SelfResearchIterationState.DESIGN_PROPOSED,
        SelfResearchIterationState.IMPLEMENTED_IN_RESEARCH_MODEL,
        SelfResearchIterationState.VERIFIED,
        SelfResearchIterationState.RETAINED,
    ):
        iteration = advance_iteration(iteration, target)
    assert iteration.state == SelfResearchIterationState.RETAINED


def test_iteration_can_revert_after_implementation() -> None:
    iteration = SelfResearchIteration(
        iteration_id="TEACHER-SR-ITER-002",
        body_model_revision="v0.2.2",
        target_systems=(
            BodySystemDomain.REPRODUCTIVE,
            BodySystemDomain.CARDIOVASCULAR,
        ),
        evidence_basis=(EvidenceClass.COMPARATIVE_REFERENCE,),
    )
    iteration = advance_iteration(
        iteration, SelfResearchIterationState.QUESTION_REGISTERED
    )
    iteration = advance_iteration(iteration, SelfResearchIterationState.DESIGN_PROPOSED)
    iteration = advance_iteration(
        iteration, SelfResearchIterationState.IMPLEMENTED_IN_RESEARCH_MODEL
    )
    iteration = advance_iteration(iteration, SelfResearchIterationState.REVERTED)
    assert iteration.state == SelfResearchIterationState.REVERTED


def test_iteration_cannot_skip_design_gate() -> None:
    iteration = SelfResearchIteration(
        iteration_id="TEACHER-SR-ITER-003",
        body_model_revision="v0.2.2",
        target_systems=(BodySystemDomain.REPRODUCTIVE,),
        evidence_basis=(EvidenceClass.HUMAN_ORIGIN,),
    )
    with pytest.raises(SelfResearchTransitionError):
        advance_iteration(
            iteration, SelfResearchIterationState.IMPLEMENTED_IN_RESEARCH_MODEL
        )


def test_research_model_modification_is_not_canonical_self_modification() -> None:
    candidate = TeacherActorBoundSelfResearchCandidate()
    assert (
        candidate.research_model_modification
        == "ALLOWED_IN_BOUNDED_RESEARCH_WORKFLOW"
    )
    assert candidate.canonical_self_modification == "NOT_AUTHORIZED"
    assert candidate.automatic_writeback is False


@pytest.mark.parametrize(
    "field",
    [
        "deployment",
        "public_release",
        "public_operation",
        "public_api",
        "third_party_access",
        "third_party_execution",
        "external_user_operation",
        "production_use",
        "merge_to_main",
    ],
)
def test_external_or_main_operation_remains_disabled(field: str) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(TeacherActorBoundSelfResearchCandidate(), **{field: True})
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("research_actor", "CHATGPT_WORK"),
        ("research_object", "GENERIC_BODY_MODEL"),
        ("bound_body_model_id", "OTHER_BODY"),
        ("biological_self_experiment", True),
        ("literal_physical_self_claim", True),
        ("identity_continuity_claim", True),
        ("subjectivity", "ESTABLISHED"),
        ("consciousness", "ESTABLISHED"),
        ("phenomenal_experience", "ESTABLISHED"),
        ("canonical_effect", "PROMOTE"),
    ],
)
def test_binding_or_claim_boundary_changes_fail_closed(
    field: str,
    value: object,
) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(TeacherActorBoundSelfResearchCandidate(), **{field: value})
        )
