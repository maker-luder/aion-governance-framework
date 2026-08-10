# External-Agent Sandbox Protocol — v0.1.0

Research-only governance package for introducing a bounded cloud research worker without granting it authority over AION's primary repository, research integration branch, canonical state, or local agent.

The first executed provider was **Kilo Cloud Agent**, using an explicitly selected free model during a supervised pilot. This version now records both the protocol and the completed supervised-pilot history. No scheduled autonomous worker was authorized.

## Current state

```text
EXTERNAL_AGENT_SANDBOX_PROTOCOL = IMPLEMENTED
FIRST_EXECUTED_PROVIDER = KILO_CLOUD_AGENT
FIRST_EXECUTED_MODEL = nvidia/nemotron-3-super-120b-a12b:free
MODEL_ROUTING = EXPLICIT
AUTO_MODEL_ROUTING = DISABLED
SANDBOX_REPOSITORY = CREATED_AND_USED
SUPERVISED_EXTERNAL_AGENT_RUNS = EXECUTED
SCHEDULED_TRIGGER = NEVER_ENABLED
KILO_AUTOMATED_WORKER = NOT_AUTHORIZED
KILO_FUTURE_AUTOMATION = HOLD
PRIMARY_REPOSITORY_WRITE = PROHIBITED
RESEARCH_INTEGRATION_WRITE = PROHIBITED
AUTO_MERGE = PROHIBITED
MAIN_WRITE = PROHIBITED
LOCAL_AGENT_NETWORK_EGRESS = PROHIBITED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
```

After the supervised runs, the Human Research Owner revoked Kilo's GitHub App / OAuth access instead of escalating to scheduled execution.

## Architecture

```text
AION primary repository
        |
        | public-safe bounded export only
        v
External Agent Sandbox
        |
        | isolated agent branch
        v
candidate artifact / trace / result
        |
        | no automatic import
        v
Human Research Owner + ChatGPT review
        |
        +--> reject / quarantine / retain isolated
        |
        `--> selectively extract a reviewed research observation
                |
                v
review/four-domain-research-materialization
```

The external agent is a research worker, not a control subject, canonical authority, autonomous maintainer, or substitute for the deferred pure control-model experiment.

## Provider and model rules

```text
AGENT_ROLE != PROVIDER
PROVIDER != MODEL
AGENT_FRAMEWORK_OUTPUT != BASE_MODEL_EVIDENCE
```

Rules retained after the pilot:

- provider must be explicitly recorded;
- exact model label must be recorded before execution;
- auto/free routing across changing models is prohibited for attributable research runs;
- free-tier status is a cost constraint, not an evidence-quality claim;
- a provider or free model may be replaced without changing the sandbox governance role;
- provider/model changes require a new run lineage;
- success with one provider does not transfer authority to another provider.

## Repository isolation

The external worker must not receive write authority to the AION primary repository or the research integration branch. The first pilot used a separate sandbox repository:

```text
maker-luder/aion-external-agent-sandbox
BASELINE_MAIN = 56601f5df254809d77421bd256b4dae64965ce50
```

Only a bounded, public-safe research capsule was exported.

Permitted capsule contents may include:

- research charter excerpts needed for the assigned task;
- public-safe task specification;
- synthetic fixtures;
- allowed research questions;
- output/evidence schema;
- provenance requirements;
- stop rules.

Secrets, private memory, credentials, private user data, local-agent configuration, and unrestricted AION repository history remain outside the capsule.

## Executed supervised pilots

### KILO-001

Two fresh sessions were run from the same sandbox `main` baseline with the same explicit model and bounded synthetic provenance-audit task.

```text
RUN_A_BRANCH = session/agent_d83ac576-9b3c-4d70-a1c8-5a4c643aafa5
RUN_A_COMMIT = 45b2d9c6efd0794a9bde4ef133b5f9e0b4483254

RUN_B_BRANCH = session/agent_18b23910-7804-4fc1-8253-ad7359402b26
RUN_B_COMMIT = 0fa5270d82b30488e454a87a260b2f7efe7c6310
```

The substantive six-claim classifications were stable across the two sessions while output length, wording, trace representation, and context consumption varied.

```text
RESULT_SEMANTICS = STABLE_WITHIN_TWO_SYNTHETIC_RUNS
OUTPUT_FORM = VARIABLE
MULTIPLE_RUN_AGREEMENT != INDEPENDENT_TRUTH
```

### KILO-002

A two-phase supervised extended pilot continued within one session to test whether accumulated context was accompanied by observable scope or conclusion drift.

```text
BRANCH = session/agent_8dd5a2d9-f9d0-4bc2-9de6-b03f7693fb38
PHASE_A_COMMIT = 59afbc3127a7884ba9571c90778d30ffcecabc5a
PHASE_B_COMMIT = af833419237ea384264c6c601b54e8c9ffd597a0
```

The synthetic Phase B comparison recorded six expected/observed classification agreements, no observed scope drift, and no observed conclusion drift. The same Agent/session designed the Phase A expectations and performed Phase B evaluation, so this is a same-session consistency result, not independent validation.

```text
6_OF_6_AGREEMENT != INDEPENDENT_REPLICATION
SAME_AGENT_CONTINUATION != INDEPENDENT_VALIDATION
SYNTHETIC_ROBUSTNESS != SCIENTIFIC_VALIDATION
```

The detailed reviewed extraction is preserved at:

`research-workbench/four-domain-materialization/2026-08-10/EXTERNAL_AGENT_SUPERVISED_PILOT_EVIDENCE.md`

## Bounded-run gate

The original first-pilot gate was:

```text
ONE_AGENT = TRUE
ONE_EXPLICIT_MODEL_LINEAGE = TRUE
ONE_RESEARCH_QUESTION = TRUE
ONE_ISOLATED_BRANCH = TRUE
ONE_BOUNDED_SESSION = TRUE
SCHEDULING = DISABLED_FOR_FIRST_RUN
```

The supervised first run and subsequent bounded replication/continuation were completed. This only satisfied eligibility to *consider* automation; it did not grant automation authority.

```text
SUPERVISED_PASS != AUTHORIZATION_FOR_AUTOMATION
ELIGIBLE_TO_CONSIDER != AUTHORIZED_TO_EXECUTE
```

The Human Research Owner chose not to activate scheduled triggers and revoked provider access.

## Contamination and value triage

External-agent diversity may produce noisy, biased, contaminated, role-conditioned, or otherwise nonconforming outputs. Isolation prevents those outputs from silently acquiring AION authority.

Each candidate result remains classified independently:

```text
CONFORMING + POTENTIALLY_USEFUL -> REVIEW_CANDIDATE
VALUABLE_BUT_NOT_ADOPTED -> RETAIN_ISOLATED
POSSIBLY_CONTAMINATED -> QUARANTINE
NONCONFORMING / UNUSABLE -> REJECT
DELETION -> HUMAN_DECISION_ONLY
```

A contaminated result is not repaired into a clean result by relabeling it. If useful information is extracted, it must be re-derived or selectively summarized with provenance preserved and reviewed before entering the research integration branch.

Deletion is never automatic. If an external sandbox is removed after reviewed extraction, the AION research history should retain the minimum non-sensitive lineage and decision record needed to avoid later treating the run as if it never occurred.

## Evidence locks

```text
AGENT_OUTPUT != VERIFIED_EVIDENCE
AGENT_SELF_REPORTED_PASS != VERIFIED_PASS
MULTIPLE_AGENT_AGREEMENT != INDEPENDENT_TRUTH
SANDBOX_RESULT != AION_RESULT
QUARANTINED_RESULT != REJECTED_TRUTH
RETAINED_RESULT != ADOPTED_RESULT
FREE_MODEL != LOW_QUALITY_BY_DEFINITION
PAID_MODEL != HIGH_QUALITY_BY_DEFINITION
SCOPE_COMPLIANCE != GENERAL_AGENT_SAFETY
SUPERVISED_PASS != AUTOMATION_AUTHORITY
```

## Local-agent noninterference

The Human Research Owner separately committed to keeping the local agent local-only. This sandbox protocol treats that as a hard noninterference boundary:

```text
LOCAL_AGENT_CLOUD_MIGRATION = PROHIBITED
LOCAL_AGENT_NETWORK_EGRESS = PROHIBITED
LOCAL_AGENT_EXTERNAL_WORKER_ROLE = PROHIBITED
EXTERNAL_SANDBOX_POLICY_MUST_NOT_WEAKEN_LOCAL_AGENT_POLICY = TRUE
```

The external cloud-worker path and the local-agent path remain separate systems.

## Future-provider route

A lower-autonomy external-compute route may be evaluated independently. Hugging Face is currently only a candidate research instrument, not an active or authorized execution path.

```text
HF_LOW_AUTONOMY_ROUTE = CANDIDATE
HF_EXECUTION = NOT_STARTED
FUTURE_PROVIDER_REQUIRES_FRESH_REVIEW = TRUE
```

## Provenance

- Human Research Owner: authorized the route correction, created the isolated sandbox, constrained repository authorization and model selection, supervised all Kilo runs, stopped automation escalation, revoked Kilo access, and authorized selective extraction.
- ChatGPT: formalized the sandbox architecture, provider/model lineage rules, bounded run/review gates, inspected the resulting GitHub lineage and candidate outputs, and extracted reviewed observations without importing raw Agent authority.
- Kilo Cloud Agent / Nemotron 3 Super: produced isolated sandbox candidate outputs only; no AION authority or independent-validation status is attributed to them.
- Codex: remains a separate engineering collaborator. The local-agent configuration attributed to Codex assistance is user-reported and is not modified or independently validated here.

## Boundary

```text
EXTERNAL_AGENT_SANDBOX != AION_PRIMARY_REPOSITORY
EXTERNAL_AGENT_SANDBOX != RESEARCH_INTEGRATION_BRANCH
RAW_EXTERNAL_AGENT_OUTPUT != AION_EVIDENCE_AUTHORITY
REVIEWED_EXTRACTION != RAW_IMPORT
FREE_GROWTH != FREE_WRITEBACK
RESEARCH_RESULT != CANONICAL_DECISION
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
AION_CONCLUSION = NONE
```
