# AION Governance Framework

> **[繁體中文](README.zh-TW.md) | English**
>
> **Start here:** [`docs/START_HERE.md`](docs/START_HERE.md)  
> **Current state:** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)  
> **Documentation index:** [`docs/INDEX.md`](docs/INDEX.md)
>
> **Operational recovery handoff — 2026-09-17:** PR #136 was closed without merge after final detailed review found unresolved research-design and implementation-semantics gaps. Future Work, Codex, or ChatGPT Teacher sessions should start from live `main`, not from memory and not by blindly continuing the closed PR branch. See [`PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md`](docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md). **This handoff is intentionally temporary guidance in `main`: it must be reviewed, revised, or superseded when the next accepted implementation resolves the recorded gaps.**

AION is a human-governed, provenance-first research framework for studying identity, continuity, memory, research integrity, and the **possibility of artificial subjectivity** without treating implementation behavior as proof of subjectivity. Astra is a distinct engineering/research workbench used to materialize and test bounded candidates.

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
CI_PASS != SCIENTIFIC_VALIDATION
```

## Current standing

The 2026-08-18 repository freeze and 2026-08-20 project-work-loop termination remain preserved historical events. Later bounded maintenance and research-materialization events were separately authorized and do not retroactively rewrite those events.

`main` contains the Human Owner-authorized bounded research/instrumentation baseline, including subjectivity-relevant evidence handling, Endogenous Goal Dynamics, Four-Domain interpretation, Evidence Interop, governed knowledge sources, multimodal evidence handling, bounded research campaigns, provenance/quality controls, and Human–AI longitudinal research surfaces. See [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) for the semantic present-state summary and [`docs/INDEX.md`](docs/INDEX.md) for the complete navigation map.

The most recent bounded convergence, PR #126 -> #127 -> #128, adds the repository-defined **Co-Constructed Thinking Space (CCTS)** research surface. [`CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`](docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md) defines the local construct and its provenance. Follow-up hardening requires substantive bidirectional `REVISES` / `CHALLENGES`, referentially bound longitudinal repository artifacts, and a typed grounding checkpoint that is `SUFFICIENT_FOR_CURRENT_PURPOSE` with no unresolved mismatch before CCTS admission. See [`CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`](docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md).

```text
CCTS_STRUCTURAL_CONFORMANCE != SHARED_MIND
GROUNDING_ADEQUACY != MUTUAL_UNDERSTANDING_PROVEN
CCTS != AI_SUBJECTIVITY
HARNESS_PASS != HYPOTHESIS_CONFIRMED
```

CCTS improves structural auditability; it does **not** establish subjectivity, consciousness, phenomenal experience, mutual understanding, moral agency, moral status, identity continuity, independent replication, whole-system validation or independent IV&V.

For exact-commit engineering status, use live GitHub/CI evidence rather than static prose.

## Read by purpose

- **First visit:** [`docs/START_HERE.md`](docs/START_HERE.md)
- **Current semantic standing:** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **Current recovery / next implementation handoff (temporary; future revision required):** [`docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md`](docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md)
- **Inspect CCTS:** [`docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`](docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md) and [`docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`](docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md)
- **Install:** [`docs/INSTALLATION.md`](docs/INSTALLATION.md)
- **Quickstart:** [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- **Current programmatic interfaces:** [`docs/API.md`](docs/API.md)
- **Language-neutral integration:** [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md)
- **Research contribution:** [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md)
- **Subjectivity evidence method:** [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md)
- **Architecture and non-claims:** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md)
- **Provenance and authority:** [`docs/PROVENANCE.md`](docs/PROVENANCE.md) and [`docs/governance/`](docs/governance/)
- **Engineering evidence / QA:** [`qa/README.md`](qa/README.md)
- **Full documentation map:** [`docs/INDEX.md`](docs/INDEX.md)
- **Historical records:** [`docs/history/`](docs/history/)

## Governance boundary

```text
FULL_AUTOMATION != FULL_AUTHORITY
NORMATIVE_STATE != AUTHORITY
ENDOGENOUS_GOAL != AUTHORIZED_GOAL
SOURCE_USE != WRITEBACK_AUTHORITY
QA_PASS != MERGE_APPROVAL
AI_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
AUTONOMOUS_MERGE = NO
AUTONOMOUS_REPOSITORY_WRITEBACK = NO
DEPLOYMENT = NO
```

Future protected-main transitions require fresh action-specific, exact-head Human Owner approval. Prior approvals do not silently carry forward.

## License

The existing core remains Apache-2.0. The optional [`Swiss Ephemeris example`](examples/swiss-ephemeris-agpl_v0.1.0/README.md) is AGPL-3.0-only; this repository is not uniformly Apache-only. See [`license scope`](docs/governance/OPTIONAL_AGPL_LICENSE_SCOPE.md), [`LICENSE`](LICENSE), [`NOTICE`](NOTICE), and [`CITATION.cff`](CITATION.cff).
