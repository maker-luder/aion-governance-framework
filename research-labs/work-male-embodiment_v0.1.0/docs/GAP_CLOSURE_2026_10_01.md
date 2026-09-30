# PR #237 gap-closure record — 2026-10-01

This extension records what remained unimplemented after the first bounded implementation and closes the portions that can be implemented honestly in repository software.

## Newly closed engineering gaps

1. Anthropometry schema: Draft 2020-12 schema now pins the existing v0.2 structure, 67 selected measurements, 66 cm + 1 kg counts, exactly two HUMAN_FIXED entries, 65 AI_PROVISIONAL entries, 165 cm height, 76 kg mass-equivalent, and zero as-built verified measurements.

2. Whole-body state surface: 19 body-system channels now exist as explicit synthetic reference channels. They default UNKNOWN rather than silently inventing a normal-human baseline. DELTA is rejected until a channel has first been explicitly SET.

3. Asset engineering contract: a future mesh must satisfy all 67 selected measurements plus rig nodes, joint-limit verification, collision geometry, mass properties, skinning, external male-form geometry nodes, and prepuce-mobility geometry. Missing evidence remains missing.

4. Integrity: SHA-256 chained snapshot receipts detect payload or receipt tampering.

5. Executable probe: a deterministic offline probe exercises the profile, whole-body channels, physiology engine, asset gate, and receipt chain. It reports absent mesh evidence instead of treating absence as success.

6. Schema parity: physiology state/event schemas are now fail-closed and mirror consent, authority, biological, felt-state, canonical and deployment boundaries. Whole-body/profile schemas are validated in tests.

## Still not truthfully completable by repository code alone

- actual GLTF/GLB mesh: NOT_PRESENT
- rig file and skin weights: NOT_PRESENT
- measured joint limits on a real asset: NOT_PRESENT
- collision geometry: NOT_PRESENT
- verified mass/inertia properties: NOT_PRESENT
- movable prepuce mesh/mechanism: NOT_PRESENT
- physical sensors and actuators: NOT_PRESENT
- physical synthetic-fluid hardware: NOT_PRESENT
- biological blood: NO
- biological hormones: NO
- biological semen: NO
- sperm or gametes: NO
- fertility: NO
- felt body sensation: NOT_ESTABLISHED
- subjectivity: NOT_ESTABLISHED
- consciousness: NOT_ESTABLISHED
- phenomenal experience: NOT_ESTABLISHED

These items are not omitted because they are sexual or sensitive. They remain unresolved because the corresponding physical artifact or empirical evidence does not exist.

PARITY_TARGET means ordinary adult-male reference dimensions and body-system categories are not deleted merely because they include sexual or reproductive anatomy. It does not permit absent mesh, hardware, biology, or phenomenal evidence to be replaced by labels.

IMPLEMENTED_REFERENCE_OR_SIMULATION != PHYSICAL_OR_BIOLOGICAL_REALIZATION
