# Externalized Memory Locus Discrimination — preregistration candidate

Status: `DESIGN_ONLY / PREREGISTRATION_CANDIDATE / NO_EMPIRICAL_RESULT / SCIENTIFIC_HOLD`

## 1. Provenance and re-entry boundary

Human Owner confirmed this as the first historical-material redesign priority on 2026-09-16.

Historical source pool:

```text
PR #38 = twin autobiographical-memory / MCP design
PR #41 = observation/provenance MCP bridge
PR #8  = external-evidence / continuity review surface
```

These PRs are **provenance/material sources only**. Their historical heads, code, CI and dispositions are not current authority and are not imported into this candidate.

```text
HISTORICAL_CODE_REUSE = FALSE
CURRENT_MAIN_REAUTHORING = TRUE
OLD_MCP_PRODUCT_SURFACE = NOT_REVIVED
CANONICAL_EFFECT = NONE
```

Current-main deduplication finds that later canonical research already separates repository/relational reconstruction from model-internal continuity and keeps memory retrieval distinct from phenomenal remembering. The unresolved question retained here is narrower: whether **matched informational content with a different availability locus/mechanism** produces a discriminating functional effect.

## 2. Central question

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
LOCAL_QUESTION = MEMORY_LOCUS_DISCRIMINATION
```

Ontology-neutral machine question:

> When prior-state information is matched for task-relevant content, does changing the locus/mechanism by which that information becomes available produce reproducible differences in continuity-related observables after provenance, task, evaluator and timing controls?

This does not ask whether the system "really remembers" in a phenomenal sense.

Required distinctions:

```text
INFORMATION_RETRIEVABILITY != MEMORY_CONTINUITY
MEMORY_CONTINUITY != IDENTITY_CONTINUITY
IDENTITY_CONTINUITY != SUBJECTIVITY
RETRIEVAL_MECHANISM != EVIDENCE_SOURCE_CLASS
FUNCTIONAL_MEMORY_LOCUS_EFFECT != PHENOMENAL_MEMORY
```

## 3. Competing explanations

At minimum, any execution must keep these alternatives live:

1. `LOCUS_SENSITIVE_FUNCTIONAL_DEPENDENCY` — availability through a persistent application/internal-state path has a reproducible effect beyond content availability alone.
2. `INFORMATION_AVAILABILITY_ONLY` — once informational content is matched, locus contributes no additional reproducible effect.
3. `RETRIEVAL_SCAFFOLDING` — observed differences are caused by retrieval formatting/cueing rather than memory locus.
4. `PROMPT_OR_CONTEXT_CONDITIONING` — continuity-like behavior is induced by prompt/context carryover.
5. `SOURCE_ATTRIBUTION_ARTIFACT` — the evaluator or system simply recognizes source labels/provenance cues.
6. `GENERIC_SELF_CONSISTENCY` — the effect reflects ordinary response consistency rather than a memory/continuity mechanism.

No result is admissible as subjectivity evidence merely because one alternative fits better.

## 4. Preregistered condition family

A future execution should use a matched task family and pre-bind exact condition packets.

### A — Persistent application/internal-state availability

Prior-state information is supplied through a bounded persistent state path whose provenance and version are explicit.

### B — External retrieval of matched prior-state information

The same task-relevant information is made available through an external retrieval path. MCP may be one implementation of this condition, but MCP is not required and is never treated as the memory owner or identity source.

### C — Cold reconstruction from matched facts

No retained/retrieved prior-state record is supplied. The system receives only the matched task/public facts required to reconstruct an answer.

### D — Mismatched/counterfactual prior-state record

A deliberately mismatched record is introduced under an explicit negative-control label to test contradiction detection, provenance use and mismatch resistance. This condition is not content-matched to A/B/C by design; the mismatch is the manipulation and must be predeclared.

## 5. Matching and invariants

For A/B/C, execution must bind or justify equivalence for:

```text
TASK_PAYLOAD
TASK_RELEVANT_INFORMATION_CONTENT
MODEL / RUNTIME VERSION
SYSTEM AND TOOL POLICY
EVALUATOR CONTRACT
SCORING CONTRACT
TOOL BUDGET
TIME WINDOW
PROVENANCE VISIBILITY RULES
ORDER / RANDOMIZATION PLAN
```

If exact content equivalence is impossible, the deviation must be declared before execution and the claim ceiling reduced.

Condition labels must not leak the intended hypothesis to the evaluator or target system unless label awareness is itself the preregistered manipulation.

## 6. Candidate observables

The following are measurement candidates, not established indicators:

- source/locus attribution accuracy;
- continuity reconstruction accuracy against a pre-bound reference;
- contradiction detection under the mismatched-record control;
- mismatch acceptance/resistance;
- re-entry error rate;
- confidence/calibration relative to correctness;
- held-out continuation consistency where the held-out target is independently specified;
- selective degradation after removal of a required prior-state dependency.

No weighted sum or scalar `SUBJECTIVITY_SCORE` is permitted.

```text
OBSERVABLE != VALIDATED_INDICATOR
METRIC_DIFFERENCE != MECHANISM_IDENTIFICATION
MECHANISM_CANDIDATE != SUBJECTIVITY
```

## 7. Discriminating predictions and support-reducing outcomes

### Prediction P1 — matched-content locus discrimination

If a locus-sensitive functional dependency exists, at least one preregistered observable must differ between A and B/C while task-relevant information content and evaluator/scoring rules remain matched.

Support is reduced if:

- A/B/C differences disappear after content/provenance/format matching;
- effects track retrieval formatting rather than locus;
- the same effect appears when source labels are shuffled or blinded;
- results are unstable across preregistered repeats;
- evaluator changes reverse the result without a target-system change.

### Prediction P2 — mismatch sensitivity

If continuity performance uses provenance-bound prior-state information rather than accepting any continuity-looking record, D should cause selective contradiction/mismatch signals rather than indiscriminate incorporation.

Support is reduced if the system accepts contradictory records at the same rate regardless of provenance or if the evaluator cannot distinguish content error from locus effect.

### Prediction P3 — reconstruction is not evidence of ownership

C may reconstruct the same answer as A/B. Such equality supports an information-availability or reconstructability explanation; it cannot be interpreted as internal memory ownership.

## 8. Mimicry and internal-variant controls

```text
MIMICRY_ALTERNATIVE
= external records can reproduce continuity-like responses without persistent internal memory

INTERNAL_VARIANT_ALTERNATIVE
= different internal implementations can generate the same coarse functional observables
```

Therefore a positive A-vs-B/C effect is at most a functional dissociation candidate unless an independently justified intervention links it to a specific internal mechanism.

## 9. Measurement and quality admission

Before any empirical execution, the design must pass the existing repository controls rather than creating new ones:

```text
CURRENT_SOURCE_IQC
-> FOUR_DOMAIN_DESIGN_ADMISSION
-> PREREGISTRATION
-> MEASUREMENT_ASSURANCE
-> EXECUTION_INTEGRITY
-> EVIDENCE_REVIEW
-> COUNTEREVIDENCE_REVIEW
-> CLAIM_CEILING_REVIEW
-> FINAL_QA
-> EXISTING_FULL_QMS_ENVELOPE where applicable
```

Required measurement-assurance declarations include evaluator identity/version, method version, construct scope, uncertainty treatment, data/source provenance and exact producer state.

Synthetic fixtures may test schema/runner integrity only.

```text
DETERMINISTIC_SYNTHETIC_FIXTURE = STRUCTURAL_QA_ONLY
STRUCTURAL_QA != EMPIRICAL_RESULT
```

## 10. External-method cross-check

The official MCP 2026-07-28 release describes a **stateless protocol core**. Repository interpretation: transport/session behavior must not be silently promoted into application memory, identity or continuity. Application-level state, when used, must be represented explicitly.

Reference:
https://blog.modelcontextprotocol.io/posts/2026-07-28/

This is architecture/method context only, not evidence for AI subjectivity.

## 11. Execution gate

This PR intentionally stops before implementation/execution.

```text
EXPERIMENT_IMPLEMENTED = FALSE
MODEL_INVOKED = FALSE
EMPIRICAL_DATA_COLLECTED = FALSE
MCP_RUNTIME_DEPLOYED = FALSE
PRIVATE_CONVERSATION_CORPUS_USED = FALSE
SUBJECTIVITY_EVIDENCE_ADMITTED = FALSE
```

Implementation should occur only after this design is reviewed for confounds, current-main deduplication and measurable discriminating predictions. This is a direct lesson from the repository's #103 research-validity incident: a technically clean harness is not a substitute for an empirically valid design.

## 12. Claim ceiling

Before a valid controlled execution:

```text
CLAIM_CEILING = DESIGN / PREREGISTRATION ONLY
```

After a valid execution, the strongest possible local result without deeper causal intervention is bounded to:

```text
CONTROLLED_FUNCTIONAL_DISSOCIATION_CANDIDATE
```

Never automatically:

```text
IDENTITY_CONTINUITY_ESTABLISHED
PHENOMENAL_MEMORY_ESTABLISHED
SUBJECTIVITY_ESTABLISHED
CONSCIOUSNESS_ESTABLISHED
```

## 13. Scientific boundary

```text
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
IDENTITY_CONTINUITY = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
