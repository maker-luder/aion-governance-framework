# POL-UPSTREAM-SUPPLIER-TRUST-001 — Freeze and Change-Control Record — 2026-08-08

- `STATUS = POLICY_CYCLE_FREEZE_AND_CAPA_RECORD`
- `GITHUB_BASELINE_REVIEWED = main@121d01e12adb7fd7c7a1da1233571773610feb33`
- `CANONICAL_EFFECT = NONE_UNTIL_OWNER_ACCEPTED_MERGE`
- `IMPLEMENTATION = NONE`
- `ACTIVE_ENFORCEMENT = NOT_ENABLED`

## Original policy freeze

The Human Owner and ChatGPT jointly reviewed `v0.1.1 PRE-FREEZE CANDIDATE`. The Owner reported no blocking issue at that review point and authorized progression to GitHub integration.

Anti-hindsight locks:

```text
KNOWN_VENDOR_CASE != CRITERION_GENERATOR
KNOWN_TEST_PASS != CRITERION_GENERATOR
```

## NCR-SUP-001 — Policy canonicalization / implementation gate conflation

**Discovery:** GitHub integration planning after the first acceptance-criteria freeze.

**Issue:** the initial `AC-SUP-*` criteria combined normative policy canonicalization with future executable schema/integration tests while the authorized policy scope explicitly remained `IMPLEMENTATION = NONE`.

**Root cause:** future engineering implementation had been implicitly assumed during test-design work.

**CAPA accepted by Human Owner:**

1. Preserve the original `AC-SUP-*` acceptance set as a future implementation baseline.
2. Create a separate `PC-*` Policy Canonicalization Gate.
3. Do not claim executable implementation or active enforcement from policy publication.
4. Require a future separate Owner authorization before any executable implementation.

- `NCR-SUP-001_STATUS = CAPA_ACCEPTED`
- `NORMATIVE_POLICY_CORE_CHANGE = NO`

## NCR-SUP-002 — Frozen release manifest scope conflation

**Discovery:** GitHub write preparation.

**Issue:** the initial GitHub integration plan proposed updating `manifest/FILE_MANIFEST.json` and `manifest/SHA256SUMS.txt` for this governance change. Repository inspection showed that the existing Quality workflow verifies the manifest against the frozen `v0.1.0-rc.1` release, not as a live main-branch inventory.

**CAPA:**

1. Do not modify the frozen release manifest for this policy-only branch.
2. Record package-specific integrity references in the policy QA evidence index instead.
3. Preserve frozen-release evidence independently from later governance documentation.

- `NCR-SUP-002_STATUS = CAPA_APPLIED_IN_BRANCH_CANDIDATE`
- `FROZEN_RELEASE_MANIFEST_MUTATION = NONE`

## NCR-SUP-003 — Provenance verb ambiguity

**Discovery:** final PR review before merge.

**Issue:** provenance text used `IMPLEMENTED_BY = CHATGPT` for policy-document work while the same policy explicitly states `IMPLEMENTATION = NONE`. This could be misread as executable supplier-trust enforcement having been implemented.

**CAPA accepted by Human Owner:** preserve the full ChatGPT contribution with role-specific attribution:

```text
POLICY_FORMALIZED_BY = CHATGPT
CROSSWALK_SYNTHESIZED_BY = CHATGPT
PRE_PROMOTION_QA_BY = CHATGPT
EXECUTABLE_IMPLEMENTED_BY = NONE
```

- `NCR-SUP-003_STATUS = CAPA_ACCEPTED_AND_APPLIED`
- `SOURCE_ATTRIBUTION_PRESERVED = YES`
- `NORMATIVE_POLICY_CORE_CHANGE = NO`

## NCR-SUP-004 — Evidence-strength enum drift

**Discovery:** final PR review before merge.

**Issue:** the Anthropic/Mythos validation record used `EVIDENCE_STRENGTH = MODERATE_TO_HIGH`, but the frozen policy enum permits only `UNASSESSED | LOW | MODERATE | HIGH | VERY_HIGH`.

**CAPA accepted by Human Owner:** normalize the formal field to:

```text
EVIDENCE_STRENGTH = MODERATE
```

and preserve the qualitative meaning in a separate `STRENGTH_NOTE`, with reassessment permitted if the primary AISI technical record is incorporated directly.

- `NCR-SUP-004_STATUS = CAPA_ACCEPTED_AND_APPLIED`
- `EVIDENCE_ENUM_CONFORMANCE = RESTORED`
- `NORMATIVE_POLICY_CORE_CHANGE = NO`

## Change-control rule

Any post-freeze change to normative policy or criteria requires:

- reason
- provenance
- impact analysis
- Human Owner review
- affected revalidation

```text
POLICY_CANONICALIZATION != EXECUTABLE_IMPLEMENTATION
EXECUTABLE_IMPLEMENTATION != ACTIVE_ENFORCEMENT
```

## Provenance

- Fair supplier governance and same-ruler requirement: `PROPOSED_BY = HUMAN_OWNER`
- `POLICY_FORMALIZED_BY = CHATGPT`
- `CROSSWALK_SYNTHESIZED_BY = CHATGPT`
- `PRE_PROMOTION_QA_BY = CHATGPT`
- NCR-SUP-001 two-gate CAPA: `ACCEPTED_BY = HUMAN_OWNER`
- NCR-SUP-003 provenance CAPA: `ACCEPTED_BY = HUMAN_OWNER`
- NCR-SUP-004 evidence-enum CAPA: `ACCEPTED_BY = HUMAN_OWNER`
- `EXECUTABLE_IMPLEMENTED_BY = NONE`
- `CODEX_CONTRIBUTION_THIS_POLICY_CYCLE = NONE`
