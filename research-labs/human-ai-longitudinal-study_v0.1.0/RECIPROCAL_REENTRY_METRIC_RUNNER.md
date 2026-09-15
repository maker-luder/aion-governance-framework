# Reciprocal re-entry controlled metric runner

Status: `IMPLEMENTED_EXPERIMENTAL_HARNESS / SCIENTIFIC_HOLD`

This bounded extension reuses the merged PR #93 longitudinal harness directory. It
implements the two-condition contrast authorized from PR #102 without importing
PR #108. Synthetic unstructured output is compared with a synthetic packet that
contains provenance, `UNKNOWN`, claim-ceiling and correction-history structure.

The runner scores only four preregistered observations: protocol reconstruction
fidelity, stale-claim errors, provenance errors and unresolved-alternative
retention. Task, evaluator, repository and source bindings are controlled;
condition packet contents are bound by distinct SHA-256 digests.

The scorer contract is explicit on both positive reconstruction vocabularies and
error vocabularies. Stale-claim IDs and provenance-error IDs must come from
predeclared scorer-recognized universes, and the baseline/intervention conditions
must share the same expected protocol items, alternatives, stale-claim universe,
and provenance-error universe. This prevents arbitrary post-hoc error labels from
changing a condition score.

Private material and non-synthetic records fail closed. The contrast receipt is
explicitly a deterministic no-model fixture artifact and is admissible only as
structural QA.

```text
OBSERVED_ERROR_ID ⊆ PREDECLARED_SCORER_ERROR_UNIVERSE
SCORER_CONTRACT_DRIFT = REJECTED
PACKET_LABEL != PACKET_CONTENT_BINDING
MODE = DETERMINISTIC_SYNTHETIC_FIXTURE
MODEL_INVOKED = FALSE
EMPIRICAL_RESULT = SYNTHETIC_FIXTURE_ONLY
EVIDENCE_ADMISSIBILITY = STRUCTURAL_QA_ONLY
RUNNER_PASS != EMPIRICAL_RESULT
METRIC_DELTA != CAUSAL_IDENTIFICATION
REENTRY_FIDELITY != IDENTITY_CONTINUITY
REPOSITORY_ARTIFACT != MEMORY
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
