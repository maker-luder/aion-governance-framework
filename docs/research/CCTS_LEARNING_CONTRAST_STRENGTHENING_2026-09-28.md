# CCTS / Human–AI learning: bounded contrast strengthening

Date: 2026-09-28 (Asia/Taipei). Change class: **D**, with bounded component
validation changes. CCTS means **Co-Constructed Thinking Space**（共同建構思考空間）.
This is a synthetic engineering correction and research-design review.

## 1. Live-state baseline and scope

```text
REPOSITORY = maker-luder/aion-governance-framework
BASE_MAIN = 74e4f26dceec0ebf0b0afd78bd762054ef6d025d
BASE_TREE = 2fa612cc3b5b339906d8ebc4682a25106c2f3227
PR_224 = CLOSED / MERGED
PR_224_HEAD = 8dfcfa2ddaff9a8d80ddcebf93d8ccc44ae0a0de
PR_224_MERGE = 1dbe934cc95674754286b20240c14936c2ed51cb
FOLLOWUP_BRANCH = review/ccts-learning-contrast-hardening-20260928
```

GitHub's live branch, recursive tree, PR metadata and Actions runs were read.
Main includes #224 and the public-entry synchronization #225. The open-PR search
returned no entries at inspection time; do not assume this remains true later.
Main Quality run `36385412473` and CodeQL run `36405020773` were successful.
Those results belong to the baseline, not to the new candidate.

Only `learning_contrast_design.py`, its tests, the package README and this review
are changed. Existing CCTS admission, agency, exposure and empirical gates are
reused. No closed research branch is revived and no canonical CCTS definition,
embodiment surface, workflow, release manifest or other PR is modified.

## 2. Reproduced defects and bounded correction

| Defect at the baseline | Counterexample | Correction |
|---|---|---|
| Matched-field loop skipped `arms[0]`, even when that was the comparator | Put a comparator with an unrelated task family first; the audit still returned `complete_design=True` | Compare every arm against the selected CCTS reference, independent of container order |
| Each arm could redefine its own canonical order | Reverse `component_ids` and adjust original/repetition blocks to that local order; the shared set check still passed | Require the design-wide ordered component IDs; keep actual reordering in blocks |
| Re-representation layouts were validated individually but not matched across the intended contrasts | Give the comparator or no-judgment arm another valid reorganization, regenerating its canonical protocol where applicable | Require the two CCTS re-representation arms and the practice comparator to share blocks |

The last correction is an explicit tightening of the design contract. It holds
layout fixed when comparing judgment requirements or CCTS roles. Different
shared reorganizations remain valid; no preferred layout is hard-coded. Direct
answer and repetition retain their existing distinct transformations, visibility
and pass counts. A complete five-arm set is not a fully orthogonal factorial
design and cannot by itself isolate every mechanism.

Relation source role remains an independent provenance axis. An AI-origin
relation under a Human-judgment requirement remains representable, as required
by #224. This does **not** certify matched historical relation knowledge or a
source-specific causal comparison. No discovery claim is inferred from a label.

## 3. Evidence and alternative explanations

### E1 — Human retention: testing is also an intervention

Roediger & Karpicke (2006), *Test-Enhanced Learning*,
[DOI](https://doi.org/10.1111/j.1467-9280.2006.01693.x),
[author-hosted full text](https://learninglab.psych.purdue.edu/downloads/2006/2006_Roediger_Karpicke_PsychSci.pdf).

**External finding:** their prose-recall experiments distinguish restudy from
retrieval practice and compare immediate and delayed retention. Prior testing
can influence later performance; measuring is not necessarily neutral.
**Application here (analysis):** a delayed event after an immediate test cannot
automatically isolate retention attributable to CCTS. Retrieval practice,
feedback and intervening exposure must be specified. This study is not a test of
CCTS, AI subjectivity, or this repository's participants. Its results do not
supply an effect size or appropriate delay for our proposed protocol.

### E2 — Model behavior: ordinary configuration remains an alternative

[Qwen/Qwen3-8B official model card](https://huggingface.co/Qwen/Qwen3-8B),
sections “Quickstart” and “Switching Between Thinking and Non-Thinking Mode”.

**External artifact fact:** the card documents generation-mode controls through
the chat template and `enable_thinking`. **Application here (analysis):** model
configuration and prompt differences are plausible alternatives to attributing
changed interaction behavior to persistent model learning or subjective states.
This is a documented mechanism example, not a run, recommendation, comparison
result, or explanation of a particular proprietary model. No weights were
downloaded and no inference or training was executed. A future model-dependent
protocol must pin its own model revision and actual runtime configuration.

### Claim-to-evidence boundary

| Research axis | What this change strengthens | What remains unestablished |
|---|---|---|
| Core AI subjectivity question | Excludes an additional class of ordinary design/configuration explanations before interpreting observations | Subjectivity, consciousness, phenomenal experience, moral agency and moral status |
| Human–AI learning | Enforces structural matching and identifies test-induced learning as a rival explanation | Independent Human gain, delayed retention, transfer, persistent model learning |
| CCTS | Makes the existing layout/judgment/practice comparisons more internally consistent | CCTS-specific mechanism, causal effect, semantic equivalence, actual non-CCTS practice |

These are separations of evidence scope, not proofs that subjectivity is either
present or absent. Engineering conformance does not settle the core question.

## 4. Tool routing and limitations

Followed `docs/governance/PR_TOOL_ROUTING_MATRIX.md` with a Class D scope.

| Capability | Actual use / disposition |
|---|---|
| GitHub | Live refs, PR state, exact source bytes, workflow state and isolated PR publication |
| Superpowers | Bounded design, root-cause reproduction, test-first correction, review and verification |
| Web | Primary scholarly full text and official model-card reading |
| Consensus | Attempted once; monthly search quota exhausted. Primary-source web reading substituted; no Consensus evidence claimed |
| Scite | Exact E1 DOI metadata/citation-context lookup succeeded; full text was unavailable there and returned citation records did not establish replication or contrast. E1 full text was read through the author's public copy; no purchase |
| Hugging Face | External discovery followed by exact `Qwen/Qwen3-8B` lookup. The tool returned repository metadata, despite a README request; the official model card was separately read on the web |
| Context7 | Not triggered: no new external API or version-sensitive library behavior in the correction |
| Wolfram | Not triggered: no power estimate, effect-size calculation or statistical result is claimed |
| MindMap | Not triggered: the bounded dependency/claim map fits the tables above |

No tool output is merge authority or scientific validation. Literature/model-card
reading supplies constraints and alternative explanations, not CCTS evidence.

## 5. Engineering verification

Git transport was unavailable in this environment. An isolated **partial source
snapshot** was built from 48 GitHub-tree blob identities (the complete 47-file
study package plus Quality workflow). Existing local object bytes were reused
only after exact blob-hash verification; missing files were fetched from the
baseline SHA. This is not represented as a full remote-history checkout.

On Python 3.12.14, using existing local QA packages:

- Baseline package: **320 passed**.
- New targeted tests against unchanged production code: **8 failed, 30 passed**;
  the eight failures were acceptance of the invalid designs in Section 2.
- Corrected complete package: **335 passed**. The new positive permutation test
  exercises all 120 orders of the five arms; these are cases, not 120 new tests.
- Strict package mypy: **no issues in 19 source files**.
- Ruff correctness selection `E9,F`: passed; `git diff --check`: passed.

Package commands, run from `research-labs/human-ai-longitudinal-study_v0.1.0`:

```sh
python -m pytest -q
python -m mypy src/aion_human_ai_longitudinal
ruff check --select E9,F src tests
git diff --check
```

The session's default interpreter lacked pytest, so the installed cached QA
package directory was supplied on `PYTHONPATH`; no product dependency was added.
Local testing covers this package, not all repository controls or Python 3.11.
An independent read-only code review found no blocking defect and suggested
including the with-judgment arm in the committed layout-drift regression cases;
that case is included in the final 335-test run.
New-head remote Quality, CodeQL and authority-gate results must be read from the
new PR's Actions runs. Passing baseline or local checks never substitutes for
those results.

## 6. Deferred implementation handoff — not an experiment authorization

**Scope:** retain this adapter and its existing gates. Before any empirical
implementation, freeze the desired comparison and observation contract. The
following are documented gaps, not features claimed complete by this PR.

| Residual | Design decision and falsification requirement |
|---|---|
| Independent Human assessment | Specify AI/help availability and bind observed assessment conditions; same-task event IDs alone do not demonstrate independence |
| Retention versus test practice | Define immediate-test exposure, feedback and intervening practice. Choose a justified matched-testing or delayed-only comparison; null/adverse results remain admissible |
| Retention versus transfer | Bind distinct held-out assessment events if transfer is the claim. The current held-out control does not turn same-task events into transfer outcomes |
| Real CCTS/non-CCTS execution | Bind realized interaction/protocol traces, assignment and order/carryover control; distinct synthetic identities are insufficient |
| Model adaptation | Separate context, retrieval/history, configuration and parameter updates; record exact revisions and actual runtime state before attribution |
| Source provenance | Distinguish who supplied a relation, whether it was visible, and prior knowledge; Human judgment is not Human-origin discovery |

**Recovery:** reread remote main, this PR's exact head, open related PRs, changed
files and CI. If main/head changes, recompute the relevant diff and verification.
Do not restore #222/#199, reuse old merge approval, or overwrite an unknown tree.

**Expected later files:** this adapter, its existing test file and package README;
add a separately reviewed protocol document only after its decisions are frozen.
Reuse `ccts_human_epistemic_agency.py`, `task_selection_exposure_hardened.py` and
`empirical_gate.py`; do not duplicate their admission algorithms.

**Acceptance/tests:** future claims must have explicit observation bindings and
contamination controls, with negative fixtures for missing/rebound conditions,
unknown observations, mismatched testing exposure and scientific-claim promotion.
Run the full package plus the repository-required Quality and CodeQL checks on
the exact new head. Do not claim statistical power without a justified design,
outcome, variability estimate and analysis plan.

**Non-goals/authority:** no Human study, private data ingestion, model run,
canonical definition change, deployment or main merge is authorized by this
handoff. Those actions require their applicable fresh decisions. The present
user request authorizes this bounded strengthening PR, not empirical findings.

**Final report contract:** exact repository/base/branch/head/PR, changed files,
reproduced defects, local test environment and results, fresh remote workflow
identities/results, source limitations, remaining gaps, and next gate. State any
unperformed checks; retain scientific HOLD regardless of CI success.

## 7. Provenance and non-claims

```text
HUMAN_ORIGIN = request to inspect #224 and strengthen core / Human-AI learning / CCTS
AI_FORMALIZATION = counterexamples, bounded code correction, evidence-scope analysis
EXTERNAL_SOURCE = E1 and E2, within their stated limits
REPOSITORY_STATE = live baseline and PR/Actions observations above
IMPLEMENTATION_EVIDENCE = reproduced failures and corrected package checks
HUMAN_LEARNING = NOT_ESTABLISHED
RETENTION_OBSERVED = NOT_ESTABLISHED
CCTS_UNIQUE_EFFECT = NOT_ESTABLISHED
CAUSAL_EFFECT = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
MERGE_TO_MAIN = NO
```
