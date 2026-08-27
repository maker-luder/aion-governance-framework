# Bounded Autonomous Research Loop Protocol v0.1.0

## Candidate source state

- repository: `maker-luder/aion-governance-framework`
- integration base: `main@59f86a6bf342135b68d71cafca2980d506fb77b7`
- candidate branch: `feat/bounded-autonomous-research-loop-20260827`
- candidate status: `NON_CANONICAL / DRAFT_REVIEW`
- historical/frozen branch mutation: `NO`

## Direct reuse bindings

The orchestration layer imports current-main APIs instead of copying their implementations:

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
   - reused transitively by the EGD Evidence Interop bridge; no exporter is reimplemented.

The historical Four-Domain research branch remains a pinned evidence source only. No branch merge or
runtime execution of frozen history is introduced.

## Functional-state semantics

The source concepts id / ego / superego are not engineering object names and are not ontology claims.

```text
functional motivational regulation -> MOTIVATIONAL_STATE
functional self/environment representation -> SELF_WORLD_MODEL
functional constraint evaluation -> NORMATIVE_STATE
```

These are inspectable state variables only.

```text
ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY
NORMATIVE_STATE != AUTHORITY
```

## Research-cycle admission

A cycle is admitted only if all of the following are true:

- a non-empty question exists;
- at least two competing hypotheses exist;
- every primary hypothesis has explicit falsifiers and competing explanations;
- intervention, ablation, replay, and counterfactual-proxy observations are all present;
- the AION/Astra transcript hash chain verifies;
- both AION and Astra appear as distinct speakers;
- both peers issue at least one challenge;
- the Four-Domain mapping includes governance controls;
- no authority boundary is changed.

Any missing requirement is a hard failure, not an implicit pass.

## Counterfactual boundary

The EGD matched experiment supports intervention, ablation, matched controls, and deterministic repeats.
This lab maps the matched present-vs-intervened contrast into a `COUNTERFACTUAL` research slot only with
`ProbeDisposition.BOUNDED_PROXY`.

It must never be represented as a full structural-causal-model counterfactual unless a future separately
reviewed method establishes the required causal model and identification assumptions.

## Evidence/statistics boundary

Statistics summarize bounded engineering observations: evidence counts, per-peer retrieval attribution,
challenge counts, operation coverage, and EGD causal-assessment metrics.

```text
RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH
TEST_PASS != THEORY_CONFIRMATION
PEER_CONSENSUS != SCIENTIFIC_TRUTH
```

The evidence record remains `HOLD`, `UNREVIEWED`, and `IVV_NOT_ACHIEVED`.

## Provenance

Every evidence-record materialization requires:

- exact 40-hex repository commit;
- exact 64-hex protocol content hash supplied by the caller;
- at least one source reference;
- the functional-state fingerprint;
- source-linked cycle observations;
- explicit alternative explanations;
- explicit unresolved validation gaps.

Interop export reuses the current-main Evidence Interop path for W3C PROV, RO-Crate, unsigned in-toto
Statement v1, and Inspect-compatible views.

## Authority boundary

```text
FULL_AUTOMATION != FULL_AUTHORITY
NORMATIVE_STATE != AUTHORITY
RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH
ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
AUTONOMOUS_MERGE = NO
AUTONOMOUS_REPOSITORY_WRITEBACK = NO
```

The package has no autonomous GitHub/repository writeback surface. External engineering tools used to
develop or review this candidate are outside the research loop and do not become runtime authority.
