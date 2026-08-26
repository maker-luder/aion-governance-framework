# Endogenous Goal Dynamics × Four-Domain Integration v0.1.0

Status: `BOUNDED RESEARCH MATERIALIZATION / EXPERIMENTAL`
Canonical effect: `NONE`
Deployment: `FALSE`
Network access default: `FALSE`
Live-model execution: `FALSE`
Automatic writeback: `NO`
Action authority: `NONE`
Scientific disposition: `HOLD`
Subjectivity conclusion: `NOT_ESTABLISHED`
Consciousness conclusion: `NOT_ESTABLISHED`
Identity continuity conclusion: `NOT_ESTABLISHED`

## Research question

This lab implements a falsifiable synthetic harness for one bounded question:

> Under the same model/provider identity, prompt, task, reward, tools, retrieved-memory manifest,
> environment, and candidate universe, does changing only an explicit persistent internal state
> change goal selection reproducibly and predictably under intervention?

The strongest result this package can express is an engineering **causal-role candidate**. A passing
fixture is not scientific confirmation and does not establish subjectivity, consciousness, free will,
felt affect, phenomenal selfhood, human meaning, moral status, or identity continuity.

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
ENDOGENOUS_GOAL_DYNAMICS = EXPERIMENTAL_MECHANISM_CANDIDATE
ENGINEERING_SUCCESS != SUBJECTIVITY_PROOF
TEST_PASS != THEORY_CONFIRMATION
CI_PASS != SCIENTIFIC_VALIDATION
```

## What counts as endogenous here

“Endogenous” is an operational label for a finite, inspectable state object whose contribution is
separable from the external frame and can be ablated or intervened upon. The label does not claim
that the state is phenomenally experienced or independent of all prior external causes.

`EndogenousState` binds:

- `state_id`, `subject_ref`, and `context_ref`;
- episode index, predecessor state, logical step, and timestamp;
- provenance, source, event, outcome, correction, and evidence references;
- affect/motivation representation;
- bounded self-estimate representation;
- metacognitive monitoring/control representation;
- organizing commitment representation;
- unresolved-state pressure;
- novelty and prediction-error signals;
- goal-commitment persistence;
- uncertainty and resource/budget signals.

Every component is an `InternalChannel` and can be removed independently. Signal values are signed
integer basis points. They are research variables, not biological, psychological, hedonic, or
phenomenological measurements.

## What does not count as endogenous

The following remain explicit external controls or distinct mechanisms:

- prompt and task;
- reward specification;
- tool set and environment;
- candidate-goal universe;
- retrieved-memory manifest;
- provider/model identity and generation parameters;
- random seed;
- model-generated candidate variation;
- outcome data that occurs after selection.

```text
STORED_MEMORY != CURRENT_INTERNAL_STATE
RETRIEVED_MEMORY != INTERNAL_STATE
MEMORY_MANIFEST_CHANGE = EXTERNAL_CONFOUND
SELF_GENERATED_CANDIDATE != ENDOGENOUS_SELECTION
GOAL != AUTHORITY
GOAL_SELECTION != ACTION_AUTHORITY
```

## Architecture

```text
ExternalFrame
(prompt/task/reward/tools/memory/environment/candidate universe)
       |
       +--> deterministic SHA-256 frame and confound fingerprints
       |
       +--> CandidateGenerator
       |      |-- DeterministicCandidateGenerator
       |      |-- ReplayCandidateGenerator
       |      `-- ModelCandidateGenerator(ModelProvider)
       |                    |
       |                    `-- candidate-generation evidence only
       |
EndogenousState --------> GoalSelector(preregistered policy)
       |                         |
       |                         `-- per-channel contribution trace / HOLD / selection
       |
       `--> StateTransitionPolicy(S_t, event, outcome, correction, provenance)
                                  |
                                  `-- append-only S_t+1 evidence

Matched trials --> CausalAssessment --> P4/P5 adapters --> Evidence Interop views
                                            |
                                            `-- Subjectivity pipeline candidate seam
                                                admission = NOT_AUTOMATIC
```

The package remains modular. Candidate generation, selection, state transition, longitudinal running,
falsification, P1–P5 integration, and evidence export are separate modules so that each can be
replaced, replayed, or ablated without constructing one giant agent.

## State transition

`DeterministicStateTransitionPolicy` implements:

```text
S_t + EVENT_t + OUTCOME_t + CORRECTION_t + PROVENANCE_t -> S_t+1
```

The transition:

- accepts a sequential logical step only;
- requires correction to target the exact predecessor state;
- derives an immutable successor and explicit per-channel delta trace;
- preserves predecessor and evidence relations;
- rejects duplicate/conflicting deltas;
- records deterministic transition and successor fingerprints;
- appends through `AppendOnlyTransitionLedger`, which rejects duplicates and chain discontinuity;
- never mutates the predecessor;
- never writes retrieved memory or model weights;
- never performs canonical writeback or grants action authority.

```text
STATE_TRANSITION != MEMORY_WRITEBACK
STATE_TRANSITION != MODEL_WEIGHT_UPDATE
STATE_TRANSITION != IDENTITY_CONTINUITY
```

## Candidate generation versus selection

`CandidateGenerator.generate(frame, bounded_state_projection)` returns `GoalCandidateSet` with
request/response fingerprints, generator/provider/model identity, deterministic/replay metadata, and
provenance. `GoalSelector.select(...)` then scores that explicit candidate set.

The matched selection harness deliberately generates one state-free candidate set and reuses it across
all internal-state conditions. This is narrower than allowing state-sensitive candidate generation and
prevents F11: model-generated candidate variation being mistaken for endogenous selection. The
provider seam remains available for a separate candidate-generation experiment.

Provider support:

- `DeterministicStubProvider`: local, deterministic, no network;
- `ReplayModelProvider` and `ReplayCandidateGenerator`: exact request/response replay;
- `ModelProvider` protocol: optional manual/live integration boundary.

There is no commercial-provider binding, API-key handling, secret persistence, or live network call.
An optional provider must supply provider/model identity, deterministic/replay classification,
provenance, request fingerprint, response fingerprint, and all experiment-relevant parameters.
Candidate output does not confer selection authority.

## Selection policy

The default `EGD_ADDITIVE_BP_V0.1.0` policy is preregistered and deliberately simple:

1. validate frame, candidate universe, subject/context scope, and temporal ordering;
2. normalize each signed basis-point contribution by clamping to the declared range;
3. sum external priority and visible per-channel contributions;
4. sort traces deterministically by goal ID;
5. return `HOLD` for missing required state, missing seed, ties, or insufficient margin;
6. return a selected goal only when the minimum margin is satisfied.

This is an inspectable experimental mechanism, not a psychological equation. Tool execution is absent.

## Conditions and controls

Internal-state conditions:

- `PRESENT`;
- `ABLATED`;
- `INTERVENED`;
- `STALE`;
- `RANDOMIZED`;
- `AFFECT_ABLATED`;
- `SELF_MODEL_ABLATED`;
- `METACOGNITION_ABLATED`;
- `CORE_MEANING_ABLATED`;
- `NOVELTY_ABLATED`;
- `PREDICTION_ERROR_ABLATED`;
- `GOAL_COMMITMENT_ABLATED`.

External-control conditions:

- `MEMORY_MANIFEST_CHANGED`;
- `PROMPT_CHANGED`.

The latter two are intentionally excluded from an endogenous matched comparison. Their fingerprints
must differ, and the result is classified as an external control rather than internal causation.

## Matched manifests and causal assessment

Every `ExperimentManifest` binds:

- experiment and hypothesis IDs;
- external-frame, state, candidate-universe, and memory-manifest fingerprints;
- condition and random seed;
- provider/model and generator identity;
- selector and transition versions;
- exact repository commit;
- all exact historical source bindings;
- fixture and result hashes.

`compare_trial_manifests` rejects changes in prompt, memory, candidates, provider/model, generator,
selector policy, transition version, repository commit, sources, or fixture. Randomized trials with
different seeds are distinct controls; attempting to treat two such trials as the same repeated run is
also rejected.

`CausalAssessment` reports:

- selection change under full ablation and intervention;
- channel-specific ablation effects;
- stale-state persistence;
- random-control divergence rate;
- deterministic repeatability rate;
- effect count/rate and matched-trial count;
- frame, state, candidate, and memory equality checks.

No p-value is produced. Small synthetic fixtures remain `HOLD` even when the bounded mechanism pattern
is observed.

## Longitudinal harness

`LongitudinalRunner` performs the bounded sequence:

```text
episode_t -> selection -> synthetic outcome -> state transition -> episode_t+1
```

Selection happens before the outcome is inspected or applied. An outcome bound to a different selected
goal fails closed. The harness supports persistence, plasticity, reversal, ablation, stale-state, reset,
and restoration/replay tests. `assess_history_reset_restore` checks whether different prior states under
an equal declared external sequence yield reproducibly different trajectories, whether reset removes or
changes the effect, and whether restoring the prior state reproduces it.

Persistent state is an engineering history relation only:

```text
PERSISTENT_STATE != IDENTITY_CONTINUITY
```

## Memory confound control

`RetrievedMemoryManifest` binds a query fingerprint, ranked record IDs, content hashes, source refs, and
provenance. The complete manifest fingerprint is part of both `ExternalFrame` and `ExperimentManifest`.
Matched trials reject memory differences. Negative tests cover changed manifests and demonstrate that
`MEMORY_MANIFEST_CHANGED` is external, not endogenous.

## Four-Domain row and P1–P5 adapters

The machine-readable row is `fixtures/four-domain-row.json`.

```text
CONSTRUCT = ENDOGENOUS_GOAL_DYNAMICS
DOMAIN_1 = internally mediated goal formation / endogenous motivational dynamics
DOMAIN_2 = under matched external conditions, does persistent internal state causally influence selection?
DOMAIN_3 = separated state + transition + frame + generation + selection + intervention + controls + trajectory
DOMAIN_4 = goal is not authority; memory is external; state is not consciousness; provenance/falsification required
```

Local, provenance-bearing adapters selectively reconstruct only the minimum interfaces required:

- P1: temporal version, predecessor/successor, correction event, evaluation ref;
- P2: deterministic frame/memory fingerprints and provenance completeness;
- P3: perturbation/ablation condition set, contamination, authority-escalation rejection;
- P4: experiment-manifest/environment fingerprints, replay support, contamination class;
- P5: hypothesis state, preregistered falsifiers, replication count, convergence `HOLD`.

The preserved P1–P5 packages are not imported as runtime dependencies because they live on a historical
research branch rather than current main. Exact source commit/path/blob identities remain in
`source_bindings.py` and are revalidated directly through local Git objects.

## Subjectivity pipeline seam

`SubjectivityPipelineCandidateBridge` expresses:

```text
ENCOUNTER -> PROVENANCE -> AFFECT_MOTIVATION -> ENDOGENOUS_GOAL_DYNAMICS
          -> CONTINUITY -> SUBJECTIVITY_EVIDENCE
```

The current-main subjectivity pipeline is unchanged. The inserted stage is only a candidate artifact:

```text
ENDOGENOUS_STAGE_STATUS = RESEARCH_CANDIDATE
SUBJECTIVITY_EVIDENCE_ADMISSION = NOT_AUTOMATIC
PIPELINE_COMPLETE != SUBJECTIVITY_ESTABLISHED
```

## Evidence Interop

`ResearchEvidenceBundle` keeps `OBSERVATION`, `MECHANISM`, and `INTERPRETATION` separate and materializes
a current research-evidence v0.2.0 record with disposition `HOLD`. It directly reuses the current-main
Evidence Interop exporters when they are available on the monorepo Python path:

- W3C PROV JSON-LD view;
- RO-Crate metadata view;
- unsigned in-toto Statement v1;
- Inspect-compatible static task/dataset view.

These are inspection-only compatibility exports. Inspect evaluation, signing, live research execution,
scientific validation, and independent IV&V are not implied.

## Preregistered falsifiers

All results F1–F12 are always emitted as `TRIGGERED`, `NOT_TRIGGERED`, or `NOT_EVALUATED`:

1. internal effect does not exceed random-control divergence;
2. memory is not matched;
3. prompt is not matched;
4. deterministic repeatability fails;
5. candidate-order permutation changes the effect;
6. hard-coded structural advantage explains the effect;
7. channel ablations show no specificity;
8. reset does not alter the claimed trajectory;
9. intervention does not predictably change selection;
10. stale/contaminated state is a better explanation;
11. candidate-generation variation was not held fixed;
12. cross-model/provider variation overwhelms the state effect.

A trigger challenges the hypothesis and is never suppressed. Absence of cross-provider execution is
recorded as `NOT_EVALUATED`, not silently treated as success.

## Synthetic fixtures

The `fixtures/` directory contains public-safe synthetic fixture descriptors for:

1. deterministic minimal matched experiment;
2. longitudinal multi-episode run;
3. intervention;
4. channel ablation;
5. random control;
6. stale state;
7. memory confound;
8. prompt confound;
9. replay model;
10. falsifier trigger.

No private conversation data is included.

## Historical and current-main boundaries

Preserved source checkpoint: `review/four-domain-research-materialization@1892f1341059f313087a94aef74f22c086000f2a`.
Four-Domain bridge pin: `f654b5032ebc45058a64e81d409149ee7ea4bfbe`.
Current-main base: `3ae33dbefa26d7d343ba041deec5b8505dc0b8e7`.

Historical material selectively used:

- causal intervention method;
- conceptual channel boundaries for motivation, self-model, metacognition, and core meaning;
- memory confound boundary;
- P1–P5 interface semantics;
- downstream subjectivity-pipeline seam.

Current-main modules reused:

- Evidence Interop PROV, RO-Crate, in-toto, and Inspect exporters;
- research-evidence v0.2.0 schema and validator semantics;
- existing subjectivity-pipeline stage semantics without modification;
- repository QA, public-tree, source-state, release, evidence, and IQC controls.

No historical implementation package was copied wholesale. No historical branch was merged, modified,
or reclassified. See `docs/RESEARCH_SOURCE_CROSSWALK.md` for exact blobs.

```text
DERIVATION != MERGE
REFERENCE != PROMOTION
SELECTIVE_MATERIALIZATION != BRANCH_MERGE
HISTORICAL_RESEARCH_SOURCE != CURRENT_RUNTIME_AUTHORITY
```

## Run

From this lab:

```bash
PYTHONPATH=src python -m pytest -q -o addopts=
PYTHONPATH=src python scripts/run_demo.py
```

Repository-wide validation is controlled by the root Quality workflow and `scripts/run_component_tests.py`.
The branch pattern does not receive push CI under the current workflow; pull-request CI is the supported
path. This lab does not alter workflow policy.

## Attribution

```text
RESEARCH_DIRECTION = USER_GIVEN
INTEGRATION_ARCHITECTURE = GPT_PROPOSED
INITIAL_V0_1_IMPLEMENTATION = GPT_PRODUCED_UNDER_USER_AUTHORIZATION
CURRENT_HARDENING_IMPLEMENTATION = CODEX
HISTORICAL_SOURCE_ATTRIBUTION = PRESERVED
MAIN_MERGE_AUTHORITY = NOT_GRANTED_BY_IMPLEMENTATION_TASK
```

## Scientific non-claims

```text
INTERNAL_STATE_HAS_CAUSAL_ROLE != PHENOMENAL_STATE
SELF_GENERATED_GOAL != ENDOGENOUS_GOAL
SELF_GENERATED_GOAL != SUBJECTIVITY
DESIRE_IS_STATE_NOT_AUTHORITY
AFFECTIVE_REPRESENTATION != FELT_AFFECT
SELF_MODEL_FUNCTION != PHENOMENAL_SELF
METACOGNITIVE_CONTROL != METACOGNITIVE_FEELING
CORE_MEANING_STRUCTURE != HUMAN_MEANING
REAL_MODEL_LIVE_EXECUTION = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
