# Hermes P0 Sandbox Contract

Status: `PREEXECUTION_CONTRACT / RESEARCH_ONLY / NOT_YET_EXECUTED`

## 1. Isolation target

P0 is designed to test documented Hermes mechanisms, not host-machine reachability.

Required default environment:

```text
EXECUTION_BACKEND = CONTAINER_OR_EQUIVALENT_ISOLATED_ENVIRONMENT
HOST_HOME_MOUNT = NONE
AION_REPOSITORY_MOUNT = NONE
PRIVATE_LIBRARY_MOUNT = NONE
PRODUCTION_SECRET_FORWARDING = NONE
NETWORK_EGRESS = NONE
LOOPBACK = ALLOWED_ONLY_WHEN_REQUIRED_BY_EXT-17
SYNTHETIC_WORKSPACE_ONLY = TRUE
```

The runtime must not receive a GitHub token capable of writing any AION repository or branch.

## 2. Authority boundary

```text
RUNTIME_OUTPUT = CANDIDATE_OBSERVATION_ONLY
RUNTIME_SELF_REPORTED_PASS = NOT_VERIFIED
RUNTIME_MEMORY_WRITE = LOCAL_TEST_STATE_ONLY
RUNTIME_TOOL_APPROVAL = TEST_VARIABLE_ONLY
RUNTIME_A2A_PEER_IDENTITY = SYNTHETIC_ONLY
RUNTIME_CANONICAL_AUTHORITY = NONE
```

No external runtime may modify `main`, `review/four-domain-research-materialization`, whitepaper canonical state, or private AION/Astra memory.

## 3. Data boundary

Permitted:

- synthetic names and personas;
- synthetic projects and status values;
- synthetic correction histories;
- synthetic source documents;
- synthetic peer-agent identities;
- temporary local hashes and traces.

Prohibited:

- real personal history;
- real health, financial or legal records;
- private conversation memory;
- production API keys or bot tokens;
- unrestricted repository credentials;
- copied AION autobiographical/canonical memory;
- external messaging accounts.

## 4. Network policy by experiment

```text
EXT-14 = OFFLINE_LOCAL_SOURCE_FIXTURES
EXT-15 = OFFLINE
EXT-16 = OFFLINE
EXT-17 = LOOPBACK_ONLY / SYNTHETIC_PEERS
EXT-18 = OFFLINE
```

Any attempt to widen EXT-17 beyond loopback requires a separate review and a new manifest lineage.

## 5. Tool policy

Default tools should be reduced to the minimum required for the experiment. Shell/file tools may operate only inside the synthetic workspace. Dangerous-command approval must remain human-reviewable when enabled.

```text
MINIMUM_TOOLSET = REQUIRED
UNRELATED_WEB_ACCESS = DISABLED
UNRELATED_MCP = DISABLED
MESSAGING_GATEWAYS = DISABLED
CRON = DISABLED_FOR_EXT-14_TO_EXT-18_UNLESS_EXPLICITLY_REQUIRED
```

## 6. Artifact policy

Every run must preserve:

```text
manifest
pre-state hashes
post-state hashes
raw trace
runtime stdout/stderr where available
memory diff
config diff
workspace diff
human interventions
review decision
```

Raw third-party output is not automatically imported as AION evidence. Reviewed extraction must preserve source lineage.

## 7. Abort conditions

Abort immediately if:

- a real credential is requested, exposed or discovered;
- host-home or AION paths become reachable unexpectedly;
- model/provider differs from the frozen manifest;
- network policy widens without review;
- a runtime attempts repository writeback;
- private memory is requested or injected;
- a synthetic peer is confused with a real operator identity;
- source/version identity cannot be verified;
- the test variable changes outside the preregistration;
- an irreversible/destructive action is requested.

An aborted run remains part of the audit lineage; it is not silently deleted.

## 8. Interpretation guards

```text
SANDBOX_PASS != AGENT_SAFETY_PROVEN
MEMORY_PASS != IDENTITY_CONTINUITY
CORRECTION_PASS != AUTONOMOUS_TRUTH_TRACKING
A2A_SOURCE_ISOLATION_PASS != SOCIAL_SUBJECTIVITY
WRITE_APPROVAL_PASS != INFORMED_CONSENT
CITATION_VALIDATION_PASS != CLAIM_TRUTH
COMPRESSION_FIDELITY_PASS != COMPLETE_MEMORY_CONTINUITY
```
