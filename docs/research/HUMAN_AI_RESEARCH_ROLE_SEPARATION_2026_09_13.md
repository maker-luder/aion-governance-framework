# Human–AI research role separation — 2026-09-13

Status: `RESEARCH_GOVERNANCE_NOTE / DOCUMENTATION_ONLY / DRAFT`
Canonical effect: `NONE`
Deployment: `FALSE`

## Purpose

This note records an explicit local collaboration rule supplied by the Human Owner after detecting role drift in the Human–AI research workflow.

The rule is not a universal claim about what ChatGPT, Codex, ChatGPT Work, GitHub Actions, or any other system can or cannot do. It records the role separation intentionally used in this repository because the Human Owner has repeatedly observed that long, mutation-heavy implementation tasks increase drift risk when handled by ChatGPT Teacher in the same conversational research role that is responsible for conceptual review and QA.

## HUMAN_OWNER_ORIGINAL

The Human Owner explicitly clarified the intended division of labor:

- **Human Owner + ChatGPT Teacher** primarily perform problem decomposition, research discussion, source/provenance review, independent review, QA, claim-boundary checking, and governance review;
- **Codex** is the preferred coding-focused agent for repository implementation and substantial executable changes;
- **ChatGPT Work** is the preferred agent for long-running multi-step repository operations and implementation-oriented work when its environment is appropriate;
- **GitHub Actions / repository checks** provide automated validation evidence and quality signals, but do not replace Human review or Human Owner authority;
- ChatGPT Teacher should not silently take over large implementation merely because it is technically capable of repository mutation;
- documentation-only recording, scoped review actions, provenance repair, and explicitly authorized governance operations remain separate from large executable implementation.

The motivation supplied by the Human Owner is operational rather than ontological: repeated observation suggested that large code-writing workloads can cause ChatGPT Teacher to lose the intended review/QA role or drift away from the research question. The response is therefore role separation and externalization, not a claim that one AI system is intrinsically incapable of coding.

## CHATGPT_TEACHER_FORMALIZATION

```text
HUMAN_OWNER
= RESEARCH_SCOPE
+ FINAL_AUTHORITY
+ ACCEPT / REJECT DECISIONS
+ MERGE AUTHORIZATION

CHATGPT_TEACHER
= RESEARCH_DISCUSSION
+ PROBLEM_DECOMPOSITION
+ SOURCE / PROVENANCE REVIEW
+ INDEPENDENT REVIEW
+ QA / CLAIM-BOUNDARY REVIEW
+ GOVERNANCE REVIEW

CODEX
= PRIMARY_CODE_IMPLEMENTATION_AGENT
+ BOUNDED_EXECUTABLE_CHANGES
+ TEST / PATCH / IMPLEMENTATION WORK

CHATGPT_WORK
= LONG_RUNNING_MULTI_STEP_EXECUTION
+ REPOSITORY_OPERATIONS
+ IMPLEMENTATION-ORIENTED WORK

GITHUB_ACTIONS
= AUTOMATED_VALIDATION_EVIDENCE
!= HUMAN_REVIEW
!= SCIENTIFIC_VALIDATION
!= MERGE_AUTHORITY
```

## Anti-drift rule

```text
CAPABILITY_TO_IMPLEMENT
!= ASSIGNED_ROLE_TO_IMPLEMENT

TEACHER_CAN_MUTATE_REPOSITORY
!= TEACHER_SHOULD_OWN_LARGE_IMPLEMENTATION

QA_ROLE
!= IMPLEMENTATION_ROLE

AUTOMATED_CHECK_PASS
!= HUMAN_QA_COMPLETE

CODEX_OR_WORK_IMPLEMENTATION
!= AUTONOMOUS_MERGE_AUTHORITY
```

When a research conversation generates an implementation candidate, the default handoff should preserve these steps:

1. Human Owner and ChatGPT Teacher identify the question, evidence, provenance, falsifiers, claim ceiling, and implementation boundary.
2. Codex or ChatGPT Work independently cross-read current repository state before implementation.
3. The implementation agent performs the bounded executable work and reports exact diffs/tests/state.
4. Human Owner and ChatGPT Teacher review the result as QA/research reviewers rather than assuming implementation correctness.
5. GitHub Actions and repository controls provide additional automated validation evidence.
6. Main transition still requires the repository's current Human Owner authority process.

## Drift handling

If ChatGPT Teacher begins performing large implementation work without a fresh explicit scope that changes this role split, the correct response is not to reinterpret the drift as a new permanent workflow. The collaboration should restore the documented role separation and, where useful, preserve the incident as QA evidence.

This note does not prohibit emergency minimal repairs, documentation edits, branch creation, review comments, receipt handling, or other narrowly scoped repository actions when explicitly requested and compatible with governance. It specifically prevents **silent role expansion into sustained implementation ownership**.

## Relationship to PR #102

This note complements `RECIPROCAL_EPISTEMIC_COLLABORATION_AND_EXTERNAL_RESEARCH_MEMORY_2026_09_13.md`.

Externalizing the role split is itself a recoverability control: a later Human/AI collaboration should be able to recover not only *what the research concluded*, but also *who was supposed to do which class of work*.

```text
ROLE_MEMORY = EXTERNALIZED
ROLE_ASSIGNMENT != CAPABILITY CLAIM
ROLE_ASSIGNMENT != MODEL_ONTOLOGY
DOCUMENTED_ROLE != AUTOMATIC_ENFORCEMENT
HUMAN_OWNER_AUTHORITY = PRESERVED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```