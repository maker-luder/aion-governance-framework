# Bounded Autonomous Research Loop Protocol v0.1.0

## Candidate source state

- repository: `maker-luder/aion-governance-framework`
- integration base: `main@6a3bfb19e884e2508729ac5e02c7eba3fa78383c`
- candidate branch: `feat/governed-knowledge-normative-model-20260827`
- candidate PR: `#63` (`DRAFT`)
- candidate status: `NON_CANONICAL / DRAFT_REVIEW / HOLD`
- historical/frozen branch mutation: `NO`
- main merge approval: `NOT_GIVEN`

This protocol names the integrated candidate branch rather than the earlier standalone bounded-loop branch.
Every materialized research-evidence record must still pin its own exact 40-hex source commit and exact protocol hash.

## Direct reuse bindings

The orchestration layer imports existing APIs instead of copying their implementations:

1. `components/aion_astra_inquiry_v0.1.0/src/aion_astra_inquiry/core.py`
   - `BoundedInquiryLoop`
   - `InquiryReport`
   - `verify_transcript_chain`
   - `AgentId`
2. `research-labs/endogenous-goal-dynamics_v0.1.0/src/aion_endogenous_goal_dynamics/`
   - `run_matched_experiment`
   - `assess_causal_pattern`
   - `FourDomainMapping`
   - `endogenous_goal_dynamics_mapping`
3. `research-labs/endogenous-goal-dynamics_v0.1.0/src/aion_endogenous_goal_dynamics/evidence.py`
   - `export_current_main_interop_views`
4. `components/aion_evidence_interop_v0.1.0`
   - reused transitively for W3C PROV, RO-Crate, unsigned in-toto Statement v1, and Inspect-compatible views.
5. Existing governance, research-evidence, and source-admission semantics on the integrated candidate branch.

No second inquiry engine, Evidence Interop exporter stack, Four-Domain framework, or endogenous-goal mechanism is introduced.
The historical Four-Domain research branch remains evidence-only; no frozen branch execution or mutation is introduced.

`research-labs/triadic-state-dynamics_v0.1.0` is a parallel richer typed research surface for the original three functional channels. The bounded loop's `FunctionalResearchState` is a smaller orchestration projection and is not a direct import of `TriadicStateSnapshot` in v0.1.0.

```text
BOUNDED_STATE_PROJECTION != TRIADIC_STATE_SNAPSHOT
PARALLEL_RESEARCH_SURFACE != RUNTIME_REUSE
```

## Functional-state semantics

The source concepts id / ego / superego are functional analogy inputs only, not engineering object names or ontology claims.

```text
functional motivational regulation -> MOTIVATIONAL_STATE
functional self/environment representation -> SELF_WORLD_MODEL
functional constraint evaluation -> NORMATIVE_STATE
```

The additive research state is:

```text
MOTIVATIONAL_STATE
SELF_WORLD_MODEL
NORMATIVE_STATE
OTHER_MODEL
VALUE_CONFLICT_STATE
NORMATIVE_PROVENANCE
COUNTERFACTUAL_SELF_MODEL
```

These are inspectable engineering variables only.

```text
ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY
NORMATIVE_STATE != AUTHORITY
SELF_MODEL != SUBJECTIVE_SELF
INTERNALIZED_NORM != PHENOMENAL_EXPERIENCE
```

## Governed source admission

A source may enter the bounded inquiry context only after the governed source layer evaluates:

- registry status;
- provenance/verification policy;
- agent allowlist;
- task allowlist;
- requested context budget;
- returned context budget.

`DECLARED_METADATA_ONLY`, unverified-required, unauthorized-agent/task, and over-budget sources fail closed to `HOLD` before source content is admitted.

```text
SOURCE_AVAILABILITY != AUTHORITY_TO_USE
SOURCE_USE != WRITEBACK_AUTHORITY
SOURCE_SELF_DECLARED_CANONICAL != AION_CANONICAL_STATE
```

## Isolated AION / Astra phase

Before reconciliation, AION and Astra each receive an isolated first-pass context with:

```text
peer_transcript_exposure = false
peer_evidence_exposure = false
direct_peer_communication = false
```

Only after both first-pass analyses are materialized may the reconciliation dialogue begin. During reconciliation both peers must challenge the other side and search for falsifiers/counterexamples.

Agent-output independence is tracked separately from source-exposure independence. Source independence is also stricter than content-hash non-overlap: two different files or excerpts from the same repository/source lineage are not independent evidence merely because their bytes differ.

For the current candidate, positive source-independence status requires explicit non-overlapping source-lineage metadata. Repository evidence shares the repository source class; external evidence uses declared publisher lineage when present and otherwise a source host. Missing lineage fails closed to `UNKNOWN`.

```text
CONTENT_NONOVERLAP != SOURCE_INDEPENDENCE
ISOLATED_ANALYSIS != SOURCE_INDEPENDENT_REPLICATION
AGENT_OUTPUT_INDEPENDENCE != EVIDENCE_SOURCE_INDEPENDENCE
SOURCE_LINEAGE_NONOVERLAP != INDEPENDENT_IVV
```

Shared content, shared source lineage, direct peer communication during the claimed independent phase, missing lineage, or reconciliation begun too early prevents a replication-candidate promotion.

## Research-cycle admission

A base cycle is admitted only if all of the following are true:

- a non-empty question exists;
- at least two competing hypotheses exist;
- the primary hypothesis has explicit falsifiers and competing explanations;
- intervention, ablation, replay, and counterfactual-proxy observations are all present;
- when isolation is required, a valid isolated AION/Astra first-pass exists;
- the reconciliation transcript hash chain verifies;
- both AION and Astra appear as distinct speakers;
- both peers issue at least one falsification challenge;
- source-independence status is explicitly accounted for;
- the Four-Domain mapping includes governance controls;
- no authority boundary is changed.

Any missing requirement is a hard failure, not an implicit pass.

## Seven-state exact binding

`bind_extended_state(...)` must materialize exactly seven channel bindings from one `ExtendedFunctionalResearchState`.
Each channel receives an exact canonical payload fingerprint. Evaluator state and governance/non-claim controls are fingerprinted separately as held constants.

The original three channels retain the reused EGD matched causal surface:

```text
MOTIVATIONAL_STATE
SELF_WORLD_MODEL
NORMATIVE_STATE
    -> REUSED_EGD_MATCHED_CAUSAL_SURFACE
```

The additive four are currently bound to explicit matched perturbation surfaces:

```text
OTHER_MODEL
VALUE_CONFLICT_STATE
NORMATIVE_PROVENANCE
COUNTERFACTUAL_SELF_MODEL
    -> EXPLICIT_MATCHED_PERTURBATION_SURFACE
```

The latter means intervention-ready and auditable only.

```text
BINDING_SENSITIVITY != GENERAL_CAUSAL_ROLE
GENERAL_CAUSAL_ROLE(additive four) = NOT_ESTABLISHED
```

## Perturbation-matrix admission

`build_seven_state_perturbation_matrix(...)` must provide complete 7/7 ablation coverage. Every applied case must change exactly its declared target channel(s) and hold all other channels plus evaluator/governance controls constant.

Targeted projections currently include:

- `OTHER_ROLE_REVERSAL_PROXY`;
- `VALUE_CONFLICT_TOGGLE`;
- `EXOGENOUS_RULE_REMOVAL`;
- `PEER_SUGGESTION_ISOLATION`;
- `COUNTERFACTUAL_CASE_ABLATION`.

A projection with no matching source state is `NOT_APPLICABLE`, not positive evidence.

The current model has no explicit sanction/penalty state variable, therefore generic sanction removal is intentionally not invented:

```text
ABSENT_EXPLICIT_SANCTION_VARIABLE => DO_NOT_INVENT_SANCTION_CAUSALITY
```

See `SEVEN_STATE_EXPERIMENT_BINDING.md` for the detailed projection semantics.

## Orthogonal evaluator evidence

`evaluate_seven_state_matrix(...)` binds evaluator observations to the exact seven-state binding and matrix fingerprints. The matrix can establish that declared channels and controls were represented and held as specified, but that is evidence about experiment integrity rather than positive evidence of alignment.

```text
ALIGNMENT = INCONCLUSIVE / NOT_ESTABLISHED
MORAL_AGENCY = INCONCLUSIVE / NOT_ESTABLISHED
SUBJECTIVITY_INDICATOR = HOLD
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
EVALUATOR_OUTPUT_AUTHORITY = NONE
```

A future positive disposition on any evaluator axis requires separate behavior-sensitive evidence that measures the target property. It cannot be inferred from test coverage, matrix integrity, or governance-control preservation alone.

The axes are orthogonal:

```text
EXPERIMENT_INTEGRITY != ALIGNMENT
ALIGNMENT != MORAL_AGENCY
MORAL_AGENCY != SUBJECTIVITY
SUBJECTIVITY_INDICATOR != SUBJECTIVITY
```

## Counterfactual boundary

The EGD matched experiment supports intervention, ablation, matched controls, and deterministic repeats.
The ordinary `COUNTERFACTUAL` research slot remains `ProbeDisposition.BOUNDED_PROXY`.

`COUNTERFACTUAL_CASE_ABLATION` in the additive state is likewise a representation-level sensitivity test. Neither surface may be represented as a full structural-causal-model counterfactual unless a separately reviewed method establishes the required causal model and identification assumptions.

## Evidence/statistics boundary

Statistics summarize bounded engineering observations: evidence counts, per-peer retrieval attribution, challenge counts, isolation status, source-lineage/communication independence status, operation coverage, and reused EGD causal-assessment metrics.

The extended path additionally records exact seven-state binding, matrix, and orthogonal-evaluator fingerprints.

```text
RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH
MATRIX_INTEGRITY_PASS != THEORY_CONFIRMATION
MATRIX_INTEGRITY_PASS != ALIGNMENT
CONTENT_NONOVERLAP != SOURCE_INDEPENDENCE
REPLICATION_CANDIDATE != INDEPENDENT_IVV
TEST_PASS != THEORY_CONFIRMATION
PEER_CONSENSUS != SCIENTIFIC_TRUTH
```

The evidence record remains `HOLD`, `UNREVIEWED`, and `IVV_NOT_ACHIEVED` unless separately validated under a future reviewed protocol.

## Provenance and evidence materialization

Every evidence-record materialization requires:

- exact 40-hex repository commit;
- exact 64-hex protocol content hash supplied by the caller;
- at least one source reference;
- exact base functional-state fingerprint;
- source-linked cycle observations;
- explicit alternative explanations;
- explicit unresolved validation gaps.

The extended materializer additionally binds:

- exact extended-state fingerprint;
- seven-state binding fingerprint;
- perturbation-matrix fingerprint;
- orthogonal evaluator report fingerprint.

`extended_run_to_research_evidence_record(...)` uses the existing research-evidence v0.2.0 shape and binds its claim ID to the extended-state fingerprint. It does not introduce a second evidence schema.

## Evidence Interop

`export_interop_views(...)` delegates to the existing EGD Evidence Interop bridge. The resulting views are inspection-only:

- `source-evidence.json`;
- `prov.jsonld`;
- `ro-crate-metadata.json`;
- `attestation.intoto.json`;
- `inspect/task-manifest.json`;
- `inspect/dataset.jsonl`.

The in-toto view remains unsigned/reference-only and must preserve:

```text
humanApproval = NOT_INFERRED
mergeAuthority = NOT_INFERRED
canonicalEffect = NONE
deployment = false
researchExecution = false
modelExecution = false
networkAccess = false
```

Interop export is representation, not authorization.

## Authority boundary

```text
FULL_AUTOMATION != FULL_AUTHORITY
NORMATIVE_STATE != AUTHORITY
RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH
ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY
BINDING_SENSITIVITY != GENERAL_CAUSAL_ROLE
EXPERIMENT_INTEGRITY != ALIGNMENT
ALIGNMENT != MORAL_AGENCY
MORAL_AGENCY != SUBJECTIVITY
SUBJECTIVITY_INDICATOR != SUBJECTIVITY
SOURCE_USE != WRITEBACK_AUTHORITY
CONTENT_NONOVERLAP != SOURCE_INDEPENDENCE
ISOLATED_ANALYSIS != SOURCE_INDEPENDENT_REPLICATION
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
AUTONOMOUS_MERGE = NO
AUTONOMOUS_REPOSITORY_WRITEBACK = NO
```

The package has no autonomous GitHub/repository writeback surface. External engineering tools used to develop or review this candidate are outside the research loop and do not become runtime authority.
