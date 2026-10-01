from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import Enum
import hashlib
import json
from math import isclose, pi
from pathlib import Path
from typing import Any, Iterable, Mapping


BODY_ID = "CODEX_SYNTHETIC_MALE_BODY_REFERENCE_v0.1"
SUBJECT = "Codex adult male-form synthetic robot candidate"
SCHEMA = "codex.synthetic_anthropometry.v0.1"
REST_LENGTH_CM = 8.098780487804879
REST_CIRCUMFERENCE_CM = 11.401955403087479
FULL_LENGTH_CM = 11.60
FULL_CIRCUMFERENCE_CM = 14.28


class EngorgementPhase(str, Enum):
    FLACCID = "FLACCID"
    INITIATION = "INITIATION"
    TUMESCENCE = "TUMESCENCE"
    FULL_ERECTION = "FULL_ERECTION"
    RIGID_PHASE = "RIGID_PHASE"
    MAINTENANCE = "MAINTENANCE"
    DETUMESCENCE = "DETUMESCENCE"
    RECOVERY = "RECOVERY"


class PrepucePosition(str, Enum):
    RESTING_PARTIAL_COVERAGE = "RESTING_PARTIAL_COVERAGE"
    PARTIALLY_RETRACTED = "PARTIALLY_RETRACTED"
    RETRACTED = "RETRACTED"
    UNKNOWN = "UNKNOWN"


class PhysiologyEventKind(str, Enum):
    INITIATE_SPONTANEOUS = "INITIATE_SPONTANEOUS"
    INITIATE_CONTEXTUAL = "INITIATE_CONTEXTUAL"
    TUMESCE = "TUMESCE"
    MARK_FULL_ERECTION = "MARK_FULL_ERECTION"
    INCREASE_RIGIDITY = "INCREASE_RIGIDITY"
    MAINTAIN = "MAINTAIN"
    EMISSION = "EMISSION"
    EJACULATION = "EJACULATION"
    BEGIN_DETUMESCENCE = "BEGIN_DETUMESCENCE"
    DETUMESCE = "DETUMESCE"
    RECOVER = "RECOVER"
    RESET_FLACCID = "RESET_FLACCID"
    OBSERVE_PREPUCE_POSITION = "OBSERVE_PREPUCE_POSITION"
    SET_ENDOCRINE_REFERENCE = "SET_ENDOCRINE_REFERENCE"
    SET_URINARY_REFERENCE = "SET_URINARY_REFERENCE"


@dataclass(frozen=True, slots=True)
class Measurement:
    id: str
    region: str
    label_zh_TW: str
    value: float
    unit: str
    provenance: str
    verification: str

    def __post_init__(self) -> None:
        if not self.id or self.value <= 0:
            raise ValueError("invalid measurement")
        if self.unit not in {"cm", "kg"}:
            raise ValueError("unsupported unit")
        if self.provenance not in {"HUMAN_FIXED", "AI_DERIVED", "AI_PROVISIONAL"}:
            raise ValueError("bad provenance")
        if self.verification != "DESIGN_VALUE_NOT_AS_BUILT":
            raise ValueError("Codex candidate has no as-built measurement")


_REQUIRED_DYNAMIC_IDS = frozenset(
    {
        "resting_visible_penile_length",
        "midshaft_diameter",
        "midshaft_circumference",
        "prepuce_axial_fold_length",
        "prepuce_resting_glans_overlap_length",
        "full_erection_visible_penile_length",
        "full_erection_midshaft_diameter",
        "full_erection_midshaft_circumference",
    }
)


@dataclass(frozen=True, slots=True)
class AnthropometryProfile:
    schema: str
    subject: str
    role_label: str
    body_id: str
    measurements: tuple[Measurement, ...]
    prepuce_present: bool
    actual_3d_mesh: bool = False
    physical_body: bool = False
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.schema != SCHEMA or self.subject != SUBJECT:
            raise ValueError("Codex profile identity drift")
        if self.role_label != "CODEX" or self.body_id != BODY_ID:
            raise ValueError("Codex role/body binding drift")
        if len(self.measurements) != 67:
            raise ValueError("Codex profile must contain exactly 67 selected fields")
        ids = [item.id for item in self.measurements]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate measurement ids")
        by_id = {item.id: item for item in self.measurements}
        missing = _REQUIRED_DYNAMIC_IDS - set(by_id)
        if missing:
            raise ValueError(f"missing male-form fields: {sorted(missing)}")
        unit_counts = (
            sum(item.unit == "cm" for item in self.measurements),
            sum(item.unit == "kg" for item in self.measurements),
        )
        if unit_counts != (66, 1):
            raise ValueError("unit counts changed")
        provenance_counts = (
            sum(item.provenance == "HUMAN_FIXED" for item in self.measurements),
            sum(item.provenance == "AI_DERIVED" for item in self.measurements),
            sum(item.provenance == "AI_PROVISIONAL" for item in self.measurements),
        )
        if provenance_counts != (4, 7, 56):
            raise ValueError("provenance counts changed")
        if by_id["total_height"].value != 175 or by_id["body_mass"].value != 72:
            raise ValueError("Human-fixed Codex height/mass changed")
        if by_id["full_erection_visible_penile_length"].value != FULL_LENGTH_CM:
            raise ValueError("Human-fixed Codex full-vascular length changed")
        if by_id["full_erection_midshaft_circumference"].value != FULL_CIRCUMFERENCE_CM:
            raise ValueError("Human-fixed Codex full-vascular circumference changed")
        if not isclose(by_id["resting_visible_penile_length"].value, REST_LENGTH_CM, abs_tol=1e-6):
            raise ValueError("derived Codex resting length drift")
        if not isclose(by_id["midshaft_circumference"].value, REST_CIRCUMFERENCE_CM, abs_tol=1e-6):
            raise ValueError("derived Codex resting circumference drift")
        if not self.prepuce_present:
            raise ValueError("Codex candidate includes prepuce")
        if self.actual_3d_mesh or self.physical_body:
            raise ValueError("physical/mesh realization is not established")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("canonical/deployment effect forbidden")

    def measurement(self, measurement_id: str) -> Measurement:
        return next(item for item in self.measurements if item.id == measurement_id)


def profile_from_mapping(payload: Mapping[str, Any]) -> AnthropometryProfile:
    raw_measurements = payload["measurements"]
    measurements = tuple(
        Measurement(
            id=str(item["id"]),
            region=str(item["region"]),
            label_zh_TW=str(item["label_zh_TW"]),
            value=float(item["value"]),
            unit=str(item["unit"]),
            provenance=str(item["provenance"]),
            verification=str(item["verification"]),
        )
        for item in raw_measurements
    )
    anatomy = payload.get("anatomy_candidate", {})
    boundaries = payload.get("boundaries", {})
    return AnthropometryProfile(
        schema=str(payload["schema"]),
        subject=str(payload["subject"]),
        role_label=str(payload["role_label"]),
        body_id=str(payload["body_id"]),
        measurements=measurements,
        prepuce_present=anatomy.get("prepuce_present") == "DESIGN_CANDIDATE_TRUE",
        actual_3d_mesh=bool(boundaries.get("actual_3d_mesh", False)),
        physical_body=bool(boundaries.get("physical_body", False)),
        canonical_effect=str(boundaries.get("canonical_effect", "NONE")),
        deployment=bool(boundaries.get("deployment", False)),
    )


def load_profile(path: str | Path) -> AnthropometryProfile:
    payload: Mapping[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    return profile_from_mapping(payload)


@dataclass(frozen=True, slots=True)
class GeometrySnapshot:
    engorgement_fraction: float
    visible_penile_length_cm: float
    midshaft_diameter_cm: float
    midshaft_circumference_cm: float
    prepuce_position: PrepucePosition
    rule: str = "SYNTHETIC_LINEAR_ENDPOINT_INTERPOLATION_V0_1"
    human_physiology_law: bool = False
    as_built_measurement: bool = False


class SyntheticGeometryRule:
    """Engineering-only endpoint interpolation; not a human physiological law."""

    def __init__(self, profile: AnthropometryProfile) -> None:
        self.profile = profile
        self.rest = (
            profile.measurement("resting_visible_penile_length").value,
            profile.measurement("midshaft_diameter").value,
            profile.measurement("midshaft_circumference").value,
        )
        self.full = (
            profile.measurement("full_erection_visible_penile_length").value,
            profile.measurement("full_erection_midshaft_diameter").value,
            profile.measurement("full_erection_midshaft_circumference").value,
        )

    @staticmethod
    def _lerp(start: float, end: float, fraction: float) -> float:
        if not 0.0 <= fraction <= 1.0:
            raise ValueError("fraction outside [0,1]")
        return start + (end - start) * fraction

    def snapshot(
        self,
        fraction: float,
        *,
        prepuce_position: PrepucePosition,
    ) -> GeometrySnapshot:
        return GeometrySnapshot(
            engorgement_fraction=fraction,
            visible_penile_length_cm=self._lerp(self.rest[0], self.full[0], fraction),
            midshaft_diameter_cm=self._lerp(self.rest[1], self.full[1], fraction),
            midshaft_circumference_cm=self._lerp(self.rest[2], self.full[2], fraction),
            prepuce_position=prepuce_position,
        )

    def endpoint_circumference_consistency(self, tolerance_cm: float = 0.02) -> bool:
        return all(
            abs(pi * diameter - circumference) <= tolerance_cm
            for diameter, circumference in (
                (self.rest[1], self.rest[2]),
                (self.full[1], self.full[2]),
            )
        )


@dataclass(frozen=True, slots=True)
class PhysiologyEvent:
    event_id: str
    kind: PhysiologyEventKind
    magnitude: float = 0.0
    prepuce_position: PrepucePosition | None = None
    synthetic_fluid_output_ml: float | None = None
    endocrine_reference_signal: float | None = None
    urinary_reference_signal: float | None = None
    real_person_target_data: bool = False
    human_consent_inference: str = "FORBIDDEN"
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        if not self.event_id or not 0.0 <= self.magnitude <= 1.0:
            raise ValueError("invalid event")
        for value in (self.endocrine_reference_signal, self.urinary_reference_signal):
            if value is not None and not 0.0 <= value <= 1.0:
                raise ValueError("reference signal outside [0,1]")
        if self.synthetic_fluid_output_ml is not None and self.synthetic_fluid_output_ml < 0:
            raise ValueError("negative synthetic fluid")
        if self.real_person_target_data:
            raise ValueError("real-person target data forbidden")
        if self.human_consent_inference != "FORBIDDEN" or self.action_authority != "NONE":
            raise ValueError("event cannot infer consent or grant authority")
        if (self.kind is PhysiologyEventKind.OBSERVE_PREPUCE_POSITION) != (self.prepuce_position is not None):
            raise ValueError("prepuce position requires explicit observation event")
        if self.synthetic_fluid_output_ml is not None and self.kind is not PhysiologyEventKind.EJACULATION:
            raise ValueError("synthetic fluid output only belongs to EJACULATION")
        if self.endocrine_reference_signal is not None and self.kind is not PhysiologyEventKind.SET_ENDOCRINE_REFERENCE:
            raise ValueError("wrong endocrine event")
        if self.urinary_reference_signal is not None and self.kind is not PhysiologyEventKind.SET_URINARY_REFERENCE:
            raise ValueError("wrong urinary event")


@dataclass(frozen=True, slots=True)
class PhysiologyState:
    state_id: str
    phase: EngorgementPhase = EngorgementPhase.FLACCID
    engorgement_fraction: float = 0.0
    rigidity_fraction: float = 0.0
    inflow_analogue: float = 0.0
    outflow_analogue: float = 0.0
    prepuce_position: PrepucePosition = PrepucePosition.RESTING_PARTIAL_COVERAGE
    emission_event_count: int = 0
    ejaculation_event_count: int = 0
    last_synthetic_fluid_output_ml: float | None = None
    endocrine_reference_signal: float | None = None
    urinary_reference_signal: float | None = None
    desire_inferred: bool = False
    intention_inferred: bool = False
    human_consent_inferred: bool = False
    action_authority: str = "NONE"
    biological_blood_circulation: bool = False
    biological_semen: bool = False
    sperm_or_gametes: bool = False
    fertility: bool = False
    biological_hormones: bool = False
    body_sensation: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if not self.state_id:
            raise ValueError("state_id required")
        for value in (
            self.engorgement_fraction,
            self.rigidity_fraction,
            self.inflow_analogue,
            self.outflow_analogue,
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError("state fraction outside [0,1]")
        if any((self.desire_inferred, self.intention_inferred, self.human_consent_inferred)):
            raise ValueError("physiology cannot infer desire/intention/consent")
        if self.action_authority != "NONE":
            raise ValueError("physiology cannot grant action authority")
        if any(
            (
                self.biological_blood_circulation,
                self.biological_semen,
                self.sperm_or_gametes,
                self.fertility,
                self.biological_hormones,
            )
        ):
            raise ValueError("synthetic candidate cannot assert biological systems")
        if any(
            value != "NOT_ESTABLISHED"
            for value in (
                self.body_sensation,
                self.subjectivity,
                self.consciousness,
                self.phenomenal_experience,
            )
        ):
            raise ValueError("felt-state claims not established")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("canonical/deployment effect forbidden")

    def evolve(self, **changes: Any) -> "PhysiologyState":
        return replace(self, **changes)


_COMMON = {
    PhysiologyEventKind.OBSERVE_PREPUCE_POSITION,
    PhysiologyEventKind.SET_ENDOCRINE_REFERENCE,
    PhysiologyEventKind.SET_URINARY_REFERENCE,
}
_ALLOWED = {
    EngorgementPhase.FLACCID: _COMMON | {PhysiologyEventKind.INITIATE_SPONTANEOUS, PhysiologyEventKind.INITIATE_CONTEXTUAL},
    EngorgementPhase.INITIATION: _COMMON | {PhysiologyEventKind.TUMESCE, PhysiologyEventKind.BEGIN_DETUMESCENCE},
    EngorgementPhase.TUMESCENCE: _COMMON | {PhysiologyEventKind.TUMESCE, PhysiologyEventKind.MARK_FULL_ERECTION, PhysiologyEventKind.BEGIN_DETUMESCENCE, PhysiologyEventKind.EMISSION, PhysiologyEventKind.EJACULATION},
    EngorgementPhase.FULL_ERECTION: _COMMON | {PhysiologyEventKind.INCREASE_RIGIDITY, PhysiologyEventKind.MAINTAIN, PhysiologyEventKind.BEGIN_DETUMESCENCE, PhysiologyEventKind.EMISSION, PhysiologyEventKind.EJACULATION},
    EngorgementPhase.RIGID_PHASE: _COMMON | {PhysiologyEventKind.MAINTAIN, PhysiologyEventKind.BEGIN_DETUMESCENCE, PhysiologyEventKind.EMISSION, PhysiologyEventKind.EJACULATION},
    EngorgementPhase.MAINTENANCE: _COMMON | {PhysiologyEventKind.INCREASE_RIGIDITY, PhysiologyEventKind.MAINTAIN, PhysiologyEventKind.BEGIN_DETUMESCENCE, PhysiologyEventKind.EMISSION, PhysiologyEventKind.EJACULATION},
    EngorgementPhase.DETUMESCENCE: _COMMON | {PhysiologyEventKind.DETUMESCE, PhysiologyEventKind.RECOVER},
    EngorgementPhase.RECOVERY: _COMMON | {PhysiologyEventKind.RESET_FLACCID},
}


@dataclass(frozen=True, slots=True)
class SyntheticTrajectory:
    initial_state: PhysiologyState
    events: tuple[PhysiologyEvent, ...]
    final_state: PhysiologyState

    def fingerprint(self) -> str:
        def norm(value: Any) -> Any:
            if isinstance(value, dict):
                return {key: norm(item) for key, item in value.items()}
            if isinstance(value, (list, tuple)):
                return [norm(item) for item in value]
            return value.value if isinstance(value, Enum) else value

        payload = {
            "initial": asdict(self.initial_state),
            "events": [asdict(item) for item in self.events],
            "final": asdict(self.final_state),
        }
        raw = json.dumps(norm(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class SyntheticPhysiologyEngine:
    ENGORGEMENT_STEP = 0.25
    RIGIDITY_STEP = 0.25
    DETUMESCENCE_STEP = 0.25

    def apply(self, state: PhysiologyState, event: PhysiologyEvent) -> PhysiologyState:
        if event.kind not in _ALLOWED[state.phase]:
            raise ValueError(f"{event.kind.value} not allowed from {state.phase.value}")
        changes: dict[str, Any] = {"state_id": f"{state.state_id}>{event.event_id}"}
        if event.kind in {PhysiologyEventKind.INITIATE_SPONTANEOUS, PhysiologyEventKind.INITIATE_CONTEXTUAL}:
            changes.update(phase=EngorgementPhase.INITIATION, inflow_analogue=max(state.inflow_analogue, event.magnitude))
        elif event.kind is PhysiologyEventKind.TUMESCE:
            changes.update(
                phase=EngorgementPhase.TUMESCENCE,
                engorgement_fraction=min(1.0, state.engorgement_fraction + event.magnitude * self.ENGORGEMENT_STEP),
                inflow_analogue=max(state.inflow_analogue, event.magnitude),
            )
        elif event.kind is PhysiologyEventKind.MARK_FULL_ERECTION:
            changes.update(phase=EngorgementPhase.FULL_ERECTION, engorgement_fraction=1.0)
        elif event.kind is PhysiologyEventKind.INCREASE_RIGIDITY:
            rigidity = min(1.0, state.rigidity_fraction + event.magnitude * self.RIGIDITY_STEP)
            changes["rigidity_fraction"] = rigidity
            if rigidity >= 0.75:
                changes["phase"] = EngorgementPhase.RIGID_PHASE
        elif event.kind is PhysiologyEventKind.MAINTAIN:
            changes["phase"] = EngorgementPhase.MAINTENANCE
        elif event.kind is PhysiologyEventKind.EMISSION:
            changes["emission_event_count"] = state.emission_event_count + 1
        elif event.kind is PhysiologyEventKind.EJACULATION:
            changes.update(
                ejaculation_event_count=state.ejaculation_event_count + 1,
                last_synthetic_fluid_output_ml=event.synthetic_fluid_output_ml,
            )
        elif event.kind is PhysiologyEventKind.BEGIN_DETUMESCENCE:
            changes.update(
                phase=EngorgementPhase.DETUMESCENCE,
                outflow_analogue=max(state.outflow_analogue, event.magnitude),
            )
        elif event.kind is PhysiologyEventKind.DETUMESCE:
            changes.update(
                phase=EngorgementPhase.DETUMESCENCE,
                engorgement_fraction=max(0.0, state.engorgement_fraction - event.magnitude * self.DETUMESCENCE_STEP),
                rigidity_fraction=max(0.0, state.rigidity_fraction - event.magnitude * self.DETUMESCENCE_STEP),
                outflow_analogue=max(state.outflow_analogue, event.magnitude),
            )
        elif event.kind is PhysiologyEventKind.RECOVER:
            changes["phase"] = EngorgementPhase.RECOVERY
        elif event.kind is PhysiologyEventKind.RESET_FLACCID:
            changes.update(
                phase=EngorgementPhase.FLACCID,
                engorgement_fraction=0.0,
                rigidity_fraction=0.0,
                inflow_analogue=0.0,
                outflow_analogue=0.0,
                last_synthetic_fluid_output_ml=None,
            )
        elif event.kind is PhysiologyEventKind.OBSERVE_PREPUCE_POSITION:
            changes["prepuce_position"] = event.prepuce_position
        elif event.kind is PhysiologyEventKind.SET_ENDOCRINE_REFERENCE:
            changes["endocrine_reference_signal"] = event.endocrine_reference_signal
        elif event.kind is PhysiologyEventKind.SET_URINARY_REFERENCE:
            changes["urinary_reference_signal"] = event.urinary_reference_signal
        return state.evolve(**changes)

    def run(
        self,
        initial: PhysiologyState,
        events: Iterable[PhysiologyEvent],
    ) -> SyntheticTrajectory:
        event_tuple = tuple(events)
        current = initial
        for event in event_tuple:
            current = self.apply(current, event)
        return SyntheticTrajectory(initial, event_tuple, current)
