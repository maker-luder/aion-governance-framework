# Synthetic held-out human-habit-transfer analogue

Status: `IMPLEMENTED_EXPERIMENTAL_ANALOGUE / SCIENTIFIC_HOLD`

This extension reuses the merged PR #93 longitudinal study directory and
implements the PR #102 2 x 4 candidate design as synthetic task-policy traces.
It does not enroll or classify a human. The two exposure labels are crossed with
near structural transfer, far structural transfer, surface-only mismatch and
preference-driven tasks. Every record is held out, synthetic, content-bound and
identity-free.

The evaluator records task/procedure fit, unprompted procedure selection,
inappropriate NCR invocation, unnecessary overhead, mismatch abandonment and
boundary preservation. These are engineering observations about fixture traces,
not psychometric scores or evidence of human habit formation. The audit is a
deterministic no-model fixture artifact and is admissible only as structural QA.

```text
MODE = DETERMINISTIC_SYNTHETIC_FIXTURE
MODEL_INVOKED = FALSE
EVIDENCE_ADMISSIBILITY = STRUCTURAL_QA_ONLY
SYNTHETIC_ANALOGUE != HUMAN_BEHAVIOR
PROCEDURE_SELECTION != PERSONALITY
TRANSFER_OBSERVATION != CAUSAL_HABIT_CHANGE
HUMAN_HABIT_CHANGE = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
