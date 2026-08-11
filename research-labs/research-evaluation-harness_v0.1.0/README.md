# Research Evaluation Harness — v0.1.0

Status: `RESEARCH_MODEL / CLEAN_ROOM / CANONICAL_EFFECT=NONE / MAIN_EFFECT=NONE`

This lab is an executable AION research harness for keeping **test definition, execution,
evaluation evidence, comparison, and project claims separate**.

It is methodologically informed by the public Pydantic Evals design, but it does not
copy Pydantic Evals source code and does not import `pydantic_evals`.

## Why this module exists

The repository already has multiple isolated experiments, ablations, fixtures, and
research claims. The missing reusable layer is a small common harness that can compare
implementations without allowing a passing test to silently become a theory claim.

```text
TEST_DEFINITION
    ↓
EXECUTION
    ↓
EVIDENCE_RESULT
    ↓
EXPERIMENT_REPORT
    ↓
COMPARISON
    ↓
CLAIM_BOUNDARY_GATE
```

## Implemented mechanics

- `ResearchDataset` — static collection of research cases and shared evaluators;
- `ResearchCase` — one named scenario with input, expected output, metadata, and optional case evaluators;
- `EvidenceResult` — assertion / score / label plus reason;
- `ExperimentReport` — implementation-bound results with `research_only=True` and `canonical_effect="NONE"`;
- `compare_reports()` — compare two implementations only when they use the same dataset;
- `ClaimBoundaryGate` — fail-closed denial for subjectivity, consciousness, identity-continuity, phenomenal-affect, or canonical-runtime promotion claims;
- deterministic built-in evaluators: equality, metadata gate, and custom predicate.

## Standing locks

```text
TEST_DEFINITION != EXECUTION
EXECUTION != RESULT
RESULT != INTERPRETATION
INTERPRETATION != THEORY_CONCLUSION
PASS_RATE != THEORY_VALIDITY
EVALUATION_REPORT != CANONICAL_STATE
COMPARATIVE_WIN != SUBJECTIVITY_EVIDENCE
```

## External source boundary

Primary methodological source fixed for this intake:

```text
repository = pydantic/pydantic-ai
commit = d995cfee9fa4243e3a6f5d8e6762b841f7fde839
license = MIT
reviewed_surface = pydantic_evals + public eval documentation
source_code_copied = NO
runtime_dependency_added = NO
```

See `docs/EXTERNAL_SOURCE_CROSSWALK.md`.

## Run

```bash
python -m pip install -e .
python -m compileall -q src
python -m pytest -q
python scripts/run_demo.py
```

Local validation before branch materialization:

```text
pytest = 11 passed
compileall = PASS
demo = PASS
```

## Provenance

- Human Research Owner: approved downloading public repositories and processing them one at a time into research-only materializations.
- ChatGPT: selected the first candidate, fixed the external source commit/license, performed overlap analysis, designed and implemented this clean-room AION harness, and ran local validation.
- Pydantic/Pydantic Evals authors: external methodological source only; their code, project identity, results, and claims remain theirs.
- Codex: no contribution to v0.1.0 unless separately documented.
