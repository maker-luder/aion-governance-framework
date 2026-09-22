"""Deterministic synthetic sensorimotor embodiment QA.

This module extends the existing twin-genesis embodiment candidate with a
content-addressed action -> expected consequence -> observed feedback ->
body-model update trace.

It does not implement live sensing, physical actuation, body sensation, pain,
body ownership experience, consciousness, or subjectivity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from hashlib import sha256

from .models import EmbodimentInstance
from .validation import ValidationError, deterministic_hash


class RegionCondition(StrEnum):
    BASELINE = "BASELINE"
    PERTURBED = "PERTURBED"


class SensorimotorDisposition(StrEnum):
    RETAIN = "RETAIN"
    HOLD = "HOLD"
    LOCALIZE_PERTURBATION = "LOCALIZE_PERTURBATION"
    RECORD_RECOVERY = "RECORD_RECOVERY"


def _require_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise ValidationError(f"{name} must be non-empty text")


def _require_digest(name: str, value: str) -> None:
    if (
        type(value) is not str
        or len(value) != 64
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise ValidationError(f"{name} must be a lowercase SHA-256 digest")


def _require_content_address(name: str, text: str, digest: str) -> None:
    _require_text(f"{name}_text", text)
    _require_digest(f"{name}_sha256", digest)
    if sha256(text.encode("utf-8")).hexdigest() != digest:
        raise ValidationError(f"{name}_sha256 must match {name}_text")


def _require_synthetic_boundary(
    *,
    synthetic: bool,
    live_input: bool,
    human_participant_observed: bool,
    contains_private_material: bool,
) -> None:
    for name, value in (
        ("synthetic", synthetic),
        ("live_input", live_input),
        ("human_participant_observed", human_participant_observed),
        ("contains_private_material", contains_private_material),
    ):
        if type(value) is not bool:
            raise ValidationError(f"{name} must be an exact bool")
    if not synthetic:
        raise ValidationError("v0.1.0 sensorimotor QA accepts synthetic records only")
    if live_input:
        raise ValidationError("live sensor or execution input is outside this candidate")
    if human_participant_observed:
        raise ValidationError("human participant observations are outside this candidate")
    if contains_private_material:
        raise ValidationError("private material is excluded from this candidate")


@dataclass(frozen=True, slots=True)
class BodyRegionState:
    region_id: str
    condition: RegionCondition

    def __post_init__(self) -> None:
        _require_text("region_id", self.region_id)
        if type(self.condition) is not RegionCondition:
            raise ValidationError("condition must be an exact RegionCondition")


@dataclass(frozen=True, slots=True)
class BodyModelSnapshot:
    snapshot_id: str
    embodiment_id: str
    sequence: int
    regions: tuple[BodyRegionState, ...]
    predecessor_snapshot_sha256: str | None = None
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        _require_text("snapshot_id", self.snapshot_id)
        _require_text("embodiment_id", self.embodiment_id)
        if type(self.sequence) is not int or self.sequence < 0:
            raise ValidationError("sequence must be a non-negative exact int")
        if type(self.regions) is not tuple or not self.regions:
            raise ValidationError("regions must be a non-empty tuple")
        if any(type(item) is not BodyRegionState for item in self.regions):
            raise ValidationError("regions must contain exact BodyRegionState values")
        region_ids = [item.region_id for item in self.regions]
        if len(region_ids) != len(set(region_ids)):
            raise ValidationError("body model region identifiers must be unique")
        if self.sequence == 0:
            if self.predecessor_snapshot_sha256 is not None:
                raise ValidationError("sequence zero body model cannot declare a predecessor")
        else:
            if self.predecessor_snapshot_sha256 is None:
                raise ValidationError("non-initial body model requires predecessor binding")
            _require_digest(
                "predecessor_snapshot_sha256", self.predecessor_snapshot_sha256
            )
        if self.canonical_effect != "NONE":
            raise ValidationError("sensorimotor body model must have no canonical effect")


@dataclass(frozen=True, slots=True)
class SensorimotorPrediction:
    prediction_id: str
    embodiment_id: str
    body_snapshot_sha256: str
    action_text: str
    action_sha256: str
    expected_feedback_text: str
    expected_feedback_sha256: str
    synthetic: bool = True
    live_execution: bool = False
    human_participant_observed: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        _require_text("prediction_id", self.prediction_id)
        _require_text("embodiment_id", self.embodiment_id)
        _require_digest("body_snapshot_sha256", self.body_snapshot_sha256)
        _require_content_address("action", self.action_text, self.action_sha256)
        _require_content_address(
            "expected_feedback",
            self.expected_feedback_text,
            self.expected_feedback_sha256,
        )
        _require_synthetic_boundary(
            synthetic=self.synthetic,
            live_input=self.live_execution,
            human_participant_observed=self.human_participant_observed,
            contains_private_material=self.contains_private_material,
        )


@dataclass(frozen=True, slots=True)
class SensorimotorObservation:
    observation_id: str
    prediction_id: str
    prediction_sha256: str
    observed_feedback_text: str
    observed_feedback_sha256: str
    affected_regions: tuple[str, ...]
    synthetic: bool = True
    live_sensor_input: bool = False
    human_participant_observed: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        _require_text("observation_id", self.observation_id)
        _require_text("prediction_id", self.prediction_id)
        _require_digest("prediction_sha256", self.prediction_sha256)
        _require_content_address(
            "observed_feedback",
            self.observed_feedback_text,
            self.observed_feedback_sha256,
        )
        if type(self.affected_regions) is not tuple or not self.affected_regions:
            raise ValidationError("affected_regions must be a non-empty tuple")
        for region_id in self.affected_regions:
            _require_text("affected region id", region_id)
        if len(self.affected_regions) != len(set(self.affected_regions)):
            raise ValidationError("affected_regions must be unique")
        _require_synthetic_boundary(
            synthetic=self.synthetic,
            live_input=self.live_sensor_input,
            human_participant_observed=self.human_participant_observed,
            contains_private_material=self.contains_private_material,
        )


@dataclass(frozen=True, slots=True)
class SensorimotorTransitionAudit:
    embodiment_id: str
    before_snapshot_sha256: str
    prediction_sha256: str
    observation_sha256: str
    after_snapshot_sha256: str
    disposition: SensorimotorDisposition
    prediction_error_present: bool
    action_consequence_bound: bool
    body_model_updated: bool
    perturbation_localized: bool
    recovery_state_transition: bool
    changed_regions: tuple[str, ...]
    mode: str = "DETERMINISTIC_SYNTHETIC_SENSORIMOTOR_QA"
    empirical_data_collected: bool = False
    body_sensation: str = "NOT_ESTABLISHED"
    pain: str = "NOT_ESTABLISHED"
    body_ownership_experience: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False


def body_model_snapshot_hash(snapshot: BodyModelSnapshot) -> str:
    if type(snapshot) is not BodyModelSnapshot:
        raise ValidationError("snapshot must be an exact BodyModelSnapshot")
    return deterministic_hash(asdict(snapshot))


def sensorimotor_prediction_hash(prediction: SensorimotorPrediction) -> str:
    if type(prediction) is not SensorimotorPrediction:
        raise ValidationError("prediction must be an exact SensorimotorPrediction")
    return deterministic_hash(asdict(prediction))


def sensorimotor_observation_hash(observation: SensorimotorObservation) -> str:
    if type(observation) is not SensorimotorObservation:
        raise ValidationError("observation must be an exact SensorimotorObservation")
    return deterministic_hash(asdict(observation))


def audit_sensorimotor_transition(
    instance: EmbodimentInstance,
    before: BodyModelSnapshot,
    prediction: SensorimotorPrediction,
    observation: SensorimotorObservation,
    after: BodyModelSnapshot,
    disposition: SensorimotorDisposition,
) -> SensorimotorTransitionAudit:
    if type(instance) is not EmbodimentInstance:
        raise ValidationError("instance must be an exact EmbodimentInstance")
    if type(before) is not BodyModelSnapshot or type(after) is not BodyModelSnapshot:
        raise ValidationError("before and after must be exact BodyModelSnapshot values")
    if type(prediction) is not SensorimotorPrediction:
        raise ValidationError("prediction must be an exact SensorimotorPrediction")
    if type(observation) is not SensorimotorObservation:
        raise ValidationError("observation must be an exact SensorimotorObservation")
    if type(disposition) is not SensorimotorDisposition:
        raise ValidationError("disposition must be an exact SensorimotorDisposition")

    if instance.canonical_effect != "NONE":
        raise ValidationError("embodiment instance must retain canonical_effect NONE")
    if instance.body_sensation != "NOT_ESTABLISHED":
        raise ValidationError("body sensation must remain NOT_ESTABLISHED")

    expected_embodiment_id = instance.embodiment_id
    for name, value in (
        ("before", before.embodiment_id),
        ("prediction", prediction.embodiment_id),
        ("after", after.embodiment_id),
    ):
        if value != expected_embodiment_id:
            raise ValidationError(f"{name} must bind the selected embodiment instance")

    before_hash = body_model_snapshot_hash(before)
    if prediction.body_snapshot_sha256 != before_hash:
        raise ValidationError("prediction must bind the exact before body-model snapshot")
    if observation.prediction_id != prediction.prediction_id:
        raise ValidationError("observation must bind the prediction_id")
    if observation.prediction_sha256 != sensorimotor_prediction_hash(prediction):
        raise ValidationError("observation must bind the exact prediction content")

    if after.sequence != before.sequence + 1:
        raise ValidationError("after body-model sequence must increment exactly once")
    if after.predecessor_snapshot_sha256 != before_hash:
        raise ValidationError("after body model must bind the exact predecessor snapshot")

    before_by_region = {item.region_id: item.condition for item in before.regions}
    after_by_region = {item.region_id: item.condition for item in after.regions}
    if set(before_by_region) != set(after_by_region):
        raise ValidationError("body-model region set cannot drift during a transition")

    affected = set(observation.affected_regions)
    if not affected.issubset(before_by_region):
        raise ValidationError("affected regions must exist in the body model")

    changed = tuple(
        region_id
        for region_id in before_by_region
        if before_by_region[region_id] is not after_by_region[region_id]
    )
    if not set(changed).issubset(affected):
        raise ValidationError("body-model changes must be localized to affected regions")

    prediction_error = (
        prediction.expected_feedback_sha256 != observation.observed_feedback_sha256
    )

    if disposition is SensorimotorDisposition.RETAIN:
        if prediction_error:
            raise ValidationError("RETAIN requires expected and observed feedback to match")
        if changed:
            raise ValidationError("RETAIN cannot change the body model")
    elif disposition is SensorimotorDisposition.HOLD:
        if not prediction_error:
            raise ValidationError("HOLD is reserved for unresolved prediction error")
        if changed:
            raise ValidationError("HOLD cannot silently change the body model")
    elif disposition is SensorimotorDisposition.LOCALIZE_PERTURBATION:
        if not prediction_error:
            raise ValidationError("perturbation localization requires prediction error")
        if not changed:
            raise ValidationError("perturbation localization requires a body-model change")
        for region_id in changed:
            if (
                before_by_region[region_id] is not RegionCondition.BASELINE
                or after_by_region[region_id] is not RegionCondition.PERTURBED
            ):
                raise ValidationError(
                    "perturbation localization only permits BASELINE -> PERTURBED"
                )
    elif disposition is SensorimotorDisposition.RECORD_RECOVERY:
        if prediction_error:
            raise ValidationError("recovery requires expected and observed feedback to match")
        if not changed:
            raise ValidationError("recovery requires a body-model change")
        for region_id in changed:
            if (
                before_by_region[region_id] is not RegionCondition.PERTURBED
                or after_by_region[region_id] is not RegionCondition.BASELINE
            ):
                raise ValidationError(
                    "recovery only permits PERTURBED -> BASELINE"
                )

    return SensorimotorTransitionAudit(
        embodiment_id=expected_embodiment_id,
        before_snapshot_sha256=before_hash,
        prediction_sha256=sensorimotor_prediction_hash(prediction),
        observation_sha256=sensorimotor_observation_hash(observation),
        after_snapshot_sha256=body_model_snapshot_hash(after),
        disposition=disposition,
        prediction_error_present=prediction_error,
        action_consequence_bound=True,
        body_model_updated=bool(changed),
        perturbation_localized=(
            disposition is SensorimotorDisposition.LOCALIZE_PERTURBATION
        ),
        recovery_state_transition=(
            disposition is SensorimotorDisposition.RECORD_RECOVERY
        ),
        changed_regions=changed,
    )