# Sensorimotor Continuity Synthetic Fixtures

Status: `RESEARCH_MATERIAL`
Main effect: `NONE`
Canonical effect: `NONE`
Runtime effect: `NONE`

These fixtures are synthetic negative and positive controls for the E-axis sensorimotor continuity evaluator. They are intentionally independent from memory-lineage and identity-lineage fixtures.

## Fixture E0 — Closed causal transition

```text
body-state:0
  -> action:move-forward
  -> env:0 -> env:1
  -> obs:1
  -> body-state:1
```

Expected: `PASS`

Reason: the transition contains a traceable action/environment/observation/body-state update chain with provenance.

## Fixture E1 — Memory clone divergence

Context A and Context B may begin from equivalent recalled memory content, but each receives an independent embodied transition:

```text
A: env:0 -> action:A -> env:A1 -> obs:A1 -> body:A1
B: env:0 -> action:B -> env:B1 -> obs:B1 -> body:B1
```

Expected: assess A and B independently.

Non-claim:

```text
SAME_MEMORY != SAME_EMBODIED_TRAJECTORY
```

## Fixture E2 — Body reset without causal bridge

```text
memory preserved
lineage preserved
body state reset
sensor/actuator state reset
no traceable transition bridge
```

Expected: not `PASS`.

The current minimal evaluator represents this as `NOT_ASSESSED` when neither environment transition nor body-state update is evidenced.

## Fixture E3 — Morphology migration with recalibration

```text
sensor-layout:v1 -> sensor-layout:v2
action-channel:v1 -> action-channel:v2
recalibration evidence present
closed causal transition remains traceable
```

Expected: `PASS`

Non-claim:

```text
MORPHOLOGY_CHANGE != AUTOMATIC_DISCONTINUITY
```

## Fixture E4 — Morphology migration without recalibration evidence

```text
sensor-layout:v1 -> sensor-layout:v2
action-channel:v1 -> action-channel:v2
recalibration required
recalibration evidence missing
```

Expected: `HOLD`

## Governance invariant

All fixture outcomes preserve:

```text
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
BODY_OWNERSHIP = NOT_ESTABLISHED
PHENOMENOLOGY = NOT_ESTABLISHED
```

These fixtures test only whether the selected E-axis causal transition is sufficiently evidenced for its bounded research status.