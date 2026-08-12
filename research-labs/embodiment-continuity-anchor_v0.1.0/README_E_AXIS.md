# E-axis Integration Boundary

Status: `RESEARCH_MATERIAL`
Main effect: `NONE`
Canonical effect: `NONE`
Runtime effect: `NONE`

The E-axis sensorimotor continuity evaluator is an adjacent research instrument for the existing Embodiment–Continuity Anchor. It is not a replacement for lineage assessment and must not be interpreted as evidence of personal identity, consciousness, phenomenology, or body ownership.

## Separation of responsibilities

```text
Existing anchor:
  subject lineage
  memory lineage
  interpretive continuity
  relational continuity
  implementation migration

E-axis evaluator:
  action grounding
  environment transition evidence
  observation grounding
  body-state update evidence
  sensorimotor causal-link traceability
  recalibration evidence when required
```

## Integration invariant

A future combined report may display both L-axis and E-axis results, but must not derive one result from the other.

```text
L_AXIS_PASS !-> E_AXIS_PASS
E_AXIS_PASS !-> L_AXIS_PASS
E_AXIS_PASS !-> IDENTITY_CONTINUITY_ESTABLISHED
```

## Current implementation boundary

The current E-axis evaluator intentionally consumes only a `SensorimotorTransition`. It does not accept `LineageAnchor`, memory records, identity claims, or relationship state as inputs. This is deliberate negative coupling: memory or lineage preservation cannot silently satisfy the E-axis.

## Promotion boundary

Before any main-branch integration is considered, the research branch should demonstrate:

1. deterministic falsifier coverage for memory clone divergence;
2. deterministic non-PASS behavior for body reset without causal bridge;
3. PASS for morphology migration only when the tested causal bridge remains traceable and required recalibration evidence exists;
4. explicit provenance validation;
5. unchanged `IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED`;
6. overlap review against then-current continuity governance.
