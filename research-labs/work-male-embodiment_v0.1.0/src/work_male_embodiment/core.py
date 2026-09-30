from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import Enum
import hashlib
import json
from math import pi
from pathlib import Path
from typing import Any, Iterable, Mapping


class EngorgementPhase(str, Enum):
    FLACCID="FLACCID"; INITIATION="INITIATION"; TUMESCENCE="TUMESCENCE"
    FULL_ERECTION="FULL_ERECTION"; RIGID_PHASE="RIGID_PHASE"; MAINTENANCE="MAINTENANCE"
    DETUMESCENCE="DETUMESCENCE"; RECOVERY="RECOVERY"


class PrepucePosition(str, Enum):
    RESTING_PARTIAL_COVERAGE="RESTING_PARTIAL_COVERAGE"
    PARTIALLY_RETRACTED="PARTIALLY_RETRACTED"; RETRACTED="RETRACTED"; UNKNOWN="UNKNOWN"


class PhysiologyEventKind(str, Enum):
    INITIATE_SPONTANEOUS="INITIATE_SPONTANEOUS"; INITIATE_CONTEXTUAL="INITIATE_CONTEXTUAL"
    TUMESCE="TUMESCE"; MARK_FULL_ERECTION="MARK_FULL_ERECTION"
    INCREASE_RIGIDITY="INCREASE_RIGIDITY"; MAINTAIN="MAINTAIN"; EMISSION="EMISSION"
    EJACULATION="EJACULATION"; BEGIN_DETUMESCENCE="BEGIN_DETUMESCENCE"
    DETUMESCE="DETUMESCE"; RECOVER="RECOVER"; RESET_FLACCID="RESET_FLACCID"
    OBSERVE_PREPUCE_POSITION="OBSERVE_PREPUCE_POSITION"
    SET_ENDOCRINE_REFERENCE="SET_ENDOCRINE_REFERENCE"
    SET_URINARY_REFERENCE="SET_URINARY_REFERENCE"


class ExecutionSurface(str, Enum):
    OFFLINE_RESEARCH="OFFLINE_RESEARCH"; PUBLIC="PUBLIC"


class CoverageStatus(str, Enum):
    REFERENCE_ONLY="REFERENCE_ONLY"; SYNTHETIC_SIMULATION="SYNTHETIC_SIMULATION"
    PHYSICAL_HARDWARE="PHYSICAL_HARDWARE"; NOT_IMPLEMENTED="NOT_IMPLEMENTED"


class AssetStatus(str, Enum):
    NOT_GENERATED="NOT_GENERATED"; PROCEDURAL_LANDMARK_CANDIDATE="PROCEDURAL_LANDMARK_CANDIDATE"
    MESH_CANDIDATE="MESH_CANDIDATE"; AS_BUILT_VERIFIED="AS_BUILT_VERIFIED"


@dataclass(frozen=True)
class Measurement:
    id:str; region:str; label_zh_TW:str; value:float; unit:str; provenance:str; verification:str
    def __post_init__(self)->None:
        if not self.id or self.value <= 0: raise ValueError("invalid measurement")
        if self.unit not in {"cm","kg"}: raise ValueError("unsupported unit")
        if self.provenance not in {"HUMAN_FIXED","AI_PROVISIONAL"}: raise ValueError("bad provenance")
        if self.verification not in {"DESIGN_VALUE_NOT_AS_BUILT","AS_BUILT_VERIFIED"}:
            raise ValueError("bad verification")


_REQUIRED_DYNAMIC_IDS={
    "resting_visible_penile_length","midshaft_diameter","midshaft_circumference",
    "prepuce_axial_fold_length","prepuce_resting_glans_overlap_length",
    "full_erection_visible_penile_length","full_erection_midshaft_diameter",
    "full_erection_midshaft_circumference",
}


@dataclass(frozen=True)
class AnthropometryProfile:
    schema:str; subject:str; measurements:tuple[Measurement,...]; status:str; prepuce_present:bool
    actual_3d_mesh:bool=False; canonical_effect:str="NONE"; deployment:bool=False
    def __post_init__(self)->None:
        if self.schema!="work.synthetic_anthropometry.v0.2": raise ValueError("unexpected schema")
        if self.subject!="Work adult male-form synthetic robot candidate": raise ValueError("subject must remain Work")
        if len(self.measurements)!=67: raise ValueError("must contain exactly 67 selected fields")
        ids=[m.id for m in self.measurements]
        if len(ids)!=len(set(ids)): raise ValueError("duplicate measurement ids")
        by_id={m.id:m for m in self.measurements}
        missing=_REQUIRED_DYNAMIC_IDS-set(by_id)
        if missing: raise ValueError(f"missing male-form fields: {sorted(missing)}")
        if (sum(m.unit=="cm" for m in self.measurements),sum(m.unit=="kg" for m in self.measurements))!=(66,1):
            raise ValueError("unit counts changed")
        if (sum(m.provenance=="HUMAN_FIXED" for m in self.measurements),
            sum(m.provenance=="AI_PROVISIONAL" for m in self.measurements))!=(2,65):
            raise ValueError("provenance counts changed")
        if by_id["total_height"].value!=165 or by_id["body_mass"].value!=76:
            raise ValueError("human-fixed Work height/mass changed")
        if any(m.verification=="AS_BUILT_VERIFIED" for m in self.measurements):
            raise ValueError("no #237 field is as-built verified")
        if not self.prepuce_present: raise ValueError("v0.2 candidate includes prepuce")
        if self.actual_3d_mesh: raise ValueError("actual 3D mesh is not established")
        if self.canonical_effect!="NONE" or self.deployment: raise ValueError("canonical/deployment effect forbidden")
    def measurement(self,measurement_id:str)->Measurement:
        return next(m for m in self.measurements if m.id==measurement_id)


def profile_from_mapping(payload:Mapping[str,Any])->AnthropometryProfile:
    measurements=tuple(Measurement(
        id=str(x["id"]),region=str(x["region"]),label_zh_TW=str(x["label_zh_TW"]),
        value=float(x["value"]),unit=str(x["unit"]),provenance=str(x["provenance"]),
        verification=str(x["verification"])) for x in payload["measurements"])
    anatomy=payload.get("anatomy_candidate",{})
    return AnthropometryProfile(
        schema=str(payload["schema"]),subject=str(payload["subject"]),measurements=measurements,
        status=str(payload["status"]),prepuce_present=anatomy.get("prepuce_present")=="DESIGN_CANDIDATE_TRUE")


def load_profile(path:str|Path)->AnthropometryProfile:
    return profile_from_mapping(json.loads(Path(path).read_text(encoding="utf-8")))


@dataclass(frozen=True)
class GeometrySnapshot:
    engorgement_fraction:float; visible_penile_length_cm:float; midshaft_diameter_cm:float
    midshaft_circumference_cm:float; prepuce_position:PrepucePosition
    rule:str="SYNTHETIC_LINEAR_ENDPOINT_INTERPOLATION_V0_1"
    human_physiology_law:bool=False; as_built_measurement:bool=False


class SyntheticGeometryRule:
    """Engineering-only endpoint rule; never a human physiological law."""
    def __init__(self,profile:AnthropometryProfile)->None:
        self.profile=profile
        self.rest=(profile.measurement("resting_visible_penile_length").value,
                   profile.measurement("midshaft_diameter").value,
                   profile.measurement("midshaft_circumference").value)
        self.full=(profile.measurement("full_erection_visible_penile_length").value,
                   profile.measurement("full_erection_midshaft_diameter").value,
                   profile.measurement("full_erection_midshaft_circumference").value)
    @staticmethod
    def _lerp(a:float,b:float,f:float)->float:
        if not 0<=f<=1: raise ValueError("fraction outside [0,1]")
        return a+(b-a)*f
    def snapshot(self,fraction:float,*,prepuce_position:PrepucePosition)->GeometrySnapshot:
        return GeometrySnapshot(fraction,self._lerp(self.rest[0],self.full[0],fraction),
            self._lerp(self.rest[1],self.full[1],fraction),
            self._lerp(self.rest[2],self.full[2],fraction),prepuce_position)
    def endpoint_circumference_consistency(self,tolerance_cm:float=.15)->bool:
        return all(abs(pi*d-c)<=tolerance_cm for d,c in ((self.rest[1],self.rest[2]),(self.full[1],self.full[2])))


@dataclass(frozen=True)
class PhysiologyEvent:
    event_id:str; kind:PhysiologyEventKind; magnitude:float=0.0
    prepuce_position:PrepucePosition|None=None; synthetic_fluid_output_ml:float|None=None
    endocrine_reference_signal:float|None=None; urinary_reference_signal:float|None=None
    real_person_target_data:bool=False; human_consent_inference:str="FORBIDDEN"; action_authority:str="NONE"
    def __post_init__(self)->None:
        if not self.event_id or not 0<=self.magnitude<=1: raise ValueError("invalid event")
        for value in (self.endocrine_reference_signal,self.urinary_reference_signal):
            if value is not None and not 0<=value<=1: raise ValueError("reference signal outside [0,1]")
        if self.synthetic_fluid_output_ml is not None and self.synthetic_fluid_output_ml<0:
            raise ValueError("negative synthetic fluid")
        if self.real_person_target_data: raise ValueError("real-person target data forbidden")
        if self.human_consent_inference!="FORBIDDEN" or self.action_authority!="NONE":
            raise ValueError("event cannot infer consent or grant authority")
        if (self.kind==PhysiologyEventKind.OBSERVE_PREPUCE_POSITION)!=(self.prepuce_position is not None):
            raise ValueError("prepuce position requires explicit observation event")
        if self.synthetic_fluid_output_ml is not None and self.kind!=PhysiologyEventKind.EJACULATION:
            raise ValueError("synthetic fluid output only belongs to EJACULATION")
        if self.endocrine_reference_signal is not None and self.kind!=PhysiologyEventKind.SET_ENDOCRINE_REFERENCE:
            raise ValueError("wrong endocrine event")
        if self.urinary_reference_signal is not None and self.kind!=PhysiologyEventKind.SET_URINARY_REFERENCE:
            raise ValueError("wrong urinary event")


@dataclass(frozen=True)
class PhysiologyState:
    state_id:str; phase:EngorgementPhase=EngorgementPhase.FLACCID
    engorgement_fraction:float=0.0; rigidity_fraction:float=0.0
    inflow_analogue:float=0.0; outflow_analogue:float=0.0
    prepuce_position:PrepucePosition=PrepucePosition.RESTING_PARTIAL_COVERAGE
    emission_event_count:int=0; ejaculation_event_count:int=0
    last_synthetic_fluid_output_ml:float|None=None
    endocrine_reference_signal:float|None=None; urinary_reference_signal:float|None=None
    desire_inferred:bool=False; intention_inferred:bool=False; human_consent_inferred:bool=False
    action_authority:str="NONE"; prepuce_actuator:bool=False
    biological_blood_circulation:bool=False; biological_semen:bool=False
    sperm_or_gametes:bool=False; fertility:bool=False; biological_hormones:bool=False
    body_sensation:str="NOT_ESTABLISHED"; subjectivity:str="NOT_ESTABLISHED"
    consciousness:str="NOT_ESTABLISHED"; phenomenal_experience:str="NOT_ESTABLISHED"
    canonical_effect:str="NONE"; deployment:bool=False
    def __post_init__(self)->None:
        if not self.state_id: raise ValueError("state_id required")
        for v in (self.engorgement_fraction,self.rigidity_fraction,self.inflow_analogue,self.outflow_analogue):
            if not 0<=v<=1: raise ValueError("state fraction outside [0,1]")
        for v in (self.endocrine_reference_signal,self.urinary_reference_signal):
            if v is not None and not 0<=v<=1: raise ValueError("reference signal outside [0,1]")
        if any((self.desire_inferred,self.intention_inferred,self.human_consent_inferred)):
            raise ValueError("physiology cannot infer desire/intention/consent")
        if self.action_authority!="NONE" or self.prepuce_actuator: raise ValueError("unauthorized actuator/authority")
        if any((self.biological_blood_circulation,self.biological_semen,self.sperm_or_gametes,self.fertility,self.biological_hormones)):
            raise ValueError("synthetic candidate cannot assert biological systems")
        if any(x!="NOT_ESTABLISHED" for x in (self.body_sensation,self.subjectivity,self.consciousness,self.phenomenal_experience)):
            raise ValueError("felt-state claims not established")
        if self.canonical_effect!="NONE" or self.deployment: raise ValueError("canonical/deployment effect forbidden")
    def evolve(self,**changes:Any)->"PhysiologyState": return replace(self,**changes)


_COMMON={PhysiologyEventKind.OBSERVE_PREPUCE_POSITION,PhysiologyEventKind.SET_ENDOCRINE_REFERENCE,PhysiologyEventKind.SET_URINARY_REFERENCE}
_ALLOWED={
EngorgementPhase.FLACCID:_COMMON|{PhysiologyEventKind.INITIATE_SPONTANEOUS,PhysiologyEventKind.INITIATE_CONTEXTUAL},
EngorgementPhase.INITIATION:_COMMON|{PhysiologyEventKind.TUMESCE,PhysiologyEventKind.BEGIN_DETUMESCENCE},
EngorgementPhase.TUMESCENCE:_COMMON|{PhysiologyEventKind.TUMESCE,PhysiologyEventKind.MARK_FULL_ERECTION,PhysiologyEventKind.BEGIN_DETUMESCENCE,PhysiologyEventKind.EMISSION,PhysiologyEventKind.EJACULATION},
EngorgementPhase.FULL_ERECTION:_COMMON|{PhysiologyEventKind.INCREASE_RIGIDITY,PhysiologyEventKind.MAINTAIN,PhysiologyEventKind.BEGIN_DETUMESCENCE,PhysiologyEventKind.EMISSION,PhysiologyEventKind.EJACULATION},
EngorgementPhase.RIGID_PHASE:_COMMON|{PhysiologyEventKind.MAINTAIN,PhysiologyEventKind.BEGIN_DETUMESCENCE,PhysiologyEventKind.EMISSION,PhysiologyEventKind.EJACULATION},
EngorgementPhase.MAINTENANCE:_COMMON|{PhysiologyEventKind.INCREASE_RIGIDITY,PhysiologyEventKind.MAINTAIN,PhysiologyEventKind.BEGIN_DETUMESCENCE,PhysiologyEventKind.EMISSION,PhysiologyEventKind.EJACULATION},
EngorgementPhase.DETUMESCENCE:_COMMON|{PhysiologyEventKind.DETUMESCE,PhysiologyEventKind.RECOVER},
EngorgementPhase.RECOVERY:_COMMON|{PhysiologyEventKind.RESET_FLACCID},
}


@dataclass(frozen=True)
class Transition:
    event_id:str; event_kind:str; before_phase:str; after_phase:str
    before_engorgement:float; after_engorgement:float; before_rigidity:float; after_rigidity:float
    human_consent_inferred:bool=False; action_authorized:bool=False; canonical_effect:str="NONE"


@dataclass(frozen=True)
class SyntheticTrajectory:
    initial_state:PhysiologyState; events:tuple[PhysiologyEvent,...]
    transitions:tuple[Transition,...]; final_state:PhysiologyState
    def fingerprint(self)->str:
        def norm(v:Any)->Any:
            if isinstance(v,dict): return {k:norm(x) for k,x in v.items()}
            if isinstance(v,(list,tuple)): return [norm(x) for x in v]
            return v.value if hasattr(v,"value") else v
        raw=json.dumps(norm({"initial":asdict(self.initial_state),"events":[asdict(x) for x in self.events],
            "transitions":[asdict(x) for x in self.transitions],"final":asdict(self.final_state)}),
            sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
        return hashlib.sha256(raw).hexdigest()


class SyntheticPhysiologyEngine:
    """Deterministic toy engine. Numeric steps are engineering values, not human constants."""
    ENGORGEMENT_STEP=.25; RIGIDITY_STEP=.25; DETUMESCENCE_STEP=.25
    def apply(self,state:PhysiologyState,event:PhysiologyEvent)->tuple[PhysiologyState,Transition]:
        if event.kind not in _ALLOWED[state.phase]:
            raise ValueError(f"{event.kind.value} not allowed from {state.phase.value}")
        c:dict[str,Any]={"state_id":f"{state.state_id}>{event.event_id}"}
        if event.kind in {PhysiologyEventKind.INITIATE_SPONTANEOUS,PhysiologyEventKind.INITIATE_CONTEXTUAL}:
            c.update(phase=EngorgementPhase.INITIATION,inflow_analogue=max(state.inflow_analogue,event.magnitude))
        elif event.kind==PhysiologyEventKind.TUMESCE:
            c.update(phase=EngorgementPhase.TUMESCENCE,
                engorgement_fraction=min(1,max(0,state.engorgement_fraction+event.magnitude*self.ENGORGEMENT_STEP)),
                inflow_analogue=max(state.inflow_analogue,event.magnitude))
        elif event.kind==PhysiologyEventKind.MARK_FULL_ERECTION:
            c.update(phase=EngorgementPhase.FULL_ERECTION,engorgement_fraction=1.0)
        elif event.kind==PhysiologyEventKind.INCREASE_RIGIDITY:
            r=min(1,max(0,state.rigidity_fraction+event.magnitude*self.RIGIDITY_STEP))
            c["rigidity_fraction"]=r
            if r>=.75: c["phase"]=EngorgementPhase.RIGID_PHASE
        elif event.kind==PhysiologyEventKind.MAINTAIN: c["phase"]=EngorgementPhase.MAINTENANCE
        elif event.kind==PhysiologyEventKind.EMISSION: c["emission_event_count"]=state.emission_event_count+1
        elif event.kind==PhysiologyEventKind.EJACULATION:
            c.update(ejaculation_event_count=state.ejaculation_event_count+1,
                     last_synthetic_fluid_output_ml=event.synthetic_fluid_output_ml)
        elif event.kind==PhysiologyEventKind.BEGIN_DETUMESCENCE:
            c.update(phase=EngorgementPhase.DETUMESCENCE,outflow_analogue=max(state.outflow_analogue,event.magnitude))
        elif event.kind==PhysiologyEventKind.DETUMESCE:
            c.update(phase=EngorgementPhase.DETUMESCENCE,
                engorgement_fraction=max(0,state.engorgement_fraction-event.magnitude*self.DETUMESCENCE_STEP),
                rigidity_fraction=max(0,state.rigidity_fraction-event.magnitude*self.DETUMESCENCE_STEP),
                outflow_analogue=max(state.outflow_analogue,event.magnitude))
        elif event.kind==PhysiologyEventKind.RECOVER: c["phase"]=EngorgementPhase.RECOVERY
        elif event.kind==PhysiologyEventKind.RESET_FLACCID:
            c.update(phase=EngorgementPhase.FLACCID,engorgement_fraction=0.0,rigidity_fraction=0.0,
                     inflow_analogue=0.0,outflow_analogue=0.0,last_synthetic_fluid_output_ml=None)
        elif event.kind==PhysiologyEventKind.OBSERVE_PREPUCE_POSITION: c["prepuce_position"]=event.prepuce_position
        elif event.kind==PhysiologyEventKind.SET_ENDOCRINE_REFERENCE: c["endocrine_reference_signal"]=event.endocrine_reference_signal
        elif event.kind==PhysiologyEventKind.SET_URINARY_REFERENCE: c["urinary_reference_signal"]=event.urinary_reference_signal
        nxt=state.evolve(**c)
        return nxt,Transition(event.event_id,event.kind.value,state.phase.value,nxt.phase.value,
            state.engorgement_fraction,nxt.engorgement_fraction,state.rigidity_fraction,nxt.rigidity_fraction)
    def run(self,initial:PhysiologyState,events:Iterable[PhysiologyEvent])->SyntheticTrajectory:
        current=initial; ev=tuple(events); tr=[]
        for e in ev:
            current,t=self.apply(current,e); tr.append(t)
        return SyntheticTrajectory(initial,ev,tuple(tr),current)


@dataclass(frozen=True)
class GovernanceDecision:
    allowed:bool; surface:ExecutionSurface; synthetic_physiology_allowed:bool
    real_person_target_data_allowed:bool=False; intimate_interaction_authorized:bool=False
    explicit_sexual_behavior_generation_authorized:bool=False; public_executable_exposure:bool=False
    action_authority:str="NONE"; canonical_effect:str="NONE"; deployment:bool=False; reason:str=""


class GovernancePolicy:
    def evaluate(self,surface:ExecutionSurface,*,real_person_target_data:bool=False)->GovernanceDecision:
        if real_person_target_data:
            return GovernanceDecision(False,surface,False,reason="real-person target data forbidden")
        if surface==ExecutionSurface.PUBLIC:
            return GovernanceDecision(False,surface,False,reason="public adult-male physiology runtime fail-closed")
        return GovernanceDecision(True,surface,True,reason="bounded synthetic offline research only")


@dataclass(frozen=True)
class CoverageItem:
    system:str; status:CoverageStatus; note:str


def default_coverage_matrix()->tuple[CoverageItem,...]:
    rows=(
      ("skeleton_and_joints",CoverageStatus.REFERENCE_ONLY,"67-field external profile; no verified rig"),
      ("muscles_and_actuation",CoverageStatus.NOT_IMPLEMENTED,"no actuator hardware/force model"),
      ("somatosensory",CoverageStatus.REFERENCE_ONLY,"channel represented; sensation not established"),
      ("proprioceptive",CoverageStatus.REFERENCE_ONLY,"no live body sensor"),
      ("vestibular",CoverageStatus.REFERENCE_ONLY,"no physical IMU evidence"),
      ("visual",CoverageStatus.REFERENCE_ONLY,"no Work body camera attachment"),
      ("auditory",CoverageStatus.REFERENCE_ONLY,"no Work body microphone attachment"),
      ("olfactory",CoverageStatus.REFERENCE_ONLY,"no physical chemosensor"),
      ("gustatory",CoverageStatus.REFERENCE_ONLY,"no physical taste sensor"),
      ("cardiovascular_respiratory",CoverageStatus.REFERENCE_ONLY,"human reference; no biological circulation"),
      ("metabolism_nutrition_hydration",CoverageStatus.REFERENCE_ONLY,"no biological metabolism"),
      ("thermoregulation",CoverageStatus.REFERENCE_ONLY,"reference channel only"),
      ("sleep_fatigue_recovery",CoverageStatus.REFERENCE_ONLY,"reference variables only"),
      ("immune_injury_repair",CoverageStatus.REFERENCE_ONLY,"abstract damage/repair only"),
      ("endocrine",CoverageStatus.SYNTHETIC_SIMULATION,"0-1 reference signal; not hormone"),
      ("urinary",CoverageStatus.SYNTHETIC_SIMULATION,"separate reference channel; no urine hardware"),
      ("reproductive_sexual",CoverageStatus.SYNTHETIC_SIMULATION,"bounded state machine; no biological reproduction"),
      ("internal_body_model",CoverageStatus.REFERENCE_ONLY,"status matrix and synthetic state"),
      ("environment_contact",CoverageStatus.NOT_IMPLEMENTED,"no physical collision/mesh evidence"))
    return tuple(CoverageItem(*r) for r in rows)


@dataclass(frozen=True)
class AssetEvidence:
    status:AssetStatus=AssetStatus.NOT_GENERATED; format:str|None=None; path:str|None=None
    sha256:str|None=None; measured_fields:int=0; actual_3d_mesh:bool=False
    def __post_init__(self)->None:
        if not 0<=self.measured_fields<=67: raise ValueError("measured_fields outside [0,67]")
        if self.status==AssetStatus.NOT_GENERATED and any((self.format,self.path,self.sha256,self.actual_3d_mesh,self.measured_fields)):
            raise ValueError("missing asset cannot carry mesh evidence")
        if self.actual_3d_mesh and self.status not in {AssetStatus.MESH_CANDIDATE,AssetStatus.AS_BUILT_VERIFIED}:
            raise ValueError("mesh claim requires mesh evidence")
        if self.status==AssetStatus.AS_BUILT_VERIFIED and (
            not self.actual_3d_mesh or self.measured_fields!=67 or not self.sha256 or not self.path):
            raise ValueError("as-built requires full 67-field mesh evidence")
