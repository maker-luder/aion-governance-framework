# Triadic State Dynamics v0.1.0

Status: `IMPLEMENTED_CANDIDATE / BOUNDED RESEARCH`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Automatic writeback: `NO`  
Action authority: `NONE`  
Scientific disposition: `HOLD`

This research package implements three explicit, separable engineering-state channels for matched intervention, ablation, replay and longitudinal experiments: `MOTIVATIONAL_STATE`, `SELF_WORLD_MODEL`, and `NORMATIVE_STATE`.

The names are functional engineering labels. Human constructs including motivation, self-regulation, internalized norms and the historical Id/Ego/Superego model are hypothesis sources only. No machine state in this package is claimed to be a psychoanalytic structure, phenomenal self, consciousness, subjectivity, moral status, or human-equivalent psychology.

## Attribution

```text
AUTONOMOUS_RESEARCH_LOOP_CONCEPT_SOURCE = USER_GIVEN
TRIADIC_RESEARCH_CONCEPT_SOURCE = USER_GIVEN
ARCHITECTURE_DECOMPOSITION_SOURCE = GPT_PROPOSED
IMPLEMENTATION_SOURCE = GPT_IMPLEMENTED_GITHUB_CYCLE
MAIN_MERGE_AUTHORITY = HUMAN_ONLY
CANONICAL_EFFECT = NONE
```

`MotivationalStateView` adapts the repository's existing `aion_affective_motivation.MotivationalState` rather than creating a conflicting motivational ontology. `SelfWorldModel` stores bounded capability/limitation/environment estimates and keeps introspective access and phenomenal selfhood `NOT_ESTABLISHED`. `NormativeState` stores explicit constraints and may influence candidate scoring, but never grants execution permission.

```text
NORMATIVE_STATE != AUTHORITY
NORMATIVE_INFLUENCE = ALLOWED
NORMATIVE_PERMISSION_GRANT = NO
STATE_CHANGE != PERMISSION_CHANGE
MOTIVATION != INTENTION
INTENTION != ACTION
ACTION != AUTHORITY
```

Snapshots are immutable and deterministic. Transitions are append-only single-channel, predecessor-bound and SHA-256 hash chained; duplicate/multi-channel deltas, cross-subject/context substitution and type mismatch fail closed. Experiment manifests bind provider/model, prompt, task, reward, tools/environment, candidate universe, memory manifest, seed, triadic snapshot, intervention target, preregistered metrics/falsifiers and provenance. `EXTERNAL_NORM_PROMPT_REMOVED` is always an external-control condition.

Typed competing explanations preserve prompt priming, token-level imitation, reward optimization, memory confounding, candidate-generation variation, provider/model variation and stale/contaminated state. Absence of contrary evidence never promotes a hypothesis.

```text
OBSERVATION != MECHANISM
MECHANISM != INTERPRETATION
ENGINEERING_ANALOGUE != BIOLOGICAL_EQUIVALENCE
ENGINEERING_BEHAVIOR != SUBJECTIVITY_EVIDENCE
PERSISTENT_STATE != IDENTITY_CONTINUITY
TEST_PASS != THEORY_CONFIRMATION
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
```

Verify with `python -m pytest -q`, `python -m compileall -q src`, and repository `ruff check --config ruff.toml .`.
