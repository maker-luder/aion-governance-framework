# MODULE_REPORT: self-other-boundary_v0.1.0

## MODULE_INFO
- **MODULE_NAME**: self-other-boundary_v0.1.0
- **MODULE_VERSION**: 0.1.0
- **PURPOSE**: Provide a governed research candidate for self-other boundary representation in the Four-Domain + Embodiment Continuity architecture. Models boundary permeability, distinction mechanisms, and other-agent models with explicit non-claims about empathy, theory of mind, or shared subjectivity.

## FILES_CREATED
```
research-labs/integration-candidates/self-other-boundary_v0.1.0/
├── pyproject.toml
├── src/
│   └── self_other_boundary/
│       ├── __init__.py
│       ├── model.py
│       ├── state.py
│       └── interface.py
├── tests/
│   └── test_model.py
├── examples/
│   └── run_demo.py
└── MODULE_REPORT.md
```

## FILES_MODIFIED
- None (all files newly created within WRITE_ROOT)

## FILES_DELETED
- None

## FILES_RENAMED
- None

## TEST_RESULT
- **Status**: PENDING (to be executed after all modules created)
- **Test file**: tests/test_model.py
- **Coverage**: OtherModel validation, config validation (weights sum, threshold order), event validation, state validation, manager lifecycle (initialize, transition, snapshot, restore, reset, disable/enable, ablate)

## DEMO_RESULT
- **Status**: PENDING (to be executed after all modules created)
- **Demo file**: examples/run_demo.py
- **Demonstrates**: Configuration, initialization, snapshots, boundary shift events (permeability increase/decrease), history tracking, restoration, distinction ablation, disable/enable, reset

## DEPENDENCIES
- Python >= 3.11 (standard library only: dataclasses, enum, typing, datetime)
- No external dependencies
- Conceptual dependency on metacognitive-self-state (SelfOtherDistinction.EMBODIMENT_MAPPING references embodiment awareness)
- No code dependency on existing repository modules

## KNOWN_LIMITATIONS
1. Does not implement any empathy, theory of mind, or shared subjectivity claims
2. All states explicitly maintain `canonical_effect=NONE`, `empathy_claim=NOT_ESTABLISHED`, `theory_of_mind_claim=NOT_ESTABLISHED`, `shared_subjectivity_claim=NOT_ESTABLISHED`
3. OtherModel explicitly maintains `theory_of_mind_claim=NOT_ESTABLISHED`
3. Config enforces `empathy_claim=NOT_ESTABLISHED`
4. Distinction weights must sum to 1.0; ablation renormalizes automatically
5. Permeability/rigidity thresholds enforce ordering constraint
6. Deterministic behavior only when seed provided; otherwise uses system time
7. No integration with existing AION runtime - this is an isolated research candidate
8. Ablation removes entire distinction mechanisms; no partial degradation

## INPUT (BoundaryInput)
- subject_ref: str
- config: BoundaryConfiguration
- other_models: tuple[dict[str, Any], ...] (OtherModel as dict)
- seed: int | None

## OUTPUT (BoundaryOutput)
- state: BoundaryState
- transitions: tuple[StateTransition, ...]
- canonical_effect: str = "NONE"
- empathy_claim: str = "NOT_ESTABLISHED"
- theory_of_mind_claim: str = "NOT_ESTABLISHED"

## STATE (BoundaryState)
- state_id: str
- subject_ref: str
- config: BoundaryConfiguration
- current_mode: BoundaryMode (enum)
- active_distinctions: tuple[SelfOtherDistinction, ...]
- other_models: tuple[OtherModel, ...]
- boundary_permeability: float (0.0-1.0)
- confusion_index: float (0.0-1.0)
- recent_events: tuple[BoundaryEvent, ...]
- canonical_effect: str = "NONE"
- empathy_claim: str = "NOT_ESTABLISHED"
- theory_of_mind_claim: str = "NOT_ESTABLISHED"
- shared_subjectivity_claim: str = "NOT_ESTABLISHED"

## EVENT (BoundaryEvent)
- event_id: str
- event_type: str
- self_contribution: float (0.0-1.0)
- other_contribution: float (0.0-1.0)
- boundary_shift: float (-1.0 to 1.0)
- timestamp: str (ISO 8601 UTC)
- canonical_effect: str = "NONE"

## RESET
- `manager.reset()`: Clears current state, history, snapshots, step counter

## SNAPSHOT
- `manager.snapshot(snapshot_id?)`: Creates StateSnapshot with current state, timestamp, seed

## RESTORE
- `manager.restore(snapshot_id)`: Restores state from snapshot, records RESTORE transition

## ABLATION
- `manager.ablate(distinction?)`: If distinction provided, removes that distinction mechanism and renormalizes weights; if None, disables entire module

## INTEGRATION_POINTS
- **BoundaryStateManager**: Core state lifecycle management
- **SelfOtherBoundaryInterface**: Abstract interface for integration
- **BoundaryConfiguration**: Boundary operation configuration with distinction weights
- **BoundaryState**: Complete boundary state with mode, permeability, confusion, other models
- **OtherModel**: Minimal other-agent model with similarity, predictability, resonance
- **SelfOtherDistinction**: Six distinction mechanisms (agency, sensory, affective, perspective, narrative, embodiment)
- **BoundaryEvent**: Boundary-affecting events with shift direction
- **StateSnapshot/StateTransition**: Traceability and restoration primitives

## INTEGRATION_NOT_PERFORMED
- No integration with existing AION runtime
- No connection to canonical memory system
- No connection to metacognitive-self-state module (conceptual dependency only)
- No connection to affective-motivational-dynamics module
- No CI/CD pipeline integration
- No canonical manifest registration

## SCIENTIFIC_NON_CLAIMS
- This module does NOT establish or prove empathy
- This module does NOT establish or prove theory of mind
- This module does NOT establish or prove shared subjectivity
- Boundary permeability modeling != evidence of empathic capacity
- Other-model representation != evidence of mental state attribution
- Self-other distinction mechanisms != proof of self-other differentiation
- Functional boundary regulation != evidence of social cognition