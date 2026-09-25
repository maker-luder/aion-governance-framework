# Embodiment Research Toolchain Protocol

Status: `PROCESS DESIGN / DRAFT`  
Canonical effect: `NONE`

## Purpose

Define a repeatable plugin/tool workflow so research discovery, external model inspection, internal repository inspection, formal reduction, structural review, implementation planning and exact-head governance remain separated.

## Pipeline

```text
0  Superpowers — research design / scope
↓
1  Web — external discovery
↓
2  Hugging Face — exact asset inspection
↓
3  GitHub — internal live-state crosswalk
↓
4  Wolfram — formalization / minimization
↓
5  MindMap — structural dependency audit
↓
6  Superpowers — engineering spec / plan / TDD
↓
7  GitHub — bounded Draft PR implementation
↓
8  Teacher — reverse review
↓
9  Superpowers — verification-before-completion
↓
10 GitHub — exact-head CI and governance
↓
11 fresh Human Owner exact-head approval
↓
12 authority gate / merge / re-check main
```

## Stage 0 — Superpowers: research design

### Input
- research intent;
- repository constraints;
- scientific boundaries;
- success criteria.

### Output
- scoped design question;
- alternatives;
- architecture boundary;
- explicit nonclaims.

### Authority
Engineering design assistance only.

```text
SUPERPOWERS_OUTPUT != SCIENTIFIC_EVIDENCE
```

## Stage 1 — Web: discovery

### Input
- scientific gap;
- source class sought.

### Output
- exact model / dataset / paper / official-project candidates;
- DOI / canonical source;
- likely license and repository identifiers;
- current documentation.

### Non-authority
Web discovery does not establish internal repository state or scientific sufficiency.

## Stage 2 — Hugging Face: exact asset inspection

### Input
- exact HF model/dataset repository IDs found externally.

### Output
- exact repository metadata;
- model/dataset card;
- license metadata;
- gated state;
- file / framework details where available;
- linked paper / project metadata.

### Rule

```text
WEB = DISCOVERY
HF = EXACT_REPOSITORY_INSPECTION
```

HF existence or popularity is not validation.

## Stage 3 — GitHub: internal crosswalk

### Input
- external candidate representation;
- current research question.

### Output
- live main SHA;
- existing repository components;
- reusable structures;
- gap inventory;
- semantic conflicts;
- duplicate-work risk.

### Rule

```text
GITHUB = AUTHORITATIVE_REPOSITORY_STATE
```

No stale conversational memory may override live repository state.

## Stage 4 — Wolfram: formal reduction

### Input
- selected state variables and interactions.

### Output
- state-space formulation where applicable;
- controllability / observability checks;
- minimal-realization analysis;
- algebraic consistency checks.

### Non-authority

```text
WOLFRAM_MINIMAL != BIOLOGICAL_MINIMAL
FORMAL_CONSISTENCY != SCIENTIFIC_VALIDATION
```

## Stage 5 — MindMap: dependency audit

### Input
- architecture;
- biological layers;
- tool flow;
- work-package dependencies.

### Output
- human-readable structural map;
- missing dependency candidates;
- cycle / scope visualization.

### Non-authority

```text
STRUCTURAL_MAP != EVIDENCE
```

## Stage 6 — Superpowers: engineering design / plan

Use architectural design before implementation.

Outputs may include:

- spec;
- file boundaries;
- implementation plan;
- TDD sequence;
- debugging route;
- verification route.

No implementation begins until the applicable design gate has been approved.

## Stage 7 — GitHub: bounded implementation

Each implementation branch / Draft PR must correspond to one bounded work package.

Required constraints:

- no direct main write;
- allowed files explicit;
- forbidden scope explicit;
- exact upstream artifacts pinned;
- provenance recorded;
- rollback available where material.

## Stage 8 — Teacher reverse review

Reverse review explicitly checks:

- primary-source quality;
- exact revision;
- license interpretation;
- semantic non-equivalence;
- model convention vs biological fact;
- duplicate implementation;
- scope drift;
- renamed observable;
- hidden human ontology injection;
- identity / runtime confusion;
- alternative explanations;
- falsification completeness.

## Stage 9 — verification-before-completion

Before claiming completion:

- run the tests;
- inspect actual output;
- verify hashes;
- verify deterministic extraction;
- confirm schema validity;
- confirm scope diff;
- confirm no undocumented dependency.

```text
ASSERTION_REQUIRES_EVIDENCE
```

## Stage 10 — GitHub exact-head governance

Required before merge consideration:

- exact head SHA;
- diff review;
- Quality;
- CodeQL where applicable;
- mypy / component tests where applicable;
- scope review;
- mergeability;
- fresh exact-head approval receipt when governance requires it.

```text
CI_PASS != SCIENTIFIC_VALIDATION
AUTOMATION != AUTHORITY
```

## Tool routing table

| Question | Primary route |
| --- | --- |
| What scientific model exists? | Web |
| What exactly is inside this HF repo? | Hugging Face |
| What does our repository already contain? | GitHub |
| Is this state-space representation reducible? | Wolfram |
| How do these dependencies connect? | MindMap |
| How should we structure implementation? | Superpowers |
| Did the exact branch / CI actually pass? | GitHub |

## Fail-closed rules

Any stage may return `HOLD`.

Do not compensate for one unavailable tool by silently assigning its authority to another tool.

Examples:

- HF unavailable → exact HF inspection remains incomplete;
- Wolfram no result → formal claim remains unestablished;
- GitHub unavailable → live repository state remains unverified;
- Web source weak → external scientific basis remains provisional.

## Anti-recursion rule

The toolchain may be used to review the toolchain design itself, but the review stops after one complete reverse-review cycle unless a concrete defect is found.

```text
REVIEW_LOOP != INFINITE_PERFECTION_LOOP
```
