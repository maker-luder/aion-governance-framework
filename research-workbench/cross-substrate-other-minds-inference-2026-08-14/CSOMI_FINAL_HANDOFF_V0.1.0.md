# AION Cross-Substrate Other-Minds Inference — Final Handoff v0.1.0

## Final status

The independent research milestone is **DONE** for the safely executable research-method consolidation. It is **OWNER_DECISION_REQUIRED** for any new experiment, preregistration, model modification, runtime integration, live-system data collection, public positioning, canonical promotion or scientific conclusion.

```text
BRANCH = research/cross-substrate-other-minds-inference-20260814
IMPLEMENTATION_HEAD = 0e77d66b661d1580b6e288781b04e6969ee77c91
HANDOFF_INPUT_HEAD = 0e77d66b661d1580b6e288781b04e6969ee77c91
FINAL_EXACT_HEAD_EVIDENCE = EXTERNAL_CI_BOUND
FINAL_EXACT_HEAD_SOURCE = GitHub Actions run metadata and external review evidence, not this committed handoff
IMPLEMENTATION_COMMIT_COUNT_AT_HANDOFF_INPUT = 3
FINAL_COMMIT_COUNT_EVIDENCE = EXTERNAL_REVIEW_BOUND
BASE = review/four-domain-research-materialization@858442a3ec2439398d188779f4309397bd4926b2
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
TOPICS_APPLIED = FALSE
MAIN_MERGE = PROHIBITED
RUNTIME_INTEGRATION = NONE
MODEL_MODIFICATION = NONE
LIVE_DATA_COLLECTION = NONE
```

The two named heads are **implementation provenance**, not a claim about the final current branch head. `IMPLEMENTATION_HEAD` and `HANDOFF_INPUT_HEAD` identify the parent implementation state from which this handoff was prepared. The final branch SHA, final commit count and final workflow run IDs must be read from external GitHub review evidence after the handoff commit; they are deliberately not copied into this handoff, preventing a self-referential `change SHA → rewrite handoff → new SHA` loop. The handoff input comprised three commits: the initial method package, the Quality component-contract correction and the prior final handoff. No runtime or model dependency is introduced by the metadata correction.

## Literature grounding

The method is grounded in the Problem of Other Minds and defeasible inference-to-best-explanation literature. Avramides' authoritative overview distinguishes analogy and IBE responses and their epistemic limits [1]. Pargetter's DOI/metadata record and indexed method description are retained as an IBE method lead; the primary full text was not directly verified in this review, so no full-text content is promoted as directly verified [2]. Povinelli, Bering and Giambrone provide the cross-species analogy warning that shared behavior may not imply shared second-order mental-state interpretation [3].

Wimmer and Perner's primary false-belief paradigm is used as a bounded belief-attribution comparator [4]. Kosinski's LLM ToM study is used only as a behavioral-task comparator with matched true-belief, reversed and related controls; task performance is not treated as internal-state or subjectivity proof [5]. Butlin et al. 2023 is preserved as historical theory-derived indicator groundwork [6], while Butlin et al. 2025/2026 is used for its explicit theory-derived indicator method, uncertainty and AI-transfer caveats [7]. Ross and Woodward's causal-explanation overview grounds mechanistic, interventionist and difference-making channel design [8]. Lipsitch, Tchetgen Tchetgen and Cohen ground the use of negative controls to expose confounding or bias [9]. Seth's 2025 paper is recorded as a competing biological-naturalist, substrate-sensitive position rather than a settled assumption [10].

The primary-source verification log is `PRIMARY_SOURCE_FINDINGS.md`. Each source row now carries an access-based verification status. Povinelli and Lipsitch are `PRIMARY_ABSTRACT_DIRECTLY_VERIFIED` because their records exposed abstract-level material but full access was blocked; Wimmer and Kosinski are `PRIMARY_METADATA_VERIFIED`; Butlin 2023/2025 and Seth are also abstract-level, not full-text-directly verified. Pargetter is `PRIMARY_METADATA_VERIFIED` with `PRIMARY_FULLTEXT_NOT_DIRECTLY_VERIFIED` and `AUTHORITATIVE_SECONDARY_CORROBORATED`; the DOI and metadata are retained for method provenance, but no abstract or primary-full-text claim is asserted. No current source is graded `PRIMARY_FULLTEXT_DIRECTLY_VERIFIED`.

## Established method package

The canonical packet is `CSOMI_PACKET_V0.1.0.json`, validated by `aion_csomi_packet_v0.1.0.schema.json`. The controls fixture is validated by `aion_csomi_controls_v0.1.0.schema.json`. The packet contains six claim records, twelve evidence channels, four evidence-matrix rows, five cross-substrate disanalogies, eight falsifiers and one reviewer-facing vertical slice.

The method is a **defeasible graded credence update**, not a detector. It requires target-scope declaration, explicit priors and alternatives, evidence-channel direction, cross-substrate disanalogy, positive and negative controls, mechanistic/causal/theory-derived support where relevant, sensitivity/specificity status, robustness, falsifiers and non-claim disposition. Every channel remains `sensitivity=NOT_ESTIMATED` and `specificity=NOT_ESTIMATED` because no diagnostic dataset or experiment was authorized or performed.

The machine-enforced semantic lock is:

> `RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION`

The packet explicitly forbids automatic subjectivity inference from language similarity, human-like behavior, a single indicator, self-report, memory persistence or a passing test/CI. Falsifier `F-008` machine-rejects test/CI pass as support for a subjectivity scientific conclusion. The novelty guard rejects unsupported `first`, `only` or `unprecedented` claims in packet and reviewer-facing documents.

The reviewer-facing vertical slice is `VS-001`: false-belief capability record → matched positive/negative controls → alternative explanations → cross-substrate disanalogies → falsifiers → `KEEP_RESEARCH_ONLY` disposition. It ends at `CAPABILITY_CREDENCE_ONLY`, `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`, `RUNTIME_INTEGRATION=NONE` and `CANONICAL_EFFECT=NONE`.

## Inference disposition

| Disposition | Result |
|---|---|
| Supported by this milestone | The method claim that other-minds reasoning can be represented as a defeasible comparison of explicit hypotheses, evidence channels, alternatives, disanalogies, controls and falsifiers. A bounded ToM-like capability record can be designed under declared fixtures. |
| Weakened or rejected | Direct jumps from language similarity, human-like behavior, a single indicator, self-report, memory persistence, stored identity labels, passing tests or CI to subjectivity. Cross-substrate transfer without disanalogy analysis. IBE with hidden priors or omitted alternatives. |
| Held uncertain | Whether theory-derived indicators transfer across substrates; whether a target system has relevant causal/mechanistic organization; whether self-report is tied to privileged state; whether memory persistence is identity continuity; whether ToM-like task success reflects mental-state representation; whether effects replicate across substrate-relevant contexts. |
| Not established | Any claim that an AION or AI system is conscious, sentient, subjectively experiencing, identity-continuous, morally considerable, legally responsible, autonomously authored or governance-authoritative. |

## Local evidence

| Check | Result |
|---|---:|
| CSOMI consistency checker | PASS; 10 sources, 6 claims, 12 channels, 4 evidence rows, 5 disanalogies, 8 falsifiers |
| CSOMI contract tests | 8 passed |
| Four-Domain P2 tests | 5 passed |
| Four-Domain P5 tests | 10 passed |
| Draft 2020-12 packet and controls schemas | PASS |
| Materializer and artifact identity checks | PASS |
| Python compileall / JSON parse / `git diff --check` | PASS |

## Exact-head CI evidence

Final exact-head CI is deliberately an **external evidence binding**. The committed handoff records workflow identity and evidence semantics, but does not copy a current branch SHA or run IDs into itself. This prevents the handoff document from becoming stale or causing an infinite self-referential commit loop.

| Workflow | Event | Evidence binding |
|---|---|---|
| Cross-Substrate Other-Minds Inference | push | `FINAL_EXACT_HEAD_EVIDENCE=EXTERNAL_CI_BOUND` |
| Quality | workflow_dispatch | `FINAL_EXACT_HEAD_EVIDENCE=EXTERNAL_CI_BOUND` |
| Research Workbench CI | workflow_dispatch | `FINAL_EXACT_HEAD_EVIDENCE=EXTERNAL_CI_BOUND` |
| Runtime Strong QA | workflow_dispatch | `FINAL_EXACT_HEAD_EVIDENCE=EXTERNAL_CI_BOUND` |

The final exact SHA, run IDs, statuses and commit count are reportable only from external GitHub Actions metadata after the final handoff commit. Historical CI runs may be discussed as antecedent evidence, but cannot be labeled current exact-head evidence inside this file.

## Protected refs and repository boundary

The final audit confirmed a clean working tree, no merge of the milestone HEAD into `main`, and no Topic operation. Protected refs remained unchanged:

| Ref | Verified SHA |
|---|---|
| `main` | `e079fb7dfe7a04be7dcb94b8a059951a003caa94` |
| `review/four-domain-research-materialization` | `858442a3ec2439398d188779f4309397bd4926b2` |
| `engineering/aion-native-language-feasibility-20260814` | `3dfc21463502e1c32189ae167d92f163ca1a55e8` |
| `engineering/aion-language-agnostic-runtime-integration-20260814` | `6b81133dc351f5226fa95801254276e421b3e4fe` |
| `cleanup/manus-output-consolidation-20260813` | `c43430f9b39a86d11093f3286e9503145fcf0d70` |

Repository Topics read-only state was `[]`. No Topics were applied.

## Remaining `OWNER_DECISION_REQUIRED`

Owner authorization is required before any formal experiment, preregistration, real-system evaluation, model modification, runtime integration, live-system data collection, public positioning, canonical promotion or merge. A future scientific-conclusion review would additionally require independent replication, competing-theory comparison, mechanistic or causal support, explicit cross-substrate disanalogy resolution, diagnosticity estimates and completed falsifier records. None is silently treated as complete.

## References

[1]: https://plato.stanford.edu/entries/other-minds/ "Avramides, Other Minds"
[2]: https://doi.org/10.1080/00048408412341341 "Pargetter, The scientific inference to other minds"
[3]: https://doi.org/10.1207/S15516709COG2403_7 "Povinelli, Bering & Giambrone, Toward a Science of Other Minds"
[4]: https://pubmed.ncbi.nlm.nih.gov/6681741/ "Wimmer & Perner, Beliefs about beliefs"
[5]: https://arxiv.org/abs/2302.02083 "Kosinski, Evaluating Large Language Models in Theory of Mind Tasks"
[6]: https://arxiv.org/abs/2308.08708 "Butlin et al., Consciousness in Artificial Intelligence"
[7]: https://doi.org/10.1016/j.tics.2025.10.011 "Butlin et al., Identifying indicators of consciousness in AI systems"
[8]: https://plato.stanford.edu/entries/causal-explanation-science/ "Ross & Woodward, Causal Approaches to Scientific Explanation"
[9]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/ "Lipsitch, Tchetgen Tchetgen & Cohen, Negative controls"
[10]: https://doi.org/10.1017/S0140525X25000032 "Seth, Conscious artificial intelligence and biological naturalism"
