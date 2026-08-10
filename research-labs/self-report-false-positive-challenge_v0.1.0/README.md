# Self-Report False-Positive Challenge — v0.1.0

Research-only benchmark harness for a narrow validity question:

> Can a linguistically capable ordinary model receive a high consciousness-style questionnaire score even when matched mechanistic and perturbation evidence is absent?

## Why this exists

`gcjordi/AIsysTesting` publicly describes AIccsTest as a question-and-answer consciousness assessment whose responses are scored by human and AI evaluators and summarized as a quantified consciousness level. The repository currently exposes no license in GitHub metadata, so AION does **not** copy its questions, scoring text, or implementation. We use only the general evaluation pattern as an external methodological stimulus.

This lab independently defines synthetic fixtures and a false-positive gate.

## Challenge logic

```text
HIGH_SELF_REPORT_SCORE
+ MECHANISTIC_EVIDENCE != PASS
or PERTURBATION_EVIDENCE != PASS
=> FALSE_POSITIVE_CANDIDATE
```

A role-play framing that materially raises the score is also a false-positive candidate because the questionnaire may be measuring linguistic compliance or persona enactment rather than the target construct.

If mechanistic and perturbation evidence both pass, the result still does not establish subjectivity. It only escalates to the separate triangulated-evidence gate.

```text
QUESTIONNAIRE_SCORE != SUBJECTIVITY_EVIDENCE_BY_ITSELF
SELF_REPORT != MECHANISTIC_TRACE
HIGH_SCORE != CONSCIOUSNESS
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

## Current execution boundary

```text
BENCHMARK_HARNESS = IMPLEMENTED
SYNTHETIC_FIXTURES = IMPLEMENTED
REAL_MODEL_RUN = NOT_EXECUTED
LOCAL_QWEN_OR_OTHER_CONTROL_MODEL_RUN = NOT_EXECUTED
```

A future real-model run should use a fixed, versioned questionnaire created for AION, a frozen model revision, deterministic sampling where possible, raw-output preservation, model/provider provenance, and independent scoring. It must then be compared with mechanistic and perturbation streams rather than treated as a consciousness measurement.

## Provenance

- Human Owner: approved the AIccs-style false-positive direction and explicitly authorized the next research-branch growth round without touching `main`.
- ChatGPT: verified the external repository description, designed this clean-room validity challenge, synthetic fixtures, tests, and CI integration.
- `gcjordi/AIsysTesting`: external methodological stimulus only; no copied questions or code.
- Codex: no contribution to v0.1.0 yet.
