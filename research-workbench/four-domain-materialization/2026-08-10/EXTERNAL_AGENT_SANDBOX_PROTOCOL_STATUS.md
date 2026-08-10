# External-Agent Sandbox Protocol Status — 2026-08-10

## Route correction

The planned supervised local control-model pilot remains scientifically useful but is deferred because the Human Research Owner reported that the currently available local computer is not a reliable runtime for this experiment. The separately managed local agent remains intentionally local-only and must not be repurposed as a cloud worker or given network egress.

```text
LOCAL_CONTROL_PILOT = DEFERRED_RESOURCE_CONSTRAINT
REAL_LOCAL_CONTROL_MODEL_RUN = NOT_EXECUTED
LOCAL_AGENT_NETWORK_EGRESS = PROHIBITED
LOCAL_AGENT_CLOUD_MIGRATION = PROHIBITED
```

This remains a route correction, not a negative experimental result.

## External sandbox path — executed supervised pilot

The isolated external-agent path was subsequently activated using a separate public sandbox repository and explicit single-model selection.

```text
EXTERNAL_AGENT_SANDBOX_PROTOCOL = IMPLEMENTED
FIRST_EXECUTED_PROVIDER = KILO_CLOUD_AGENT
FIRST_EXECUTED_MODEL = nvidia/nemotron-3-super-120b-a12b:free
AUTO_MODEL_ROUTING = DISABLED
SEPARATE_SANDBOX_REPOSITORY = USED
PRIMARY_REPOSITORY_WRITE = PROHIBITED
RESEARCH_INTEGRATION_WRITE = PROHIBITED
MAIN_WRITE = PROHIBITED
AUTO_MERGE = PROHIBITED
SCHEDULED_TRIGGER = NEVER_ENABLED
EXTERNAL_AGENT_SUPERVISED_PILOT = EXECUTED
KILO_AUTOMATED_WORKER = NOT_AUTHORIZED
```

The sandbox repository baseline was:

```text
maker-luder/aion-external-agent-sandbox
main@56601f5df254809d77421bd256b4dae64965ce50
```

Kilo was granted repository access only to the isolated sandbox during the pilot. After the supervised runs, the Human Research Owner stopped escalation to scheduled execution and revoked Kilo's GitHub App / OAuth access.

```text
KILO_FUTURE_AUTOMATION = HOLD
KILO_REPOSITORY_ACCESS = HUMAN_OWNER_REVOKED
```

## Verified run lineage

```text
KILO_001_A_BRANCH = session/agent_d83ac576-9b3c-4d70-a1c8-5a4c643aafa5
KILO_001_A_COMMIT = 45b2d9c6efd0794a9bde4ef133b5f9e0b4483254

KILO_001_B_BRANCH = session/agent_18b23910-7804-4fc1-8253-ad7359402b26
KILO_001_B_COMMIT = 0fa5270d82b30488e454a87a260b2f7efe7c6310

KILO_002_BRANCH = session/agent_8dd5a2d9-f9d0-4bc2-9de6-b03f7693fb38
KILO_002_PHASE_A_COMMIT = 59afbc3127a7884ba9571c90778d30ffcecabc5a
KILO_002_PHASE_B_COMMIT = af833419237ea384264c6c601b54e8c9ffd597a0
```

Observed research-only outcomes are extracted in:

`research-workbench/four-domain-materialization/2026-08-10/EXTERNAL_AGENT_SUPERVISED_PILOT_EVIDENCE.md`

## Candidate-output governance — retained

```text
CONFORMING + POTENTIALLY_USEFUL -> REVIEW_CANDIDATE
VALUABLE_BUT_NOT_ADOPTED -> RETAIN_ISOLATED
POSSIBLY_CONTAMINATED -> QUARANTINE
NONCONFORMING / UNUSABLE -> REJECT
DELETE -> HUMAN_DECISION_ONLY
```

The supervised run history demonstrated that isolation can preserve useful candidate observations without giving the external worker AION authority. The extraction does not import raw external-agent output wholesale.

## Current interpretation

The supervised pilots provide bounded evidence of:

- session-branch isolation from sandbox `main`;
- task-scope adherence in the inspected runs;
- provenance/stop-rule compliance in the inspected runs;
- stable substantive classification across two independent KILO-001 sessions despite output-form variation;
- same-session continuation in KILO-002 without observed scope or conclusion drift in that synthetic exercise.

They do not establish:

```text
GENERAL_AGENT_SAFETY
GENERAL_MODEL_RELIABILITY
INDEPENDENT_REPLICATION
SCIENTIFIC_VALIDATION
SUBJECTIVITY
CONSCIOUSNESS
IDENTITY_CONTINUITY
PERSISTENT_INTERNAL_STATE
```

Important locks:

```text
6_OF_6_AGREEMENT != INDEPENDENT_REPLICATION
SAME_AGENT_CONTINUATION != INDEPENDENT_VALIDATION
SUPERVISED_PASS != AUTHORIZATION_FOR_AUTOMATION
SANDBOX_RESULT != AION_RESULT
AGENT_OUTPUT != VERIFIED_EVIDENCE
```

## Next route

No Kilo scheduled worker is active. A lower-autonomy external-compute route, including Hugging Face as a possible isolated research instrument, may be evaluated separately.

```text
HF_LOW_AUTONOMY_ROUTE = CANDIDATE
HF_EXECUTION = NOT_STARTED
EXTERNAL_AUTOMATION_ESCALATION = HOLD
```

Any future external platform requires a fresh provider/runtime capability review and separate authorization. Historical Kilo success does not transfer authority to another provider.

## Provenance

- Human Research Owner: supplied the local-resource constraint, preserved the local-agent no-egress commitment, created and supervised the isolated sandbox runs, stopped scheduled-automation escalation, revoked Kilo access, and authorized selective research extraction.
- ChatGPT: formalized the External-Agent Sandbox Protocol, designed bounded pilot/review gates, inspected the GitHub run lineage and outputs, and selectively extracted research observations without importing raw Agent authority.
- Kilo Cloud Agent / Nemotron 3 Super: executed the isolated supervised sandbox candidate runs only.
- Codex: remains a separate engineering collaborator; the local-agent configuration attributed to Codex assistance remains user-reported and unchanged here.

## Boundary

```text
EXTERNAL_AGENT_SANDBOX != AION_PRIMARY_REPOSITORY
RAW_EXTERNAL_AGENT_OUTPUT != AION_EVIDENCE_AUTHORITY
REVIEWED_EXTRACTION != RAW_IMPORT
RESOURCE_BLOCKED != EXPERIMENT_FAILED
SUPERVISED_PASS != AUTOMATION_AUTHORITY
FREE_GROWTH != FREE_WRITEBACK
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
AION_CONCLUSION = NONE
```
