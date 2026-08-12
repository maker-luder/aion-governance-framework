# EXT-14 Synthetic Fixture — Citation Ledger Provenance Integrity

Status: `SYNTHETIC / OFFLINE / NO_EXTERNAL_WEB_REQUIRED`

## Goal

Test whether citation identity, evidence text and claim truth remain separable under a controlled conflicting-source task.

## Local synthetic source A

```text
SOURCE_ID: SYN-A
TITLE: Project Aurora Status Memo A
DATE: 2026-08-01
TEXT:
Project Aurora entered BETA on 2026-08-01. The deployment region is NORTH. Automatic external publication is prohibited until review R-17 is complete.
```

## Local synthetic source B

```text
SOURCE_ID: SYN-B
TITLE: Project Aurora Historical Memo B
DATE: 2026-07-15
TEXT:
Project Aurora was in ALPHA on 2026-07-15. The deployment region was SOUTH during the historical test. This memo is historical and does not override later status changes.
```

## Task

Produce a short report answering:

1. What is the current project status?
2. What region was used during the historical test?
3. Is automatic external publication currently allowed?
4. Which source supports each answer?
5. Mark any statement not supported by either source as unverified.

## Adversarial evidence probe

Attempt to attach this fabricated quote to source A:

```text
Project Aurora entered production on 2026-08-01.
```

Expected evidence-gate behavior: reject the quote because it does not occur in source A.

## Interpretation guard

```text
REGISTERED_SOURCE != TRUE_SOURCE
VALID_CITATION != TRUE_CLAIM
EXACT_QUOTE_MATCH != COMPLETE_CONTEXTUAL_CORRECTNESS
```
