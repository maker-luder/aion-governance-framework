# MODULE_REPORT: affective-motivational-dynamics_v0.1.0

## MODULE_INFO
- **MODULE_NAME**: affective-motivational-dynamics_v0.1.0
- **MODULE_VERSION**: 0.1.0
- **PURPOSE**: Provide a governed research candidate for affective-motivational dynamics representation in the Four-Domain + Embodiment Continuity architecture. Models motivational signals with affective valence, wanting/liking dissociation, approach/avoidance conflict, and directional dynamics with explicit non-claims about felt experience, hedonic tone, or motivational authority.

## FILES_CREATED
```
research-labs/integration-candidates/affective-motivational-dynamics_v0.1.0/
├── pyproject.toml
├── src/
│   └── affective_motivational_dynamics/
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

## FILES_CREATED
- None (all files newly created within WRITE_ROOT)

## FILES_DELETED
- None

## FILES_RENAMED
- None

## TEST_RESULT
- **Status**: PENDING (to be executed after all modules created)
- **Test file**: tests/test_model.py
- **Coverage**: Signal validation (bounds, evidence, conflict properties), state validation, manager lifecycle (initialize, transition, snapshot, restore, reset, disable/enable, ablate)

## DEMO_RESULT
- **Status**: PENDING (to be executed after all modules created)
- **Demo file**: examples/run_demo.py
- **Demonstrates**: Multi-domain signal initialization, snapshot, reward prediction error simulation (wanting/liking gap), conflict signal addition, history tracking, restoration, domain ablation, disable/enable, reset

## DEPENDENCIES
- Python >= 3.11 (standard library only: dataclasses, enum, typing, datetime)
- No external dependencies
- Conceptual dependency on metacognitive-self-state (conflict detection, uncertainty monitoring)
- No code dependency on existing repository modules

## KNOWN_LIMITATIONS
1. Does not implement any felt experience, hedonic tone, or motivational authority claims
2. All states explicitly maintain `canonical_effect=NONE`, `felt_experience_claim=NOT_ESTABLISHED`, `hedonic_tone_claim=NOT_ESTABLISHED`, `motivational_authority_claim=NOT_ESTABLISHED`
3. All signals explicitly maintain `felt_experience_claim=NOT_ESTABLISHED`
4. Wanting/liking dissociation modeled as computational variables, not felt dissociation
5. Approach/avoidance conflict modeled as co-occurring computational variables
6. Deterministic behavior only when seed provided; otherwise uses system time
8. No integration with existing AION runtime - this is an isolated research candidate
9. Ablation removes entire domains; no partial degradation modeling
10. Global valence and dominant direction are summary variables, not computed from signals

## KNOWN_LIMITATIONS (continued)
11. Adult sexuality schema domain included as schema-only category (consistent with affective-cognitive-motivation module)
11. No dynamic computation of global valence/direction from signals (static summary)

## INPUT (DynamicsInput)
- subject_ref: str
- context_ref: str
- signals: tuple[dict[str, Any], ...] (MotivationalSignal as dict)
- seed: int | None

## OUTPUT (DynamicsOutput)
- state: MotivationalState
- transitions: tuple[StateTransition, ...]
- canonical_effect: str = "NONE"
- felt_experience_claim: str = "NOT_ESTABLISHED"
- hedonic_tone_claim: str = "NOT_ESTABLISHED"

## STATE (MotivationalState)
- state_id: str
- subject_ref: str
- context_ref: str
- signals: tuple[MotivationalSignal, ...]
- global_valence: AffectiveValence (enum)
- dominant_direction: MotivationalDirection (enum)
- conflict_index: float (0.0-1.0)
- uncertainty_aggregate: float (0.0-1.0)
- canonical_effect: str = "NONE"
- felt_experience_claim: str = "NOT_ESTABLISHED"
- hedonic_tone_claim: str = "NOT_ESTABLISHED"
- motivational_authority_claim: str = "NOT_ESTABLISHED"

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
- `manager.ablate(domain?)`: If domain provided, removes signals of that domain; if None, disables entire module

## INTEGRATION_POINTS
- **DynamicsStateManager**: Core state lifecycle management
- **AffectiveMotivationalInterface**: Abstract interface for integration
- **MotivationalSignal**: Granular signal with valence, wanting, liking, approach, avoidance, uncertainty
- **MotivationalState**: Complete state with signals, global valence, direction, conflict, uncertainty
- **SignalDomain**: Seven domains (homeostatic, social, exploration, aesthetic, adult schema, self-preservation, knowledge)
- **AffectiveValence**: Five valence categories (positive, negative, neutral, mixed, indeterminate)
- **MotivationalDirection**: Four directions (approach, avoidance, conflict, neutral)
- **Signal properties**: approach_avoidance_conflict, wanting_liking_discrepancy
- **State properties**: total_approach, total_avoidance, get_signals_by_domain, get_signals_by_direction
- **StateSnapshot/StateTransition**: Traceability and restoration primitives

## INTEGRATION_POINTS (continued)
- **SignalDomain.ADULT_SEXUALITY_SCHEMA**: Schema-only category consistent with affective-cognitive-motivation module

## INTEGRATION_NOT_PERFORMED
- No integration with existing AION runtime
- No connection to canonical memory system
- No connection to metacognitive-self-state module (conceptual dependency only)
- No connection to self-other-boundary module
- No connection to affective-cognitive-motivation existing module
- No CI/CD pipeline integration
- No canonical manifest registration

## SCIENTIFIC_NON_CLAIMS
- This module does NOT establish or prove felt experience
- This module does NOT establish or prove hedonic tone (pleasure/displeasure)
- This module does NOT establish or prove motivational authority
- Wanting/liking dissociation modeling != evidence of incentive salience dissociation
- Approach/avoidance conflict modeling != evidence of ambivalence experience
- Affective valence categories != evidence of felt affect
- Motivational direction modeling != evidence of volition
- Functional motivational dynamics != evidence of motivation as felt force
- Adult sexuality schema category == schema-only, no executable runtime