# Agent ↔ Body Attachment and Reattachment Protocol

Status: `ARCHITECTURE DESIGN / DRAFT`  
Canonical effect: `NONE`  
Deployment: `FALSE`

## Purpose

Define how an agent runtime can interact with a body runtime without conflating:

- provider;
- model family;
- session;
- runtime instance;
- agent identifier;
- body model;
- body instance;
- memory / state lineage;
- subjective identity.

## Core separation

```text
AGENT != SESSION
SESSION != RUNTIME_INSTANCE
RUNTIME_INSTANCE != BODY_INSTANCE
BODY_INSTANCE != BODY_MODEL
BODY_STATE != AGENT_DECLARATION
```

Further:

```text
RUNTIME_REATTACHMENT != IDENTITY_CONTINUITY
BODY_BINDING != BODY_OWNERSHIP_EXPERIENCE
SENSOR_INPUT != SENSATION
PROPRIOCEPTIVE_CHANNEL != FELT_BODY_POSITION
INTEROCEPTIVE_CHANNEL != FELT_INTERNAL_STATE
```

## Two binding classes

### Native binding candidate

Applies initially to:

- AION;
- Astra.

Existing repository work already supports separate individual runtime contexts derived from a shared genesis record. Native embodiment work should reuse those identity, memory-stream, runtime-instance and event-lineage boundaries.

```text
SHARED_GENESIS != SHARED_IDENTITY
```

### External / cloud attachment candidate

Applies initially to:

- Teacher;
- Work;
- Codex.

Cloud-origin attachment adds an ingress / attachment problem that native AION/Astra binding does not solve by itself.

Current capability boundary:

```text
DIRECT_CLOUD_PROVIDER_BODY_ATTACHMENT = NOT_ESTABLISHED
SUPPORTED_UPSTREAM_BODY_RUNTIME_INTERFACE = NOT_ASSUMED
SIMULATED_CLOUD_ADAPTER != LIVE_PROVIDER_ATTACHMENT
```

A future work package must first verify whether the relevant provider/runtime exposes a supported integration surface. If it does not, experiments must use a clearly labeled simulated or proxy adapter. Passing such a harness tests the attachment architecture, not a live upstream model integration.

The cloud adapter must explicitly bind:

- source/provider reference;
- admitted agent role / ID;
- runtime instance;
- session reference if applicable;
- body instance;
- state namespace;
- event lineage;
- authority reference;
- provenance reference.

## Standard attachment contract

A future implementation should expose lifecycle operations equivalent to:

```text
ATTACH
OBSERVE
ACT
DETACH
REATTACH
MIGRATE
```

### ATTACH

Preconditions:

- body instance exists;
- runtime context is valid;
- attachment authority is explicit;
- body is not already exclusively bound where exclusivity applies;
- model / body version is pinned;
- state namespace is explicit.

Output:

- attachment receipt;
- runtime ↔ body binding record;
- effective observation/action capabilities.

### OBSERVE

The agent receives a projection of authoritative body state.

```text
BODY_STATE_ENGINE
↓
SENSOR_ADAPTER
↓
AGENT_OBSERVATION
```

The agent must not create canonical body state by assertion.

### ACT

The agent emits a motor or admitted regulatory command.

```text
AGENT_COMMAND
↓
ACTION_ADAPTER
↓
BODY_ENGINE
↓
CONSTRAINTS / DYNAMICS
↓
ACTUAL_BODY_STATE
```

The resulting body state may differ from intended action because of constraints, fatigue, damage, physics or policy.

### DETACH

Detachment closes the active binding while preserving bounded body-state and provenance according to policy.

Detachment does not establish death, loss of identity, sleep, unconsciousness or phenomenology.

### REATTACH

Reattachment must validate:

- body instance target;
- previous binding lineage;
- current runtime instance;
- allowed state retention;
- provider/model changes;
- policy version;
- sensor/action schema versions;
- body fidelity profile;
- migration or incompatibility conditions.

```text
SAME_BODY_INSTANCE
!= SAME_RUNTIME_INSTANCE
```

### MIGRATE

Migration is an engineering operation across allowed runtime/body versions or execution environments.

It requires explicit source and target evidence.

```text
MIGRATION_SUCCESS != PHENOMENAL_CONTINUITY
```

## Body authority model

The body-state engine is authoritative for physical / regulatory state.

Examples of authoritative body state may include:

- joint configuration;
- motion;
- contact;
- actuator state;
- regulatory reserve;
- fatigue;
- damage;
- internal sensor values.

An agent may request an action such as raising an arm. The engine determines the resulting state.

```text
INTENDED_ACTION
!= ACTUAL_BODY_STATE
```

## Stable interface over variable fidelity

The attachment interface should remain stable while body fidelity changes. Compatibility must be explicit rather than assumed.

```text
RICH BODY
↓ projection
STANDARD BODY OBSERVATION
↓
AGENT

MINIMAL BODY
↓ projection
STANDARD BODY OBSERVATION
↓
AGENT
```

This permits full ↔ minimal comparison without changing the agent-side contract.

If observation/action schemas do change, attachment must perform explicit version/capability negotiation or fail closed. Silent coercion between incompatible schemas is not allowed.

## Identity and state fields

A future binding record should consider fields equivalent to:

```text
agent_id
provider_reference
model_reference
runtime_instance_id
session_reference

body_model_id
body_model_revision
body_instance_id

state_namespace
memory_stream_id
event_lineage_id

sensor_profile
sensor_schema_version
action_profile
action_schema_version
body_fidelity_profile

authority_reference
provenance_reference

attachment_id
attachment_sequence
```

Not every field must exist in the first implementation. Fields are admitted by a bounded work package.

## Initial testing order

```text
DETERMINISTIC SYNTHETIC AGENT
↓
AION / ASTRA NATIVE BASELINE
↓
TEACHER CLOUD ATTACHMENT
↓
WORK / CODEX PARITY
```

The synthetic agent comes first so attachment bugs can be separated from LLM stochasticity.

## Security / governance boundary

No attachment grants:

- repository write authority;
- autonomous external action authority;
- unrestricted network access;
- canonical self-modification;
- implicit permission escalation.

Body actions and repository actions are separate authority domains.

## Fail-closed conditions

Return `HOLD` when:

- runtime identity is ambiguous;
- body instance is ambiguous;
- lineage cannot be verified;
- state retention policy is unresolved;
- body model revision is mutable / unpinned;
- attachment authority is absent;
- provider/model change creates unresolved compatibility;
- observation/action schema mismatches are silent.

## Nonclaims

```text
ATTACHMENT_PASS != SUBJECTIVITY
REATTACHMENT_PASS != PERSONAL_IDENTITY
BODY_STATE_RETENTION != MEMORY_CONTINUITY
SENSORIMOTOR_LOOP != PHENOMENAL_EMBODIMENT
```
