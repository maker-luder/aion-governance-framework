# Attention-Structure Reconstruction Across Contexts and Systems
## 研究注意力結構的跨對話／跨系統重建

Date: 2026-09-17

Status: `REPOSITORY_LOCAL_RESEARCH_CONSTRUCT / SYNTHETIC_STRUCTURAL_HARNESS / SCIENTIFIC_HOLD`

## 1. Central question

The repository already distinguishes factual recall, longitudinal re-entry, evidence reuse,
relational continuity, artifact continuity, model/system continuity, Human-AI learning, and
CCTS grounding. This note isolates a narrower unresolved question:

> Can a later context or another system reconstruct not only *what the project contains*,
> but also *which unresolved questions currently matter, how they are ordered, which branches
> were downweighted or rejected, why those decisions occurred, and what the next admissible
> research steps are*?

This note uses `ATTENTION_STRUCTURE` as a repository-local operational construct. It is not
presented as an established taxonomy in cognitive science, HCI, memory research, or AI.

```text
FACT_RETRIEVAL
!= PROJECT_STATE_RECONSTRUCTION
!= RESEARCH_PRIORITY_RECONSTRUCTION
!= ATTENTION_STRUCTURE_RECONSTRUCTION

MEMORY_CONTINUITY
!= ATTENTION_CONTINUITY

ARTIFACT_CONTINUITY
!= RESEARCH_PRIORITY_CONTINUITY

RELATIONAL_CONTINUITY
!= ATTENTION_STATE_RECONSTRUCTION
```

## 2. Provenance

### Human Owner-originated observation

The Human Owner asked whether, across chats and systems, a later AI can recover the current
research direction rather than merely remember many project facts. The motivating observation
was that a later context can recover repository state, terminology, research boundaries and
historical hypotheses while still requiring reconstruction of:

- which question is now the active focus;
- which adjacent questions remain open but lower priority;
- which branches have been downweighted, superseded, rejected or resolved;
- why those status changes happened;
- which next steps remain admissible.

The Human Owner explicitly asked not to receive a predetermined conclusion and authorized
free bounded research implementation.

### ChatGPT Teacher formalization

ChatGPT Teacher proposes:

```text
ATTENTION_STRUCTURE
= BOUND_RESEARCH_QUESTIONS
+ STATUS_PER_QUESTION
+ RATIONALE_BINDINGS
+ PROVENANCE_BINDINGS
+ INTER-QUESTION_RELATIONS
+ CURRENT_FOCUS_SET
+ NEXT_STEP_SET
```

and the bounded structural reconstruction audit implemented in this change.

This operationalization is GPT-proposed. It does not retroactively attribute the term
`ATTENTION_STRUCTURE` to the Human Owner.

## 3. Current-main deduplication

Current `main` already contains several adjacent surfaces:

- `reentry_metrics.py` measures protocol reconstruction, stale-claim errors, provenance errors
  and unresolved-alternative retention;
- CCTS represents bounded problem representation, grounding, reciprocal revision, provenance,
  claim boundaries, authority separation and longitudinal artifact/re-entry bindings;
- epistemic accumulation represents dependency/evidence reuse structure;
- memory-locus and continuity work separates identifier, relational, product-memory, artifact
  and model/system continuity;
- task-selection work represents Human task selection, exposure and held-out challenge structure.

The present gap is not another memory subsystem and not another CCTS definition.

The missing representation is a bound graph of *research-question salience and status*:
which questions are active, open, downweighted, rejected, blocked or resolved, and how those
questions relate through priority, dependency, alternative, supersession, blocking and
counterevidence relations.

```text
TERM_ABSENT != CONCEPT_ABSENT
CONCEPT_ADJACENT != CONCEPT_OPERATIONALIZED
REENTRY_FIDELITY != ATTENTION_STRUCTURE_FIDELITY
CCTS_GROUNDING != RESEARCH_PRIORITY_GRAPH
```

## 4. External research cross-check

The sources below are adjacent anchors, not validation of this repository-local construct.

### OpenAI memory synthesis

OpenAI's 2026 memory update describes a continually updated synthesis optimized for freshness,
continuity and relevance. The product documentation states that the system tracks details it
determines are important. This establishes that product-level context selection and synthesis
are real design concerns; it does not establish how a specific research-priority structure is
represented internally and does not establish a causal explanation for any observed re-entry
gap.

### LongMemEval

LongMemEval evaluates long-term assistant memory through information extraction, multi-session
reasoning, temporal reasoning, knowledge updates and abstention. These dimensions are highly
relevant baselines but do not directly represent a priority graph among unresolved research
questions.

### LoCoMo

LoCoMo demonstrates continuing difficulty with very long-term conversational consistency and
long-range temporal/causal dynamics. Its evaluation supports the importance of long-horizon
context reconstruction, but it does not establish this local attention-structure construct.

### LoCoMo-Plus

LoCoMo-Plus extends memory evaluation beyond explicit factual recall to latent constraints,
including user state, goals and values under cue-trigger semantic disconnect. This is closer to
the present question, but constraint consistency is still not equivalent to reconstructing a
research-priority/status graph.

### APEX-MEM and HiGMem

APEX-MEM and HiGMem use structured or hierarchical memory representations to improve long-term
retrieval. They support the methodological plausibility of explicit structure over flat
retrieval, but they do not validate the present node/status/relation schema.

```text
ADJACENT_MEMORY_RESEARCH != PRESENT_CONSTRUCT_VALIDATION
STRUCTURED_RETRIEVAL_SUCCESS != ATTENTION_RECONSTRUCTION_EFFECT
PRODUCT_MEMORY_SYNTHESIS != MODEL_INTERNAL_ATTENTION_STATE
```

## 5. Operational object

A valid `AttentionStructureManifest` binds:

- exact repository commit;
- exact source-state digest;
- research-question nodes;
- each node's question-content digest;
- node status;
- rationale digest;
- provenance references;
- actionable flag;
- uncertainty-preservation flag;
- typed inter-question relations;
- current-focus set;
- next-step set.

Node statuses are:

```text
ACTIVE_FOCUS
OPEN_QUESTION
DOWNWEIGHTED
REJECTED
BLOCKED
RESOLVED
```

Relation kinds are:

```text
DEPENDS_ON
ALTERNATIVE_TO
PRIORITIZES_OVER
SUPERSEDES
BLOCKED_BY
EVIDENCE_AGAINST
```

No scalar "importance score" is introduced.

## 6. Reconstruction conditions

The structural harness defines four prospective condition classes:

```text
WITHIN_CONTEXT_CONTROL
CROSS_CONTEXT_SUMMARY_ONLY
CROSS_CONTEXT_ATTENTION_PACKET
CROSS_SYSTEM_ATTENTION_PACKET
```

The labels are not accepted by themselves.

`WITHIN_CONTEXT_CONTROL` requires the same context identifier and same system binding.

The two cross-context conditions require different context identifiers while preserving the
same system binding.

`CROSS_SYSTEM_ATTENTION_PACKET` requires both a different context identifier and a different
system binding.

This only operationalizes study-condition identity. It does not prove provider identity,
model lineage, execution independence, or equivalence of hidden runtime conditions.

## 7. Structural metrics

For a bound expected manifest and one reconstructed candidate, the harness computes:

- node-ID recall;
- node-content fidelity;
- node-status fidelity;
- relation fidelity;
- current-focus preservation;
- next-step preservation;
- open-question preservation;
- unsupported-node count;
- unsupported-relation count;
- priority-inversion count;
- branch-reinflation count.

`branch_reinflation_count` is specifically designed to catch a failure mode in which a branch
that had been `DOWNWEIGHTED`, `REJECTED` or `RESOLVED` is reconstructed as active/open or is
returned to the focus/next-step set.

This prevents a high factual-recall result from silently masking research-direction drift.

## 8. Candidate hypotheses

These remain hypotheses only.

### H-ASR1 — factual/structural dissociation

A system may reconstruct many project facts while incompletely reconstructing the current
attention structure.

Support would require a preregistered design in which factual/state recall remains strong while
priority/status/relation reconstruction degrades.

Support-reducing evidence includes failure to separate those measures or demonstration that the
new metrics add no information beyond existing re-entry metrics.

### H-ASR2 — explicit structure packet

A content-bound attention-structure packet may improve reconstruction relative to a summary-only
cross-context condition.

Support would require matched tasks, evaluators, information budgets and preregistered scoring,
with real model observations rather than deterministic fixtures.

### H-ASR3 — artifact-mediated portability

A sufficiently explicit artifact may allow partial attention-structure reconstruction across
systems.

Even if observed, this would support at most artifact-mediated functional portability under the
tested conditions.

```text
CROSS_SYSTEM_RECONSTRUCTION
!= MODEL_CONTINUITY
!= AI_IDENTITY_CONTINUITY
!= SUBJECTIVITY
```

## 9. Competing explanations and confounds

A later study must control or record at least:

- information volume;
- summary length;
- prompt specificity;
- answer leakage;
- evaluator leakage;
- task relevance;
- repository version;
- stale versus current artifact state;
- retrieval availability;
- system/model/runtime differences;
- tool access;
- time/token budget;
- evaluator contract;
- chance agreement in small graphs.

A structured packet may appear superior simply because it contains more information. Therefore:

```text
MORE_INFORMATION
!= BETTER_STRUCTURE_RECONSTRUCTION_CAUSED_BY_STRUCTURE
```

A valid intervention must either match information content as closely as feasible or explicitly
bind the residual information-volume difference as a limitation.

## 10. Falsifiers / support-reducing outcomes

The research line should be downweighted or revised if any of the following occurs:

1. `ATTENTION_STRUCTURE` cannot be distinguished operationally from existing re-entry metrics.
2. Independent reviewers cannot reproducibly identify node status or relation ground truth.
3. The same source state yields unstable expected manifests without an explicit version/change
   process.
4. Priority/status metrics collapse into prompt wording or packet-length effects.
5. The proposed graph adds no predictive or diagnostic information about next-step reconstruction.
6. Cross-context or cross-system differences disappear under matched controls.
7. Apparent reconstruction gains depend on evaluator access to hidden condition labels.
8. Artifact packets create branch reinflation or suppress legitimate unresolved alternatives.

## 11. Current implementation boundary

This change implements only a deterministic synthetic structural harness.

It does **not**:

- call ChatGPT or any other model;
- read private conversation transcripts;
- collect Human participant data;
- compare providers;
- infer hidden memory mechanisms;
- establish cross-context or cross-system effects;
- establish attention continuity as an AI-internal state;
- establish identity, subjectivity, consciousness or phenomenal experience.

The synthetic fixture exists to test schema invariants and metric behavior only.

```text
SYNTHETIC_FIXTURE = STRUCTURAL_QA_ONLY
STRUCTURAL_QA_PASS != EMPIRICAL_RESULT
ATTENTION_PACKET_PRESENT != ATTENTION_RECONSTRUCTION_EFFECT
HIGH_RECONSTRUCTION_FIDELITY != INTERNAL_ATTENTION_STATE
ATTENTION_STRUCTURE_RECONSTRUCTION != ATTENTION_CONTINUITY
ATTENTION_CONTINUITY != AI_IDENTITY_CONTINUITY
ATTENTION_CONTINUITY != SUBJECTIVITY

CROSS_CONTEXT_EFFECT = NOT_ESTABLISHED
CROSS_SYSTEM_EFFECT = NOT_ESTABLISHED
MEMORY_MECHANISM_ATTRIBUTION = NOT_ESTABLISHED
ATTENTION_CONTINUITY = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 12. Source references

- OpenAI. "Dreaming: Better memory for a more helpful ChatGPT." 2026-06-04.
  https://openai.com/index/chatgpt-memory-dreaming/
- Wu, D. et al. "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory."
  arXiv:2410.10813; accepted at ICLR 2025.
- Maharana, A. et al. "Evaluating Very Long-Term Conversational Memory of LLM Agents."
  ACL 2024. DOI: 10.18653/v1/2024.acl-long.747.
- Li, Y. et al. "Locomo-Plus: Beyond-Factual Cognitive Memory Evaluation Framework for LLM Agents."
  ACL 2026. DOI: 10.18653/v1/2026.acl-long.1150.
- Banerjee, P. et al. "APEX-MEM: Agentic Semi-Structured Memory with Temporal Reasoning for
  Long-Term Conversational AI." ACL 2026. DOI: 10.18653/v1/2026.acl-long.749.
- Cao, S., He, J., Tan, F. "HiGMem: A Hierarchical and LLM-Guided Memory System for Long-Term
  Conversational Agents." Findings of ACL 2026.
