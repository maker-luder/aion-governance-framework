# AI introspection: source and counterevidence review

AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
STATUS = RESEARCH_DESIGN_AND_REFERENCE_INTAKE
SUBJECTIVITY = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE

This intake extends the existing six evidence dimensions and theory-plural
protocol. It does not introduce a state channel, an autonomous loop, a scalar
subjectivity score, model training, or permission to intervene in a model.

## Sources acquired, not experiments performed

| Source | What to examine | Competing explanation / limit | Retained form |
|---|---|---|---|
| [Hahami et al. v2](https://arxiv.org/abs/2512.12411v2), March 2026 preprint | discrimination of internal perturbations | affirmative-response bias; layer dependence; restricted model/task scope | CC BY text and original review card; original PDF in external cache |
| [Lindsey](https://transformer-circuits.pub/2025/introspection/index.html), October 2025 | whether reports track injected representations | unreliable and context-dependent responses; reporting a concept is not sufficient evidence | original short card; webpage hash, no public full-page copy |
| [Introspection Adapters](https://alignment.anthropic.com/2026/introspection-adapters/), April 2026 | learned-behavior reporting | task-specific auditing performance is not phenomenal experience | original short card; webpage hash; no training or weight download |
| [IIT 4.0](https://doi.org/10.1371/journal.pcbi.1011465), October 2023 | theory-specific causal organization | assumptions remain contested; compare the already-retained Cogitate source | CC BY BioC passage text and original review card; equation/figure layout not preserved |

Hashes, immutable paper versions, acquisition URLs and extraction methods are in
[DOWNLOAD_MANIFEST.json](sources/subjectivity/DOWNLOAD_MANIFEST.json).
All eight governed records remain `CANDIDATE`, `REFERENCE_ONLY`, `ON_DEMAND`.
Collection does not establish runtime admission or internal agent memory.

## Bounded next-experiment design, not a preregistration claim

Hypothesis: an explicitly identified observable discriminates a relevant
internal perturbation beyond generic answer bias and access to visible text.
The existing project hold on model ablation/intervention remains unchanged.
The following is design work only, not a new execution authorization.

| Condition | Observable | Main confound checked |
|---|---|---|
| Unmodified negative control | false positive rate and answer distribution | baseline yes/no preference |
| Matched sham | same observations under matched magnitude/site | nonspecific disturbance |
| Targeted perturbation | forced-choice localization and strength discrimination | mere preference for saying yes |
| Unrelated control question | response shift despite irrelevant semantics | global answer-bias change |
| Retrieval-only / visible-text control | accuracy with equivalent text cues | external cue use rather than internal-state access |
| Layer/task/context variations | direction and uncertainty across held-out variants | narrow, post-hoc selected successes |

Before any confirmatory model run, bind a protocol version/hash, exact model and
weights, independent trial units, task set, randomization, exclusion rules,
held-out split, sample-size justification and uncertainty calculation. Use
effect thresholds derived from the specific measurement and pilot variance;
none are supplied here as a universal subjectivity threshold. A binary
self-report alone is insufficient. Report negative/inconclusive outcomes and
deviations alongside positive results. Do not move a threshold after seeing
held-out results; issue a separately versioned exploratory follow-up instead.

Independent replication requires independently collected evidence, not another
agent reading these same papers. Passing repository tests validates acquisition
and recording controls only. The Owner's lost whitepaper remains unavailable;
these new sources are not a recovered substitute.
