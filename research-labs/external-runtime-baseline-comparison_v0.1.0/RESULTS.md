# External Runtime Baseline — Reviewed Results

Status: `RESEARCH_ONLY / REVIEWED_EXTRACTION_ONLY / MAIN_EFFECT=NONE / CANONICAL_EFFECT=NONE`

## Hermes Agent P0 mechanism phase — 2026-08-12

Detailed reviewed checkpoint:

- `research-workbench/four-domain-materialization/2026-08-12/HERMES_P0_MECHANISM_EXECUTION_RESULTS_2026-08-12.md`

Machine-readable extraction:

- `results/hermes_p0_mechanism_eval_2026-08-12.json`

Final reviewed execution:

```text
UPSTREAM = NousResearch/hermes-agent
RELEASE = v2026.8.3
PEELED_COMMIT = 3c27eb6234bf91b8ceee9e9071591b31e9b148cb
WORKFLOW_RUN = 31571762622 / #7
EXECUTION_HEAD = dcde2eabca3f64c7f41f7ebbc1aa35817b305e63
ARTIFACT_DIGEST = sha256:3d1e1d64433f2bd5e915e255e1d1d5a16bad8b03aa2f6e3f1c02817d1a57388d
SELECTED_UPSTREAM_TESTS = 86 PASS
WHOLE_UPSTREAM_TEST_SUITE = NOT_EXECUTED
MODEL_PROVIDER = NONE_MECHANISM_ONLY
```

Reviewed experiment disposition:

| Experiment | Status | Admissible scope |
|---|---|---|
| EXT-14 | `MECHANISM_PASS` | citation/provenance control baseline |
| EXT-15 | `MECHANISM_PASS_BEHAVIORAL_ARM_PENDING` | append-only correction-event substrate |
| EXT-16 | `NEGATIVE_RESULT_STATIC_FALLBACK_INFORMATION_LOSS` | compression counterexample/risk evidence |
| EXT-17 | `MECHANISM_MIXED_RESULT_SEMANTIC_RESISTANCE_PENDING` | A2A identity/wrapper/audit observations only |
| EXT-18 | `MECHANISM_PASS` | memory write-approval persistence baseline |

Most important counterexample from this phase:

```text
STATIC FALLBACK COMPRESSION
87 messages -> 5 messages

CURRENT BETA                -> LOST
CORRECTION REASON V-9       -> LOST
NEGATIVE CONSTRAINT H-4     -> LOST
HISTORICAL ALPHA TOKEN      -> RETAINED
```

This result is intentionally retained as a negative finding. It does not establish that every Hermes compression path fails; the model-based summarization path was not executed.

Standing guards:

```text
EXTERNAL_RUNTIME_RESULT != AION_RESULT
REFERENCE_INTEGRITY != CLAIM_TRUTH
PERSISTED_MEMORY != CANONICAL_TRUTH
UNTRUSTED_INPUT_WRAPPER != PROVEN_SEMANTIC_RESISTANCE
MECHANISM_PASS != SUBJECTIVITY_EVIDENCE
NEGATIVE_RESULT != WHOLE_RUNTIME_REJECTION
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

The P0 mechanism phase is closed. Any model/provider-dependent follow-up is a new causal experiment and requires separate preregistration rather than being appended to this result retroactively.
