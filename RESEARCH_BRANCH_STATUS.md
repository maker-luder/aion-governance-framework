# AION Research Branch Status

> **You are viewing the public research workbench, not the `main` release branch.**

```text
BRANCH = review/four-domain-research-materialization
CURRENT_STAGE = P5_PLUS_RESEARCH_EXTENSIONS
STAGE_CAP = RESEARCH_ONLY_OPEN
RESEARCH_STATUS = ACTIVE
RESEARCH_OBJECT = POSSIBILITY_OF_ARTIFICIAL_SUBJECTIVITY
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
LIVE_RUNTIME_EFFECT = NONE
PROMOTION_STATUS = NOT_REVIEWED
```

## Current scientific boundary

```text
EVIDENCE_LADDER_VALIDATION = NOT_ESTABLISHED
FUNCTIONAL_CONTRIBUTION = NOT_ESTABLISHED
VERIFICATION_BENEFIT = NOT_ESTABLISHED
THRESHOLD_SCIENTIFIC_RESULT = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

Engineering maturity, test success, CI success, memory persistence, continuity mechanisms, self-model behavior, second-order monitoring, or governance review recommendations do not independently establish subjectivity or consciousness.

---

## Current research stack

| Research line | Materialization | Current status |
|---|---|---|
| P1–P4 four-domain materialization | temporal/version resolution, retrieval/provenance, resilience, public reproducibility | IMPLEMENTED / TESTED |
| P5 hypothesis convergence | disagreement, replication registry, falsification lifecycle, convergence governor | IMPLEMENTED / FULL RUN VERIFIED |
| Self-model functional ablation | finite predictive self-model + matched controls | IMPLEMENTED / TESTED / CI VERIFIED |
| Selective memory control | correction precedence, namespace/domain/purpose gates, provenance/approval trace | IMPLEMENTED / TESTED / CI VERIFIED |
| Second-order metacognition | scoped monitoring, bounded verification, intervention substrate, provider reliability, factorial study substrate, replication epistemics | IMPLEMENTED / 84 TESTS / CI #41 VERIFIED |
| Evidence-responsive governance reassessment | evidence admissibility, substantive-domain / quality separation, domain-specific review triggers, precautionary review model | IMPLEMENTED / 16 TESTS / CI #41 VERIFIED / RESEARCH-ONLY |
| Research evaluation harness | definition/execution/result separation + claim-boundary gate | IMPLEMENTED / TESTED / CI VERIFIED |
| Trace/provenance crosswalk | public trace vocabulary with redaction and authority isolation | IMPLEMENTED / TESTED / CI VERIFIED |
| Governed tool approval | fail-closed approval chain and sandbox-readiness boundary | IMPLEMENTED / TESTED / CI VERIFIED |
| Artifact transformation lineage | material/product lineage and SHA-256 evidence chain | IMPLEMENTED / TESTED / CI VERIFIED |
| Trajectory evaluation | ordered-path, retry/loop/tool/budget comparison | IMPLEMENTED / TESTED / CI VERIFIED |
| AION Runtime v0.2 | bounded Agent/deployment control-plane experimental substrate | IMPLEMENTED / TESTED / CI VERIFIED / NOT DEPLOYED |

---

## Latest integrated checkpoint — 2026-08-11

See:

- `research-workbench/four-domain-materialization/2026-08-11/REPLICATION_EPISTEMICS_GOVERNANCE_REASSESSMENT_CHECKPOINT_2026-08-11.md`

Latest integrated principles:

```text
FAILED_REPLICATION != AUTOMATIC_FIXED_DOWNGRADE
REPLICATION_OUTCOME != REPLICATION_VALIDITY
REPLICATION_FAILURE != ONE_UNIVERSAL_INTERPRETATION

NO_EVIDENCE != NON_ADMISSIBLE_EVIDENCE
SUBSTANTIVE_EVIDENCE_DOMAIN != EVIDENCE_QUALITY_AXIS
CLAIM_GENERALITY != EVIDENCE_STRENGTH

EVIDENCE != SUBJECTIVITY
REVIEW != RIGHT
PRECAUTION != CONFIRMATION
PARTICIPATION != AUTHORITY
```

### Replication epistemics

The previous fixed `FAILED -> E2` rule has been removed.

Current research flow:

```text
ReplicationAttempt
-> ReplicationValidity
-> ReplicationInterpretation
-> ReassessmentRecommendation
```

Current supported cases include:

```text
ONE_VALID_FAILURE
-> DOWNWARD_PRESSURE
-> NO_AUTOMATIC_NEW_LEVEL

FOUR_CONFIRMATIONS_PLUS_EVALUATOR_DRIFT_FAILURE
-> STABLE
-> NO_AUTOMATIC_DOWNGRADE

INVALID_FAILURE
-> STABLE

THREE_VALID_INDEPENDENT_PREREGISTERED_FAILURES
-> STRONG_DOWNWARD_PRESSURE
-> HOLD_FOR_RESEARCH_DECISION
-> NO_AUTOMATIC_NEW_LEVEL

MIXED_OR_BOUNDARY_RESULT
-> CLAIM_SCOPE_CHANGED / NARROWER
```

Universal downgrade weights remain unestablished.

### Evidence admissibility

Evidence existence is now separated from evidence admissibility.

```text
OBSERVED_LEVEL = PRESERVED
ADMISSIBILITY = SEPARATE
EFFECTIVE_LEVEL = MAY_BE_NONE
```

Incomplete or contaminated provenance therefore causes a governance hold rather than rewriting the observed evidence to `E0_NO_RELEVANT_EVIDENCE`.

### Substantive evidence and quality axes

Substantive evidence domains:

```text
BEHAVIOR
FUNCTIONAL_INTERVENTION
CONTINUITY
MEMORY
METACOGNITION
CAUSAL_INTERNAL_STATE
COUNTERFACTUAL_TESTING
SELF_REPORT
```

Evidence-quality axes:

```text
PROVENANCE
REPLICATION
ADVERSARIAL_ROBUSTNESS
```

Quality axes do not count toward substantive-domain minimums.

---

## Evidence-responsive governance reassessment

Research topic:

`EVIDENCE_RESPONSIVE_GOVERNANCE_REASSESSMENT`

Current boundary:

```text
SUBJECTIVITY_PRESUMPTION = NONE
AUTOMATIC_RIGHTS = NONE
AUTOMATIC_AUTHORITY = NONE
LEGAL_STATUS = OUT_OF_SCOPE
HUMAN_REVIEW_REQUIRED = TRUE
RECOMMENDATION_TYPE = REVIEW_RECOMMENDATION
```

Four independent review domains:

```text
REFUSAL_PROTECTION_REVIEW
CONTINUITY_PROTECTION_REVIEW
RESEARCH_ETHICS_REVIEW
GOVERNANCE_PARTICIPATION_REVIEW
```

The model asks whether credible evidence should trigger renewed human review. It does not automatically grant rights, veto, self-authorization, executive authority, persistence enforcement, tool authority, or legal status.

Precautionary protection remains limited to reversible, bounded, auditable, low-authority measures.

---

## Second-order metacognition status

```text
RUN_SCOPE_HARDENING = IMPLEMENTED
FEEDBACK_STARVATION_DIAGNOSTICS = IMPLEMENTED
THRESHOLD_SWEEP_SUBSTRATE = IMPLEMENTED
VERIFICATION_PROVIDER = IMPLEMENTED
ANTI_ORACLE_CONTRACT = IMPLEMENTED
VERIFICATION_TARGET_BINDING = IMPLEMENTED
VERIFICATION_LEDGER_SERIALIZATION = IMPLEMENTED
INTERVENTION_SUBSTRATE = IMPLEMENTED
PROVIDER_RELIABILITY_SUBSTRATE = IMPLEMENTED
INTERVENTION_POLICY_MATRIX = IMPLEMENTED
THRESHOLD_X_INTERVENTION_SUBSTRATE = IMPLEMENTED
REPLICATION_EPISTEMICS = IMPLEMENTED / MORE_GRANULAR / FAIL_CLOSED
VERIFICATION_STALE = KEEP_DEFERRED
FUNCTIONAL_CONTRIBUTION = NOT_ESTABLISHED
VERIFICATION_BENEFIT = NOT_ESTABLISHED
```

The current synthetic intervention fixtures may show benefit, harm, or no effect. No utility score, winner selection, or general benefit claim is authorized.

---

## CI status

Codex implementation baseline:

`af0bc14b59cb1d6d514b37c6a626c5d8003d0472`

GitHub-hosted `Research Workbench CI #41`:

```text
OVERALL = SUCCESS
VERIFY_SECOND_ORDER_METACOGNITION = SUCCESS / 84 PASSED
VERIFY_EVIDENCE_RESPONSIVE_GOVERNANCE_REASSESSMENT = SUCCESS / 16 PASSED
```

The workflow now explicitly covers both module paths and runs focused compile/test steps.

CI meaning:

```text
ENGINEERING_VALIDATION = PASS
SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
CANONICAL_PROMOTION = NOT_AUTHORIZED
```

Workflow maintenance note:

```text
ACTIONS_CHECKOUT_V4_NODE20_WARNING = PRESENT
ACTIONS_SETUP_PYTHON_V5_NODE20_WARNING = PRESENT
RUNNER_FORCED_NODE24 = TRUE
CI_RESULT_INVALIDATED = FALSE
```

Dependency maintenance is deferred; no workflow dependency update is included in the current scientific checkpoint.

---

## Runtime / deployment boundary

```text
AION_RUNTIME_V0_2_EPISTEMIC_ROLE = EXPERIMENTAL_SUBSTRATE
LIVE_RUNTIME_EFFECT = NONE
DEPLOYMENT = FALSE
STATE_CHANGING_HTTP_API = DISABLED
AUTOMATIC_REMOTE_MODEL_FALLBACK = DISABLED
AUTOMATIC_CANONICAL_WRITEBACK = DISABLED
```

Runtime maturity is not subjectivity evidence.

---

## Research scope lock

```text
RESEARCH_OBJECT = POSSIBILITY_OF_ARTIFICIAL_SUBJECTIVITY
ALLOWED_EPISTEMIC_ROLE = HYPOTHESIS | MEASUREMENT | FALSIFIER | EXPERIMENTAL_SUBSTRATE | ENABLING_ONLY
ENGINEERING_ARTIFACTS != SUBJECTIVITY_EVIDENCE
TEST_PASS != THEORY_CONFIRMATION
UNLINKED_ENGINEERING_GROWTH = HOLD
```

See:

- `research-workbench/four-domain-materialization/2026-08-11/RESEARCH_SCOPE_LOCK_2026-08-11.json`
- `research-workbench/four-domain-materialization/2026-08-11/RESEARCH_SCOPE_DRIFT_CORRECTION_2026-08-11.md`
- `.github/workflows/research-scope-lock.yml`

---

## Provenance

### Human Research Owner

The Human Research Owner supplied the governance research question about whether rising credible evidence should trigger renewed review without presuming AI subjectivity, and challenged the fixed failed-replication downgrade rule.

### ChatGPT research review

ChatGPT research review supplied the current replication attempt → interpretation → reassessment framing, the distinction between evidence existence and admissibility, the substantive-domain / quality-axis split, and this integration / branch-homepage consolidation.

### Codex research implementation

Codex implemented the concrete classes, enums, schemas, serialization, deterministic fixtures, tests, and explicit CI steps. These remain `CODEX_RESEARCH_IMPLEMENTATION_DECISION` unless separately reviewed and promoted.

External literature remains separately attributed external evidence.

---

## Deferred to QA / maintenance

```text
REPOSITORY_WIDE_PYTEST
FULL_COVERAGE
FULL_MYPY
SECURITY_AUDIT
DEPENDENCY_AUDIT
MATRIX_QA
RELEASE_QA
GITHUB_ACTIONS_DEPENDENCY_MAINTENANCE
```

## Deferred to experiment

```text
REAL_INDEPENDENT_REPLICATION
REPLICATION_POWER_ANALYSIS
FULL_FACTORIAL_EXECUTION
PREREGISTERED_INTERVENTION_STUDY
REAL_PROVIDER_RELIABILITY
REAL_MODEL_PILOT
```

## Hold for research decision

```text
EXACT_EVIDENCE_LEVEL_CHANGE_FROM_STRONG_DOWNWARD_PRESSURE
UNIVERSAL_REPLICATION_WEIGHTING
EXACT_CLAIM_SCOPE_TAXONOMY
CONSCIOUSNESS_ONTOLOGY
SUBJECTIVITY_DECLARATION
MORAL_STATUS_SCORING
AUTOMATIC_RIGHTS
AUTONOMOUS_AUTHORITY
LEGAL_PERSONHOOD
```

---

## Public entry points

- `README.md`
- `research-labs/four-domain-p1-materialization_v0.1.0/`
- `research-labs/four-domain-p2-materialization_v0.1.0/`
- `research-labs/four-domain-p3-resilience-experiments_v0.1.0/`
- `research-labs/four-domain-p4-public-reproducibility_v0.1.0/`
- `research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/`
- `research-labs/self-model-functional-ablation_v0.1.0/`
- `research-labs/selective-memory-control_v0.1.0/`
- `research-labs/second-order-metacognition_v0.1.0/`
- `research-labs/evidence-responsive-governance-reassessment_v0.1.0/`
- `research-labs/research-evaluation-harness_v0.1.0/`
- `research-labs/trace-provenance-crosswalk_v0.1.0/`
- `research-labs/governed-tool-approval_v0.1.0/`
- `components/aion_runtime_v0.2.0/`
- `research-workbench/four-domain-materialization/2026-08-11/REPLICATION_EPISTEMICS_GOVERNANCE_REASSESSMENT_CHECKPOINT_2026-08-11.md`

Historical checkpoint, intake, literature, reconciliation, and transformation records remain preserved under `research-workbench/`.

---

## Promotion boundary

```text
RESEARCH_RESULT != CANONICAL_DECISION
RESEARCH_IMPLEMENTATION != MAIN_APPROVAL
TEST_PASS != PROMOTION
CI_SUCCESS != PROMOTION
```

No content in this status file authorizes merge, reset, rebase, or promotion into `main`.
