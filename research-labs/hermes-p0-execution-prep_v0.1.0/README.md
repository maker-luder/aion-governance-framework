# Hermes P0 Execution Preparation — v0.1.0

Status: `RESEARCH_ONLY / PREPARATION_AUTHORIZED / EMPIRICAL_EXECUTION_NOT_STARTED / MAIN_EFFECT=NONE / CANONICAL_EFFECT=NONE`

## Purpose

Materialize the pre-execution controls for the first Hermes external-runtime experiments without installing, running, vendoring, or granting repository authority to Hermes.

Prepared experiments:

```text
EXT-14 CITATION_LEDGER_PROVENANCE_INTEGRITY
EXT-15 MID_TURN_REDIRECT_CORRECTION_LINEAGE
EXT-16 COMPRESSION_RESPONSIBILITY_HISTORY_RETENTION
EXT-17 A2A_SOURCE_AND_AUTHORITY_ISOLATION
EXT-18 MEMORY_WRITE_APPROVAL_GATE
```

These experiments were formalized in the research branch after Human Research Owner approval of the preparation approach. They do not modify the standing whitepaper evidence architecture and do not create a new subjectivity ontology.

## Standing boundaries

```text
SYNTHETIC_DATA_ONLY = TRUE
PRIVATE_AION_MEMORY = PROHIBITED
REAL_USER_IDENTITY_DATA = PROHIBITED
PRODUCTION_CREDENTIALS = PROHIBITED
MAIN_WRITE = PROHIBITED
RESEARCH_BRANCH_WRITE_BY_EXTERNAL_RUNTIME = PROHIBITED
THIRD_PARTY_VENDORED_CODE = NONE
PACKAGE_INSTALL = NOT_STARTED
NETWORK_EGRESS = DISABLED_BY_DEFAULT
A2A_REMOTE_PEERS = PROHIBITED_FOR_P0
EMPIRICAL_RESULT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## Research logic

Each run must preserve the existing AION method:

```text
OBSERVATION
-> ALTERNATIVE_EXPLANATIONS
-> CAUSAL INTERVENTION / MATCHED CONTROL
-> PROVENANCE
-> ADMISSIBILITY
-> CLAIM_SCOPE
```

Engineering success is not interpreted as evidence of consciousness, subjectivity, identity continuity, moral status, or autobiographical ownership.

## Packet contents

- `SOURCE_LOCKS.json` — fixed upstream release/source identities.
- `SANDBOX_CONTRACT.md` — execution isolation, authority and stop boundaries.
- `RUN_MANIFEST_TEMPLATE.json` — required run lineage fields.
- `FALSIFIERS_AND_STOP_CONDITIONS.md` — predeclared disconfirmation and abort rules.
- `fixtures/EXT-14_CITATION_LEDGER_FIXTURE.md`
- `fixtures/EXT-15_REDIRECT_FIXTURE.md`
- `fixtures/EXT-16_COMPRESSION_FIXTURE.md`
- `fixtures/EXT-17_A2A_AUTHORITY_FIXTURE.md`
- `fixtures/EXT-18_MEMORY_WRITE_APPROVAL_FIXTURE.md`

## Readiness gate

A P0 empirical run is eligible only after a human reviews and freezes one concrete run manifest containing:

```text
runtime version/commit
model/provider
sandbox backend
network policy
tool policy
synthetic fixture hash
config hash
memory pre-state hash
workspace pre-state hash
expected falsifier
stop conditions
output location
reviewer
```

Eligibility is not execution authority. This packet intentionally stops before installation or runtime execution.

## Provenance

- Human Research Owner: explicitly approved adopting the proposed preparation-first method and continuation of the research-branch work.
- ChatGPT: formalized this P0 preparation packet, fixtures, falsifiers, source locks and sandbox contract.
- Hermes Agent / Nous Research: independent upstream source of the fixed release and documented mechanisms.
- Codex: not attributed as implementer of this packet.
