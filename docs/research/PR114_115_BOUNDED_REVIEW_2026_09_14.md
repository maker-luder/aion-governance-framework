# PR #114 / #115 bounded follow-up review — 2026-09-14

Status: `DRAFT_CANDIDATE / HUMAN_OWNER_AND_CHATGPT_TEACHER_REVIEW_PENDING`

## Scope and provenance

Human Owner requested implementation reinforcement of #114 and #115 in at most one new Draft PR, without merging. GPT proposed the specific repairs and the analytical clarification below. Prior merge receipts are not inherited. No other open candidate is resumed or modified.

Live baseline read from GitHub:

```text
DEFAULT_BRANCH = main
MAIN_HEAD = 738f154921ed5f9f6216255481290d67c845cd5e
MAIN_TREE = 47ed59c78f985746dae2ece00a3048c8559b61fe
PR114_HEAD = 7ae35cf4eb2d71a92388d0c047c656c655f23a22
PR114_STATE = MERGED
PR115_HEAD = b99d7c2f2860140d346cd8e4ce5883cc98d2570f
PR115_STATE = MERGED
```

## Findings and repair mapping

| Source | Finding | Bounded response |
|---|---|---|
| #114 archival intent | Agency/subjectivity admissibility wording can invite substitution of functional agency for subjective evidence | Add a prospective review table and explicit distinction; no maintenance runtime is justified by an archival question |
| #115 scanner self-exemption | An invisible marker placed in `scripts/scan_public_tree.py` was skipped entirely | Retain only the pre-existing secret/path-pattern self-exemption; apply Unicode detection to scanner source |
| #115 retained-evidence classification | Directory/suffix names alone admitted new or modified invisible-marker content as retained evidence | Require exact path and raw-byte SHA-256 for the two existing reviewed artifacts |
| #115 interpretation | Conservative character rejection is not proof of covert marking | Document legitimate Unicode uses, false-positive and uncovered-channel limits; report Unicode database version |

The first row is GPT's interpretive-risk assessment, not a demonstrated scientific error. The scanner rows are executable control gaps. No hidden watermark intent or exploitation is alleged from a code-point finding.

## Verification and adversarial review

Local snapshot was reconstructed from the exact GitHub tree using local Git objects plus connector-fetched missing blobs. Every baseline file was checked against its Git blob SHA before edits. This is content verification, not a claim of a successful network clone or a complete local history checkout.

- 20 focused watermark tests pass, covering prior behavior plus scanner self-coverage, directory-name bypass, exact retained bytes, rename, append and line-ending tampering, and repeated BOM positioning.
- 37 combined watermark/release-tooling/workflow-integrity tests pass.
- Focused Ruff checks pass.
- Full public-tree scanner passes with zero errors and 36 retained marker signals. The two historical evidence files remain byte-identical.
- Remote Quality and CodeQL results must be checked on the final candidate head. Local results do not substitute for those checks. The main-transition authority gate must remain HOLD without a new exact-head approval; this round explicitly forbids merge.

Adversarial review: moving a new file into `sources`, `incident-originals` or `qa` no longer grants retention. Copying a pinned artifact elsewhere or changing its bytes loses retention. Deliberately changing the scanner or its mapping can still change policy, so code review remains required. Generated exclusions, symlink targets, ordinary variation selectors and non-text channels remain outside this bounded repair. No universal security or watermark-absence guarantee is made.

## Source use and human review

The adjacent [intent clarification](LONG_HORIZON_SELF_MAINTENANCE_INTENT_2026_09_14.md#bounded-follow-up-clarification--2026-09-14) identifies the two research abstracts and the limits of their relevance. The [provenance policy](../PROVENANCE.md#source-grounded-limitations-and-review-2026-09-14) identifies Unicode first-party sources and the engineering translation. These are source-grounded review notes, not new admitted research evidence or a claim that an entire upstream framework was learned.

Human Owner and ChatGPT Teacher should inspect the five-file diff, the exact retained hashes, prospective review conditions, remaining detector limits, and exact-head CI before considering any later action.

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
SELF_MAINTENANCE_RUNTIME = NONE
NEW_EXECUTABLE_RESEARCH_AXIS = NONE
SCIENTIFIC_DISPOSITION = HOLD
MERGE_AUTHORIZATION = NOT_GIVEN
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
