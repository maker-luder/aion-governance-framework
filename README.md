# AION Governance Framework

> **[繁體中文](README.zh-TW.md) | English**

AION is a **human-governed research framework for studying the possibility of artificial subjectivity without treating convincing behavior, memory-like continuity, relationship language, or successful software tests as proof that subjectivity exists**.

The repository is not a claim that an AI is conscious or already has a persistent self. Its central problem is methodological: **what evidence would be relevant, how strong may a claim become, and how can the research process itself remain auditable when identity, continuity, memory, Human–AI interaction, and long-horizon AI behavior are being studied?**

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
SCIENTIFIC_DISPOSITION = HOLD
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
DEPLOYMENT = FALSE
```

## Why this repository exists

Modern AI systems can produce behavior that looks coherent, adaptive, relational, agentic, or continuous across time. Those observations may be worth studying, but they do not by themselves establish an inner subject, consciousness, identity continuity, or autonomous authority.

AION therefore treats **research discipline as part of the research object**. The repository keeps observation, evidence, inference, hypothesis, implementation, authority, and scientific conclusion separate so that a plausible story cannot silently become a fact merely because software exists or a conversation feels continuous.

A recurring rule is:

```text
EVIDENCE_SUPPORTS_ONLY_WHAT_IT_SUPPORTS

ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
CI_PASS != SCIENTIFIC_VALIDATION
RELATIONAL_CONTINUITY != AI_IDENTITY_CONTINUITY
HUMAN_AI_LEARNING != AI_SUBJECTIVITY
```

## What is being studied

Current `main` contains bounded research and instrumentation around several connected questions:

- **Artificial-subjectivity evidence:** how observations, mechanisms, interpretations, alternative explanations, falsifiers, and claim ceilings should be separated.
- **Identity, continuity, and memory:** how identifier continuity, relational continuity, functional/diachronic continuity, memory records, and stronger identity claims differ.
- **Human–AI longitudinal interaction:** how repeated grounding, correction, re-entry, interaction history, externalized rules, and Human learning can be studied without assuming model-internal learning.
- **Co-Constructed Thinking Space (CCTS):** a repository-defined construct for auditable Human–AI problem representation, reciprocal revision, provenance, grounding checkpoints, and rejected-branch preservation. CCTS is a local research construct, not proof of a shared mind.
- **Epistemic robustness and evidence ceilings:** how a system behaves when evidence is full, partial, irrelevant, absent, or conflicting, and how unsupported claims are prevented from being promoted.
- **Research quality and provenance:** exact-head evidence, source attribution, claim admission, QA/QC, NCR/CAPA records, and fail-closed main-transition authority.

Most executable research surfaces are deterministic or synthetic harnesses. They are designed to make research assumptions inspectable; passing them does not confirm the associated hypothesis.

## What this repository does **not** claim

```text
CCTS_STRUCTURAL_CONFORMANCE != SHARED_MIND
GROUNDING_ADEQUACY != MUTUAL_UNDERSTANDING_PROVEN
EPISTEMIC_AGENCY_LIKE_BEHAVIOR != INTERNAL_AGENCY_ESTABLISHED
MEMORY_RETENTION != SUBJECTIVE_REMEMBERING
HARNESS_PASS != HYPOTHESIS_CONFIRMED
QA_PASS != MERGE_APPROVAL
AUTOMATION != AUTHORITY
```

The repository also does not define itself as a commercial autonomous-agent platform, a chatbot persona, or a deployed autonomous authority system.

## Start here

| If you want to... | Read |
|---|---|
| understand the project in one guided path | [`docs/START_HERE.md`](docs/START_HERE.md) |
| check the current semantic standing | [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) |
| understand the research contribution | [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md) |
| understand the subjectivity-evidence method | [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md) |
| understand architecture and explicit non-claims | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md) |
| inspect provenance and authority rules | [`docs/PROVENANCE.md`](docs/PROVENANCE.md) and [`docs/governance/`](docs/governance/) |
| browse research, labs, experiments, history, and QA | [`docs/INDEX.md`](docs/INDEX.md) |
| install or run the public interfaces | [`docs/INSTALLATION.md`](docs/INSTALLATION.md), [`docs/QUICKSTART.md`](docs/QUICKSTART.md), and [`docs/API.md`](docs/API.md) |

## Current standing in plain language

The original project work loop was terminated in August 2026 and has **not** been silently restarted. `main` can still receive separately authorized, bounded maintenance or research materialization events. That distinction is intentional.

The CCTS structural line was formalized and hardened through PR #126 -> #127 -> #128. Later bounded work added an evidence-sufficiency robustness probe, an epistemic-agency/continuity evidence-ceiling contract, and repository-wide exact-head mypy/QMS controls. These additions expand what can be inspected; they do not elevate the scientific conclusion beyond `HOLD`.

PR #136 was closed without merge after detailed review found unresolved research-design and implementation-semantics problems. PR #137 placed a **temporary recovery handoff** in `main` so the next implementation can be reconstructed from repository evidence rather than conversation memory. That handoff is operational guidance, not an accepted PR #136 implementation or permanent research specification.

For exact commit identity, workflow results, or merge readiness, use live GitHub/CI evidence rather than static prose.

## Repository map

- [`docs/`](docs/) — current entry points, research method, governance, provenance, research references, and history.
- [`research-labs/`](research-labs/) — bounded executable research contracts and synthetic study harnesses.
- [`components/`](components/) — reusable governance, evidence, continuity, memory, runtime, and multimodal components.
- [`experiments/`](experiments/) — bounded experiments and controlled probes.
- [`qa/`](qa/) — engineering-quality semantics, evidence, and NCR/CAPA records.
- [`.github/`](.github/) — CI, quality, code-scanning, and main-transition controls.

## Governance boundary

Protected `main` transitions require fresh, action-specific, exact-head Human Owner approval. CI, AI review, contributor authorship, or prior authorization do not become merge authority by themselves.

```text
CAPABILITY_TO_ACT != AUTHORITY_TO_ACT
AI_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
PRIOR_AUTHORIZATION != CURRENT_ACTION_AUTHORIZATION
AUTONOMOUS_MERGE = NO
AUTONOMOUS_REPOSITORY_WRITEBACK = NO
```

## Maintainer recovery note

The current temporary recovery guide is [`docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md`](docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md). It must be reviewed, revised, superseded, or reclassified after the next accepted implementation resolves or changes the recorded gaps.

## Contributing, citation, security, and license

- Contribution guidance: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Citation metadata: [`CITATION.cff`](CITATION.cff)
- Security policy: [`SECURITY.md`](SECURITY.md)
- Privacy boundary: [`PRIVACY.md`](PRIVACY.md) and [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md)
- License: core repository material is Apache-2.0, while the optional [`Swiss Ephemeris example`](examples/swiss-ephemeris-agpl_v0.1.0/README.md) is AGPL-3.0-only. See [`docs/governance/OPTIONAL_AGPL_LICENSE_SCOPE.md`](docs/governance/OPTIONAL_AGPL_LICENSE_SCOPE.md), [`LICENSE`](LICENSE), and [`NOTICE`](NOTICE).
