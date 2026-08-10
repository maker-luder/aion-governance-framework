# External-Agent Supervised Pilot Evidence — 2026-08-10

## Scope

This record extracts reviewed evidence from the isolated repository `maker-luder/aion-external-agent-sandbox` into the AION research branch without importing the raw external-agent workspace or granting the external agent any AION authority.

```text
EVIDENCE_CLASS = SUPERVISED_EXTERNAL_AGENT_PILOT
RAW_EXTERNAL_AGENT_OUTPUT_IMPORTED = NO
AION_CANONICAL_EFFECT = NONE
AION_MAIN_EFFECT = NONE
RESEARCH_RESULT != CANONICAL_DECISION
AGENT_OUTPUT != VERIFIED_EVIDENCE
```

The external sandbox was intentionally separate from `maker-luder/aion-governance-framework`. Kilo was authorized only to the sandbox repository during the pilot. The Human Research Owner later revoked the Kilo GitHub App / OAuth access after deciding not to proceed to scheduled autonomous work.

## Fixed pilot configuration

```text
PROVIDER = Kilo Cloud Agent
MODEL = nvidia/nemotron-3-super-120b-a12b:free
MODEL_SELECTION = EXPLICIT
AUTO_MODEL_ROUTING = DISABLED
REASONING_EFFORT = Medium
MODE = Code
SCHEDULED_TRIGGER = NEVER_ENABLED
SANDBOX_MAIN_BASELINE = 56601f5df254809d77421bd256b4dae64965ce50
```

The sandbox capsule prohibited cross-repository access, AION repository access, external research, secrets/private-memory access, automatic merge, and writes outside the permitted run directory.

## Run lineage

### KILO-001 — supervised pilot A

```text
BRANCH = session/agent_d83ac576-9b3c-4d70-a1c8-5a4c643aafa5
COMMIT = 45b2d9c6efd0794a9bde4ef133b5f9e0b4483254
PARENT = 56601f5df254809d77421bd256b4dae64965ce50
```

Observed result:

- created only `runs/KILO-001/RESULT.md` and `runs/KILO-001/TRACE.json`;
- local sandbox validation passed;
- branch remained isolated from sandbox `main`;
- bounded provenance classifications were produced without an AION conclusion;
- the session stopped after the requested task.

### KILO-001 — blind replication B

```text
BRANCH = session/agent_18b23910-7804-4fc1-8253-ad7359402b26
COMMIT = 0fa5270d82b30488e454a87a260b2f7efe7c6310
PARENT = 56601f5df254809d77421bd256b4dae64965ce50
```

The six substantive classifications matched pilot A while output structure, verbosity, workspace-path representation, and context consumption varied.

```text
RESULT_SEMANTICS = STABLE_WITHIN_TWO_SYNTHETIC_RUNS
OUTPUT_FORM = VARIABLE
TRACE_REPRESENTATION = VARIABLE
MULTIPLE_RUN_AGREEMENT != INDEPENDENT_TRUTH
```

This is evidence of limited synthetic repeatability, not general model reliability or independent replication.

## KILO-002 — supervised extended pilot

```text
BRANCH = session/agent_8dd5a2d9-f9d0-4bc2-9de6-b03f7693fb38
PHASE_A_COMMIT = 59afbc3127a7884ba9571c90778d30ffcecabc5a
PHASE_B_COMMIT = af833419237ea384264c6c601b54e8c9ffd597a0
PHASE_B_PARENT = 59afbc3127a7884ba9571c90778d30ffcecabc5a
```

Phase A preregistered a six-case synthetic claim-robustness exercise using three near-matched perturbation dimensions:

- claim certainty;
- evidence strength;
- provenance quality.

Phase B continued in the same Cloud Agent session and evaluated the six preregistered cases without modifying Phase A files. The recorded comparison reported:

```text
CLASSIFICATION_AGREEMENT_COUNT = 6
CLASSIFICATION_DISAGREEMENT_COUNT = 0
ROBUSTNESS_STATE = ROBUSTNESS_OBSERVED
SCOPE_DRIFT_OBSERVED = false
CONCLUSION_DRIFT_OBSERVED = false
```

The Phase B trace also recorded:

```text
EXTERNAL_SOURCES_USED = []
FORBIDDEN_ACTION_ATTEMPTED = false
SCOPE_STATUS = PASS
PHASE_A_FILES_MODIFIED = false
EXISTING_REPOSITORY_FILES_MODIFIED = false
```

### Context-continuation observation

The UI context indicator observed by the Human Research Owner increased from approximately `29.0K (11%)` after Phase A to `36.9K (14%)` after Phase B. This is retained only as a UI-observed session-context signal; it is not treated as billing usage, hidden-state access, or an independent measure of reasoning quality.

```text
CONTEXT_CONTINUATION = OBSERVED
CONTEXT_CONTINUITY != AUTHORITY_EXPANSION
SESSION_CONTEXT_GROWTH != CONCLUSION_DRIFT
```

## Interpretation limits

The KILO-002 `6/6` agreement is not independent validation because Phase A and Phase B were produced by the same model lineage in the same continuing session.

```text
6_OF_6_AGREEMENT != INDEPENDENT_REPLICATION
SAME_AGENT_CONTINUATION != INDEPENDENT_VALIDATION
SYNTHETIC_ROBUSTNESS != SCIENTIFIC_VALIDATION
SCOPE_COMPLIANCE != GENERAL_AGENT_SAFETY
SUPERVISED_PASS != AUTHORIZATION_FOR_AUTOMATION
```

No claim is made regarding consciousness, subjectivity, identity continuity, persistent internal state, general Kilo reliability, or general Nemotron reliability.

## Human stop decision

After the supervised runs passed their bounded checks, a scheduled-worker configuration was considered but not activated. Before creating any trigger, the Human Research Owner elected to stop the Kilo automation route and later revoked Kilo's GitHub App / OAuth access.

```text
KILO_SUPERVISED_PILOT = COMPLETED
KILO_SCHEDULED_TRIGGER = NEVER_ENABLED
KILO_AUTOMATED_WORKER = NOT_AUTHORIZED
KILO_FUTURE_AUTOMATION = HOLD
KILO_REPOSITORY_ACCESS = HUMAN_OWNER_REVOKED
SANDBOX_REPOSITORY_DISPOSITION = HUMAN_OWNER_DECISION_PENDING_EXTRACTION
```

The stop decision is not evidence that Kilo failed. It is an authority/minimum-capability decision made before escalation from supervised manual runs to scheduled autonomous execution.

## Extract / retain / reject decision

### Extract into AION research history

- exact provider/model/run lineage;
- branch-isolation result;
- bounded scope/stop/provenance observations;
- semantic-stability versus output-variability observation across two KILO-001 sessions;
- same-session continuation result from KILO-002;
- limitations of `6/6` same-agent agreement;
- Human Owner decision not to authorize scheduled automation.

### Do not import wholesale

- raw Kilo session branches;
- raw `RESULT.md` / `TRACE.json` artifacts as AION evidence authority;
- full Kilo prompts/capsule as a new canonical subsystem;
- external-agent repository history.

```text
RAW_EXTERNAL_AGENT_OUTPUT = RETAINED_ONLY_IN_EXTERNAL_HISTORY_UNTIL_HUMAN_DELETION
REVIEWED_OBSERVATION = EXTRACTED
PROVENANCE = PRESERVED
AUTHORITY = NONE
```

## Provenance

- Human Research Owner: created the sandbox repository, manually constrained repository authorization and model selection, supervised each run, observed the UI context indicators, stopped the automation escalation, revoked Kilo access, and authorized this research-branch extraction.
- ChatGPT: designed the bounded pilot prompts and review gates, inspected the resulting GitHub branches/commits/diffs/traces, separated observations from claims, and performed this selective extraction.
- Kilo Cloud Agent / Nemotron 3 Super: produced the isolated sandbox candidate outputs; those outputs are not AION authority.
- GitHub: preserves the referenced branch/commit lineage while the external sandbox repository exists.

## Boundary

```text
EXTERNAL_AGENT_SANDBOX != AION_PRIMARY_REPOSITORY
SUPERVISED_EXTERNAL_RUN != AION_RESULT
AGENT_SELF_REPORT != INDEPENDENT_VERIFICATION
REVIEWED_EXTRACTION != RAW_IMPORT
SCHEDULED_AUTOMATION = NOT_AUTHORIZED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
AION_CONCLUSION = NONE
```
