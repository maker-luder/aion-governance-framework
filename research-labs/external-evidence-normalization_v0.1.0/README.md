# External Evidence Normalization Lab v0.1.0

Status: `RESEARCH_CANDIDATE`
Canonical effect: `NONE`
Main effect: `NONE`
Runtime effect: `NONE`

This research-only lab studies how external human/AI research reports can be admitted without silently upgrading their evidential strength.

## Research question

How can a public external report be normalized into a machine-checkable evidence class while preserving provenance, execution limits and epistemic boundaries?

The lab deliberately separates:

```text
STATIC_REVIEW
LOGICAL_REPRODUCTION
EXECUTED_REPLICATION
```

A report may be useful evidence without being eligible for the P5 replication registry.

## Core invariants

- `EXTERNAL_REPORT != EXECUTED_REPLICATION`
- `SELF_REPORTED_PASS != VERIFIED_PASS`
- `DESCRIPTOR_LABELED_SHA256 != CRYPTOGRAPHIC_SHA256`
- `STATIC_REVIEW != TEST_EXECUTION`
- `REPLICATION_ELIGIBLE != CANONICAL_PROMOTION`
- `RUNNER_SELF_IDENTIFICATION != INDEPENDENT_IDENTITY_VERIFICATION`
- `MAIN_EFFECT = NONE`
- `CANONICAL_EFFECT = NONE`

## Current gate behavior

`normalize_external_report(...)` preserves the declared execution class and evaluates whether the report has enough provenance to become an executed-replication candidate.

Executed replication currently requires:

- exact 40-character baseline git SHA;
- module references;
- fixture references;
- environment fingerprint;
- network mode and benchmark policy;
- real lowercase SHA-256 input/output digests;
- evidence references;
- search-trace references when execution used `PUBLIC_WEB`.

Static review and logical reproduction are accepted as their own evidence classes but remain ineligible for replication promotion.

A static review that presents a cryptographic output hash together with a bare `PASS`/`REPRODUCED` claim is rejected as internally inconsistent rather than silently upgraded.

## Origin of the research question

This lab was opened after Human Owner-supplied external AI reports exposed a practical interoperability problem: natural-language research reports can use terms such as `PASS`, `consistent`, `clean`, `hash` and `supported` more loosely than the repository's machine-governed schemas.

The implementation is a ChatGPT research-engineering materialization of that observed problem on the explicitly reopened research branch.

External report contents are not copied into this lab as authoritative facts. Runner identities remain attributable to their supplied reports unless independently verified.

## Verification

```bash
python -m pytest -q
python -m compileall -q src
```

## Non-claims

This lab does not establish that any external report is true, independently executed, identity-verified, canonical, or suitable for `main`. It does not alter P4/P5 historical results and does not grant any external actor repository write authority.
