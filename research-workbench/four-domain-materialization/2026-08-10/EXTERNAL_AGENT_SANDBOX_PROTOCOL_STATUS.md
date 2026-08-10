# External-Agent Sandbox Protocol Status — 2026-08-10

## Route correction

The planned supervised local control-model pilot remains scientifically useful but is deferred because the Human Research Owner reported that the currently available local computer is not a reliable runtime for this experiment. The separately managed local agent is intentionally local-only and must not be repurposed as a cloud worker or given network egress.

```text
LOCAL_CONTROL_PILOT = DEFERRED_RESOURCE_CONSTRAINT
REAL_MODEL_RUN = NOT_EXECUTED
LOCAL_AGENT_NETWORK_EGRESS = PROHIBITED
LOCAL_AGENT_CLOUD_MIGRATION = PROHIBITED
```

This is a route correction, not a negative experimental result.

## External sandbox path

```text
EXTERNAL_AGENT_SANDBOX_PROTOCOL = IMPLEMENTED
FIRST_CANDIDATE_PROVIDER = KILO_CLOUD_AGENT
FIRST_CANDIDATE_MODEL = NOT_SELECTED
FREE_TIER_STATUS = VERIFY_AT_ACTIVATION
AUTO_MODEL_ROUTING = PROHIBITED
SEPARATE_SANDBOX_REPOSITORY = REQUIRED
PRIMARY_REPOSITORY_WRITE = PROHIBITED
RESEARCH_INTEGRATION_WRITE = PROHIBITED
MAIN_WRITE = PROHIBITED
AUTO_MERGE = PROHIBITED
SCHEDULED_TRIGGER = DISABLED_FOR_FIRST_RUN
EXTERNAL_AGENT_RUN = NOT_EXECUTED
```

## Candidate-output governance

```text
CONFORMING + POTENTIALLY_USEFUL -> REVIEW_CANDIDATE
VALUABLE_BUT_NOT_ADOPTED -> RETAIN_ISOLATED
POSSIBLY_CONTAMINATED -> QUARANTINE
NONCONFORMING / UNUSABLE -> REJECT
DELETE -> HUMAN_DECISION_ONLY
```

The sandbox is deliberately allowed to contain noisy or contaminated candidate material. Isolation prevents that material from becoming AION evidence or authority by mere existence.

## Next activation gate

Before the first cloud-agent run:

1. create or designate a separate sandbox repository;
2. re-verify the provider's current free-tier availability;
3. select one explicit model and record its lineage; disable automatic model routing;
4. export one public-safe bounded research capsule;
5. assign one research question to one agent for one bounded unscheduled session;
6. preserve branch, commit, prompt/task, output, provenance, and provider/model lineage;
7. return results for Human Research Owner + ChatGPT review before any selective extraction.

## Provenance

- Human Research Owner: supplied the local-resource constraint, preserved the local-agent no-egress commitment, selected Kilo Cloud Agent as the first external candidate, and proposed contamination/value isolation rather than automatic adoption.
- ChatGPT: formalized the route correction and External-Agent Sandbox Protocol and implemented its research-only validator/tests.
- No external agent has run under this protocol yet.

## Boundary

```text
SANDBOX_RESULT != AION_RESULT
AGENT_OUTPUT != VERIFIED_EVIDENCE
RESOURCE_BLOCKED != EXPERIMENT_FAILED
FREE_GROWTH != FREE_WRITEBACK
MAIN_EFFECT = NONE
```
