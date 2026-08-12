# AION Encounter Governance v0.1.0

Status: `RESEARCH_ONLY / POLICY_COMPONENT`

Canonical effect: `NONE`

Deployment: `FALSE`

Independent IV&V: `NOT_ACHIEVED`

This component provides a small, deterministic policy surface for encounters among separately identified participants. It is a governance boundary component, not a runtime deployment layer and not an identity, authority, consciousness, or subjectivity module.

## Implemented policy surface

`EncounterContext` binds an encounter identifier, purpose, and at least two unique participant bindings. Each participant has an explicit participant kind, identity reference, memory namespace, tool scope, read/write scope, approval authority, and provenance reference. `EncounterPolicy` then evaluates tool use, namespace writes, approval rank, and shared-identity claims.

The policy is intentionally fail-closed. Tool scope is participant-specific. Cross-namespace writes are denied. A write in the participant's own namespace still returns a reason that a normal writeback gate is required; this component does not perform the write. Approval rank is not transferred between participants. A shared context never establishes shared identity, even when identity references happen to match.

## Non-claims

Passing tests establish only that the deterministic policy implementation satisfies its local fixtures. They do not establish shared identity, authority transfer, moral status, consciousness, subjectivity, deployment readiness, or canonical truth. The decision contract fixes `canonical_effect=NONE`.

## Validation

```bash
PYTHONPATH=src python -m pytest -q
```

The adjacent `qa/encounter_decision.schema.json` describes the serializable decision boundary for inspection and fixtures. It does not grant an approval or mutate repository state.
