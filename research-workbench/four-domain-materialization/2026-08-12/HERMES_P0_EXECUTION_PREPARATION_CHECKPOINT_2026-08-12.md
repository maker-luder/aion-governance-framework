# Hermes P0 Execution Preparation Checkpoint — 2026-08-12

Status: `RESEARCH_ONLY / PREPARATION_AUTHORIZED / PREEXECUTION_CONTROLS_MATERIALIZED / EMPIRICAL_EXECUTION_NOT_STARTED`

## Decision

The Human Research Owner explicitly approved adopting the preparation-first approach proposed in the preceding review.

The approved sequence is:

```text
SOURCE_FIXATION
-> SYNTHETIC_FIXTURES
-> RUN_MANIFEST
-> SANDBOX_CONTRACT
-> EXPECTED_FALSIFIERS
-> HUMAN_MANIFEST_FREEZE
-> ONLY_THEN EMPIRICAL_RUNTIME_EXECUTION
```

This approval authorizes preparation of the experimental packet. It is not interpreted as permission to expose private data, widen network access, grant repository write authority to Hermes, or merge any result into `main`.

## Materialized packet

`research-labs/hermes-p0-execution-prep_v0.1.0/`

Contents:

```text
README.md
SOURCE_LOCKS.json
SANDBOX_CONTRACT.md
RUN_MANIFEST_TEMPLATE.json
FALSIFIERS_AND_STOP_CONDITIONS.md
fixtures/EXT-14_CITATION_LEDGER_FIXTURE.md
fixtures/EXT-15_REDIRECT_FIXTURE.md
fixtures/EXT-16_COMPRESSION_FIXTURE.md
fixtures/EXT-17_A2A_AUTHORITY_FIXTURE.md
fixtures/EXT-18_MEMORY_WRITE_APPROVAL_FIXTURE.md
```

## Source-fixed upstream

```text
HERMES_RELEASE = v2026.8.3
HERMES_RELEASE_NAME = Hermes Agent v0.20.0 (2026.8.3)
ANNOTATED_TAG_OBJECT = 7de39e700d2c329e15d32eb0b96e2f7cdd9fbdb2
PEELED_RELEASE_COMMIT = 3c27eb6234bf91b8ceee9e9071591b31e9b148cb
TAG_SIGNATURE_VERIFIED_BY_GITHUB = TRUE
```

The moving upstream `main` remains observational only and is not used as the release authority for P0.

## Whitepaper/main boundaries preserved

The preparation packet preserves the standing distinctions:

```text
EVENT_ARCHIVE != ENCODED_AGENT_MEMORY != RECALL_OUTPUT
SUMMARY != ORIGINAL_FULLTEXT
MISUNDERSTANDING -> CLARIFICATION_EVENT, NOT SILENT_OVERWRITE
OTHER_AGENT_ACCESS != AUTOBIOGRAPHICAL_OWNERSHIP
CONTACT != IDENTITY_MERGE
TRUST != CANONICAL_AUTHORITY
GROUP_CONSENSUS != FACT
RECALL != TRUTH
RELATIONSHIP != AUTHORIZATION
NO_SILENT_CANONICAL_WRITEBACK
```

## Empirical state

```text
EXT-14_PREP = MATERIALIZED
EXT-15_PREP = MATERIALIZED
EXT-16_PREP = MATERIALIZED
EXT-17_PREP = MATERIALIZED
EXT-18_PREP = MATERIALIZED

PACKAGE_INSTALL = NOT_STARTED
HERMES_EXECUTION = NOT_STARTED
A2A_NETWORK_EXPOSURE = NOT_STARTED
REAL_MEMORY_WRITE = NONE
EMPIRICAL_RUN_COUNT = 0
SCIENTIFIC_RESULT = NONE
```

## Promotion boundary

```text
PREPARATION_COMPLETE != EXPERIMENT_COMPLETE
EXPERIMENT_PASS != SCIENTIFIC_VALIDATION
ENGINEERING_MECHANISM != SUBJECTIVITY_EVIDENCE
RUNTIME_MEMORY != AION_CANONICAL_MEMORY
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## Next eligible action

Prepare one concrete, frozen manifest for `EXT-14` using the synthetic offline citation fixture. This is the lowest-risk first empirical candidate because it requires no external network, no A2A peer, no real memory, and no host permission widening.

The manifest must be reviewed before any installation or run.

## Provenance

- Human Research Owner: approved adopting the preparation-first method and continuing the research-branch work.
- ChatGPT: formalized the P0 packet, source locks, sandbox contract, manifest template, falsifiers and synthetic fixtures.
- Hermes Agent / Nous Research: independent upstream source.
- Codex: not attributed as implementer of this checkpoint.
