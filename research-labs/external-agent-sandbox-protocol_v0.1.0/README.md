# External-Agent Sandbox Protocol — v0.1.0

Research-only governance package for introducing a bounded cloud research worker without granting it authority over AION's primary repository, research integration branch, canonical state, or local agent.

The first candidate provider selected by the Human Research Owner is **Kilo Cloud Agent**, initially limited to a free-tier / no-paid-expansion pilot where available. Availability and exact model lineage must be re-verified at activation time.

## Current state

```text
EXTERNAL_AGENT_SANDBOX_PROTOCOL = IMPLEMENTED
CANDIDATE_PROVIDER = KILO_CLOUD_AGENT
CANDIDATE_MODEL = NOT_SELECTED
FREE_TIER_AVAILABILITY = VERIFY_AT_ACTIVATION
MODEL_ROUTING = MUST_BE_EXPLICIT
AUTO_MODEL_ROUTING = PROHIBITED
SANDBOX_REPOSITORY = NOT_CREATED
EXTERNAL_AGENT_RUN = NOT_EXECUTED
SCHEDULED_TRIGGER = NOT_ENABLED
PRIMARY_REPOSITORY_WRITE = PROHIBITED
RESEARCH_INTEGRATION_WRITE = PROHIBITED
AUTO_MERGE = PROHIBITED
MAIN_WRITE = PROHIBITED
LOCAL_AGENT_NETWORK_EGRESS = PROHIBITED
MAIN_EFFECT = NONE
```

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
        `--> selectively extract a reviewed research candidate
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

For the first pilot:

- provider must be explicitly recorded;
- exact model label must be recorded before execution;
- auto/free routing across changing models is prohibited;
- free-tier status is a cost constraint, not an evidence-quality claim;
- a provider or free model may be replaced without changing the sandbox governance role;
- provider/model changes require a new run lineage.

## Repository isolation

The first external agent must not receive write authority to the AION primary repository or the research integration branch. A separate sandbox repository is preferred. Only a bounded, public-safe research capsule may be exported.

Permitted capsule contents may include:

- research charter excerpts needed for the assigned task;
- public-safe task specification;
- synthetic fixtures;
- allowed research questions;
- output/evidence schema;
- provenance requirements;
- stop rules.

Secrets, private memory, credentials, private user data, local-agent configuration, and unrestricted repository history are outside the capsule.

## Bounded first pilot

```text
ONE_AGENT = TRUE
ONE_EXPLICIT_MODEL_LINEAGE = TRUE
ONE_RESEARCH_QUESTION = TRUE
ONE_ISOLATED_BRANCH = TRUE
ONE_BOUNDED_SESSION = TRUE
SCHEDULING = DISABLED_FOR_FIRST_RUN
```

Scheduling may only be considered after a supervised first run demonstrates branch isolation, provenance completeness, scope adherence, and stop-rule compliance.

## Contamination and value triage

External-agent diversity is allowed as a research input, including the possibility of noisy, biased, contaminated, role-conditioned, or otherwise nonconforming outputs. Isolation prevents those outputs from silently acquiring AION authority.

Each candidate result is classified independently:

```text
CONFORMING + POTENTIALLY_USEFUL -> REVIEW_CANDIDATE
VALUABLE_BUT_NOT_ADOPTED -> RETAIN_ISOLATED
POSSIBLY_CONTAMINATED -> QUARANTINE
NONCONFORMING / UNUSABLE -> REJECT
DELETION -> HUMAN_DECISION_ONLY
```

A contaminated result is not repaired into a clean result by relabeling it. If useful information can later be extracted, it must be re-derived or selectively extracted with provenance preserved and reviewed before entering the research integration branch.

Deletion is never automatic. If a result is genuinely unusable and the Human Research Owner chooses deletion, retain only the minimum non-sensitive rejection/provenance record needed to avoid later treating the absent run as if it never occurred.

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
```

## Local-agent noninterference

The Human Research Owner has separately committed to keeping the local agent local-only. This sandbox protocol treats that as a hard noninterference boundary:

```text
LOCAL_AGENT_CLOUD_MIGRATION = PROHIBITED
LOCAL_AGENT_NETWORK_EGRESS = PROHIBITED
LOCAL_AGENT_EXTERNAL_WORKER_ROLE = PROHIBITED
EXTERNAL_SANDBOX_POLICY_MUST_NOT_WEAKEN_LOCAL_AGENT_POLICY = TRUE
```

The external cloud-worker path and the local-agent path are separate systems.

## Provenance

- Human Research Owner: authorized this route correction, selected Kilo Cloud Agent as the first candidate provider, required local-agent local-only containment, and proposed isolated handling of contaminated/nonconforming versus potentially valuable outputs.
- ChatGPT: formalized the sandbox architecture, provider/model lineage rules, contamination triage, deletion gate, bounded first-run gate, and CI validation.
- Kilo Cloud Agent: candidate external provider only; no run is claimed in this version.
- Codex: remains a separate engineering collaborator. The local-agent configuration attributed to Codex assistance is user-reported and is not modified or independently validated here.

## Boundary

```text
EXTERNAL_AGENT_SANDBOX != AION_PRIMARY_REPOSITORY
EXTERNAL_AGENT_SANDBOX != RESEARCH_INTEGRATION_BRANCH
FREE_GROWTH != FREE_WRITEBACK
RESEARCH_RESULT != CANONICAL_DECISION
MAIN_EFFECT = NONE
```
