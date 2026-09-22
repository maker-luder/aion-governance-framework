# CCTS PR #197–199 cross-review — 2026-09-23

Status: `BOUNDED_ENGINEERING_HARDENING / SYNTHETIC_ONLY / SCIENTIFIC_HOLD`

## Reviewed baseline and authority

The Human requested Work to assist implementation and cross-review the preceding
conversations, public literature, and PRs #197–199. This authorizes bounded work
on the existing draft implementation; it is not merge authority.

| Surface | Inspected commit | Role |
| --- | --- | --- |
| main | `27f42f0636583a7f2da5a3d5b8a2352aecd1cfc8` | Repository baseline |
| #197 | `3f33568b39977058c2c7c7444f3bc5f26c630595` | Human judgement retention design |
| #198 | `fa7e3b99e7a46aa0d3be8106dd15b6004788fcaf` | Three separately sourced observations |
| #199 | `8e8576f6c36081dc002577a43974de5437bc9258` | Implementation before this hardening |

The #199 body still described three phases and a PASS for `635da33...`, while
its inspected code already used four phases plus two held-out scopes. Historical
PASS results must not be inherited by later commits. The current PR body and
commit-specific workflow runs are the handoff surface for remote verification.

## Conversation provenance and mapping

Review window: Taiwan dates 2026-09-21 and 2026-09-22, including the immediate
2026-09-23 continuation. Retrieval returned selected user reports and prior
assistant summaries, not a complete contemporaneous transcript. The following
are abstractions, not quotations, verified event reconstructions, or empirical
observations fed into the harness. No private transcript, identity, workplace
procedure or operational criminal detail is included.

| Retrieved theme | Source ceiling | Existing surface and bounded use |
| --- | --- | --- |
| Repeated counterexamples challenge a proposed resource bottleneck | User inquiry plus later assistant reconstruction; no proof of a real-world causal bottleneck | Existing bypass/alternative-explanation revision fixtures; preserve multiple surviving constraints |
| A surprising counterexample challenges a prior research-eligibility assumption | User-reported surprise; the reconstructed before/after proposition is partly assistant-supplied | Existing grounding-revision fixture; a synthetic example is not a measurement of conceptual change |
| Requests for stronger evidence and traceable qualification claims | Inquiry/review requirement, not verified credential or institutional evidence | Source-to-claim inspection, explicit unknowns and counterevidence; do not infer validity from a fluent explanation |
| External reuse of repository ideas | #198 explicitly marks first-person report and absent corroboration | Keep source dependency distinct from external publication; no misconduct determination |
| Third-party problem decomposition and workplace correction | #198 bounded reports; not controlled transfer evidence | Keep process observation separate from #199 withheld-assistance transfer design |
| Sequential advice and stopping concerns | Partial retrospective reconstruction; adjacent #196 design | Cross-reference only; no new stopping controller or expansion into closed embodiment PRs |

Human-origin inquiry, prior Teacher formalization, this Work review, and external
sources remain distinct. Repetition by multiple assistant summaries does not
create independent corroboration.

## First-party/publication cross-check

Checked during this review. These sources motivate distinctions, not validation
of CCTS or this dyad.

| Source | What was checked | Limit on use |
| --- | --- | --- |
| [Du & Yuan, 2026](https://link.springer.com/article/10.1007/s00146-026-03294-1) | Critical-integrative review; contestability, recoverability and transfer among its criteria | Conceptual/normative synthesis, not an effect estimate or experiment on this repository |
| [Zhu et al., 2026](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1878629/full) | Three-wave correlational study, N=589; perceived outcomes; explicit causal limitations | Temporal ordering is not causal mediation; self-report is not demonstrated ability |
| [Bastani et al., 2025, author-hosted paper](https://hamsabastani.github.io/education_llm.pdf), [publication DOI](https://doi.org/10.1073/pnas.2422633122) | Randomized mathematics study separates assisted practice from later unassisted examination and a no-AI arm | Design precedent for an actual comparator; no extrapolated effect size for this dyad |
| [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) | Structured adversarial system analysis, trust boundaries, iterative review | Adjacent reasoning method, not proof that conversational disagreement is a formal security assessment |
| [Posner et al., 1982](https://onlinelibrary.wiley.com/doi/10.1002/sce.3730660207) | Primary publisher record for conceptual-change theory | Conceptual correspondence only; no psychological diagnosis from surprise or changed text |
| [Yamamura et al., 2026](https://www.frontiersin.org/journals/virtual-reality/articles/10.3389/frvir.2026.1817800/full) | Human virtual-cat-ear experiment, N=24; subjective ownership findings and absent significant proprioceptive-drift effects | Shows such a research object can be operationalized; does not establish biological equivalence, AI embodiment, or AI subjectivity |

The previously cited Wang scoping review, Samuel theory article and BMJ
transformative-learning example were not successfully opened in this pass.
Their retrieval failures neither establish falsity nor count as re-verification.
No new implementation claim relies on them. The BMJ analogy remains unverified
in this pass and is not evidence that this interaction caused transformation.

## Reproduced defects and corrections

Regression tests were first run against the inspected implementation. Ten negative
cases failed to reject invalid inputs; fifty existing/positive cases passed.
The corrections stay inside the existing two modules.

| Finding | Counterexample | Correction |
| --- | --- | --- |
| Same-space proposal substitution | Replace the AI proposal and its contribution in the judgement manifest while keeping the assisted space name | Require the same complete admitted manifest snapshot across assistance and judgement |
| Revision-loop snapshot drift | Keep space/problem unchanged but change provenance, authority, claim boundary or rejected-branch binding | Require one complete manifest snapshot across the loop |
| Cross-task contamination | Use a payload, prior output or AI proposal from another task class as a held-out task | Check held-out task hashes against declared prior-phase exposure across the entire single-unit matrix |
| Repeated held-out material | Reuse one held-out payload in another task class | Require held-out payload uniqueness across all scopes and classes |
| HOLD bypass | Change a model under HOLD while omitting the rejected branch | Require preservation for every changed model, including HOLD; unchanged HOLD remains representable |

Full snapshot equality is intentionally conservative in v0.1. This is a frozen
synthetic design, not a versioned live-session protocol. Future evolving
manifests need explicit predecessor bindings rather than relaxing to name-only
identity. A differently ordered snapshot is not silently treated as identical.

Exposure checking includes known task payloads, human outputs, proposal/rationale
artifacts and CCTS contribution payloads from earlier phases. It detects exact
content reuse only. It does not inspect arbitrary prose for paraphrased answers,
prove that a human saw a record, or detect unobserved contamination.

## Residual gaps and claim ceilings

1. **Matched practice comparator:** a `practice_exposure` binding is not an
   independently represented non-CCTS practice arm. #197's comparator falsifier
   remains unimplemented. The present matrix cannot identify a CCTS-specific effect.
2. **Exposure and access semantics:** digests bind declared contents, while leakage
   flags remain supplied assertions. No resource-access enforcement, semantic
   answer-equivalence detector or live exposure log exists in this synthetic design.
3. **Revision semantics:** hashes and graph edges do not establish that a challenge
   refutes the target, that a retained model is correct, or that a rejected-branch
   text meaningfully describes the abandoned proposition. Semantic rubric/adjudication
   remains separate from this structural pass.
4. **Longitudinal inference:** phase indices encode order, not elapsed time, delayed
   retention, baseline ability or a causal comparison. No Human score is computed.
5. **Evidence independence:** #198 supplies a provenance boundary, not an executable
   independent-data/method/analysis admission result. An external work can derive a
   hypothesis from CCTS while collecting genuinely independent data; independence
   must be assessed by dimension rather than banning all derivative studies.
6. **Retrieval completeness:** incomplete conversational recall cannot establish the
   absence of other observations. No missing original dialogue has been invented.

These are explicit research/design limits, not silently completed features. This
review does not reopen the closed embodiment work or add a new research axis.

```text
FIXTURE_PASS != COMPLETE_RESEARCH_DESIGN
SAME_SPACE_LABEL != SAME_MANIFEST_SNAPSHOT
CONTENT_HASH_MATCH != SEMANTIC_ENTAILMENT
NO_EXACT_PAYLOAD_REUSE != NO_CONTAMINATION
ASSISTED_OUTPUT_GAIN != HUMAN_INDEPENDENT_GAIN
EXTERNAL_PUBLICATION != INDEPENDENT_CORROBORATION
SURPRISE != CONCEPTUAL_CHANGE_ESTABLISHED
CCTS != AI_SUBJECTIVITY
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
MERGE = NOT_AUTHORIZED
WRITE_TO_MAIN = NO
READY_FOR_REVIEW = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Local verification

- Component suite: 252 passed on Python 3.12.
- Strict mypy: no issues in 15 component source files.
- Ruff correctness checks: passed for component source/tests.
- `git diff --check`: passed.
- The eleven added tests include ten negative regression cases plus a positive
  unchanged-HOLD case; each negative case failed before its correction.

These are local results. Remote Quality and CodeQL must be checked for the exact
pushed commit; an authority gate hold is not a scientific or engineering verdict.
