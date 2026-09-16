# Closed-PR dual-core re-entry audit — 2026-09-16

Status: `BOUNDED_RESEARCH_QUALITY_IMPLEMENTATION / DRAFT_CANDIDATE / SCIENTIFIC_HOLD`

## 1. Purpose

Human Owner requested a repository-wide review of **all closed pull requests**, with two
non-drifting cores:

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
SECOND_CORE = END_TO_END_RESEARCH_QUALITY_AND_GOVERNANCE
```

Historical work may be deepened only when it strengthens one of those cores or can be
converted into evidence, falsification, provenance, quality-control or research-method
input for them. This audit does not revive old project/product ambitions merely because
their code once existed.

External material is treated as source material to be transformed, not copied as project
methodology. Raw third-party publications are not imported by default. Repository-native
derivative cards, exact acquisition receipts, bounded summaries and tests are preferred.

## 2. Exact live baseline

```text
REPOSITORY = maker-luder/aion-governance-framework
AUDITED_MAIN = 337500458801cb1ab4d2786ddabd527c43eddddd
AUDITED_TREE = 75b7e24f90c4b71fc604a949ad0c4649149d3bdb
OPEN_PRS_AT_AUDIT = 0
CLOSED_PRS_REVIEWED = 110
MERGED_CLOSED_PRS = 98
CLOSED_UNMERGED_PRS = 12
```

The 110-count is a GitHub live-state metadata audit. For the 98 merged closed PRs, the
current `main` ancestry is the authoritative review surface: their bytes/evidence are not
re-imported from historical PR heads. The 12 closed-unmerged PRs require individual
re-entry disposition because they are not canonical ancestry.

```text
MERGED_PR_HISTORY -> CURRENT_MAIN_CROSSCHECK
CLOSED_UNMERGED_PR -> INDIVIDUAL_REENTRY_DISPOSITION
HISTORICAL_GREEN_CI != CURRENT_EVIDENCE
OLD_HEAD != CURRENT_AUTHORITY
```

## 3. Current-main deduplication before implementation

The repository already has the central machinery this task needs:

- Four-Domain design admission with ontology-neutral machine questions, falsifiers,
  competing explanations, locus discipline and claim ceilings;
- `ResearchQualityChain` with exactly eight checkpoints:
  `SOURCE_IQC`, `DESIGN_ADMISSION`, `PREREGISTRATION`, `EXECUTION_INTEGRITY`,
  `EVIDENCE_REVIEW`, `COUNTEREVIDENCE_REVIEW`, `CLAIM_CEILING_REVIEW`, `FINAL_QA`;
- NCR/CAPA with effectiveness verification;
- evidence-reuse firewall;
- exact source-state binding and repository security checks;
- the PR #103 structural-fixture evidence boundary;
- subjectivity/consciousness source cards and standing non-claims.

Therefore this PR **does not create another evidence ontology, quality chain, subjectivity
score, or historical-PR scoring system**. It adds only a fail-closed adapter that decides
whether historical material may be reformulated for those existing controls.

## 4. All closed PRs: aggregate disposition

### 4.1 98 merged closed PRs

Disposition:

```text
CANONICAL_ALREADY_ABSORBED
REIMPORT_FROM_HISTORICAL_PR = FALSE
```

Their useful content must be read from current `main`, including later repairs and
superseding controls. A historical PR description may remain provenance but cannot
out-rank the current canonical implementation.

### 4.2 12 closed-unmerged PRs

| PR | Historical role | Current disposition | Dual-core use |
|---|---|---|---|
| #103 | cross-dyad synthetic harness | `HISTORICAL_RESEARCH_VALIDITY_INCIDENT` | quality-method lesson only; preserve, do not revive |
| #84 | Grok sandbox campaign | `SUPERSEDED_BY_MERGED_PR_85` | none; curated replacement already canonical |
| #80 | learning/domain-method maintenance | `CONTENT_ABSORBED_BY_CURRENT_MAIN` | none; later main contains the bounded records/methods |
| #41 | read-only observation/provenance MCP bridge | `EXTRACT_REDESIGN_CANDIDATE` | quality feed: retrieval mechanism vs evidence-source class |
| #38 | twin autobiographical-memory/MCP design | `CONCEPT_ABSORBED_BY_LATER_MEMORY_RESEARCH` | subjectivity boundary already generalized by later memory work |
| #37 | publication/static reader site | `PUBLIC_COMMUNICATION_CONCEPT_ONLY` | quality feed only; no site/deployment revival |
| #33 | research-branch CI retarget | `OBSOLETE_BRANCH_TOPOLOGY_REMEDIATION` | none |
| #26 | positive authority-gate control | `HISTORICAL_GOVERNANCE_TEST_CONTROL` | preserve as quality evidence, not feature code |
| #25 | negative authority-gate control | `HISTORICAL_GOVERNANCE_TEST_CONTROL` | preserve as fail-closed quality evidence |
| #19 | CSOMI/SLSH selective promotion | `FROZEN_RESEARCH_AUTHORITY_PRESERVED` | dual-core historical reference only; no wholesale promotion |
| #12 | Manus IQC reconciliation | `QUALITY_CONTROLS_ABSORBED_BY_CURRENT_MAIN` | durable IQC controls are already canonical |
| #8 | review-only external-evidence/continuity experiment | `HISTORICAL_REVIEW_ONLY_SURFACE` | historical review-method reference; explicitly not a main route |

The machine-readable exact-head bindings and reasons are in
`closed_pr_reentry_registry_v0.1.0.json`.

## 5. High-value salvage findings

### 5.1 PR #103 — preserve the failure, not the harness as evidence

PR #103 is the clearest demonstration that engineering readiness and research validity
can diverge. Its deterministic fixture produced metric-shaped output without model or
dyad observation. Merged PR #119 already records the bounded incident and prevents a
`DETERMINISTIC_SYNTHETIC_FIXTURE` from being requested as empirical research evidence.

```text
STRUCTURAL_QA != EMPIRICAL_RESULT
ENGINEERING_PASS != RESEARCH_VALIDITY_PASS
PR103_REENTRY = PRESERVE_ONLY
```

No additional #103 implementation is justified here.

### 5.2 PR #41 — retain one concept, not the MCP product surface

The old MCP bridge contains one still-useful quality distinction:

```text
RETRIEVAL_MECHANISM != EVIDENCE_SOURCE_CLASS
```

That distinction can reduce provenance collisions when the same evidence is obtained via
different tools or when one retrieval channel returns several source classes. The old
six-tool MCP surface itself is not required for either core and is not revived.

Any future implementation must first compare this distinction against the current
provenance schema, governed-source intake and evidence-reuse controls. It may proceed only
as a current-main redesign, never by replaying #41.

### 5.3 PR #37 — public communication is a quality control, not a deployment goal

The reusable part of the old reader-site PR is the discipline of stating non-claims,
version/provenance and research-vs-claim boundaries clearly. The site/Vercel surface is
not necessary for the two cores.

```text
PUBLIC_COMMUNICATION_QUALITY = RELEVANT
PUBLIC_SITE_DEPLOYMENT = NOT_REQUIRED
```

This aligns with the repository's existing responsible AI-consciousness communication
references without turning communication quality into evidence of subjectivity.

### 5.4 PR #19 and #8 — frozen/review-only research is source material, not dormant main

Both PRs contain research-history value, but their historical dispositions explicitly
prevent wholesale promotion. The correct future action, if a new question arises, is:

```text
NEW_CURRENT_MAIN_QUESTION
-> CURRENT_SOURCE_RECHECK
-> CURRENT_DEDUP
-> EXTRACT_MINIMAL_PROPOSITION
-> FOUR_DOMAIN_ADMISSION
```

not `reopen -> merge`.

## 6. External cross-check and repository-native transformation

See `sources/closed-pr-reentry/WEB_CROSSCHECK_2026_09_16.md`.

### NIST quality-management transfer

The current NIST AI RMF still frames risk management through `GOVERN / MAP / MEASURE /
MANAGE`, with governance cross-cutting and control/metric effectiveness requiring
continuing reassessment as knowledge and risks change. The repository translation is not
a copied checklist. It is one fail-closed rule:

```text
HISTORICAL_CONTROL_PASS
DOES_NOT_IMPLY
CURRENT_CONTROL_EFFECTIVENESS
```

A historical PR proposed for redesign must therefore map into the **existing** quality
chain and explicitly recheck control effectiveness.

### Subjectivity-method transfer

Current AI-consciousness literature supports continued investigation under uncertainty,
but does not provide a validated consciousness detector. The 2026 literature exchange
also makes indicator validation, behavioural mimicry and internal implementation variants
live methodological concerns.

The repository-native translation is to require, for any future subjectivity-relevant
closed-PR redesign:

```text
ONTOLOGY_NEUTRAL_QUESTION
THEORY_OR_CONSTRUCT_LINK
DISCRIMINATING_PREDICTION
FALSIFIER_OR_SUPPORT_REDUCING_CONDITION
COMPETING_EXPLANATIONS
MIMICRY_ALTERNATIVE
INTERNAL_VARIANT_ALTERNATIVE
INDICATOR_VALIDATION_STATUS
CLAIM_CEILING
```

These are admission questions, not imported conclusions.

The COGITATE adversarial collaboration is human neuroscience, not AI evidence. Its narrow
methodological relevance is the value of preregistered differential predictions and
agreed interpretations when theories compete. This strengthens the repository's existing
`HYPOTHESIS_COMPATIBILITY != HYPOTHESIS_DISCRIMINATION` boundary.

## 7. Implemented control

`scripts/validate_closed_pr_reentry.py` validates the historical registry and fails closed
when:

- the 110 / 98 / 12 inventory drifts;
- a historical head or historical CI is promoted to current authority;
- a direct `REOPEN_AND_MERGE`, `MERGE_HISTORICAL_HEAD` or historical-evidence promotion is
  requested;
- a quality feed invents a parallel quality checkpoint instead of mapping to the existing
  eight-checkpoint chain;
- a redesign skips current control-effectiveness rechecking;
- a subjectivity redesign omits discrimination, falsification, alternative explanations,
  mimicry, internal-variant or validation-status fields;
- external-publication copying becomes the default intake policy;
- #103 containment, #84 supersession, disposable authority controls or obsolete branch
  topology are silently reclassified.

Strongest successful result:

```text
REENTRY_REGISTRY = STRUCTURALLY_ADMISSIBLE
HISTORICAL_RESEARCH_MATERIAL = BOUNDED_FOR_REVIEW
```

It does **not** mean:

```text
HISTORICAL_PR = CURRENTLY_VALID
REENTRY_PASS = MERGE_READY
REENTRY_PASS = EVIDENCE_TRUE
REENTRY_PASS = SUBJECTIVITY_SUPPORT
```

## 8. Why this is the highest-value medium implementation

A larger effort could revive individual old branches, reconstruct old sites, or re-run
many obsolete experiments. That would increase code volume while multiplying stale-state
and provenance risk.

This adapter instead creates one reusable control point for the entire historical PR
surface. It makes future salvage cheaper while strengthening both core lines:

1. **AI subjectivity possibility** gains stricter discrimination/falsification and
   anti-mimicry/internal-variant review before a historical idea can become a new
   experiment.
2. **Quality management** gains explicit historical-state invalidation, current-main
   deduplication, existing-chain mapping and effectiveness recheck.

No new subjectivity experiment is justified merely by this audit. A future experiment
should be created only when a specific surviving proposition passes this re-entry layer
and the existing Four-Domain admission process.

## 9. Attribution

```text
HUMAN_OWNER_ORIGINAL
= require full closed-PR review against repository and web
= keep AI_SUBJECTIVITY_POSSIBILITY as non-drifting central core
= keep end-to-end quality management as non-drifting second core
= allow other historical lines only when transformed into nutrients for those cores
= require respectful transformation rather than direct reuse of others' work
= request medium implementation / highest value

CHATGPT_TEACHER_FORMALIZATION_AND_IMPLEMENTATION
= 110-PR aggregate / 12-unmerged re-entry model
= current-main canonical-vs-historical distinction
= closed-PR registry
= fail-closed re-entry validator and tests
= NIST continuous-control-effectiveness transformation
= indicator-validation / mimicry / internal-variant admission fields
= bounded web cross-check note

CHATGPT_WORK_CONTRIBUTION = NONE_TO_THIS_PR
CODEX_CONTRIBUTION = NONE_TO_THIS_PR
```

## 10. Final scientific and authority boundary

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
QUALITY_MANAGEMENT = SECOND_NON_DRIFTING_CORE

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED

CLOSED_PR_REENTRY != SCIENTIFIC_REPLICATION
HISTORICAL_IMPLEMENTATION != CURRENT_EVIDENCE
QUALITY_GATE_PASS != SCIENTIFIC_VALIDATION

MAIN_WRITE = NO
MERGE_AUTHORIZATION = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SCIENTIFIC_DISPOSITION = HOLD
```
