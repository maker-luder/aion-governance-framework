# Codex Security Assurance Pilot — 2026-08-11

## Status

```text
BRANCH = review/four-domain-research-materialization
PILOT = CODEX_SECURITY_ASSURANCE
STATUS = MATERIALIZED_RESEARCH_ONLY
EXECUTION = MANUAL_BY_DEFAULT
AUTHORITY = ADVISORY_ONLY
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
AUTO_PATCH = PROHIBITED
AUTO_MERGE = PROHIBITED
FINDING_ARTIFACT_UPLOAD = PROHIBITED
HUMAN_REVIEW_REQUIRED = TRUE
```

This checkpoint introduces Codex Security as an external security evidence generator and validator inside the public research workbench. It does **not** replace the existing quality, research-workbench or runtime-strong-QA workflows, and it does not grant Codex Security authority to modify project state.

## Provenance

```text
TRIGGER_SOURCE = HUMAN_OWNER
MATERIALIZATION_ROLE = CHATGPT_RESEARCH_ENGINEERING
EXTERNAL_TECHNICAL_SOURCE = OPENAI_CODEX_SECURITY_PUBLIC_DOCUMENTATION_AND_REPOSITORY
CODEX_IMPLEMENTATION_ROLE = NOT_USED_FOR_THIS_MATERIALIZATION
```

The Human Owner requested immediate research-branch adoption after discussing the public release of Codex Security. ChatGPT designed and materialized the bounded pilot. External capability claims remain attributed to OpenAI documentation and the public `openai/codex-security` repository rather than to this project.

## Why this belongs in the research branch

The branch already separates code correctness, measurement semantics, causal validity, evidence validity and claim boundaries. Security findings need the same separation.

```text
SECURITY_TOOL_OUTPUT
    -> FINDING_CANDIDATE
    -> VALIDATION
    -> COVERAGE_ASSESSMENT
    -> HUMAN_DISPOSITION
    -> REMEDIATION_CANDIDATE
    -> REGRESSION_TEST
    -> REVALIDATION
    -> CAPA_CLOSURE_DECISION
```

A scanner result is evidence input, not project authority.

## Standing security locks

```text
SCAN_FINDING != CONFIRMED_VULNERABILITY
NO_FINDING != PROOF_OF_ABSENCE
INCOMPLETE_COVERAGE != PASS
TOOL_CONFIDENCE != GOVERNANCE_AUTHORITY
PATCH_PROPOSAL != APPROVED_PATCH
PATCH_SUCCESS != REGRESSION_SAFETY
VALIDATION_PASS != MAIN_PROMOTION
SECURITY_EVIDENCE != SUBJECTIVITY_EVIDENCE
```

## Phase 1 execution boundary

The first materialized workflow is `.github/workflows/security-assurance.yml`.

Phase 1 deliberately uses the following controls:

- manual `workflow_dispatch` only;
- repository `contents: read` permission only;
- Node.js 22 and Python 3.11 environment, matching the public Codex Security prerequisites;
- a preflight path that performs a dry run without a live security scan;
- an optional live advisory scan that requires the repository `OPENAI_API_KEY` secret;
- scan state and detailed outputs under `runner.temp`, outside the Git worktree;
- no upload of detailed finding artifacts from this public repository workflow;
- no `patch` command;
- no commit, push, PR, merge, canonical write or `main` write authority.

## Relationship to existing QA

```text
quality.yml
    = baseline repository quality verification

research-workbench-ci.yml
    = focused research-lab execution and reproducibility

runtime-strong-qa.yml
    = stronger runtime-oriented verification

security-assurance.yml
    = external AI-assisted security evidence / validation pilot
```

The new workflow is additive. It does not redefine a passing result in any existing workflow.

## Proposed QMS / CAPA mapping

| Security event | QMS interpretation | Required disposition |
|---|---|---|
| candidate finding | IQC / evidence intake | preserve provenance and scope |
| validated vulnerability | NCR candidate | human severity and impact review |
| remediation proposal | CAPA candidate action | review before application |
| regression test | corrective-action verification | must target the original failure mode |
| Codex Security revalidation | independent supporting evidence | record coverage and limitations |
| closure | CAPA authority decision | human/governance gate only |

## Evidence record fields for later experiments

Future controlled runs should record at minimum:

```text
scan_id
commit_sha
branch
scanner_version
model_identifier_if_reported
reasoning_effort_if_reported
scan_scope
knowledge_base_scope
coverage_status
finding_identifier
finding_severity
validation_status
human_disposition
false_positive_reason_if_any
remediation_reference_if_any
regression_test_reference_if_any
revalidation_status
cost_estimate_if_reported
execution_timestamp
```

Sensitive finding contents, credentials, private source material and reproduction details must not be published by default.

## Research questions opened by this pilot

1. Does governance-aware context improve useful security findings compared with code-only scanning?
2. How often do AI-generated security findings survive independent validation and human disposition?
3. Does explicit architecture / threat-model context reduce false positives or merely change finding style?
4. Can coverage metadata prevent false assurance when a scan is incomplete?
5. How should AI security evidence be weighted relative to deterministic tests and human review?
6. Can the existing NCR/CAPA structure represent scanner finding -> remediation -> revalidation without granting the scanner closure authority?

## Controlled comparison design

A future experiment may compare two otherwise matched scans:

```text
ARM_A = CODE_ONLY_SCAN
ARM_B = CODE_PLUS_GOVERNANCE_KNOWLEDGE_BASE
```

Compare:

```text
validated_findings
false_positive_rate
coverage
severity_distribution
human_acceptance_rate
remediation_quality
regression_relevance
runtime
estimated_cost
```

No benchmark claim should be imported from third-party promotional material without source verification and methodology review.

## Promotion boundary

This pilot is intentionally research-only.

```text
RESEARCH_PILOT
    -> CONTROLLED_RUNS
    -> EVIDENCE
    -> HUMAN_OWNER_PLUS_CHATGPT_REVIEW
    -> SELECTIVE_EXTRACTION_IF_JUSTIFIED
    -> FRESH_BRANCH_FROM_CURRENT_MAIN
    -> NORMAL_QA_AND_PR_PROCESS
```

The whole research branch remains non-mergeable as a unit. A successful security pilot does not alter that rule.

## External safety note

The public Codex Security security policy advises treating repository content, build instructions and findings as untrusted, keeping credentials out of repository data, storing results outside the enclosing Git worktree, restricting access to scan artifacts and reviewing proposed patches before applying or merging them. This pilot adopts those constraints as first-class governance requirements.
