# Codex Local Recovery and ChatGPT Reconstruction — 2026-08-09

## Status

```text
SOURCE_PACKAGE = HUMAN_OWNER_PROVIDED_GOOGLE_DRIVE_COPY
DRIVE_ACCESS = READ_ONLY
REMOTE_RESEARCH_BASELINE = 9729ee789d214f01aa5d55987821dbfc5d4eb1f4
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
```

## Source lineage

The Human Owner supplied a Google Drive copy of a local Codex working tree after Codex could no longer complete the remote Git operations.

Codex reported that the local work included:

- structural relationships and drift analysis for core meaning commitments;
- public research-source and privacy-boundary documentation;
- synthetic test data;
- core module: 27 passed;
- P1–P5 plus core: 69 passed;
- public-tree scan: PASS;
- AST syntax check: PASS;
- no commit or push had been completed;
- `main` had not been touched.

## What was recoverable from Drive

The connected Drive folder exposed the updated root research documents, including:

- `README.md`;
- `RESEARCH_BRANCH_STATUS.md`;
- `AI_EXPERIMENT_GUIDE.md`.

Those documents explicitly record the reopened research-only growth boundary and the core-meaning structure/drift/fingerprint extension.

The nested local Python source tree was not exposed through the supplied Drive folder structure available to ChatGPT. Therefore this commit does **not** claim byte-for-byte recovery of Codex's local implementation.

## Reconstruction boundary

ChatGPT independently reconstructed a compatible research-only extension against the existing remote `core-meaning-commitments_v0.1.0` API:

- explicit relation graph;
- deterministic structure fingerprint;
- same-scope structural drift comparison;
- synthetic fixture;
- 11 extension tests.

The 11-test extension plus the 16 pre-existing core tests yields 27 core tests by structural count. Together with the existing 42 P1–P5 tests, the aggregate is 69, matching the Codex local report.

```text
MATCHING_TEST_COUNT != BYTE_IDENTICAL_RECOVERY
CHATGPT_RECONSTRUCTION != CODEX_IMPLEMENTATION
```

## Attribution

- Research-branch reopening and authorization: Human Owner.
- Local unpushed implementation/report: Codex.
- Drive transfer to this review path: Human Owner.
- Root-document recovery: copied from the Drive source package.
- Structure/drift Python reconstruction and tests: ChatGPT research engineering.

This separation is intentional and should remain visible in later review.

## Main branch boundary

No part of this recovery authorizes modification, merge, rebase, reset or promotion into `main`.
