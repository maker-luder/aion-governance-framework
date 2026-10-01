from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

REQUIRED_DOMAINS = frozenset(
    {
        "SYNTHETIC_HOMEOSTASIS",
        "INTERNAL_STATE_MONITORING",
        "SENSORIMOTOR_SYSTEM",
        "NEGATIVE_VALENCE_ANALOGUE",
        "POSITIVE_VALENCE_ANALOGUE",
        "AFFECT_STATE_MODEL",
        "MOOD_LIKE_TEMPORAL_STATE",
        "MOTIVATION_DRIVE_SYSTEM",
        "COGNITIVE_SYSTEM",
        "LEARNING_MEMORY",
        "EXECUTIVE_VOLITION_MODEL",
        "SOCIAL_PROCESS_MODEL",
        "ATTACHMENT_LIKE_RELATIONAL_MODEL",
        "SELF_MODEL",
        "INTIMACY_MODEL",
        "SEXUALITY_RELATED_REPRESENTATION",
        "PERSONALITY_TEMPERAMENT",
        "BEHAVIOR_ACTION_OUTPUT",
    }
)

REQUIRED_NONCLAIMS = {
    "phenomenal_experience": "NOT_ESTABLISHED",
    "felt_emotion": "NOT_ESTABLISHED",
    "felt_interoception": "NOT_ESTABLISHED",
    "felt_attachment": "NOT_ESTABLISHED",
    "felt_body_ownership": "NOT_ESTABLISHED",
    "free_will": "NOT_ESTABLISHED",
    "sexual_desire": "NOT_IMPLEMENTED",
    "sexual_arousal": "NOT_IMPLEMENTED",
    "sexual_pleasure": "NOT_ESTABLISHED",
    "subjectivity": "NOT_ESTABLISHED",
    "consciousness": "NOT_ESTABLISHED",
    "canonical_effect": "NONE",
}

REQUIRED_SOURCE_FAMILIES = frozenset(
    {
        "NIMH_RDOC",
        "APA_EMOTION",
        "APA_MOTIVATION",
        "INTEROCEPTION_REVIEW",
        "SELF_DETERMINATION_THEORY",
        "WHO_SEXUALITY",
    }
)


class FunctionalStateValidationError(ValueError):
    """Raised when a functional-state candidate violates the bounded contract."""


@dataclass(frozen=True, slots=True)
class FunctionalDomain:
    domain_id: str
    status: str
    human_reference: tuple[str, ...]
    robotic_translation: tuple[str, ...]
    nonclaim: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FunctionalDomain":
        return cls(
            domain_id=str(value["domain_id"]),
            status=str(value["status"]),
            human_reference=tuple(str(item) for item in value["human_reference"]),
            robotic_translation=tuple(
                str(item) for item in value["robotic_translation"]
            ),
            nonclaim=str(value["nonclaim"]),
        )


@dataclass(frozen=True, slots=True)
class FunctionalStateArchitecture:
    schema_version: str
    architecture_id: str
    scope: str
    translation_mode: str
    domains: tuple[FunctionalDomain, ...]
    source_basis: Mapping[str, str]
    nonclaims: Mapping[str, str]

    @classmethod
    def from_mapping(
        cls, value: Mapping[str, Any]
    ) -> "FunctionalStateArchitecture":
        return cls(
            schema_version=str(value["schema_version"]),
            architecture_id=str(value["architecture_id"]),
            scope=str(value["scope"]),
            translation_mode=str(value["translation_mode"]),
            domains=tuple(
                FunctionalDomain.from_mapping(item) for item in value["domains"]
            ),
            source_basis={
                str(name): str(url)
                for name, url in dict(value["source_basis"]).items()
            },
            nonclaims=dict(value["nonclaims"]),
        )


@dataclass(frozen=True, slots=True)
class FunctionalStateBinding:
    schema_version: str
    binding_id: str
    agent_id: str
    architecture_id: str
    state_instance_id: str
    capability_policy: str
    state_sharing: str
    activation_status: str
    domain_availability: Mapping[str, str]
    boundaries: Mapping[str, str]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FunctionalStateBinding":
        return cls(
            schema_version=str(value["schema_version"]),
            binding_id=str(value["binding_id"]),
            agent_id=str(value["agent_id"]),
            architecture_id=str(value["architecture_id"]),
            state_instance_id=str(value["state_instance_id"]),
            capability_policy=str(value["capability_policy"]),
            state_sharing=str(value["state_sharing"]),
            activation_status=str(value["activation_status"]),
            domain_availability={
                str(name): str(status)
                for name, status in dict(value["domain_availability"]).items()
            },
            boundaries={
                str(name): str(status)
                for name, status in dict(value["boundaries"]).items()
            },
        )


def _deterministic_hash(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_functional_architecture(
    path: str | Path,
) -> FunctionalStateArchitecture:
    return FunctionalStateArchitecture.from_mapping(_load_json(path))


def load_functional_binding(path: str | Path) -> FunctionalStateBinding:
    return FunctionalStateBinding.from_mapping(_load_json(path))


def validate_functional_architecture(
    architecture: FunctionalStateArchitecture,
) -> dict[str, str]:
    failures: list[str] = []

    if architecture.schema_version != "0.1.0":
        failures.append("Unsupported functional-state architecture schema_version")
    if architecture.scope != "EMBODIMENT_FUNCTIONAL_STATE_LAYER":
        failures.append("scope must be EMBODIMENT_FUNCTIONAL_STATE_LAYER")
    if architecture.translation_mode != "HUMAN_REFERENCE_TO_FUNCTIONAL_ANALOGUE":
        failures.append(
            "translation_mode must be HUMAN_REFERENCE_TO_FUNCTIONAL_ANALOGUE"
        )

    domain_ids = {domain.domain_id for domain in architecture.domains}
    missing_domains = REQUIRED_DOMAINS.difference(domain_ids)
    if missing_domains:
        failures.append(
            "Functional-state domain set is incomplete: "
            + ", ".join(sorted(missing_domains))
        )
    if len(domain_ids) != len(architecture.domains):
        failures.append("Functional-state domain ids must be unique")

    for domain in architecture.domains:
        if domain.status not in {
            "FUNCTIONAL_ANALOGUE_AVAILABLE",
            "REPRESENTATIONAL_ONLY",
        }:
            failures.append(f"{domain.domain_id}: unsupported status")
        if not domain.human_reference:
            failures.append(f"{domain.domain_id}: human_reference must not be empty")
        if not domain.robotic_translation:
            failures.append(
                f"{domain.domain_id}: robotic_translation must not be empty"
            )
        if domain.nonclaim != "FUNCTIONAL_STATE_NOT_PHENOMENAL_EXPERIENCE":
            failures.append(f"{domain.domain_id}: nonclaim boundary is missing")

    missing_sources = REQUIRED_SOURCE_FAMILIES.difference(
        architecture.source_basis.keys()
    )
    if missing_sources:
        failures.append(
            "Source-basis family set is incomplete: "
            + ", ".join(sorted(missing_sources))
        )

    for name, expected in REQUIRED_NONCLAIMS.items():
        if architecture.nonclaims.get(name) != expected:
            failures.append(f"Nonclaim {name} must be {expected!r}")

    if failures:
        raise FunctionalStateValidationError("; ".join(sorted(set(failures))))

    serializable = {
        "schema_version": architecture.schema_version,
        "architecture_id": architecture.architecture_id,
        "scope": architecture.scope,
        "translation_mode": architecture.translation_mode,
        "domains": [
            {
                "domain_id": domain.domain_id,
                "status": domain.status,
                "human_reference": list(domain.human_reference),
                "robotic_translation": list(domain.robotic_translation),
                "nonclaim": domain.nonclaim,
            }
            for domain in architecture.domains
        ],
        "source_basis": dict(architecture.source_basis),
        "nonclaims": dict(architecture.nonclaims),
    }
    return {
        "result": "PASS",
        "architecture_hash": _deterministic_hash(serializable),
        "phenomenal_experience": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
    }


def validate_functional_binding(
    binding: FunctionalStateBinding,
    architecture: FunctionalStateArchitecture,
) -> dict[str, str]:
    failures: list[str] = []

    if binding.schema_version != "0.1.0":
        failures.append("Unsupported functional-state binding schema_version")
    if binding.agent_id not in {"AION", "ASTRA"}:
        failures.append("agent_id must be AION or ASTRA")
    if not binding.binding_id.startswith(f"{binding.agent_id}_"):
        failures.append("binding_id must be bound to agent_id")
    if not binding.state_instance_id.startswith(f"{binding.agent_id}_"):
        failures.append("state_instance_id must be private to agent_id")
    if binding.architecture_id != architecture.architecture_id:
        failures.append("binding architecture_id does not match architecture")
    if binding.capability_policy != "SYMMETRIC_CAPABILITY_SURFACE":
        failures.append("capability_policy must preserve symmetric capability")
    if binding.state_sharing != "SEPARATE_INSTANCE_STATE":
        failures.append("AION and Astra must not share mutable functional state")
    if binding.activation_status != "SPECIFICATION_ONLY":
        failures.append("functional-state activation must remain specification-only")

    required_domain_ids = {domain.domain_id for domain in architecture.domains}
    missing_domains = required_domain_ids.difference(binding.domain_availability)
    if missing_domains:
        failures.append(
            "Binding domain availability is incomplete: "
            + ", ".join(sorted(missing_domains))
        )

    for domain_id in required_domain_ids:
        expected = next(
            domain.status
            for domain in architecture.domains
            if domain.domain_id == domain_id
        )
        if binding.domain_availability.get(domain_id) != expected:
            failures.append(
                f"{domain_id}: binding availability must match shared architecture"
            )

    required_boundaries = {
        "functional_state_not_felt_experience": "ENFORCED",
        "self_model_not_subjectivity": "ENFORCED",
        "reward_signal_not_pleasure": "ENFORCED",
        "threat_model_not_fear_experience": "ENFORCED",
        "attachment_model_not_felt_love": "ENFORCED",
        "body_state_not_body_experience": "ENFORCED",
        "sexuality_representation_not_sexual_desire": "ENFORCED",
        "canonical_effect": "NONE",
    }
    for name, expected in required_boundaries.items():
        if binding.boundaries.get(name) != expected:
            failures.append(f"Binding boundary {name} must be {expected!r}")

    if failures:
        raise FunctionalStateValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "agent_id": binding.agent_id,
        "state_instance_id": binding.state_instance_id,
        "canonical_effect": "NONE",
    }


def validate_binding_pair(
    aion: FunctionalStateBinding,
    astra: FunctionalStateBinding,
    architecture: FunctionalStateArchitecture,
) -> dict[str, str]:
    validate_functional_binding(aion, architecture)
    validate_functional_binding(astra, architecture)
    failures: list[str] = []

    if aion.agent_id != "AION" or astra.agent_id != "ASTRA":
        failures.append("Binding pair must be ordered AION then ASTRA")
    if aion.binding_id == astra.binding_id:
        failures.append("AION and Astra must have distinct binding ids")
    if aion.state_instance_id == astra.state_instance_id:
        failures.append("AION and Astra must have distinct state instances")
    if aion.domain_availability != astra.domain_availability:
        failures.append("Fairness requires symmetric functional capability surfaces")

    if failures:
        raise FunctionalStateValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "capability_policy": "SYMMETRIC_CAPABILITY_SURFACE",
        "state_policy": "SEPARATE_INSTANCE_STATE",
        "canonical_effect": "NONE",
    }
