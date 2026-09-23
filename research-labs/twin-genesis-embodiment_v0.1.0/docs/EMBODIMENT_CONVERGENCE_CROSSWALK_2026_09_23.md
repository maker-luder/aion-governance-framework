# Embodiment archive convergence crosswalk — 2026-09-23

Status: `SYNTHETIC_ENGINEERING_CANDIDATE / CLOSED_DRAFT / SCIENTIFIC_HOLD`

The v0.1 ledger remains historical input. The authoritative Phase A coverage
contract is
`../data/EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_v0.2.json`. It classifies exact
semantic units from closed, unmerged archive PRs, independently records their
Phase A disposition, and binds every source/support artifact to its Git blob.
Its source heads
are #190 `066ed1afccebee869eb658c09691b7f096694332`, #191
`48bcf45a55a0b67dfc0e7b9cd838c5f9068b08d2`, and #192
`861e6a556a21afffd04b187714c0608fe73ea4fc`; #202 is recorded only as
deferred provenance at `7f84ae8c95f1b7caaaa0c3850a0b6cfd049b7108`.
The matrix records origin and engineering disposition, not scientific
correctness.

| Current candidate | Admitted archive semantics | What remains outside |
| --- | --- | --- |
| `shared_core.py` | Role-neutral body region taxonomy (#191); system identifiers without biological functions (#190); sensory/motor domains and observability classes (#192) | AION/Astra identity, Teacher measurements, subjective experience, real sensors/actuators |
| `role_extensions.py` | One unique deferred capability per exact #192 role-specific semantic-unit ID, source path, and source blob | No broad capability buckets, Teacher runtime, active measurement port, or extension required by the shared core |
| `active_baseline.py` | Content hashes for the historical ledger, v0.2 coverage matrix, shared core, and optional extension IDs paired with full extension content hashes | #202 sensorimotor integration and empirical/physical control |

The body region `EXTERNAL_MALE_FORM_SURFACE` is included only when the
input template explicitly chooses `ADULT_MALE_ANATOMY_CANDIDATE`; it is a
template-dependent static surface, never an identity or experiential claim.
Other role or morphology profiles require separate review and must not be
silently inferred from this reference.

The shared core accepts no unreviewed dependencies. The Teacher manifest
does not turn an archive feature into active implementation; its capability
families remain `DEFERRED`. The baseline can be built with zero extensions.

Each Teacher capability maps one-to-one to a reviewed v0.2 #192 semantic unit;
the former broad runtime/avatar/channel buckets are absent. If a unit loses its
exact deferred role-extension classification, source path, source blob, or
canonical order, baseline construction fails closed. The baseline ID binds the
v0.2 matrix and extension content, not only their names. Schemas describe
serialized records and reject unexpected fields; semantic uniqueness, source
bindings, target/replacement existence, and hash equality are checked by Python
validators.

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
