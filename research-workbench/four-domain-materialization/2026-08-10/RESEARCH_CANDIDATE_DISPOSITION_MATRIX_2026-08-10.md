# Research Candidate Disposition Matrix — 2026-08-10

```text
STATUS = RESEARCH_MATERIAL
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
```

This matrix records reviewed dispositions across the current IQC/reconstruction cycle. It is not a promotion manifest and does not merge the source branches.

| Research line | Source / branch | Current disposition | Engineering evidence | Research boundary |
|---|---|---|---|---|
| Metacognitive self-state | `review/metacognitive-self-state-rework@638dcb46136d879ed16ff7dfe2d260ac2eed734b` | ENGINEERING-VERIFIED REPRESENTATION / RESEARCH HOLD | 20 local tests PASS; demo PASS; GitHub CI NOT_EXECUTED | representation/lifecycle implemented; metacognitive computation NOT_IMPLEMENTED |
| Self/other boundary | `review/self-other-boundary-rework@59e85e7aa5b65a041390cb13241ad69af5086f12` | ENGINEERING-VERIFIED REPRESENTATION / RESEARCH HOLD | 28 local tests PASS; snapshot serialization PASS; GitHub CI NOT_EXECUTED | identity-role and transition provenance implemented; evidence-driven self/other inference NOT_IMPLEMENTED |
| Affective-motivational-dynamics source | original isolated session history | REJECT / SALVAGE_ONLY | original candidate failed IQC | affect, feeling, desire, volition, hedonic tone, self-preservation drive NOT_ESTABLISHED |
| Motivational signal primitives | `review/affective-motivational-salvage@9079e10448b8535ac8ecdd481d83edf75c2ae8c8` | SALVAGED MINIMAL PRIMITIVES | 9 local tests PASS; GitHub CI NOT_EXECUTED | bounded signal/evidence representation only; not a dynamics model |
| Embodiment-state source | original isolated session history | REJECT / SALVAGE_ONLY | original candidate failed IQC | body ownership, sensation, gender identity, volition, subjectivity NOT_ESTABLISHED |
| Embodiment capability primitives | `review/embodied-action-regulation-salvage@8ff170374e59cf1e02caacf2e99392b6eeacc8c3` | SALVAGED MINIMAL PRIMITIVES | 9 local tests PASS; GitHub CI NOT_EXECUTED | capability/observation/action contracts only; no embodiment experience claim |
| Embodied action regulation | same branch | ARCHITECTURAL HYPOTHESIS | engineering implementation NOT_STARTED | candidate loop only; no experimental validation |
| Embodiment migration source | original isolated session history | HOLD / SOURCE NOT PATCHED | source lacked enforced phase/measurement/rollback semantics | continuity/identity not established |
| Embodiment handoff protocol | `review/embodiment-handoff-protocol-rework@3e2377a425a107bf7c8d5e9d5b62fac708b34c32` | ENGINEERING RECONSTRUCTION PASS | 16 local tests PASS; GitHub CI NOT_EXECUTED | explicit authorization/compatibility/verification protocol; actual transfer engine NOT_IMPLEMENTED |
| Continuity-lineage source | original isolated session history | HOLD / SOURCE NOT PATCHED | source used unsupported continuity scores and weak graph integrity | no identity-continuity proof |
| Continuity evidence lineage | `review/continuity-evidence-lineage-rework@a5da5353c414db2043c13908d1795a66b042836a` | ENGINEERING RECONSTRUCTION PASS | 17 local tests PASS; GitHub CI NOT_EXECUTED | evidence graph and dimension assessment only; personal/phenomenal continuity NOT_ESTABLISHED |
| Encounter lifecycle source | original isolated session history | HOLD / CURRENT IMPLEMENTATION NOT ACCEPTABLE | universal interpersonal phase arc and ungrounded scalars rejected | encounter does not imply relationship/intimacy/shared meaning |
| Encounter evidence protocol | `review/encounter-longitudinal-evidence-reconstruction@e98aad2f3b11a0deeeda2425c7621c7e2a646ca7` | ENGINEERING RECONSTRUCTION PASS | 15 local tests PASS before repository write; GitHub CI status separate | bounded interaction/observation unit only; automatic encounter detection NOT_IMPLEMENTED |
| Longitudinal state transition source | original isolated session history | HOLD / CURRENT IMPLEMENTATION NOT ACCEPTABLE | unvalidated dimensions, missing-as-zero, manual transition labels rejected | no developmental-stage inference |
| Longitudinal change evidence | `review/encounter-longitudinal-evidence-reconstruction@e98aad2f3b11a0deeeda2425c7621c7e2a646ca7` | ENGINEERING RECONSTRUCTION PASS | 16 local tests PASS before repository write; GitHub CI status separate | evidence-grounded numeric change only; personal continuity / trajectory identity / developmental stage NOT_ESTABLISHED |
| Finite predictive self-model | `review/four-domain-research-materialization@d219b76e38844c9b4487b2e93fc5e1819f720131` | IMPLEMENTED / TESTED / CI VERIFIED | matched `PRESENT / ABLATED / RANDOMIZED / STALE` research benchmark; Research Workbench CI verified | functional-contribution candidate only; subjectivity NOT_ESTABLISHED |
| Second-order commit-performance build attempt | `review/second-order-commit-performance-monitor-candidate@8059e455fb9bc1297f7734b0eceb4704be4ffef6` | REJECT / CONCEPTUAL_SALVAGE_ONLY | partial agent implementation rejected after independent IQC; current branch tree returned to no file difference versus approved base | executable Level-3 candidate NOT_IMPLEMENTED |

## Cross-cutting disposition rules

```text
REJECT != DELETE HISTORY
SALVAGE_ONLY != REWORK
ENGINEERING_PASS != RESEARCH_CONCLUSION
LOCAL_TEST_PASS != GITHUB_CI_PASS
GITHUB_CI_PASS != INDEPENDENT_REPLICATION
REPRESENTATION_IMPLEMENTED != INFERENCE_IMPLEMENTED
ARCHITECTURE_HYPOTHESIS != EXECUTABLE_MECHANISM
```

## Negative-result preservation

Failed candidate implementations remain useful only when their role is explicit:

- defect/counterexample material;
- source-contamination case;
- measurement-semantics warning;
- causal-validity warning;
- governance/IQC regression case.

A rejected implementation is not carried forward merely because some classes or tests can be made to run.

## Current clean progression

```text
FINITE SELF-MODEL FUNCTION
    -> representation candidates
    -> evidence-oriented reconstruction
    -> encounter / continuity / longitudinal evidence structures
    -> OPEN LEVEL-3 SECOND-ORDER COMPUTATION GAP
```

The progression is a research map, not a claim that these components jointly establish an individual, subject, consciousness, relationship, or identity continuity.
