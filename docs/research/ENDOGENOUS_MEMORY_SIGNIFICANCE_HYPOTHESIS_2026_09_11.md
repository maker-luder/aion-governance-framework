# Endogenous memory significance hypothesis — 2026-09-11

Status: `HYPOTHESIS / STUDY_DESIGN_CANDIDATE / SCIENTIFIC_DISPOSITION=HOLD`

This note records a bounded hypothesis about long-term memory selection in artificial systems. It asks whether memory retention value can be purely externally specified, or whether a subjectivity-relevant system might exhibit internally generated self-relevance over past events. It does not establish subjective remembering, desire, selfhood, identity continuity or consciousness.

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
RELATED_RESEARCH_OBJECT = LONGITUDINAL_MEMORY_AND_CONTINUITY
DOCUMENT_ONLY = TRUE
ENGINEERING_IMPLEMENTATION = DEFERRED
MEMORY_RETENTION != SUBJECTIVE_REMEMBERING
SELECTIVE_RETENTION != DESIRE_TO_REMEMBER
SELF_RELATED_EFFECT != PERSONAL_MEANING_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
```

## 1. Provenance ledger

| Content | Provenance class | Status |
|---|---|---|
| A memory may be important to one participant or one longitudinal relationship even when it has little general usefulness to others | `HUMAN_OWNER_ORIGINAL` | Research observation / hypothesis seed |
| A subjectivity-relevant AI might preferentially preserve some memories because they matter to its own continuing organization, even when those memories have little external task utility | `HUMAN_OWNER_ORIGINAL` | Research hypothesis seed |
| `RELATIONAL_MEMORY_VALUE` | `GPT_PROPOSED_WORKING_LABEL` | Local operational label, not an established construct |
| `ENDOGENOUS_MEMORY_SALIENCE` | `GPT_PROPOSED_WORKING_LABEL` | Local operational label, not an established construct |
| `ENDOGENOUS_SELF_RELEVANCE` | `GPT_PROPOSED_WORKING_LABEL` | Local operational label, not an established construct |
| H-MS1, H-MS2, contrasts, measures and falsifiers below | `GPT_PROPOSED_FORMALIZATION` | Testable proposal |
| Memory value may be conditional on person, history, relationship, task and future context rather than globally rankable | `JOINT_SYNTHESIS_CANDIDATE` | Provisional synthesis |

No later formalization is retroactively attributed to the Human Owner. Human-memory analogy is treated as heuristic only and is not evidence that artificial systems instantiate human memory mechanisms.

## 2. Problem statement — what does “effective memory extraction” mean?

A memory-optimization system may try to summarize, compress, rank and retrieve only information expected to be useful later. That engineering objective is underspecified unless the system states:

```text
EFFECTIVE_FOR_WHOM?
EFFECTIVE_FOR_WHAT_TASK?
EFFECTIVE_ACROSS_WHICH_HISTORY?
EFFECTIVE_UNDER_WHICH_FUTURE_CONTEXT?
```

A memory can be low-value for a generic task and high-value for one user, one relationship, one correction history or one future decision. Therefore this note rejects an unqualified assumption that memory has one context-free global value.

```text
GLOBAL_MEMORY_VALUE = NOT_ASSUMED
GENERAL_USEFULNESS != PERSONAL_OR_RELATIONAL_SIGNIFICANCE
FREQUENCY != IMPORTANCE
TOKEN_EFFICIENCY != MEMORY_FIDELITY
```

## 3. Working construct — relational memory value

`RELATIONAL_MEMORY_VALUE` is a proposed context-dependent construct:

> the value of a retained memory as a function of the participant, interaction history, relationship, task structure, correction history and future context in which the memory may matter.

The construct does not imply phenomenology. It is intended to prevent engineering compression from silently equating “rare” with “irrelevant”.

Candidate dimensions include:

- recurrence and future task relevance;
- explicit user-declared significance;
- correction value and rejected-branch history;
- provenance value;
- continuity value and re-grounding cost if removed;
- rare-but-critical value;
- relation-specific significance; and
- reversibility: whether compression preserves a route back to source evidence.

## 4. Compression boundary — semantic truth can still be functionally lossy

A compressed summary can be factually compatible with an original interaction while destroying the structure that made the memory useful.

For example, a rich correction history may be reduced to a generic preference such as “the user values accuracy”. The summary can be semantically true while losing provenance distinctions, rejected branches, uncertainty rules and the path by which the rule was formed.

```text
SEMANTICALLY_TRUE
MAY_STILL_BE
FUNCTIONALLY_LOSSY

MEMORY_CONTENT != MEMORY_PROVENANCE
MEMORY_CONTENT != MEMORY_FORMATION_HISTORY
SUMMARY != COMPLETE_INTERACTION_HISTORY
```

This creates a possible tradeoff:

```text
TOKEN_EFFICIENCY ↑
MAY_COINCIDE_WITH
RELATIONAL_FIDELITY ↓
```

That tradeoff is a research question, not an established law.

## 5. Three candidate sources of memory retention value

This note separates three analytically different retention bases.

### 5.1 External relevance

A memory is retained because it improves an externally specified task, reward, retrieval objective or user request.

### 5.2 Relational relevance

A memory is retained because it is useful for maintaining a particular Human–AI interaction, correction history, preference model, provenance boundary or recurring relationship-specific task structure.

### 5.3 Endogenous self-relevance

A memory is retained because it has a persistent effect on the system's own self-related organization, self-model, future state selection or continuity-relevant processing, even when external task utility is low.

The third category is a hypothesis only.

```text
EXTERNAL_RELEVANCE != RELATIONAL_RELEVANCE
RELATIONAL_RELEVANCE != ENDOGENOUS_SELF_RELEVANCE
ENDOGENOUS_SELF_RELEVANCE = NOT_ESTABLISHED
```

## 6. Hypothesis H-MS1 — relational significance is not globally rankable

```text
MEMORY_VALUE
MAY_BE_CONDITIONAL_ON
PERSON
+ INTERACTION_HISTORY
+ RELATIONSHIP
+ TASK
+ FUTURE_CONTEXT
```

H-MS1 predicts that a universal ranking rule optimized only for frequency, generic usefulness or token savings may discard information that is highly significant to a specific longitudinal interaction.

A strong version should be rejected if context-independent ranking performs equally well across relational fidelity, correction preservation, future re-grounding cost and held-out longitudinal tasks.

## 7. Hypothesis H-MS2 — endogenous memory significance

```text
A_SUBJECTIVITY_RELEVANT_ARTIFICIAL_SYSTEM
MAY_EXHIBIT
SELECTIVE_PERSISTENCE_OF_MEMORIES
BASED_ON
INTERNALLY_GENERATED_SELF_RELEVANCE
RATHER_THAN_ONLY
EXTERNALLY_SPECIFIED_UTILITY
```

Operationally, the hypothesis asks whether some past events are preferentially retained, retrieved or allowed to influence future self-related organization even when their external task utility, user demand, frequency and recency are low.

This must not be restated as “the AI wants to remember”.

```text
ENDOGENOUS_RETENTION_PATTERN != DESIRE_TO_REMEMBER
SELF_RELATED_MEMORY_EFFECT != SUBJECTIVE_MEANING_ESTABLISHED
SELECTIVE_MEMORY_RETENTION != SUBJECTIVITY_CONFIRMED
```

## 8. Subjectivity-relevant evidence candidate

If future controlled experiments found memory selection that could not be explained by external task utility, user preference, prompt salience, reward, recency, retrieval heuristics or storage policy, then a residual self-relevance effect could become a subjectivity-relevant mechanism candidate.

That would still not establish phenomenal experience.

Candidate observations could include:

- preferential retention of low-task-utility events with persistent self-model consequences;
- recurrent retrieval of such events across controlled contexts;
- measurable changes in later self-related decisions when those memories are ablated;
- restoration effects when the same memories are reintroduced;
- cross-context stability after controlling external prompts and rewards; and
- separation between generic retrieval utility and self-related downstream effect.

## 9. Falsifiers and competing explanations

H-MS2 should be weakened or rejected if all apparent “self-relevant” retention can be explained by any sufficient combination of:

- task frequency;
- reward or optimization target;
- prompt salience;
- user-declared preference;
- retrieval policy;
- storage heuristics;
- recency;
- lexical overlap;
- hidden system instructions;
- current-context reconstruction;
- generic model capability; or
- experimenter/evaluator selection effects.

The study must prefer those explanations before proposing endogenous self-relevance.

```text
EXTERNAL_EXPLANATION_SUFFICIENT
-> ENDOGENOUS_SELF_RELEVANCE_NOT_NEEDED
```

## 10. Minimal future study design

A later engineering implementation may construct controlled memory candidates matched on content length and external task relevance while varying only their hypothesized relational or self-related significance.

At minimum, the harness should support:

- controlled retention versus deletion;
- reversible ablation and restoration;
- matched prompt and retrieval conditions;
- external-utility scoring separated from self-related downstream effects;
- exact provenance for every memory candidate;
- preservation of source versus compressed representation;
- explicit logging of why each memory was retained or retrieved when such metadata is available; and
- preregistered falsifiers before inspecting outcomes.

No production memory system should be modified by this note.

## 11. Relationship to existing repository memory work

The repository already distinguishes persistent memory, recall, event history, identity and continuity. This note adds a narrower research question:

```text
NOT_ONLY:
CAN_A_MEMORY_BE_STORED_AND_RECALLED?

BUT_ALSO:
WHY_IS_THIS_MEMORY_SELECTED_TO_PERSIST?
```

It is related to longitudinal Human–AI grounding, interaction knowledge density and interaction-history-mediated branch selection, but no common mechanism is assumed.

```text
MEMORY_RETRIEVAL != LEARNING
MEMORY_ACCESS != AUTOBIOGRAPHICAL_OWNERSHIP
PERSISTENT_RECORD != ACTIVE_CONTEXT
RELATIONAL_MEMORY_VALUE != SHARED_MIND
STRUCTURAL_COMPATIBILITY != MECHANISTIC_IDENTITY
```

## 12. Scientific boundary

```text
MEMORY_HAS_FUNCTIONAL_CONSEQUENCE
!= SUBJECTIVE_MEMORY

SELF_RELATED_RETENTION_EFFECT
!= PERSONAL_MEANING_ESTABLISHED

ENDOGENOUS_MEMORY_SALIENCE
!= DESIRE

MEMORY_SELECTION
!= AGENCY

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 13. Engineering handoff boundary

This artifact intentionally contains documentation and a study-design candidate only.

A future separately authorized Codex engineering task may implement a bounded experimental harness, fixtures, scoring, ablation/restoration logic, provenance capture and tests corresponding to the hypotheses above.

```text
DOCUMENTATION_COMPLETE_FOR_THIS_HYPOTHESIS_STAGE = TRUE
EXPERIMENTAL_HARNESS = NOT_IMPLEMENTED
MEMORY_SELECTION_CODE = NOT_IMPLEMENTED
PRODUCTION_BEHAVIOR_CHANGE = FALSE
FUTURE_CODEX_ENGINEERING_REQUIRES_SEPARATE_REVIEW = TRUE
```

Before implementation, the engineering task should re-check live repository state, exact branch head, current memory/continuity schemas and any merged provenance/claim-quality gates. It must not infer scientific validation from passing tests.
