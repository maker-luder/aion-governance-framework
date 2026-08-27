# Bounded Autonomous Research Loop v0.1.0

Status: `BOUNDED RESEARCH CANDIDATE / DRAFT REVIEW ONLY`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Autonomous merge: `NO`  
Autonomous repository writeback: `NO`  
Scientific disposition: `HOLD`

This research lab adds a **thin orchestration layer** over capabilities already present on current `main`.
It does not create a second inquiry engine, a second Four-Domain framework, or a second endogenous-goal
mechanism.

The design target is:

```text
question
  -> bounded hypothesis set + competing explanations
  -> intervention / ablation / replay / matched counterfactual proxy
  -> independent AION and Astra inquiry
  -> mutual falsification / counterexample pressure
  -> evidence statistics + provenance integrity
  -> Four-Domain interpretation
  -> bounded follow-up question
  -> hard stop
```

## Mandatory boundary

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

The id/ego/superego idea is used only as a source of a functional engineering analogy. Public API names are
neutral:

- `MOTIVATIONAL_STATE`
- `SELF_WORLD_MODEL`
- `NORMATIVE_STATE`

`NORMATIVE_STATE` carries inspectable constraints. It cannot grant action authority.

## Why this is a research lab

The repository already has production-adjacent governance and evidence components plus experimental
research labs. This feature remains a research candidate because it coordinates experimental state
interventions and automated research follow-up. It therefore lives under `research-labs/` and exposes
no deployment, merge, repository-write, secret, shell, or arbitrary tool-execution surface.

## Reuse map

| Need | Reused current-main surface |
| --- | --- |
| AION/Astra independent inquiry | `components/aion_astra_inquiry_v0.1.0` |
| alternating peer challenge + hash-chain provenance | `BoundedInquiryLoop`, `verify_transcript_chain` |
| intervention / ablation / repeatability | `research-labs/endogenous-goal-dynamics_v0.1.0` |
| matched causal statistics | `run_matched_experiment`, `assess_causal_pattern` |
| Four-Domain data type + governance vocabulary | `FourDomainMapping`, `endogenous_goal_dynamics_mapping` |
| Evidence Interop | EGD `export_current_main_interop_views` -> current-main PROV / RO-Crate / in-toto / Inspect exporters |
| subjectivity/consciousness nonclaims | existing research-evidence v0.2.0 semantics |

The separate historical/frozen Four-Domain source is not executed or modified. The current-main bridge remains
pinned and read-only.

## Components

`FunctionalResearchState` is a small immutable snapshot. It keeps the three neutral state surfaces separate,
hashes them for provenance, constrains motivation-like signals to signed basis points, and fails closed if
`authority_granted=True`.

`BoundedHypothesisGenerator` emits a small explicit hypothesis set with falsifiers and competing explanations.
It is deterministic and bounded; it does not claim that model-generated hypotheses are exhaustive.

`BoundedProbePlanner` requires exactly four probe classes. `EGDExperimentRunner` reuses the current EGD matched
experiment and causal assessment. The `COUNTERFACTUAL` observation is deliberately marked `BOUNDED_PROXY`:
a matched present-vs-intervened contrast is useful evidence, but it is **not** promoted to a full SCM
counterfactual.

`AionAstraInquiryRunner` directly reuses `BoundedInquiryLoop`. A run fails closed unless both AION and Astra
contribute and both issue a falsification challenge. The existing transcript hash chain must verify.

`BoundedAutonomousResearchLoop` may derive a follow-up research question from the strongest unresolved peer
challenge, but `max_cycles` is hard-bounded to 1..4. A follow-up is only a question. It is not a repository
action or authorization token.

`run_to_research_evidence_record` materializes a current research-evidence v0.2.0-shaped `HOLD` record and
requires an exact Git commit and exact protocol hash. `export_interop_views` delegates to the existing
Evidence Interop exporter path.

## Epistemic semantics

A successful run may establish only that the bounded engineering pipeline executed with the required
provenance, peer participation, probe coverage, and authority constraints.

```text
run_integrity_pass = true
```

does **not** set, imply, or serialize:

```text
scientific_truth = true
```

The strongest default disposition remains `HOLD`.

## Repository authority

This package intentionally contains no GitHub client, Git write command, subprocess execution, deployment API,
merge API, or repository output writer. Reports are returned as in-memory values. Any external human-authorized
engineering action (for example, opening a Draft PR) remains outside the autonomous research loop.

## Tests

From this lab:

```bash
PYTHONPATH=src python -m pytest -q -o addopts=
```

The repository-wide `scripts/run_component_tests.py` automatically includes this lab because it has a `tests/`
directory and adds all component/research-lab source roots to `PYTHONPATH`.

See `docs/PROTOCOL.md` for source bindings, provenance semantics, and failure conditions.
