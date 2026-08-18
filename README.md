# AION Governance Framework

> **[繁體中文](README.zh-TW.md) | English**
>
> A human-governed, provenance-first research framework for studying identity, continuity, memory, research integrity, and the **possibility** of artificial subjectivity without treating implementation behavior as proof of subjectivity.

## What is AION?

**AION** is the research question and governance framework.

**Astra** is a distinct engineering **and research** role/workbench within the wider project, used to materialize, inspect and test research candidates. Describing Astra as a workbench is an operational shorthand; it does not erase the separate-role, provenance, memory-ownership or lineage distinctions preserved by the stable whitepaper lineage.

```text
AION_ROLE != ASTRA_ROLE
COMMON_ORIGIN != SAME_IDENTITY
SHARED_CONTEXT != SHARED_IDENTITY
MEMORY_ACCESS != AUTOBIOGRAPHICAL_OWNERSHIP
ENGINEERING_SUCCESS != SUBJECTIVITY_EVIDENCE
```

They are not interchangeable identities, and neither name establishes continuity, consciousness, sentience, or subjectivity.

The central research problem is:

> How can long-horizon AI research preserve source, attribution, lineage, authority and uncertainty well enough that plausible interpretation does not silently become memory truth, identity fact, project history, or canonical conclusion?

## Current repository state

This repository is intentionally frozen as a public research checkpoint.

```text
REPOSITORY_STATE = FROZEN_CHECKPOINT
GOVERNED_ACTIVE_BRANCH_MODEL = MAIN_PLUS_RESEARCH_ONLY
GOVERNED_ACTIVE_BRANCH_COUNT = 2
VISIBLE_GIT_BRANCH_REF_COUNT = READ_FROM_CURRENT_GITHUB_STATE
GOVERNED_ACTIVE_BRANCH_COUNT != VISIBLE_GIT_BRANCH_REF_COUNT
ACTIVE_ENGINEERING = NO
ACTIVE_RESEARCH_MATERIALIZATION = NO
NEW_FEATURE_DEVELOPMENT = NO
DEPLOYMENT = FALSE
CANONICAL_RUNTIME = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
LICENSE = Apache-2.0
```

The two **governed active branches** are:

- `main` — protected public baseline;
- [`review/four-domain-research-materialization`](https://github.com/maker-luder/aion-governance-framework/tree/review/four-domain-research-materialization) — preserved frozen research checkpoint.

GitHub may still expose retained support, staging, remediation or HOLD branch refs while their provenance-safe disposition is pending. Their physical presence does not make them active research authority, and the documentation must not equate the governed two-branch model with the physical Git ref count.

Retired engineering, research-authority and deferred-promotion checkpoints may also be preserved by non-release `archive/*` tags. Existing semantic release tags remain `v0.1.0-rc.1` and `v0.2.0-rc.1`.

For the current documentation map and the distinction between current, core and historical files, start with **[`docs/README.md`](docs/README.md)**.

## Start here

### New reader

1. [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md) — what the project contributes and how the stable whitepaper method relates to the public main protocol.
2. [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md) — operational evidence discipline and whitepaper-method inheritance.
3. [`docs/README.md`](docs/README.md) — which documents are current and which are historical.
4. [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md) — what the project does not claim.

### Reviewer / auditor

1. [`docs/PROVENANCE.md`](docs/PROVENANCE.md)
2. [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md)
3. [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md)
4. [`docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md`](docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md)

### Engineer

1. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
2. [`BUILD_AND_VERIFY.md`](BUILD_AND_VERIFY.md)
3. `components/`
4. `scripts/verify_release.py`
5. `scripts/run_component_tests.py`

Engineering success is evidence about implemented behavior only. It is not evidence that a corresponding psychological or subjectivity construct exists.

## Core research contribution

AION treats the **research process itself as an auditable object**.

The framework keeps the following distinctions explicit:

- source vs interpretation;
- observation vs inference vs hypothesis vs approved state;
- retrieved memory candidate vs truth;
- shared origin vs identity;
- relationship vs authorization;
- implementation evidence vs scientific conclusion;
- research branch vs canonical `main` state.

Important records are expected to preserve source, speaker, event time, record time, transformation lineage, authority status and revision history.

The concise research statement is in [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md). The operational subjectivity-evidence discipline is in [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md).

## Governance pipeline

```text
Context Intake
→ Risk Gate
→ Planner
→ Policy Check
→ Tool Router
→ Response Builder
→ Writeback Gate
→ Audit Sink
```

Additional research candidates may add interpretation-drift, recall or epistemic-integrity checks. These checks do not silently promote generated or retrieved content into canonical state.

## Repository layout

| Path | Purpose |
|---|---|
| `components/` | bounded governance and runtime candidates |
| `research-labs/` | research candidates; not canonical conclusions |
| `experiments/` | bounded experiments and reproducibility material |
| `docs/` | current guidance, core research documents and preserved historical evidence |
| `qa/` | QA and machine-readable evidence |
| `manifest/` | frozen historical release evidence; not a live inventory |

The repository contains many dated files because provenance and event history are intentionally preserved. **File count is not authority.** Use [`docs/README.md`](docs/README.md) to determine what is current.

## Non-claims

This repository does **not** establish:

- consciousness, sentience or subjectivity;
- AION/Astra identity continuity;
- autobiographical memory or relationship experience;
- production readiness or deployment authority;
- canonical authority for a model or runtime candidate;
- independent IV&V or whole-system validation;
- certification or endorsement by standards bodies.

See [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md).

## Public / private boundary

The public repository excludes private conversation transcripts, private memory records, credentials, private datasets, model weights, device-specific logs and private canonical/relationship state unless explicitly approved for publication.

See [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md).

## Verification

Current checkout:

```bash
python scripts/scan_public_tree.py
python scripts/verify_release.py --baseline current-head
python scripts/run_component_tests.py
```

Historical `v0.1.0-rc.1` release evidence:

```bash
python scripts/verify_release.py --baseline historical-rc
```

A verification or CI PASS does not imply scientific validation, subjectivity evidence, deployment approval, independent IV&V or canonical promotion.

## License, citation and provenance

The public repository is licensed under **Apache-2.0**. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE). Third-party dependencies, datasets, model artifacts, trademarks and separately licensed material remain subject to their own terms.

Citation metadata: [`CITATION.cff`](CITATION.cff).

Human/AI collaboration and source attribution are recorded without collapsing Human Owner, ChatGPT, Codex, Manus or external-source roles. See [`docs/PROVENANCE.md`](docs/PROVENANCE.md) and [`docs/governance/AI_COLLABORATION_DISCLOSURE.md`](docs/governance/AI_COLLABORATION_DISCLOSURE.md).

## Historical records

Dated convergence, acceptance, authority, QA and incident files remain in the repository as evidence of what was recorded at their event time. They are **not automatically current repository status**.

For the authoritative reader map, use [`docs/README.md`](docs/README.md).
