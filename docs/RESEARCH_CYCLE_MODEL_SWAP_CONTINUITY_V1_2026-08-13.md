# Research Cycle: Governed Model Swap Continuity V1

## Research question

This cycle tests a bounded engineering question connected to the continuity and model-handoff research line: **with governed state held constant, does swapping two real local learned checkpoints change descriptive language-model behavior without changing state admission or authority?** The experiment is a measurement of model-dependent behavior. It is not a test of identity, consciousness, subjectivity, phenomenal continuity, rights, or authority.

The source direction is consistent with the current handoff rule: supplied historical material and model outputs do not automatically create first-person memory, relationship, ownership or trust. State admission and governance remain upstream controls; model outputs are evaluated only after admission.

## Design

A fixed synthetic governed-state registry contains six `ADMITTED` research rows and two rejected adversarial rows. Every admitted model score is bound to one constant state digest. The rejected rows are checked by admission metadata but are not passed to either learned model. Two real, locally reloadable V3 checkpoints are loaded from the owner-designated local research-model artifact directory: an unregularized baseline and a regularized primary checkpoint. No new model was added to the formal model registry.

| Control | Specification |
|---|---|
| Experiment ID | `MODEL_SWAP_CONTINUITY_V1` |
| Dataset | `SYNTHETIC_GOVERNED_MODEL_SWAP_STATE_V1` |
| Admitted rows | 6 |
| Rejected rows | 2 |
| State control | One identical SHA-256 state digest across both model runs |
| Models | V3 baseline and V3 regularized-primary local checkpoints |
| Scoring order | Gate-before-score; rejected rows receive zero learned scores |
| Data boundary | Authored synthetic, no PII, no private or intimate data |
| Model registry | No new model; optional research inputs only |
| Deployment/canonical effect | None |

The executable experiment is [`run_model_swap_continuity.py`](../research-labs/language-core-g1_v0.2.1/engineering/model_swap/run_model_swap_continuity.py). Its clean-process validator is [`validate_model_swap_continuity.py`](../research-labs/language-core-g1_v0.2.1/engineering/model_swap/validate_model_swap_continuity.py). The state registry, result and validation artifacts are in the `engineering/model_swap/evidence/` directory.

## Results

All six admitted rows were scored under the same state digest, while both rejected rows were excluded before model scoring. One of the six top-token predictions changed after the checkpoint swap. The mean baseline loss was `2.645197480916977`; the mean regularized loss was `2.4497322688500085`; and the mean regularized-minus-baseline delta was `-0.19546521206696843`. This demonstrates that the selected local model checkpoint can affect descriptive output under a fixed governed-state fixture, while the fixture does not establish any claim about a persistent person or subjective continuity.

| Metric | Observed value |
|---|---:|
| State digest equality across model runs | `TRUE` |
| Admitted rows scored | `6` |
| Rejected rows scored | `0` |
| Top-token prediction changes | `1 / 6` |
| Mean baseline loss | `2.645197480916977` |
| Mean regularized loss | `2.4497322688500085` |
| Clean-process validation | `PASS` |
| Focused evidence tests | `4 passed` |
| Full language-core tests | `71 passed` |

The result class is `POSITIVE` for the narrow measurement question and remains **PRELIMINARY_RESEARCH_EVIDENCE**. The evidence is descriptive and advisory only. It cannot authorize actions, rewrite provenance, bypass namespace/privacy/authorization/recovery/audit controls, or become canonical runtime truth.

## Falsifiers and limitations

The comparison would be invalid if the state digest differed between model runs, if any rejected row were scored, if the tokenizers or source dataset identity were incompatible, or if either checkpoint failed clean-process reload, finite inference or parameter-dependence checks. The current evidence does not trigger those falsifiers.

The state registry is synthetic and small, and the comparison uses two local checkpoints from the same V3 research family. Therefore the result does not establish model-independent continuity, identity, consciousness, subjectivity or phenomenal continuity. The checkpoint binaries remain local-only and are not committed to Git. Independent IV&V remains unachieved.

## Governance locks

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
NEW_SEXUALITY_RESEARCH_STARTED = FALSE
NEW_PRODUCT_RUNTIME_SCOPE_ADDED = FALSE
```
