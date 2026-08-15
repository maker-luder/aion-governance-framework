# PR #23 Governance Control Closure Record

**Artifact status:** `CONTROL_CLOSURE = OPEN`

**Remediation PR:** [#27](https://github.com/maker-luder/aion-governance-framework/pull/27)

**Artifact commit:** `580aba11611c261e7d5a03c56d64ff41c213f505`
**Prepared by:** Manus AI as implementation and evidence-producing agent  
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
| `PLATFORM_ENFORCEMENT` | `VERIFIED` by live ruleset readback and negative API merge rejection on PR #25. |
| `NEGATIVE_TEST` | `PASS` |
| `NEGATIVE_TEST_MEANING` | `GATE_FAIL_CANNOT_MERGE` |
| `POSITIVE_TEST` | `NOT_EXECUTED` |
| `POSITIVE_TEST_MEANING` | `ALL_REQUIRED_GATES_PASS_ENABLE_ELIGIBILITY` remains unverified because Human Owner approval was not provided. |
| `ADMIN_BYPASS_STATUS` | No ruleset bypass actors were returned. Administrator/owner exception behavior was not certified by a positive authorization test. |
| `OWNER_BYPASS_STATUS` | No ruleset bypass actors were returned. Human Owner approval remains an external authority boundary and was not simulated. |
| `RESIDUAL_RISK` | Positive eligibility test is outstanding; legacy branch-protection endpoint returned 404; administrator/owner exception semantics remain explicitly unclosed. |
| `CONTROL_CLOSURE` | `OPEN` |
| `CANONICAL_EFFECT` | `NONE` |
| `DEPLOYMENT` | `FALSE` |
| `NEW_RESEARCH` | `NONE` |

## Root cause and corrective action

PR #23 targeted `main` at exact head `dd2af70d93792e7bb1e84e853d99df1a3c9d1f6e` and merged at `2026-08-15T14:02:12Z` into merge commit `3819f2eae763fd4de6b6d3c63f9beba3db014705`. Its `Main Transition Authority Gate` check failed because the Human Owner receipt timestamp was not fresh for the PR-body edit event. The two checks that GitHub actually required at that time, `Python 3.11` and `Python 3.12`, passed. Consequently, workflow execution and workflow failure were not connected to platform merge enforcement.

The minimal corrective action was applied at the GitHub platform layer rather than by modifying research or historical content. Active ruleset `Main Protection` (`20545803`) now requires the existing Authority Gate job context `Fresh exact-head Human Owner approval receipt` in addition to the two existing Python checks. The ruleset still targets `~DEFAULT_BRANCH`, remains active, retains pull-request, deletion, and non-fast-forward protections, and returned no bypass actors.

## Verification evidence

The disposable negative control was PR [#25](https://github.com/maker-luder/aion-governance-framework/pull/25), head `26de721573a0f4210a1aab8e92dc86dc82be1b9c`. Its Quality checks passed while the Authority Gate failed. GitHub reported `mergeStateStatus = BLOCKED`, and an API merge attempt was rejected with HTTP 405 because the required Authority check was failing. PR #25 was closed without merge.

A disposable positive control was opened as PR [#26](https://github.com/maker-luder/aion-governance-framework/pull/26), head `bedcf6a6a56fa6f5c79e3806384f6519817b492a`. It was intentionally not authorized for a Human Owner body edit. No approval was inferred, simulated, or delegated. PR #26 was closed without merge, so the positive eligibility criterion remains `NOT_EXECUTED`.

The historical record remains available at [PR #23](https://github.com/maker-luder/aion-governance-framework/pull/23) and [PR #24](https://github.com/maker-luder/aion-governance-framework/pull/24). The repository’s current main snapshot at audit time is `d7de6a52585b5d9ee7bcdc3d0b748b75d512f6e0`. The protected research lineage `review/four-domain-research-materialization` was not modified.

## Exact provenance

| Evidence | Exact reference |
|---|---|
| Historical PR #23 head | `dd2af70d93792e7bb1e84e853d99df1a3c9d1f6e` |
| Historical PR #23 merge | `3819f2eae763fd4de6b6d3c63f9beba3db014705` |
| Current main at audit | `d7de6a52585b5d9ee7bcdc3d0b748b75d512f6e0` |
| Active ruleset | [Ruleset API resource](https://api.github.com/repos/maker-luder/aion-governance-framework/rulesets/20545803), updated `2026-08-15T14:52:13.759Z` |
| PR #23 failing Authority runs | [Run #31](https://github.com/maker-luder/aion-governance-framework/actions/runs/31888661555), [Run #32](https://github.com/maker-luder/aion-governance-framework/actions/runs/31888805797), [Run #33](https://github.com/maker-luder/aion-governance-framework/actions/runs/31888907477) |
| PR #23 Quality run | [Quality #392](https://github.com/maker-luder/aion-governance-framework/actions/runs/31888661603) |
| Negative test | [PR #25](https://github.com/maker-luder/aion-governance-framework/pull/25) |
| Positive test, not executed | [PR #26](https://github.com/maker-luder/aion-governance-framework/pull/26) |

## Authority boundary

Manus did not merge PR #25 or PR #26, did not alter PR #23 history, did not modify the research branch, and did not declare Human Owner approval, ChatGPT approval, canonical promotion, deployment, or governance closure. The record remains `OPEN` until an authorized Human Owner decides whether to perform the positive eligibility test and whether the residual risks are acceptable.

## References

[1]: https://docs.github.com/en/pull-requests/reference/status-checks "GitHub Docs — Status checks"
[2]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches "GitHub Docs — About protected branches"
[3]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository "GitHub Docs — Creating rulesets for a repository"
