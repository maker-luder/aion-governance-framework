from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .errors import ValidationError
from .json_types import JsonValue


class CapabilityArtifactStatus(StrEnum):
    CANDIDATE_ARTIFACT = "CANDIDATE_ARTIFACT"
    EXPERIMENT_ONLY = "EXPERIMENT_ONLY"
    QA_HOLD = "QA_HOLD"
    REJECTED = "REJECTED"
    APPROVED_CAPABILITY_ARTIFACT_CANDIDATE = "APPROVED_CAPABILITY_ARTIFACT_CANDIDATE"
    APPROVED_CAPABILITY_ARTIFACT = "APPROVED_CAPABILITY_ARTIFACT"


class ProposalStatus(StrEnum):
    RESEARCH_PROPOSAL = "RESEARCH_PROPOSAL"
    SCOPE_HOLD = "SCOPE_HOLD"
    ARCHITECTURE_PROPOSAL = "ARCHITECTURE_PROPOSAL"


LANGUAGE_CORE_CLASSIFICATION = "LANGUAGE_CAPABILITY_LAYER"
LANGUAGE_CORE_ALTERNATE_CLASSIFICATION = "LANGUAGE_PROCESSING_COMPONENT"
LANGUAGE_CORE_IS_IDENTITY_CORE = False


@dataclass(frozen=True, slots=True)
class CapabilityArtifactRecord:
    artifact_id: str
    artifact_status: CapabilityArtifactStatus = CapabilityArtifactStatus.CANDIDATE_ARTIFACT
    qa_status: str = "QA_HOLD"
    canonical_effect: str = "NONE"
    identity_inheritance: str = "DENIED"
    memory_writeback: str = "DENIED"
    tool_privilege_inheritance: str = "DENIED"
    runtime_admission: str = "NOT_APPROVED"

    def __post_init__(self) -> None:
        if not self.artifact_id.strip():
            raise ValidationError("artifact_id must be non-empty")
        if self.canonical_effect != "NONE":
            raise ValidationError("capability artifacts cannot write canonical state")
        if self.identity_inheritance != "DENIED":
            raise ValidationError("capability artifacts cannot inherit AION/Astra identity")
        if self.memory_writeback != "DENIED" or self.tool_privilege_inheritance != "DENIED":
            raise ValidationError("capability artifacts cannot inherit memory or tool authority")

    def may_be_called_aion_or_astra(self) -> bool:
        return False

    def may_promote(self, *, all_gates_passed: bool, owner_approved: bool) -> bool:
        return all_gates_passed and owner_approved


@dataclass(frozen=True, slots=True)
class ResearchProposal:
    proposal_id: str
    title: str
    target: str
    status: ProposalStatus
    source: str
    implementation: str = "NOT_STARTED"
    canonical_effect: str = "NONE"
    qa_status: str = "QA_HOLD"
    human_approval_required: bool = True
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    preference_origin: str = "NOT_ESTABLISHED"
    model_download_triggered: bool = False
    dataset_creation_triggered: bool = False
    training_triggered: bool = False
    lora_triggered: bool = False
    ablation_triggered: bool = False
    runtime_privilege_triggered: bool = False
    canonical_writeback_triggered: bool = False

    def __post_init__(self) -> None:
        if not self.proposal_id.strip() or not self.title.strip() or not self.target.strip():
            raise ValidationError("proposal identity fields must be non-empty")
        if self.implementation != "NOT_STARTED":
            raise ValidationError("registered research proposals must remain NOT_STARTED")
        if self.canonical_effect != "NONE" or self.canonical_writeback_triggered:
            raise ValidationError("research proposals cannot change canonical state")
        if self.qa_status != "QA_HOLD":
            raise ValidationError("unimplemented research proposals must remain QA_HOLD")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValidationError("research proposals cannot establish subjectivity")
        if not self.human_approval_required:
            raise ValidationError("research proposals require human approval")
        if any(
            (
                self.model_download_triggered,
                self.dataset_creation_triggered,
                self.training_triggered,
                self.lora_triggered,
                self.ablation_triggered,
                self.runtime_privilege_triggered,
            )
        ):
            raise ValidationError("registration must not trigger engineering execution")

    def side_effects(self) -> dict[str, bool]:
        return {
            "model_download": self.model_download_triggered,
            "dataset_creation": self.dataset_creation_triggered,
            "training": self.training_triggered,
            "lora": self.lora_triggered,
            "ablation": self.ablation_triggered,
            "runtime_privilege": self.runtime_privilege_triggered,
            "canonical_writeback": self.canonical_writeback_triggered,
        }

    def may_promote(self, *, owner_approved: bool) -> bool:
        return owner_approved and self.implementation != "NOT_STARTED"


def _text(data: dict[str, JsonValue], key: str, default: str | None = None) -> str:
    value = data.get(key, default)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{key} must be a non-empty string")
    return value


def _boolean(data: dict[str, JsonValue], key: str, default: bool) -> bool:
    value = data.get(key, default)
    if not isinstance(value, bool):
        raise ValidationError(f"{key} must be a boolean")
    return value


def proposal_from_dict(data: dict[str, JsonValue]) -> ResearchProposal:
    triggers_value = data.get("execution_triggers", {})
    if not isinstance(triggers_value, dict):
        raise ValidationError("execution_triggers must be an object")
    triggers: dict[str, JsonValue] = triggers_value
    try:
        status = ProposalStatus(_text(data, "status"))
    except ValueError as exc:
        raise ValidationError("unsupported research proposal status") from exc
    return ResearchProposal(
        proposal_id=_text(data, "proposal_id"),
        title=_text(data, "title"),
        target=_text(data, "target"),
        status=status,
        source=_text(data, "source"),
        implementation=_text(data, "implementation", "NOT_STARTED"),
        canonical_effect=_text(data, "canonical_effect", "NONE"),
        qa_status=_text(data, "qa_status", "QA_HOLD"),
        human_approval_required=_boolean(data, "human_approval_required", True),
        subjectivity_conclusion=_text(data, "subjectivity_conclusion", "NOT_ESTABLISHED"),
        preference_origin=_text(data, "preference_origin", "NOT_ESTABLISHED"),
        model_download_triggered=_boolean(triggers, "model_download", False),
        dataset_creation_triggered=_boolean(triggers, "dataset_creation", False),
        training_triggered=_boolean(triggers, "training", False),
        lora_triggered=_boolean(triggers, "lora", False),
        ablation_triggered=_boolean(triggers, "ablation", False),
        runtime_privilege_triggered=_boolean(triggers, "runtime_privilege", False),
        canonical_writeback_triggered=_boolean(triggers, "canonical_writeback", False),
    )


def language_core_definition() -> dict[str, str | bool]:
    return {
        "classification": LANGUAGE_CORE_CLASSIFICATION,
        "alternate_classification": LANGUAGE_CORE_ALTERNATE_CLASSIFICATION,
        "identity_core": LANGUAGE_CORE_IS_IDENTITY_CORE,
        "canonical_effect": "NONE",
    }
