# Bazi Data Dictionary

- `bazi_rule_profiles`: immutable calculation rules and source references.
- `bazi_source_inputs`: immutable civil-time and provenance input records.
- `bazi_calculation_runs`: immutable run identity, versions and hashes.
- `bazi_natal_profiles`: immutable deterministic result identity.
- `bazi_pillars`: year, month, day and hour facts.
- `bazi_hidden_stems`: hidden-stem facts attached to a pillar.
- `bazi_ten_gods`: day-master-relative facts attached to a pillar.
- `bazi_relations`: deterministic relation lookup results.
- `bazi_luck_cycles`: owner-parameterized cycle candidates.
- `bazi_interpretation_candidates`: reviewable, supersedable interpretations.
- `agent_bazi_bindings`: owner-gated symbolic-genesis bindings.
- `bazi_calendar_source_register`: algorithm and calendar dependency records.
- `bazi_audit_events`: append-only component audit stream.

There are 13 domain tables plus one migration table, six indexes and fourteen
immutability triggers. SQLite may additionally create its own internal
sequence table. Foreign-key enforcement is enabled on every component
connection.
