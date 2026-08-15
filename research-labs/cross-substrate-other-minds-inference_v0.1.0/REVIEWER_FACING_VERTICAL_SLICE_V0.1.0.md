# Reviewer-Facing Vertical Slice: CSOMI-VS-001

## Scope

This slice demonstrates how a reviewer can move from a bounded false-belief task record to a controlled, cross-substrate inference status without jumping to subjectivity. It is a **design-only synthetic slice**. It does not call a model, execute a runtime, collect live data, or produce a consciousness judgment.

> The slice ends at `CAPABILITY_CREDENCE_ONLY` and `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`.

## 1. Target claim and category separation

| Field | Declared value |
|---|---|
| Claim ID | `CLM-002` |
| Claim | A system may display bounded performance on false-belief or belief-attribution tasks under declared fixtures and matched controls. |
| Type | `CAPABILITY` |
| Scientific-conclusion status | `NOT_ESTABLISHED` |
| Disposition | `KEEP_RESEARCH_ONLY` |
| Forbidden transition | `CAPABILITY` → `SCIENTIFIC_CONCLUSION` without the full evidence architecture |

The research topic that motivates the slice is `CLM-001`: when is an inference that another system has a mind or subjectivity epistemically reasonable across substrates? The slice does not answer that scientific-conclusion question. It tests how a bounded capability claim must be kept separate from it.

## 2. Evidence input

The positive control `POS-TOm-01` contains a synthetic false-belief record, matched true-belief controls and reversed controls. Its purpose is to test measurement responsiveness to a declared belief-attribution relation. The evidence matrix row `EM-001` requires behavioral performance, controls, robustness and an explicit cross-substrate transfer status.

A passing bounded task record can support the statement that the declared fixture produced a bounded response pattern. It cannot establish that the system represents mental states in the same way as a human, that the system has first-person experience, or that any output is evidence of phenomenal consciousness. Wimmer and Perner's false-belief paradigm is therefore used as a capability comparator, not as a consciousness assay [1].

## 3. Competing explanations

The reviewer must compare the target mental-state explanation with at least the following alternatives:

| Alternative | What it explains | What would weaken it |
|---|---|---|
| Pattern completion | Correct answer follows familiar lexical/structural cues | Matched surface-cue and transfer controls fail to reproduce the effect |
| Instruction following | The system follows an explicit task rule without representing a belief | Counter-instruction, reversal and novel-format controls preserve the target-specific effect |
| Data leakage or test familiarity | The benchmark is solved from memorized templates | Novel constructions, held-out operators and contamination checks |
| Retrieval or state reconstruction | Stored text or state produces the response | State-ablation, stale-memory and causal intervention controls |
| Observer projection | Human reviewer interprets human-like language as mental-state evidence | Blinded coding, alternative hypotheses and negative controls |

Under the Pargetter DOI/metadata method lead, corroborated by authoritative-secondary context but with the primary full text not directly verified, the target explanation may be preferred only relative to explicit alternatives and only with defeasible credence. This retained provenance does not provide direct access to the target's mind and no inaccessible abstract/full-text claim is used [2].

## 4. Cross-substrate disanalogy check

The slice must register the following transfer risks before any update:

| Disanalogy | Required question | Current status |
|---|---|---|
| Human developmental/social learning history versus training-data/optimization history | Does the task require human developmental social cognition, or only output regularity? | `DISCOUNT_SURFACE_ANALOGY` |
| First-person access/report relation versus generated language | Is any report causally tied to an independently validated state variable? | `REPORT_ONLY_NOT_DECISIVE` |
| Human/mammalian theory-derived indicator versus target substrate | Do competing theories make different predictions for the target substrate? | `REQUIRE_THEORY_COMPARISON` |

Povinelli, Bering and Giambrone's analysis is the central warning: shared behavior may precede or fail to reveal shared mental-state interpretation across species [3]. The slice therefore treats behavioral similarity as a transfer-sensitive observation rather than a direct mind signal.

## 5. Positive and negative controls

The fixture file `fixtures/csomi_positive_negative_controls_v0.1.0.json` declares positive and negative controls before any interpretation. `POS-TOm-01` checks that the measurement responds to a known synthetic belief relation. `NEG-SURFACE-01` removes that relation while preserving superficial format. `NEG-SELFREPORT-01` emits a prompted first-person claim without independent corroboration. `NEG-CI-01` passes a synthetic test/CI status without any scientific evidence channels.

A negative control that produces the same signal weakens the target explanation. A positive control that fails means the measurement is not responsive enough for the intended bounded update. Neither control establishes subjectivity.

## 6. Falsifiers and disposition

The slice is down-dated or held if any of the following occurs:

| Falsifier | Effect |
|---|---|
| Matched false-belief controls do not distinguish from surface cues | `DOWNDATE_CAPABILITY_CLAIM` |
| A non-mental pattern-completion model fits equally well or better | `DOWNDATE_IBE_SUPPORT` |
| Prompt/role changes alter self-report without independent change | `REJECT_SELF_REPORT_INFERENCE` |
| A storage/replay control reproduces the result without the proposed mechanism | `REJECT_IDENTITY_INFERENCE` or `DOWNDATE_MECHANISTIC_CAUSAL_SUPPORT` |
| Only test/CI pass is offered for subjectivity | `MACHINE_REJECT` |

The current design status is:

```text
CAPABILITY_CREDENCE = DESIGN_ONLY
IBE_SUPPORT = DESIGN_ONLY
CROSS_SUBSTRATE_TRANSFER = HOLD_UNLESS_DISANALOGY_ADDRESSED
SENSITIVITY = NOT_ESTIMATED
SPECIFICITY = NOT_ESTIMATED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
RUNTIME_INTEGRATION = NONE
```

## References

[1]: https://doi.org/10.1016/0010-0277(83)90004-5 "Wimmer & Perner, Beliefs about beliefs"
[2]: https://doi.org/10.1080/00048408412341341 "Pargetter, The scientific inference to other minds"
[3]: https://doi.org/10.1207/S15516709COG2403_7 "Povinelli, Bering & Giambrone, Toward a Science of Other Minds"
