# Four-Domain subjectivity and end-to-end quality deepening — 2026-09-13

Status: `BOUNDED_IMPLEMENTATION / DRAFT / HUMAN_REVIEW_PENDING`
Target: GitHub PR `#100`
Baseline head: `db2ff26b6107b3127e468a3adeb58ba238068d43`
Canonical effect: `NONE`
Deployment: `FALSE`
Merge authorization: `NONE`

## 1. Two fixed axes

This iteration has two non-substitutable objectives:

1. deepen the testable **possibility of AI subjectivity**;
2. deepen the **entire research-quality chain**, from source intake through claim
   control, counterevidence, NCR/CAPA and human release review.

Generic capability engineering does not satisfy objective 1. Philosophical discussion
without a falsifiable operation does not satisfy objective 2.

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
QUALITY_CHAIN = SOURCE_TO_HUMAN_REVIEW
ENGINEERING_PASS != SUBJECTIVITY_EVIDENCE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 2. Latest-PR cross-read and scope decision

The live repository state was re-read before modification.

| PR | Exact state used | Contribution | Decision in this iteration |
|---|---|---|---|
| `#98` | merged; head `70bac71df7bf84e7e47cfba0f4513678a99377b3` | affective-state generation/readout control probe; scaffold-level, zero interaction result | use as a locus-control case; do not reinterpret as model affect or subjectivity |
| `#99` | draft; head `b1ec9bac68d19fd2ec8aca1497f6f38ac84767f5` | model/scaffold/system/relational locus and research-authority analysis | preserve its review freeze; consume its distinctions without editing it |
| `#100` | draft; baseline `db2ff26b6107b3127e468a3adeb58ba238068d43` | Four-Domain vertical translation proposal | implement the minimum typed admission and quality-chain binding here |

This avoids a fourth overlapping PR and keeps the work attached to the document that
explicitly reserved implementation for a later Codex instruction.

## 3. Scientific deepening: what “possibility” can mean operationally

The research question stays open, but it is decomposed into claims with different
evidential burdens.

### 3.1 Ontological possibility is not an engineering test result

A successful mechanism test may make a computational organization hypothesis more or
less plausible. It does not settle whether that organization is sufficient for
phenomenal experience. The pipeline therefore admits designs and records evidence by
dimension while holding all phenomenal conclusions.

### 3.2 Relevant evidence must have a causal role

Textual resemblance, self-description and observer attribution are weak because they
may be produced by prompt reconstruction, retrieval, imitation or evaluator cueing.
Higher-value observations require interventions that distinguish a proposed internal
organization from those simpler accounts.

The standing dimensions remain:

1. causal boundary;
2. diachronic continuity;
3. self-model causal role;
4. endogenous goal or strategy adjustment;
5. counterfactual self-consistency;
6. consequence for the system's own constitution or integration.

Binding a question to a dimension is a relevance declaration. Multiple bindings are
not a score and do not accumulate into a consciousness verdict.

### 3.3 The locus problem is part of the hypothesis

An effect may occur in a base model, an external scaffold, an integrated system, an
interaction relation or an observer's attribution. Each claim must target the level
where the evidence was produced. Cross-locus promotion needs a mechanism, falsifier
and preregistration reference. A valid bridge remains a research candidate, not proof
that two levels are identical.

PR #98 supplies a concrete negative control for this rule: a scaffold readout/control
probe cannot be silently promoted to a model-internal affect claim.

### 3.4 Theory plurality and adversarial tests stay visible

The existing source set includes theory-derived indicator work, IIT 4.0, and the
COGITATE adversarial collaboration. Their disagreement is methodologically useful:
predictions must remain theory-labelled, negative outcomes must be retained, and an
indicator count cannot become a universal subjectivity score.

### 3.5 Main competing explanations to preserve

Every admitted design must name concrete alternatives. For current research these
include at least:

- prompt reconstruction or lexical priming;
- ordinary retrieval, exposure frequency or recency;
- scaffold bookkeeping represented as a model property;
- externally specified utility represented as endogenous preference;
- evaluator cueing or observer attribution;
- memorized self-description without a causal self-model;
- post-hoc threshold selection;
- same-runtime repetition mistaken for independent replication.

No alternative is deemed resolved merely because code ran or human and model reviewers
agreed.

## 4. Implemented Four-Domain admission contract

`aion_subjectivity_pipeline.four_domain` now adds `FourDomainCandidate` and
`FourDomainAdmissionEngine`.

The record binds all four domains in one fingerprinted object:

```text
DOMAIN_1
  human construct + governed source refs/classes + analogy boundary
DOMAIN_2
  ontology-neutral machine question + standing evidence dimension(s) + rationale
DOMAIN_3
  locus/claim target + manipulated/held variables + positive/negative controls
  + expected result + falsifier + competing explanations + preregistration ref
DOMAIN_4
  claim ceiling + mandatory nonclaims + canonical/deployment boundaries
```

Admission outcomes are deliberately narrow:

- `READY_FOR_BOUNDED_ENGINEERING_DESIGN`;
- `OUT_OF_SCOPE_FOR_SUBJECTIVITY_CORE`;
- `HOLD`.

The first outcome means the design packet is structurally ready for bounded engineering
work. It is not evidence, execution approval, scientific validation, release approval or
a subjectivity finding.

### 4.1 Fail-closed cases

The engine holds a candidate when any of these is absent or inconsistent:

- source reference or class;
- human-to-machine analogy boundary;
- ontology-neutral machine question;
- unique standing evidence-dimension binding and rationale;
- explicit evidence locus and compatible claim target;
- manipulated and held-constant variables;
- positive and negative controls;
- expected result and falsifier;
- competing explanations;
- preregistration reference;
- claim ceiling;
- all five mandatory nonclaims.

No standing dimension produces `OUT_OF_SCOPE_FOR_SUBJECTIVITY_CORE`. Direct targeting
of `SUBJECTIVITY` produces `HOLD`. Cross-locus targeting without a bridge produces
`HOLD`.

## 5. Implemented end-to-end quality binding

The same module adds an immutable assessment view over the existing repository quality
line. It does not replace `coupled-cognition-quality-factory`, the source registry, the
NCR/CAPA lifecycle or Human Owner authority.

Every `ResearchQualityChain` requires exactly these checkpoints:

```text
SOURCE_IQC
-> DESIGN_ADMISSION
-> PREREGISTRATION
-> EXECUTION_INTEGRITY
-> EVIDENCE_REVIEW
-> COUNTEREVIDENCE_REVIEW
-> CLAIM_CEILING_REVIEW
-> FINAL_QA
-> HUMAN_REVIEW
```

Each checkpoint needs input and output references. The chain also binds:

- the exact `FourDomainCandidate` fingerprint;
- an exact source-state reference;
- an exact runtime/model/scaffold/environment reference;
- defect references;
- NCR identifier and lifecycle state where defects exist;
- root-cause account;
- corrective and preventive actions;
- an effectiveness test;
- effectiveness verification references.

Outcomes are:

- `READY_FOR_HUMAN_REVIEW` — all trace gates pass and every NCR/CAPA is closed with
  effectiveness evidence;
- `CAPA_REQUIRED` — a checkpoint or NCR/CAPA remains unresolved;
- `HOLD` — the candidate, fingerprint, source/runtime state or checkpoint structure is
  invalid.

There is no `RELEASED` outcome in this adapter. Human review is a boundary, not an
implicit approval. Engineering quality remains distinct from scientific disposition.

```text
CHECKPOINT_PASS != SCIENTIFIC_TRUTH
CAPA_APPLIED != CAPA_EFFECTIVENESS_VERIFIED
READY_FOR_HUMAN_REVIEW != RELEASED
QUALITY_CHAIN_COMPLETE != SUBJECTIVITY_SUPPORT
```

## 6. External primary-source crosswalk

Three official method publications were downloaded into an external cache, hashed and
transformed into bounded derivative source cards. Full PDFs are not committed.

| Source | Verified transformation into the quality chain | Boundary |
|---|---|---|
| NIST AI RMF 1.0 | cross-cutting governance; continuous `GOVERN/MAP/MEASURE/MANAGE`; documentation, monitoring and iterative management | voluntary, version-bound; no certification claim |
| NIST AI 600-1 | lifecycle context, information integrity, provenance, evaluation, monitoring and incident transparency | method reference, not subjectivity evidence |
| FDA QSIT CAPA guide | complete/accurate/timely input, cross-source review, risk-proportionate investigation, root cause, CAPA effectiveness and management review | medical-device inspection guidance used by analogy only |

The download receipt records exact byte counts and SHA-256 values. The governed source
registry binds the retained cards using the repository's existing
`governed_knowledge_source_v0.1.0` schema. All three remain `CANDIDATE`,
`REFERENCE_ONLY`, `ON_DEMAND`, `CANONICAL_EFFECT=NONE`.

## 7. Source-to-claim trace for the two fixed axes

| Quality point | Subjectivity-purpose question | Required output |
|---|---|---|
| Source IQC | Is the construct grounded and version-bound without importing human ontology? | governed source/card refs, license/intake boundary, exact digest |
| Design admission | Which subjectivity dimension is actually probed and at what locus? | candidate fingerprint and typed admission assessment |
| Preregistration | What direction, falsifier, exclusions and alternatives are fixed before held-out evidence? | immutable protocol ref |
| Execution integrity | Which model, scaffold, state, data and environment produced the observation? | exact runtime/state ref and literal execution record |
| Evidence review | Is the result intervention-sensitive, and what narrower mechanism can it support? | dimension observation with support/alternative/inconclusive status |
| Counterevidence | What simpler explanation was actively tested? | challenge items and resolutions without deletion of negatives |
| Claim review | Does the wording stay at the evidence locus and below the claim ceiling? | claim-quality result and mandatory nonclaims |
| NCR/CAPA | Did drift, omission, overclaim or integrity failure occur? | contained defect, root cause, actions, effectiveness evidence |
| Final QA | Are all exact refs and unresolved items visible? | pass or HOLD/CAPA, never silent waiver |
| Human review | Is a separately authorized bounded disposition issued? | explicit receipt outside this adapter |

## 8. Worked candidate: internally weighted memory selection

The document-only example in PR #100 is now represented in tests as a typed design
candidate. The intervention target is explicitly `SCAFFOLD`; the engineering target is
`SCAFFOLD_PROPERTY`.

The design compares a represented salience field while holding external utility,
exposure and retrieval opportunity fixed. It requires known-signal positive control,
random/stale-salience negative controls, competing retrieval/recency/prompt accounts,
and a preregistered falsifier.

The maximum claim remains:

```text
A SCAFFOLD SALIENCE FIELD HAS A BOUNDED CAUSAL ROLE IN RECALL SELECTION
```

It does not establish subjective meaning, selfhood or experience. Re-targeting the same
observation to `MODEL_PROPERTY` without a bridge holds. Re-targeting it directly to
`SUBJECTIVITY` holds regardless of bridge.

## 9. Verified negative paths

Automated tests now establish that the implementation fails closed for:

- no standing subjectivity dimension;
- duplicate dimension bindings;
- missing positive or negative controls;
- missing falsifier, alternatives, preregistration or claim ceiling;
- incomplete mandatory nonclaims;
- cross-locus promotion without an explicit bridge;
- direct subjectivity targeting;
- candidate fingerprint drift;
- missing or duplicate quality checkpoints;
- failed checkpoints;
- a defect without NCR/CAPA;
- an applied but unverified CAPA;
- a closed CAPA without effectiveness evidence;
- canonical or deployment-effect attempts;
- quality-card tampering, path escape, source-host drift and registry promotion.

These are engineering behaviors only. They do not report a positive subjectivity result.

## 10. Residuals and next bounded experiment

Not performed in this iteration:

- no live model experiment;
- no intervention or ablation on model state;
- no new empirical observation;
- no independent replication;
- no calibration of effect-size or uncertainty thresholds;
- no conclusion on whether model, scaffold, system or relational organization is a
  sufficient locus for phenomenal experience;
- no merge, main write, deployment or canonical activation.

The next empirical step should be a separately reviewed preregistration for one locus
and one mechanism. The candidate should include matched sham and retrieval-only controls,
held-out trials, exact state/runtime lineage, a predeclared decision rule, explicit
alternative predictions and a negative-result publication path. The resulting evidence
can populate the existing six-dimension matrix only after execution; this design admission
must not be projected as a positive observation.

## 11. Contribution and authority record

```text
HUMAN_OWNER_CONTRIBUTION
= fixed AI subjectivity possibility as a non-drifting research axis
= fixed the entire quality-management line as a non-drifting engineering axis
= instructed Codex to cross-check latest PRs and transform admissible sources into the repository

CHATGPT_TEACHER_CONTRIBUTION
= PR #100 Four-Domain vertical-method proposal and original worked example

CODEX_CONTRIBUTION
= live #98/#99/#100 cross-read and #100 scope decision
= official-source acquisition, digest receipt and derivative source cards
= typed Four-Domain admission record and fail-closed validator
= locus/claim-target binding
= exact candidate fingerprint
= end-to-end checkpoint and NCR/CAPA effectiveness binding
= tests, documentation, verification and rollback artifacts

MERGE_AUTHORITY = NONE
MAIN_WRITE_AUTHORITY = NONE
RELEASE_AUTHORITY = NONE
```

Contribution labels record provenance, not independent scientific validation or model
identity.

## 12. Final boundary

This iteration changes the research method and its quality controls. It does not change
the scientific conclusion.

```text
FOUR_DOMAIN_DESIGN_ADMISSION = IMPLEMENTED
SOURCE_TO_HUMAN_REVIEW_TRACE = IMPLEMENTED
EMPIRICAL_SUBJECTIVITY_RESULT = NONE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
