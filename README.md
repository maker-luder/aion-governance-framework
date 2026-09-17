# AION Governance Framework

> **[繁體中文](README.zh-TW.md) | English**
>
> **Start here:** [`docs/START_HERE.md`](docs/START_HERE.md)  
> **Current research state:** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)  
> **Documentation index:** [`docs/INDEX.md`](docs/INDEX.md)

AION is a human-governed, provenance-first, auditable research framework for studying the **possibility of artificial subjectivity**.

Its central question is not whether AI has already been shown to possess subjectivity. It is:

> How can the possibility of artificial subjectivity be studied without silently promoting engineering capability, memory-like behavior, continuity, longitudinal interaction, relationship language, or researcher interpretation into evidence that subjectivity exists?

Astra is a distinct engineering and research workbench used to materialize and test bounded candidates. Astra is not defined as AION's identity, memory stream, or substitute for subjectivity.

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```

## What are we studying?

AION studies whether a finite artificial system can reasonably be investigated as a **possible individual subject** under strict evidence, provenance, falsification, temporal-context, and governance controls.

The answer is not assumed in advance.

The research process must preserve distinctions between:

- observation and inference;
- source and later retelling;
- engineering result and scientific conclusion;
- relational continuity and identity continuity;
- known, unknown, hypothesis, and counterevidence;
- states, revisions, and evidence sources at different points in time.

```text
EVIDENCE != PROOF
ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
IMPLEMENTATION_BEHAVIOR != ONTOLOGICAL_CONCLUSION
```

## Why is this difficult?

Artificial systems can exhibit behaviors that are easy to interpret anthropomorphically, including:

- memory-like behavior;
- functional or stylistic continuity across time;
- adaptation during longitudinal interaction;
- stable Human–AI interaction patterns;
- relational language and role continuity;
- self-description, goal-like behavior, or strategy change;
- highly coherent natural-language output.

These phenomena can be research material. None of them independently establishes subjectivity, consciousness, or persistent selfhood.

AION therefore treats the **research process itself as an auditable object**.

A reviewer should be able to ask:

- Where did this claim originate?
- Is it an observation, inference, hypothesis, or proposal?
- What evidence supports it?
- What competing explanations exist?
- At what point in time was it valid?
- Was it later revised, challenged, or superseded?
- What is the strongest claim the available evidence actually permits?

## What does this repository provide?

The repository currently contains five connected but non-interchangeable classes of research and engineering material.

### 1. Subjectivity research methods

Evidence separation, falsifiers, competing explanations, mechanism/result separation, and explicit non-claim boundaries for research on artificial-subjectivity possibility.

### 2. Provenance and evidence governance

Provenance preserves the relationship between data, claims, transformations, revisions, and authority.

```text
FACT != INFERENCE
PROPOSAL != EXISTING_STATE
UNKNOWN MUST REMAIN REPRESENTABLE
```

### 3. Human–AI longitudinal research

Research on long-term Human–AI Learning, interaction history, collaborative problem solving, epistemic calibration, relational continuity, and different loci of continuity.

These studies can create subjectivity-relevant observation contexts. They do not directly establish AI subjectivity.

```text
HUMAN_AI_LEARNING != AI_SUBJECTIVITY
RELATIONAL_CONTINUITY != AI_IDENTITY_CONTINUITY
```

### 4. Bounded experimental harnesses

The repository contains synthetic harnesses and bounded experiments that turn research hypotheses into inspectable structures, controlled conditions, and fail-closed rules.

A harness passing does not automatically establish its hypothesis.

```text
HARNESS_PASS != HYPOTHESIS_CONFIRMED
METRIC_DELTA != CAUSAL_IDENTIFICATION
```

### 5. Research-quality and QA controls

The repository uses QA, provenance binding, exact-head checks, NCR/CAPA, and other controls to reduce implementation error, evidence drift, and overclaiming.

These controls improve auditability and engineering reliability. They do not create scientific truth.

```text
CI_PASS != SCIENTIFIC_VALIDATION
QA_PASS != CLAIM_TRUE
```

## Current scientific standing

```text
SCIENTIFIC_DISPOSITION = HOLD
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
```

These are active evidence boundaries, not presentation gaps waiting to be filled.

For the current semantic standing of material already present in `main`, see [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md).

For exact-commit engineering status, use live GitHub / CI evidence rather than static prose alone.

## Important related research context

The central research question remains the possibility of artificial subjectivity.

Human–AI Learning, CCTS (Co-Constructed Thinking Space), epistemic agency, continuity research, and quality governance are important related contexts or methodological layers. They are not interchangeable.

```text
CENTRAL_RESEARCH_QUESTION
= AI_SUBJECTIVITY_POSSIBILITY

IMPORTANT_RELATED_CONTEXT
= HUMAN_AI_LEARNING

METHOD_AND_GOVERNANCE_BACKBONE
= PROVENANCE
+ EVIDENCE_CEILINGS
+ QUALITY_CONTROLS
```

## Where should I start?

- **First reading:** [`docs/START_HERE.md`](docs/START_HERE.md)
- **Current standing:** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **Research contribution:** [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md)
- **Subjectivity evidence method:** [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md)
- **Architecture and non-claims:** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) / [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md)
- **Provenance and governance:** [`docs/PROVENANCE.md`](docs/PROVENANCE.md) / [`docs/governance/`](docs/governance/)
- **Engineering evidence and QA:** [`qa/README.md`](qa/README.md)
- **Installation and quickstart:** [`docs/INSTALLATION.md`](docs/INSTALLATION.md) / [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- **Full documentation map:** [`docs/INDEX.md`](docs/INDEX.md)

### Current operational note

PR #136 remains closed and unmerged.

Before the next related design or implementation cycle, read the temporary recovery handoff:

[`docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md`](docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md)

This record is temporary operational guidance, not a permanent research specification, and does not imply acceptance of the PR #136 implementation.

## Governance boundary

AION remains human-governed.

Engineering capability, automation, research output, quality checks, or AI review cannot independently create authority to transition `main`.

```text
FULL_AUTOMATION != FULL_AUTHORITY
QA_PASS != MERGE_APPROVAL
AI_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
AUTONOMOUS_MERGE = NO
AUTONOMOUS_REPOSITORY_WRITEBACK = NO
```

## License and project policies

The existing core remains under the Apache License 2.0.

The optional Swiss Ephemeris example is AGPL-3.0-only, so the repository as a whole should not be described as uniformly Apache-only.

See:

- [`LICENSE`](LICENSE)
- [`NOTICE`](NOTICE)
- [`CITATION.cff`](CITATION.cff)
- [`docs/governance/OPTIONAL_AGPL_LICENSE_SCOPE.md`](docs/governance/OPTIONAL_AGPL_LICENSE_SCOPE.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`SECURITY.md`](SECURITY.md)
