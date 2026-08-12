# Autonomous Pre-Merge Gate Repair — 2026-08-12

Status: `RESEARCH_ONLY / GOVERNANCE_INFRASTRUCTURE_REPAIR`

```text
TARGET = review/four-domain-research-materialization
PREMERGE_RESEARCH_GATES = REQUIRED
ALL_CANDIDATE_PATHS = TRUE
PULL_REQUEST_TARGET_EVENT = PROHIBITED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
```

## Problem

The first autonomous candidate correctly remained `HOLD` because its declared research-specific pre-merge checks were unavailable. Review found two closure defects:

1. `Research Workbench CI` originally ran only after a push to the research branch, so a candidate could be required to pass a check that did not run before merge.
2. Path-filtered `pull_request` validation could leave a later candidate head without fresh research-specific checks when the final change touched only documentation or another path outside the focused filter.

## Repair

For pull requests targeting the research branch:

- `Research Scope Lock` runs for every candidate path;
- `Research Workbench CI` runs for every candidate path;
- generic `Quality` is supplemental rather than a substitute;
- ordinary `pull_request` is used;
- `pull_request_target` is prohibited;
- workflow contents permissions remain read-only;
- first-party Actions remain pinned by full commit SHA;
- checkout credential persistence remains disabled.

Push-triggered Research Workbench CI may retain focused path filters for normal research-branch maintenance. The all-path rule applies to the pre-merge candidate surface.

## Machine-checkable contract

`AUTONOMOUS_GROWTH_CONTRACT.json` v1.1.0 records:

```text
TARGET_BRANCH = review/four-domain-research-materialization
REQUIRED_WORKFLOWS = Research Scope Lock + Research Workbench CI
REQUIRE_GREEN_BEFORE_INTEGRATION = TRUE
ALL_CANDIDATE_PATHS = TRUE
PULL_REQUEST_TARGET_EVENT = FALSE
```

`check_autonomous_growth_contract.py` fails closed if these conditions drift.

## Scientific boundary

This repair changes validation timing and governance infrastructure only.

```text
CI_SUCCESS != SCIENTIFIC_VALIDATION
TEST_PASS != THEORY_CONFIRMATION
PREMERGE_GATE_CLOSURE != SUBJECTIVITY_EVIDENCE
```

## Provenance

- Human Research Owner: authorized bounded autonomous growth and requested the later large repair after reviewing the first cycle.
- ChatGPT research review: identified and repaired the pre-merge gating deadlock and path-filter freshness defect.
- Codex research implementation: previously created the machine-checkable autonomous-growth contract/checker and CI hardening that this repair extends.
