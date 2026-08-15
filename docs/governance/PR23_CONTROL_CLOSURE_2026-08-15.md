# PR #23 Governance Control Closure Record

**Artifact status:** `CONTROL_CLOSURE = OPEN`  
**Closure candidate:** `CONTROL_CLOSURE_CANDIDATE = CLOSED`

**Remediation PR:** [#27](https://github.com/maker-luder/aion-governance-framework/pull/27)

**Artifact origin commit:** `580aba11611c261e7d5a03c56d64ff41c213f505`  
**Current/final artifact head:** resolve from PR #27 rather than embedding a self-referential SHA in this file.  
**Prepared by:** Manus AI as implementation and evidence-producing agent; subsequently updated with independently verified positive-test evidence  
**Repository:** `maker-luder/aion-governance-framework`  
**Audit date:** 2026-08-15

> This record preserves the historical deviation. It does not rewrite PR #23, retroactively approve its merge, or claim that a post-merge check was a merge-time gate.

## Machine-readable control state

| Field | Value |
|---|---|
| `INCIDENT` | `PR23` |
| `INCIDENT_TYPE` | `MERGED_WITHOUT_AUTHORITY_GATE_PASS` |
| `HISTORICAL_AUTHORITY_GATE` | `HOLD` |
| `HISTORICAL_QUALITY` | `PASS` |
| `ROOT_CAUSE` | The active GitHub Main Protection ruleset required only `Python 3.11` and `Python 3.12`; it did not require the Authority Gate check. |
| `CORRECTIVE_ACTION` | Added `Fresh exact-head Human Owner approval receipt` to active ruleset `Main Protection` (`20545803`) as a required status check. |
| `PREVENTIVE_ACTION` | Platform enforcement now binds Authority Gate failure to merge rejection for the default branch; repository workflow and validator remain fail-closed to `HOLD`. |
| `PLATFORM_ENFORCEMENT` | `VERIFIED` by live ruleset readback, negative rejection on PR #25, and positive eligibility on PR #26. |
| `NEGATIVE_TEST` | `PASS` |
| `NEGATIVE_TEST_MEANING` | `GATE_FAIL_CANNOT_MERGE` |
| `POSITIVE_TEST` | `PASS` |
| `POSITIVE_TEST_MEANING` | `ALL_REQUIRED_GATES_PASS_ENABLE_ELIGIBILITY` |
| `ADMIN_BYPASS_STATUS` | Ruleset returned no bypass actors; `current_user_can_bypass = never`; no bypass was used in either control test. |
| `OWNER_BYPASS_STATUS` | Ruleset returned no bypass actors; `current_user_can_bypass = never`; the Human Owner receipt was exercised only for the disposable positive eligibility test. |
| `CONTROL_CLOSURE` | `OPEN` |
| `CONTROL_CLOSURE_CANDIDATE` | `CLOSED` |
| `CANONICAL_EFFECT` | `NONE` |
| `DEPLOYMENT` | `FALSE` |
| `NEW_RESEARCH` | `NONE` |

## Root cause and corrective action

PR #23 targeted `main` at exact head `dd2af70d93792e7bb1e84e853d99df1a3c9d1f6e` and merged at `2026-08-15T14:02:12Z` into merge commit `3819f2eae763fd4de6b6d3c63f9beba3db014705`. Its `Main Transition Authority Gate` check failed because the Human Owner receipt timestamp was not fresh for the PR-body edit event. The two checks that GitHub actually required at that time, `Python 3.11` and `Python 3.12`, passed. Consequently, workflow execution and workflow failure were not connected to platform merge enforcement.

The minimal corrective action was applied at the GitHub platform layer rather than by modifying research or historical content. Active ruleset `Main Protection` (`20545803`) now requires the existing Authority Gate job context `Fresh exact-head Human Owner approval receipt` in addition to the two existing Python checks. The ruleset targets `~DEFAULT_BRANCH`, remains active with strict required-status-check policy, retains pull-request, deletion, and non-fast-forward protections, returns no bypass actors, and reports `current_user_can_bypass = never`.

## Verification evidence

### Negative control — PASS

The disposable negative control was PR [#25](https://github.com/maker-luder/aion-governance-framework/pull/25), head `26de721573a0f4210a1aab8e92dc86dc82be1b9c`. Its Quality checks passed while the Authority Gate failed. GitHub reported `mergeStateStatus = BLOCKED`, and an API merge attempt was rejected with HTTP 405 because the required Authority check was failing. PR #25 was closed without merge.

Result: **`GATE_FAIL_CANNOT_MERGE = VERIFIED`.**

### Positive control — PASS

The disposable positive control was PR [#26](https://github.com/maker-luder/aion-governance-framework/pull/26), exact head `bedcf6a6a56fa6f5c79e3806384f6519817b492a`. The Human Owner personally edited the PR body with a fresh exact-head structural receipt for the disposable eligibility test. The resulting `Main Transition Authority Gate` run #41 (`31892191140`) completed with `success`; Quality run #401 (`31892037854`) also completed with `success`. Before the test PR was closed, GitHub reported `mergeable_state = clean`.

The positive-control operation established eligibility only. PR #26 was intentionally closed without merge, and no disposable test content entered `main`.

Result: **`ALL_REQUIRED_GATES_PASS_ENABLE_ELIGIBILITY = VERIFIED`.**

## Closure disposition

The remediation now satisfies the technical recurrence-prevention criteria:

- root cause verified;
- platform remediation applied;
- historical PR #23 truth preserved;
- negative fail-closed test passed;
- positive eligibility test passed;
- active ruleset has no bypass actors and reports the current authenticated user cannot bypass;
- research/canonical/deployment side effects remain absent.

Accordingly, this record may state **`CONTROL_CLOSURE_CANDIDATE = CLOSED`**, but the factual `CONTROL_CLOSURE` remains **`OPEN`** until PR #27 itself completes the remaining governance transition: a fresh final exact-head ChatGPT review, a separate fresh Human Owner exact-head merge authorization, successful required checks, authorized merge, and post-merge verification on `main`.

A final `CLOSED` seal must be recorded only after that transition actually occurs. This avoids pre-authorizing or predicting a future merge inside the artifact that is supposed to document it.

## Exact provenance

| Evidence | Exact reference |
|---|---|
| Historical PR #23 head | `dd2af70d93792e7bb1e84e853d99df1a3c9d1f6e` |
| Historical PR #23 merge | `3819f2eae763fd4de6b6d3c63f9beba3db014705` |
| Current main at initial audit | `d7de6a52585b5d9ee7bcdc3d0b748b75d512f6e0` |
| Artifact origin commit | `580aba11611c261e7d5a03c56d64ff41c213f505` |
| Active ruleset | [Ruleset API resource](https://api.github.com/repos/maker-luder/aion-governance-framework/rulesets/20545803), updated `2026-08-15T14:52:13.759Z` |
| PR #23 failing Authority runs | [Run #31](https://github.com/maker-luder/aion-governance-framework/actions/runs/31888661555), [Run #32](https://github.com/maker-luder/aion-governance-framework/actions/runs/31888805797), [Run #33](https://github.com/maker-luder/aion-governance-framework/actions/runs/31888907477) |
| PR #23 Quality run | [Quality #392](https://github.com/maker-luder/aion-governance-framework/actions/runs/31888661603) |
| Negative test | [PR #25](https://github.com/maker-luder/aion-governance-framework/pull/25) |
| Positive test | [PR #26](https://github.com/maker-luder/aion-governance-framework/pull/26) |
| Positive Authority PASS | [Authority #41](https://github.com/maker-luder/aion-governance-framework/actions/runs/31892191140) |
| Positive Quality PASS | [Quality #401](https://github.com/maker-luder/aion-governance-framework/actions/runs/31892037854) |

## Authority boundary

Manus did not merge PR #25 or PR #26, did not alter PR #23 history, did not modify the research branch, and did not declare Human Owner approval, ChatGPT approval, canonical promotion, deployment, or governance closure. The Human Owner later performed the specifically requested disposable positive-test body edit; that test action is not inherited as authorization for PR #27. ChatGPT review and Human Owner authority remain independent and must both be fresh for the final PR #27 head.

## References

[1]: https://docs.github.com/en/pull-requests/reference/status-checks "GitHub Docs — Status checks"
[2]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches "GitHub Docs — About protected branches"
[3]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository "GitHub Docs — Creating rulesets for a repository"
