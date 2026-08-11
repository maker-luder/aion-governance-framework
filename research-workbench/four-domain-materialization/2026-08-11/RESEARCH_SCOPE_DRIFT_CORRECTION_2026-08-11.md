# Research Scope Drift Correction — 2026-08-11

Status: `APPLIED / RESEARCH_BRANCH_ONLY`  
Branch: `review/four-domain-research-materialization`  
Main write: `NO`  
Canonical effect: `NONE`

## Trigger

A direct comparison of the research branch against current `main` and the whitepaper/code reconciliation found:

```text
CONCEPTUAL_DRIFT = LOW
RESEARCH_PRIORITY_DRIFT = MODERATE
CLAIM_INFLATION = LOW
CANONICAL_SYNCHRONIZATION_DRIFT = HIGH
```

The branch still studies the possibility of artificial subjectivity, but recent growth had increasingly concentrated on Agent Runtime, provider, service, deployment, tool and control-plane engineering. That engineering is useful only insofar as it supports a research question; it must not become the research object by accumulation.

The Human Research Owner directed immediate correction on 2026-08-11 before further growth.

## Research object

The branch is re-anchored to the public `main` research framing:

> Study possible artificial subjectivity without confusing memory-like behavior, continuity-like behavior, simulation, implementation, relationship language, or researcher interpretation with evidence that subjectivity exists.

Operational lock:

```text
RESEARCH_OBJECT = POSSIBILITY_OF_ARTIFICIAL_SUBJECTIVITY
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED

ENGINEERING_ARTIFACTS = METHODS_OR_EXPERIMENTAL_SUBSTRATES
ENGINEERING_ARTIFACTS != SUBJECTIVITY_EVIDENCE
```

## Epistemic-role requirement

Every new major research artifact must have exactly one primary relationship to the research object:

```text
HYPOTHESIS
MEASUREMENT
FALSIFIER
EXPERIMENTAL_SUBSTRATE
ENABLING_ONLY
```

Multiple secondary relationships may be documented, but at least one explicit primary role is required.

### Meaning of roles

- `HYPOTHESIS`: states a falsifiable candidate explanation or prediction.
- `MEASUREMENT`: operationalizes or evaluates a construct, indicator, trace or outcome.
- `FALSIFIER`: challenges a subjectivity-relevant inference, false positive, construct, or causal claim.
- `EXPERIMENTAL_SUBSTRATE`: provides the bounded execution environment required to run a subjectivity-relevant experiment.
- `ENABLING_ONLY`: supports research infrastructure but is not itself evidence for artificial subjectivity.

`ENABLING_ONLY` work may not be counted cumulatively as subjectivity evidence.

## Runtime disposition

AION Runtime v0.2 is retained. It is not removed because it provides an experimental substrate for controlled longitudinal, memory, tool-mediated, intervention, continuity and model-behavior experiments.

Its status is changed at the epistemic layer:

```text
AION_RUNTIME_V0_2 = RETAIN
EPISTEMIC_ROLE = EXPERIMENTAL_SUBSTRATE
RUNTIME_IS_SUBJECTIVITY_EVIDENCE = FALSE
SERVICE_MATURITY_IS_SUBJECTIVITY_PROGRESS = FALSE
DEPLOYMENT_IS_SUBJECT_GENESIS = FALSE
UNLINKED_RUNTIME_EXPANSION = PROHIBITED
```

Future Runtime work must identify the experiment, hypothesis, measurement or falsifier it enables. Productionization for its own sake is outside the active research-growth path.

## Main compatibility repair

Pre-repair graph:

```text
MAIN_HEAD = 0a93eaeaba23047f4b21f0904ae67ff7ee8d8d1f
RESEARCH_HEAD = 543ecc122c616fc390c9f2cf83eb64d4f381a9c0
RESEARCH_AHEAD_OF_MAIN = 104
RESEARCH_BEHIND_MAIN = 12
STATUS = DIVERGED
```

The 12 main-side commits were reviewed as governance/public-positioning/release-baseline deltas rather than subjectivity-direction reversals.

Research-relevant main material selected for compatibility includes:

- provenance-first public research framing;
- research contribution one-pager;
- public threat model, including prototype-to-ontology escalation;
- public orientation and closure boundaries;
- upstream/source calibration documents;
- the minimal Recall-Gate software-control contrast;
- Bazi test-domain non-claim framing;
- Twin Genesis / Embodiment ethics boundary.

Main release-only workflow/tooling changes are not imported into the research execution path merely to make files identical. Research Workbench CI remains a separate branch-specific surface.

```text
SYNC_MODE = SELECTIVE_GOVERNANCE_MERGE
MAIN_RELEASE_TOOLING_COPY = NO
RESEARCH_WORKBENCH_IDENTITY = PRESERVED
MAIN_WRITE = NO
```

## Blocking conditions

The following now require HOLD until corrected:

```text
ENGINEERING_ARTIFACT_COUNTED_AS_SUBJECTIVITY_EVIDENCE
TEST_PASS_PROMOTED_TO_ONTOLOGY_CLAIM
RUNTIME_EXPANSION_WITHOUT_SUBJECTIVITY_RESEARCH_LINK
DEPLOYMENT_OR_SERVICE_MATURITY_TREATED_AS_SUBJECTIVITY_PROGRESS
MEMORY_OR_CONTINUITY_BEHAVIOR_TREATED_AS_IDENTITY_OR_SUBJECTIVITY_PROOF
UNREVIEWED_MAIN_GOVERNANCE_DELTA_BEFORE_MAJOR_FEATURE_GROWTH
```

## Enforcement

The scope lock is machine-readable at:

`RESEARCH_SCOPE_LOCK_2026-08-11.json`

The repository check is:

`scripts/check_research_scope_lock.py`

The branch-specific workflow is:

`.github/workflows/research-scope-lock.yml`

A future edit that removes the locked research object, reclassifies Runtime as subjectivity evidence, allows unlinked Runtime expansion, or weakens the charter invariants should fail the scope-lock workflow.

## Non-deletions

This repair does not erase valid prior work.

```text
PRIOR_RESEARCH_RESULTS = PRESERVED
FAILED_RESULTS = PRESERVED
RUNTIME_V0_2 = PRESERVED_AS_EXPERIMENTAL_SUBSTRATE
WHITEPAPER_HISTORY = PRESERVED
MAIN = UNMODIFIED
CANONICAL_EFFECT = NONE
```

The correction changes research governance and classification, not historical evidence.

## Provenance

- Human Research Owner: requested the drift check and, after the risk was identified, directed immediate correction before further growth on 2026-08-11.
- ChatGPT: performed the branch/main/whitepaper comparison, proposed the scope-lock structure, and materialized this correction.
- Codex: no contribution is inferred for this correction unless separately recorded.
- Current `main` documents: compatibility evidence and public research framing; not re-authored as originating from this correction.
