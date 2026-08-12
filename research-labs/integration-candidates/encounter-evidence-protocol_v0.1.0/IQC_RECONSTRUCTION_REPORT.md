# IQC-07 RECONSTRUCTION REPORT — encounter evidence protocol

## DISPOSITION

- SOURCE_CANDIDATE: `encounter-lifecycle_v0.1.0`
- SOURCE_IQC: `HOLD / CURRENT_IMPLEMENTATION_NOT_ACCEPTABLE`
- RECONSTRUCTION_BRANCH: `review/encounter-longitudinal-evidence-reconstruction`
- SOURCE_BRANCH_FOR_PRIOR_REWORK: `review/continuity-evidence-lineage-rework`
- ORIGINAL_NEMOTRON_SOURCE: preserved on isolated session history
- ORIGINAL_PACKAGE_ON_THIS_BRANCH: removed
- NEW_CANDIDATE: `encounter-evidence-protocol_v0.1.0`
- MAIN_BRANCH_WRITE: NONE
- FOUR_DOMAIN_RESEARCH_BRANCH_WRITE: NONE
- CANONICAL_EFFECT: NONE
- RUNTIME_EFFECT: NONE

## CHANGE BOUNDARY

`main` and `review/four-domain-research-materialization` are read-only comparison sources.
They are not merge targets and are not modified by this reconstruction.

The only write target is `review/encounter-longitudinal-evidence-reconstruction`.

## WHY THE SOURCE CANDIDATE WAS NOT PATCHED

The source candidate treated a human-style progression
`PRE_ENCOUNTER -> INITIATION -> ENGAGEMENT -> DEEPENING -> CLIMAX -> RESOLUTION -> POST_ENCOUNTER`
as a generic encounter lifecycle without enforcing the phase machine.

It also used manually supplied agency, familiarity, trust, power, progress, depth and intensity values without measurement contracts, lacked a stable `encounter_id`, admitted free-text mechanism/relationship escape hatches, and used the recurring mutable-manager scaffold with false reinitialization roots, sentinel restore provenance, wall-clock timestamps and non-causal ablation.

The reconstruction keeps only the bounded encounter/evidence problem.

## READ-ONLY CROSS-CHECK

### Main branch

Existing repository governance already models explicit participant bindings, namespace/scope controls and approval boundaries. This candidate does not replace those authority services and does not infer authority from a participant role or relationship representation.

### Four-domain research branch

The research branch is used only to compare evidence/provenance and continuity assumptions. No research-only identity, memory or encounter semantics are promoted into this candidate.

### Whitepaper/governance semantics

The project distinguishes event records, testimony, memory encodings and recall outputs and requires source/ownership distinctions. Encounter evidence therefore carries evidence and provenance references instead of free-text claims about relationship, intimacy, shared meaning or mutual understanding.

## NEW CORE

The candidate uses:

- `EncounterBinding`
- `EncounterBoundaryEvidence`
- `EncounterEventEvidence`
- `EncounterRecord`

An encounter is a bounded, auditable interaction/observation unit identified by `encounter_id`.
It is not a universal interpersonal story arc.

## BOUNDARY MODEL

Only three lifecycle boundary kinds are core:

- `START`
- `END`
- `ABORT`

There is exactly one `START` and at most one terminal boundary.
The derived record status is `OPEN`, `CLOSED` or `ABORTED`.

There is no generic `DEEPENING`, `CLIMAX`, depth threshold, progress score or intensity trajectory.
Domain-specific protocols may reference their own event kinds through `event_kind_ref` without changing this core.

## PARTICIPANT / ACTOR MODEL

`EncounterBinding` carries:

- `entity_ref`
- `entity_kind_ref`
- one or more `role_refs`
- evidence/provenance references

Roles are open references rather than a mutually exclusive fixed enum. A subject can therefore have multiple represented roles without that role becoming identity or authority.

The encounter requires the primary `subject_ref` to be bound exactly once, but does not require a second social participant. This leaves room for subject-to-tool, subject-to-environment, subject-to-artifact and self/prior-state observation units.

## EVENT INTEGRITY

Events carry structured references rather than a free `description` field:

- `event_id`
- `encounter_id`
- timestamp
- `event_kind_ref`
- `source_actor_ref`
- involved entity refs
- `content_ref`
- evidence/provenance refs

Validation rejects:

- duplicate binding/boundary/event IDs;
- duplicate entity bindings;
- missing subject binding;
- boundary/event encounter mismatch;
- ghost source/involved entities;
- events before START;
- events after END/ABORT;
- terminal boundary earlier than START;
- naive timestamps without a timezone.

## AUTHORITY AND RELATIONSHIP NON-CLAIMS

`ROLE != IDENTITY`

`ROLE != AUTHORITY`

`ENCOUNTER != RELATIONSHIP_FORMATION`

`ENCOUNTER != INTIMACY`

`ENCOUNTER != SHARED_MEANING`

`ENCOUNTER != MUTUAL_UNDERSTANDING`

`ENCOUNTER != SUBJECTIVITY_PROOF`

All such claims remain `NOT_ESTABLISHED`; canonical effect remains `NONE`.

## REMOVED SOURCE MATERIAL

Not carried forward:

- universal interpersonal phase arc;
- `DEEPENING` / `CLIMAX` as generic lifecycle phases;
- manual agency/familiarity/trust/power scalars;
- progress/depth/intensity trajectory;
- expected-duration/depth-threshold pseudo-gates;
- mutable state manager;
- initialize/restore scaffold;
- participant list deletion presented as causal ablation;
- free-text relationship/mechanism claims.

## INTEGRATION PATH

Encounter records and events can later be represented as event/state artifacts in `continuity-evidence-lineage_v0.1.0` through an adapter. This package intentionally has no code dependency on that candidate.

A handoff protocol event may be referenced by an encounter, but a successful encounter or handoff does not prove personal identity continuity.

## VERIFICATION

Independent local verification before repository write:

```text
15 passed in 0.04s
```

GitHub Actions status must be checked independently after the final repository write.
