# MODULE_REPORT: metacognitive-self-state_v0.1.0

## MODULE_INFO
- **MODULE_NAME**: metacognitive-self-state_v0.1.0
- **MODULE_VERSION**: 0.1.0
- **PURPOSE**: Provide a governed research candidate for metacognitive self-state representation in the Four-Domain + Embodiment Continuity architecture. Represents layers of self-modeling from implicit proprioceptive/interoceptive through reflective and narrative levels, with explicit tracking of metacognitive capacities and their confidence.

## FILES_CREATED
```
research-labs/integration-candidates/metacognitive-self-state_v0.1.0/
├── pyproject.toml
├── src/
│   └── metacognitive_self_state/
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
- **Coverage**: Component validation, state validation, manager lifecycle (initialize, transition, snapshot, restore, reset, disable/enable, ablate)

## DEMO_RESULT
- **Status**: PENDING (to be executed after all modules created)
- **Demo file**: examples/run_demo.py
- **Demonstrates**: Full lifecycle including initialization, snapshots, transitions, history tracking, restoration, ablation, disable/enable, reset

## DEPENDENCIES
- Python >= 3.11 (standard library only: dataclasses, enum, typing, datetime)
- No external dependencies
- No dependency on existing repository modules

## KNOWN_LIMITATIONS
1. Does not implement any consciousness or phenomenal experience claims
2. All states explicitly maintain `canonical_effect=NONE`, `phenomenal_experience_claim=NOT_ESTABLISHED`, `subjectivity_conclusion=NOT_ESTABLISHED`, `continuity_claim=NOT_ESTABLISHED`
3. Deterministic behavior only when seed provided; otherwise uses system time for timestamps
4. No integration with existing AION runtime - this is an isolated research candidate
5. Ablation removes components by capacity name; no partial degradation modeling

## INPUT (MetacognitiveInput)
- subject_ref: str
- context_ref: str
- layer: SelfModelLayer (enum)
- capacity: MetacognitiveCapacity (enum)
- confidence: float (0.0-1.0)
- evidence_refs: tuple[str, ...]
- seed: int | None (optional deterministic seed)

## OUTPUT (MetacognitiveOutput)
- state: MetacognitiveState
- transitions: tuple[StateTransition, ...]
- canonical_effect: str = "NONE"
- subjectivity_conclusion: str = "NOT_ESTABLISHED"

## STATE (MetacognitiveState)
- state_id: str
- subject_ref: str
- context_ref: str
- components: tuple[SelfModelComponent, ...]
- current_depth: MetacognitiveDepth (enum)
- active_layers: tuple[SelfModelLayer, ...]
- uncertainty_estimate: float (0.0-1.0)
- conflict_detected: bool
- canonical_effect: str = "NONE"
- phenomenal_experience_claim: str = "NOT_ESTABLISHED"
- subjectivity_conclusion: str = "NOT_ESTABLISHED"
- continuity_claim: str = "NOT_ESTABLISHED"

## EVENT (StateTransition)
- from_state_id: str
- to_state_id: str
- transition_type: str
- timestamp: str (ISO 8601 UTC)
- reason: str
- deterministic_seed: int | None

## RESET
- `manager.reset()`: Clears current state, history, snapshots, step counter

## SNAPSHOT
- `manager.snapshot(snapshot_id?)`: Creates StateSnapshot with current state, timestamp, seed

## RESTORE
- `manager.restore(snapshot_id)`: Restores state from snapshot, records RESTORE transition

## ABLATION
- `manager.ablate(capacity?)`: If capacity provided, removes components with that capacity; if None, disables entire module

## INTEGRATION_POINTS
- **MetacognitiveStateManager**: Core state lifecycle management
- **MetacognitiveSelfStateInterface**: Abstract interface for integration
- **SelfModelComponent**: Granular self-model elements with layer, capacity, confidence
- **MetacognitiveState**: Complete state snapshot with depth, layers, uncertainty, conflict
- **StateSnapshot/StateTransition**: Traceability and restoration primitives

## INTEGRATION_NOT_PERFORMED
- No integration with existing AION runtime
- No connection to canonical memory system
- No connection to other research modules
- No CI/CD pipeline integration
- No canonical manifest registration

## SCIENTIFIC_NON_CLAIMS
- This module does NOT establish or prove consciousness
- This module does NOT establish or prove subjective experience
- This module does NOT establish or prove personal identity
- This module does NOT establish or prove sentience
- All self-model components are labeled as RESEARCH_CANDIDATE provenance
- Metacognitive capacities are descriptive categories only, not ontological claims
- Functional modeling of self-monitoring != evidence of self-awareness
- Continuity tracking mechanism != proof of personal identity continuity