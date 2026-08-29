# Documentation Index / 文件索引

> Curated catalog. This is not a second `START_HERE` and does not create authority by listing a file.

For first reading, use [`START_HERE.md`](START_HERE.md). For current semantic standing, use [`CURRENT_STATE.md`](CURRENT_STATE.md).

## Current entry and state

| Class | Document | Responsibility |
|---|---|---|
| `CURRENT_ENTRY` | [`../README.md`](../README.md) / [`../README.zh-TW.md`](../README.zh-TW.md) | Short public orientation and route to the single entry point |
| `CURRENT_ENTRY` | [`START_HERE.md`](START_HERE.md) | Single human reader entry point |
| `CURRENT_STATE` | [`CURRENT_STATE.md`](CURRENT_STATE.md) | Single semantic present-state summary |
| navigation | [`README.md`](README.md) | Compatibility documentation guide pointing to current navigation |
| navigation | this file | Curated catalog and class map |

## Onboarding and external interfaces

- [`INSTALLATION.md`](INSTALLATION.md) — source checkout, component-scoped installs, and tests.
- [`QUICKSTART.md`](QUICKSTART.md) — deterministic inspection-only Evidence Interop export.
- [`API.md`](API.md) — current public-interface classification.
- [`EXAMPLES.md`](EXAMPLES.md) — runnable example map.
- [`INTEROPERABILITY.md`](INTEROPERABILITY.md) — JSON/subprocess boundary and reference integrations.
- [`VERSIONING.md`](VERSIONING.md) and [`RELEASE_READINESS.md`](RELEASE_READINESS.md) — experimental version policy and conservative release gate.

## Current research core

| Class | Document | Responsibility |
|---|---|---|
| `CURRENT_CORE` | [`PROJECT_PURPOSE_ANCHOR.md`](PROJECT_PURPOSE_ANCHOR.md) | Protect central purpose from engineering/product drift |
| `CURRENT_CORE` | [`RESEARCH_CONTRIBUTION_ONE_PAGER.md`](RESEARCH_CONTRIBUTION_ONE_PAGER.md) | One-page research contribution |
| `CURRENT_CORE` | [`SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](SUBJECTIVITY_EVIDENCE_PROTOCOL.md) | Operational discipline for subjectivity-relevant evidence |
| `CURRENT_CORE` | [`ARCHITECTURE.md`](ARCHITECTURE.md) | Current high-level architecture and separation rules |
| `CURRENT_CORE` | [`NON_CLAIMS.md`](NON_CLAIMS.md) | Explicit scientific/engineering non-claims |
| `CURRENT_CORE` | [`PROVENANCE.md`](PROVENANCE.md) | Source, attribution, temporal and authority rules |
| `CURRENT_CORE` | [`PUBLIC_PRIVATE_BOUNDARY.md`](PUBLIC_PRIVATE_BOUNDARY.md) | Public/private data boundary |
| `CURRENT_CORE` | [`THREAT_MODEL.md`](THREAT_MODEL.md) | Threat and failure assumptions |

## Governance and active controls

Directory: [`governance/`](governance/)

Use for authority, source admission, writeback, transition, risk, memory, and documentation controls. Important entry-level controls include:

- [`governance/GOVERNED_KNOWLEDGE_SOURCE_REGISTRY.md`](governance/GOVERNED_KNOWLEDGE_SOURCE_REGISTRY.md)
- [`governance/MAIN_TRANSITION_AUTHORITY_GATE.md`](governance/MAIN_TRANSITION_AUTHORITY_GATE.md)
- [`governance/DOCUMENTATION_GOVERNANCE.md`](governance/DOCUMENTATION_GOVERNANCE.md)

Bounded norm-formation and related normative-state research material remains component/lab-local under [`../research-labs/`](../research-labs/) unless a dedicated governance control explicitly promotes a narrower rule.

Action-specific governance controls outrank this index for the actions they govern.

## Engineering evidence and QA

- [`evidence/`](evidence/) — supporting engineering-evidence material and standards mappings.
- [`../qa/README.md`](../qa/README.md) — semantics of committed QA snapshots vs live exact-head CI.
- GitHub Actions — live exact-commit workflow evidence.

```text
ENGINEERING_EVIDENCE != SCIENTIFIC_VALIDATION
CI_PASS != THEORY_CONFIRMATION
```

## Component-local documentation

These are bounded to the component/lab they describe and are not global reader entry points:

- [`../components/`](../components/) — governance, execution, evidence and runtime components;
- [`../research-labs/`](../research-labs/) — bounded research materialization, including subjectivity pipeline, Endogenous Goal Dynamics, norm formation, triadic state dynamics and bounded research loop;
  - [`Diachronic and Collective Dynamics profile`](../research-labs/bounded-autonomous-research-loop_v0.1.0/docs/DIACHRONIC_COLLECTIVE_DYNAMICS.md) — component-local derived observations over the unchanged seven-state surface;
- [`../components/multimodal_media_core_v0.1.0/`](../components/multimodal_media_core_v0.1.0/) — governed local-first image, video and 3D evidence generation with provider-neutral admission controls;
- [`../components/aion_astra_autonomous_research_v0.1.0/`](../components/aion_astra_autonomous_research_v0.1.0/) — finite 17-stage synthetic Triadic research campaign using existing inquiry, bounded-loop and Evidence Interop owners;
- [`../experiments/`](../experiments/) — bounded experiments and baselines.

Read the local `README`/`docs` only after the relevant global method/architecture document.

## Research references

Directory: [`research/`](research/)

Research-reference material supports interpretation and method development. Presence in this directory does not create current-state, canonical, or scientific authority.

## Historical records

Directory: [`history/`](history/)

Dated/event-specific records outside `history/` are also historical when their purpose is to preserve an event-time snapshot, for example:

- `REPOSITORY_FREEZE_NOTICE_2026-08-18.md`;
- `PROJECT_TERMINATION_NOTICE_2026-08-20.md`;
- dated post-merge reconciliation, acceptance-evidence, transition, audit or incident records.

These files should not be mechanically rewritten to match the present.

```text
HISTORICAL_RECORD = PRESERVE_EVENT_TIME_MEANING
HISTORICAL_RECORD != CURRENT_STATE
```

## Release, legal, security and community support

Root-level files such as `LICENSE`, `NOTICE`, `CITATION.cff`, `SECURITY.md`, `PRIVACY.md`, `PUBLIC_RELEASE_POLICY.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md` retain their specialized responsibilities. They are supporting controls, not scientific current-state documents.

`docs/RELEASE_STATUS.md` preserves release/termination/bounded-event standing and exact historical engineering evidence. For a concise present semantic summary, prefer `CURRENT_STATE.md`.

## Classification rules

The complete path-based classification policy is in [`governance/DOCUMENTATION_GOVERNANCE.md`](governance/DOCUMENTATION_GOVERNANCE.md). The important rules are:

```text
FILE_COUNT != AUTHORITY
NEWER_FILE != MORE_AUTHORITATIVE
HISTORICAL_RECORD != CURRENT_STATE
SUPPORTING_DOCUMENT != ENTRY_POINT
COMPONENT_LOCAL != GLOBAL_AUTHORITY
DOCUMENTATION_CONVERGENCE != RESEARCH_SCOPE_EXPANSION
```

If a new document does not fit a defined class, classify it before treating it as current authority.
