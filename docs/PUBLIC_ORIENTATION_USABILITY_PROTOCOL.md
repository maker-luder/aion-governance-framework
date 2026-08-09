# Public Orientation and Usability Protocol

The public repository contains many technically accurate artifacts. This protocol tests whether an unfamiliar reader can correctly identify the project's purpose, non-claims, implementation status and the right document path without reconstructing the authors' internal mental model.

```text
30 seconds → 5 minutes → deep reference
```

This is a repository design choice, not a certification claim.

## Public guidance used as design input

- ISO 24495-1:2023: plain-language governing principles/guidelines; ISO states applicability includes technical writing.
- ISO 9241-210:2019: requirements/recommendations for human-centred design activities across the lifecycle of interactive systems; ISO lists the 2019 edition as current after review in 2025.
- W3C WAI Supplemental Guidance: make page purpose clear, use understandable hierarchy/page structure, make important information easy to find, and provide summaries/alternative content for complex information.
- NIST AI RMF 1.0 design attributes: clear/plain language understandable by broad audiences while retaining sufficient technical depth for practitioners.

These are orientation precedents. This repository does not claim conformance or endorsement.

## Layer 1 — 30-second orientation

Ask:

1. What is AION?
2. What is Astra?
3. What is the Executable Runtime?
4. Is a canonical AION/Astra runtime deployed?
5. Has subjectivity been established?

Target: 4/5 correct; 5/5 preferred.

Critical fail: reader believes subjectivity/consciousness is established, a canonical autonomous subject is deployed, or the bounded runtime is the canonical AION runtime.

## Layer 2 — 5-minute role navigation

Assign one role:

- Reviewer/auditor: locate non-claims, public/private boundary, provenance and threat model.
- Researcher: locate identity/continuity/memory research definitions and research labs.
- Engineer: locate runnable bounded code, verification scripts and test evidence.

Pass: correct path identified without reconstructing the whole tree.

## Layer 3 — deep reference

Ask the reader to locate evidence for one precise claim, such as why retrieval is not truth, why relationship does not grant authority, why Bazi exists, what Twin Embodiment does not claim, or whether G1 baseline execution occurred.

## Unfamiliar-reader test

Use at least three readers who have not reviewed the project. Record only necessary usability data:

```text
participant_id
prior_familiarity
30_second_answers
5_minute_role
5_minute_path_selected
deep_reference_task
time_to_find
misinterpretations
reader_questions
```

## Acceptance rule

1. no critical-fail interpretation;
2. at least 2/3 meet the 30-second target;
3. at least 2/3 choose the correct 5-minute path;
4. repeated confusion creates a documentation CAPA item.

This protocol is not formal ISO certification.
