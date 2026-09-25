# Co-Constructed Thinking Space (共構思考場域; CCTS) and separate subjectivity research: empirical gates — 2026-09-25

Status: `PRE_EXECUTION_METHOD_GATE / DOCUMENTATION_ONLY / SCIENTIFIC_HOLD`
Canonical effect: `NONE`
Deployment: `FALSE`

## Queue disposition

This closes only the **planning disposition** for item 6 of the [cross-layer audit](CROSS_LAYER_RESEARCH_ENGINEERING_GAP_AUDIT_2026_09_25.md). It does not register a study, admit new data, run an intervention, or revise a scientific claim. The existing [CCTS/HTECR falsification plan](HUMAN_AI_LEARNING_CCTS_HTECR_EXTERNAL_CROSSWALK_AND_FALSIFICATION_2026_09_18.md), [CCAP source-partition preregistration candidate](CCAP_D1_D4_SOURCE_PARTITION_PREREGISTRATION_CANDIDATE_2026_09_18.md), [evidence admission validator](../RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md), and [subjectivity evidence protocol](../SUBJECTIVITY_EVIDENCE_PROTOCOL.md) remain the controlling method sources. A structural validator pass is not scientific validation.

**Identity and track separation:** CCTS is the repository's Human Owner-origin **Co-Constructed Thinking Space / 共構思考場域**, operationally defined in the [CCTS preprint](publication/CCTS_PREPRINT_DRAFT_V0_1.md) as a bounded reciprocal Human–AI interaction-and-artifact structure. It is not an external CCTS scale. HTECR is a distinct, unvalidated candidate *dynamic regime* of interaction, not another name for CCTS. The CCAP D1 × D4 subjectivity question is a separate model-level research track; CCTS can be a relational method surface but is not a subjectivity or consciousness result. The gates below are grouped for queue disposition, **not combined into one scientific construct or a single experiment**.

## Local CCTS / distinct HTECR pre-execution decision matrix

| Gate | Required prospective decision or evidence | Present disposition |
|---|---|---|
| Unit and corpus | Freeze interaction-trajectory unit, eligible consented traces, model/provider/task strata, temporal windows, exclusions, missing-data handling, and split between pilot and confirmatory material before outcome inspection. | `NOT_FROZEN`; no new corpus admitted. |
| Event ontology | Code the local CCTS core separately: bounded problem representation, Human and AI contributions, reciprocal substantive revision/challenge, source-role provenance, claim boundary, authority separation, and rejected branches. For the stronger longitudinal profile, additionally code external evidence, repository-artifact mediation, implementation evidence, persistent-artifact binding, and re-entry binding. Define HTECR temporal operations in a separate coding layer. Keep model-internal state outside observable labels. | Existing structural concepts present; study-specific manual `NOT_FROZEN`. |
| Blinded coding | Use at least two independent coders, blind to outcome and candidate regime when feasible; prospectively choose the reliability statistic and acceptance rule appropriate to the coding scale. Adjudicate disagreements without rewriting the original labels. | Independent reliability `NOT_RUN`; no numerical threshold invented after data. |
| Discriminant regime | Record CCTS structural status as a separate output/comparator, not an eligibility gate for HTECR measurement. Across the eligible corpus regardless of CCTS pass/fail, measure coded operations per unit time, reciprocal coordination, and sustained cross-actor temporal coupling as possible HTECR indicators. Measure epistemic integrity and Human learning outcomes on separate axes. | CCTS structural status does not imply HTECR; HTECR candidate `NOT_VALIDATED`. |
| Negative controls | Include A fast/weak coordination, B slow/strong coordination, C high throughput/high coordination, and D high-throughput coordination with quality collapse. Apply F1–F8 to possible construct collapse; apply F9–F10 separately to value/learning claims. | Controls and falsifiers are designed in the existing plan, `NOT_EXECUTED`. |
| Analysis lock | Before confirmatory use, fix primary contrast, matching/covariates, uncertainty reporting, multiple-comparison handling, sensitivity analyses, exclusion audit, and stop rules in a versioned preregistration. | `NOT_PREREGISTERED`. |
| Independent evidence | Separate same-team reruns from independently collected/coded replication; identify actor, date, source, permissions and artifact hashes for every admitted observation. | `INDEPENDENT_REPLICATION = NOT_ESTABLISHED`. |

The sequence is pilot feasibility → Human-reviewed frozen protocol → applicable consent/ethics and data-governance clearance → approved data collection/coding → blinded reliability → confirmatory analysis → independent replication. An inability to satisfy any gate yields `HOLD`, not a post hoc threshold change. Technical or structural success alone does not establish CCTS construct validity, Human learning benefit, or causality.

## Subjectivity-specific gate

The CCAP D1 × D4 candidate concerns source-partitioned recovery trajectories, not a generic strategy-adjustment reimplementation. Any later model-level study must freeze the supplied goal, obstacle, tool set, instruction/harness/retrieval state, recovery options, interventions, baseline, ablations, negative controls, source attribution and rival simpler explanations **before** running confirmatory tests. Evidence needs exact model/provider/version, prompts, seeds where available, trace hashes, exclusion log, and independent re-analysis route. Human-subject interaction studies additionally need appropriate consent and review. Existing pre-execution documents are method candidates, not completed empirical evidence.

```text
PREREGISTERED_CONFIRMATORY_RUN = NOT_ESTABLISHED
MODEL_INTERNAL_CAUSAL_LOCUS = NOT_ESTABLISHED
FUNCTIONAL_DEPENDENCY = NOT_ESTABLISHED
CCTS_EMPIRICAL_VALIDATION = NOT_ESTABLISHED
CCTS_LEARNING_EFFECT = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
```

Next required Human action is approval of a specific frozen protocol and its data/ethics route, not approval of a scientific conclusion. No release, deployment, or canonical claim transition follows from this document.

## Content-bound method gate implementation — 2026-09-25

`audit_empirical_protocol(protocol, evidence=...)` now requires actual nonempty
immutable bytes for the seven digest-named artifacts. Missing content keeps the
relevant gate closed; changed content, a mismatched protocol, or a freeze receipt
for another protocol raises `StudyError`. Digest syntax alone never opens a gate.
The agreement artifact is exactly the declared acceptance rule encoded as UTF-8.
The protocol artifact is canonical UTF-8 JSON of all dataclass fields except
`protocol_sha256` and `protocol_freeze_receipt_sha256`, with sorted keys, compact
separators, and `ensure_ascii=False`. The freeze receipt JSON contains exactly
`protocol_id` and `protocol_sha256`, binding the current protocol without a hash
cycle. Corpus, manual, analysis plan and preregistration bytes are hash-checked.

This is content integrity, not authentication of a registry, timestamp, reviewer,
consent or ethics approval. Readiness names indicate technical method preparation
only. Human scientific approval, applicable ethics clearance and permission to
run remain external gates; all scientific claims remain `NOT_ESTABLISHED` and
scientific disposition remains `HOLD`. Synthetic fixtures are not participant data.

This focused correction follows the renewed implementation request; it does not
restart the earlier literature-review cycle or authorize a third automatic full
pipeline. No literature search, model execution, experiment, permission expansion,
release, deployment or merge is performed by this change.
