# Embodiment archive convergence crosswalk — 2026-09-23

Status: `SYNTHETIC_ENGINEERING_CANDIDATE / CLOSED_DRAFT / SCIENTIFIC_HOLD`

The source ledger `../data/EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_v0.1.json`
classifies semantic units from closed, unmerged archive PRs. Its source heads
are #190 `066ed1afccebee869eb658c09691b7f096694332`, #191
`48bcf45a55a0b67dfc0e7b9cd838c5f9068b08d2`, and #192
`861e6a556a21afffd04b187714c0608fe73ea4fc`. It records origin and
adoption status, not scientific correctness.

| Current candidate | Admitted archive semantics | What remains outside |
| --- | --- | --- |
| `shared_core.py` | Role-neutral body region taxonomy (#191); system identifiers without biological functions (#190); sensory/motor domains and observability classes (#192) | AION/Astra identity, Teacher measurements, subjective experience, real sensors/actuators |
| `role_extensions.py` | Exact #192 head and deferred Teacher-only capability provenance | No Teacher runtime, no active measurement port, no extension required by the shared core |
| `active_baseline.py` | Content hashes for validated ledger, shared core, and optional extension IDs paired with full extension content hashes | #202 sensorimotor integration and empirical/physical control |

The body region `EXTERNAL_MALE_FORM_SURFACE` is included only when the
input template explicitly chooses `ADULT_MALE_ANATOMY_CANDIDATE`; it is a
template-dependent static surface, never an identity or experiential claim.
Other role or morphology profiles require separate review and must not be
silently inferred from this reference.

The shared core accepts no unreviewed dependencies. The Teacher manifest
does not turn an archive feature into active implementation; its capability
families remain `DEFERRED`. The baseline can be built with zero extensions.

Each Teacher capability is reconciled against its reviewed #192 ledger unit;
multiple fine-grained capabilities may map to one recorded archive unit. If the
unit loses its deferred role-extension classification, baseline construction
fails closed. The baseline ID binds extension content, not only its name.
Schemas describe serialized records and reject unexpected fields; semantic
uniqueness, source bindings, and hash equality are checked by Python validators.

```text
ARCHIVE_HISTORY_MERGE = NO
SENSORIMOTOR_PR_202 = DEFERRED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SCIENTIFIC_DISPOSITION = HOLD
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
ENGINEERING_EMBODIMENT != BIOLOGICAL_EMBODIMENT
TEST_PASS != SCIENTIFIC_VALIDATION
```
