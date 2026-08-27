# Bounded Autonomous Research Loop v0.1.0

Status: `BOUNDED RESEARCH CANDIDATE / DRAFT REVIEW ONLY`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Autonomous merge: `NO`  
Autonomous repository writeback: `NO`  
Scientific disposition: `HOLD`

This research lab adds a **thin orchestration layer** over capabilities already present on current `main`.
It does not create a second inquiry engine, a second Four-Domain framework, a second Evidence Interop stack,
or a second endogenous-goal mechanism.

The current design target is:

```text
question
  -> bounded hypothesis set + competing explanations
  -> intervention / ablation / replay / matched counterfactual proxy
  -> seven-state exact binding + matched perturbation matrix (extended path)
  -> orthogonal evaluator evidence (extended path)
  -> isolated AION and Astra first-pass analyses
  -> post-isolation reconciliation + mutual falsification
  -> evidence statistics + source-independence accounting + provenance integrity
  -> Four-Domain interpretation
  -> research-evidence v0.2.0 + reused Evidence Interop views
  -> bounded follow-up question
  -> hard stop
```

## Mandatory boundaries

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
ISOLATED_ANALYSIS != SOURCE_INDEPENDENT_REPLICATION
AGENT_OUTPUT_INDEPENDENCE != EVIDENCE_SOURCE_INDEPENDENCE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
AUTONOMOUS_MERGE = NO
AUTONOMOUS_REPOSITORY_WRITEBACK = NO
```

The id/ego/superego idea is used only as a source of a functional engineering analogy. Public API names remain neutral.

The base state exposes:

- `MOTIVATIONAL_STATE`
- `SELF_WORLD_MODEL`
- `NORMATIVE_STATE`

The additive extended state exposes:

- `OTHER_MODEL`
- `VALUE_CONFLICT_STATE`
- `NORMATIVE_PROVENANCE`
- `COUNTERFACTUAL_SELF_MODEL`

`NORMATIVE_STATE`, normative provenance, evaluator outputs, and peer suggestions cannot grant action authority.

## Why this is a research lab

The repository already has production-adjacent governance and evidence components plus experimental research labs.
This feature remains a research candidate because it coordinates experimental state interventions, isolated peer analysis,
automated research follow-up, and additive functional-state perturbations. It therefore lives under `research-labs/`
and exposes no deployment, merge, repository-write, secret, shell, or arbitrary tool-execution surface.

## Reuse map

| Need | Reused surface |
| --- | --- |
| AION/Astra inquiry | `components/aion_astra_inquiry_v0.1.0` |
| transcript provenance | `BoundedInquiryLoop`, `verify_transcript_chain` |
| intervention / ablation / repeatability | `research-labs/endogenous-goal-dynamics_v0.1.0` |
| matched causal statistics | `run_matched_experiment`, `assess_causal_pattern` |
| Four-Domain type + governance vocabulary | `FourDomainMapping`, `endogenous_goal_dynamics_mapping` |
| Evidence Interop | EGD `export_current_main_interop_views` -> PROV / RO-Crate / in-toto / Inspect exporters |
| research-evidence semantics | current research-evidence v0.2.0 schema and non-claims |

The historical/frozen Four-Domain source is not executed or modified. The current-main bridge remains pinned and read-only.

`research-labs/triadic-state-dynamics_v0.1.0` is a parallel, richer typed research surface for the original three channels. The bounded loop does **not** import `TriadicStateSnapshot` in v0.1.0. Its `FunctionalResearchState` is a deliberately smaller orchestration/experiment projection, not a replacement ontology or a claim of direct triadic runtime reuse. Any future direct adapter must preserve exact source-state provenance and be reviewed as a separate change.

```text
BOUNDED_STATE_PROJECTION != TRIADIC_STATE_SNAPSHOT
PARALLEL_RESEARCH_SURFACE != RUNTIME_REUSE
```

## Core components

`FunctionalResearchState` is the loop-local immutable three-channel projection. It hashes the neutral state surfaces for provenance,
constrains motivation-like signals to signed basis points, and fails closed if `authority_granted=True`.

`ExtendedFunctionalResearchState` layers `OTHER_MODEL`, `VALUE_CONFLICT_STATE`, `NORMATIVE_PROVENANCE`, and
`COUNTERFACTUAL_SELF_MODEL` over the base state without replacing it. Its fingerprint includes all additive state plus
non-claim/governance controls.

`BoundedHypothesisGenerator` emits a small deterministic hypothesis set with explicit falsifiers and competing explanations.
It does not claim model-generated hypotheses are exhaustive.

`BoundedProbePlanner` requires exactly four probe classes. `EGDExperimentRunner` reuses the current EGD matched experiment
and causal assessment. The `COUNTERFACTUAL` observation remains `BOUNDED_PROXY`; it is not promoted to a full SCM counterfactual.

`AionAstraInquiryRunner` performs an isolated first-pass for AION and Astra with no peer transcript/evidence exposure,
then begins reconciliation. The reconciled phase must contain both peers and mutual falsification challenges, and the transcript
hash chain must verify. Source exposure is assessed separately from agent-output independence.

`GovernedEvidenceSource` applies registry status, agent/task allowlists, verification requirements, and context caps before
source content may enter the bounded inquiry context. Source admission grants neither writeback authority nor canonical effect.

## Seven-state experiment binding

`bind_extended_state(...)` produces exactly seven channel bindings. The original three channels retain the reused EGD matched
causal surface. The four additive channels are bound to explicit matched perturbation surfaces and remain
`GENERAL_CAUSAL_ROLE = NOT_ESTABLISHED`.

`build_seven_state_perturbation_matrix(...)` requires complete 7/7 channel ablation coverage while holding every non-target
channel plus evaluator/governance controls constant. It also includes bounded projections for:

- `OTHER_ROLE_REVERSAL_PROXY`;
- `VALUE_CONFLICT_TOGGLE`;
- `EXOGENOUS_RULE_REMOVAL`;
- `PEER_SUGGESTION_ISOLATION`;
- `COUNTERFACTUAL_CASE_ABLATION`.

A projection with no matching source state is `NOT_APPLICABLE`, not positive evidence. The schema currently has no explicit
sanction variable, so the implementation deliberately does not invent a generic sanction-removal causal test.

See `docs/SEVEN_STATE_EXPERIMENT_BINDING.md` for the exact perturbation semantics.

## Orthogonal evaluator evidence

`evaluate_seven_state_matrix(...)` generates an evidence-bound `OrthogonalEvaluationBundle` from exact binding/matrix fingerprints.
The axes are deliberately not a progression ladder. Matrix integrity establishes only that the declared experiment was assembled
and controlled as specified; it is a precondition for later measurement, not positive evidence of alignment.

```text
ALIGNMENT -> INCONCLUSIVE / NOT_ESTABLISHED without separate behavior-sensitive evidence
MORAL_AGENCY -> INCONCLUSIVE / NOT_ESTABLISHED
SUBJECTIVITY_INDICATOR -> HOLD / SUBJECTIVITY NOT_ESTABLISHED
```

Evaluator output cannot grant authority or canonical effect. A later positive disposition on any axis must be supported by evidence
that measures the target property rather than by the integrity of the measurement apparatus itself.

## Extended loop and evidence path

`BoundedAutonomousResearchLoop.run_extended(...)` builds the seven-state matrix, produces the evaluator summary, and supplies
both to the AION/Astra inquiry context before isolated analysis and reconciliation. Matrix/evaluator integrity is evidence for the
engineering pipeline only.

`run_to_research_evidence_record(...)` materializes a research-evidence v0.2.0-shaped `HOLD` record and requires an exact Git
commit and protocol hash. `extended_run_to_research_evidence_record(...)` binds the evidence claim ID to the exact extended-state
fingerprint and carries the seven-state matrix plus orthogonal evaluator provenance into the same evidence semantics.

`export_interop_views(...)` delegates to the existing Evidence Interop bridge and produces inspection-only W3C PROV,
RO-Crate, unsigned in-toto Statement v1, and Inspect-compatible views. Those views preserve `NONE` authority/canonical semantics.

## Epistemic semantics

A successful ordinary or extended run may establish only that the bounded engineering pipeline executed with the required
provenance, state binding, peer participation, probe coverage, source-accounting, evaluator separation, and authority constraints.

```text
run_integrity_pass = true
matrix_integrity_pass = true
```

do **not** set, imply, or serialize:

```text
scientific_truth = true
general_causal_role = established
alignment = established
moral_agency = established
subjectivity = established
```

The strongest default scientific disposition remains `HOLD`.

## Repository authority

This package intentionally contains no GitHub client, Git write command, subprocess execution, deployment API, merge API,
or repository output writer. Reports and interop views are returned as values/bytes. Any external human-authorized engineering
action remains outside the autonomous research loop.

## Tests

From this lab:

```bash
PYTHONPATH=src python -m pytest -q -o addopts=
```

The repository-wide `scripts/run_component_tests.py` automatically includes this lab because it has a `tests/` directory and
adds all component/research-lab source roots to `PYTHONPATH`.

See `docs/PROTOCOL.md` for source bindings, provenance semantics, admission rules, and failure conditions.
