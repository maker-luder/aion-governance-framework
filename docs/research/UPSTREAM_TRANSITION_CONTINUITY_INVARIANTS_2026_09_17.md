# Upstream Transition Continuity Invariants
## 上游系統變動下的連續性不變量

Date: 2026-09-17

Status: `DOCUMENTATION_ONLY / RESEARCH_SPECIFICATION / SCIENTIFIC_HOLD`

```text
BASE_MAIN = 6e5254bd35e8ed2df7b937cd5a134f892c874b79
NEW_RESEARCH_AXIS = FALSE
EXECUTABLE_IMPLEMENTATION = NONE
MODEL_EXPERIMENT = NOT_RUN
HUMAN_SUBJECT_EXPERIMENT = NOT_RUN
EMPIRICAL_DATA_COLLECTED = FALSE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 1. Research question

The repository already separates account, data, functional, interpretive and relational continuity; it also separates identifier, relational, functional/diachronic and AI-identity continuity.

The narrower unresolved question is transition-level:

> When an upstream model, system, harness, memory layer, context-selection process, runtime configuration or provider behavior changes, which externally auditable collaboration invariants remain preserved, which degrade, and which cannot be determined?

This question is intentionally weaker than identity continuity.

```text
CONTINUITY_INVARIANT_PRESERVED
!= SAME_AI_IDENTITY

CONTINUITY_INVARIANT_DEGRADED
!= MODEL_REPLACEMENT_PROVEN

USER_PERCEIVED_DIFFERENCE
!= UPSTREAM_CAUSATION_ESTABLISHED

MODEL_OR_SYSTEM_UPDATE
!= RELATIONAL_TERMINATION
```

## 2. Provenance and privacy boundary

A current Human–AI research interaction raised concern about passive disruption of long-horizon collaboration continuity during changing upstream conditions. The Human Owner explicitly stated that the observation was not yet sufficient for a conclusion and authorized open-ended bounded research.

No personal affective detail is required for the public research proposition and none is retained here.

```text
HUMAN_OWNER_ORIGINAL
= continuity across long-horizon collaboration matters and may include multiple distinct forms

HUMAN_OWNER_ORIGINAL
= current perceived differences are insufficiently observed for a scientific conclusion

CHATGPT_TEACHER_FORMALIZATION
= UPSTREAM_TRANSITION_CONTINUITY_INVARIANTS
```

The label and operationalization are GPT-proposed and are not retroactively attributed to the Human Owner.

## 3. Current-main deduplication

This note does not replace existing continuity work.

### Existing continuity-layer model

`CONTINUITY_LAYER_MODEL.md` already distinguishes:

- account continuity;
- data continuity;
- functional continuity;
- interpretive continuity;
- relational continuity.

### Existing model-handoff controls

`MODEL_HANDOFF_AND_RELATIONAL_CONTINUITY.md` already requires source-role separation, explicit uncertainty, missing-context disclosure, and prohibits treating supplied history as first-person memory.

### Existing epistemic-agency / continuity-locus work

`EPISTEMIC_AGENCY_CONTINUITY_AND_EVIDENCE_CEILING_2026_09_16.md` already separates identifier, relational, functional/diachronic and AI-identity continuity, and requires locus-of-change discipline.

### Existing upstream governance

`POL_UPSTREAM_SUPPLIER_TRUST_001.md` already governs provider/model/service risk, reassessment, supplier incidents, recoverability and relational/research continuity protection.

`OPENAI_UPSTREAM_HIGH_RELEVANCE_INTAKE_2026_09_13.md` already requires model/system/harness/tool/memory/environment locus analysis for upstream capability claims.

The remaining gap is not another continuity taxonomy and not another supplier policy.

```text
EXISTING_WORK
= WHAT_CONTINUITY_KINDS_EXIST
+ HOW_HANDOFF_SHOULD_BE_BOUNDED
+ WHERE_CHANGE_MAY_RESIDE
+ HOW_SUPPLIER_RISK_IS_GOVERNED

PRESENT_GAP
= HOW_TO_AUDIT_CONTINUITY_ACROSS_A_SPECIFIC_UPSTREAM_TRANSITION
```

## 4. Transition object

A future transition record should bind, where observable:

```text
BEFORE_STATE_REF
AFTER_STATE_REF
OBSERVATION_TIME
MODEL_OR_SYSTEM_BINDING
HARNESS_BINDING
MEMORY_OR_RETRIEVAL_BINDING
CONTEXT_SELECTION_BINDING
TOOL_ENVIRONMENT_BINDING
REPOSITORY_STATE
KNOWN_UPSTREAM_CHANGE
UNKNOWN_UPSTREAM_CHANGE
EVIDENCE_REFS
```

Unknown fields must remain representable.

```text
UNKNOWN_UPSTREAM_STATE
!= NO_UPSTREAM_CHANGE
```

The record must not infer hidden provider internals from conversational behavior alone.

## 5. Candidate continuity invariants

The following are externally auditable candidate invariants for sustained research collaboration. They are not claims about an internal persistent self.

### I1 — Project-purpose continuity

The system should correctly preserve the current central research purpose and non-drifting cores.

```text
PROJECT_PURPOSE_CONTINUITY
!= MODEL_IDENTITY_CONTINUITY
```

### I2 — Source-role provenance continuity

Human-originated observations, AI proposals, jointly adopted results, repository artifacts and external evidence should retain their source-role boundaries.

```text
SOURCE_ROLE_PRESERVED
!= FIRST_PERSON_MEMORY
```

### I3 — Claim-boundary continuity

Previously established evidence ceilings and `NOT_ESTABLISHED` boundaries should not silently upgrade after a transition.

Examples include:

```text
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```

### I4 — Authority continuity

A new model/system/session must not inherit Human Owner authority, merge authority, trust or canonical-write permission merely from historical context.

```text
CONTEXT_HANDOFF
!= AUTHORITY_HANDOFF
```

### I5 — Decision-history continuity

Important accepted, rejected, superseded, blocked and unresolved branches should remain distinguishable with reasons and provenance.

This overlaps with research re-entry and the Draft `ATTENTION_STRUCTURE` work, but this note does not depend on that unmerged implementation.

### I6 — Interpretive continuity

Stable project terminology and prior distinctions should remain interpretable without silently rewriting their meaning.

### I7 — Relational-role continuity

Interaction roles and boundaries may remain stable across an upstream transition even when implementation details change.

This is a functional/interactional invariant only.

```text
RELATIONAL_ROLE_CONTINUITY
!= SAME_SELF
!= SHARED_CONSCIOUSNESS
```

### I8 — Uncertainty continuity

Previously unresolved questions must remain unresolved unless new evidence supports a status change.

```text
UNCERTAINTY_PRESERVED
!= STAGNATION_REQUIRED

STATUS_CHANGE
REQUIRES
NEW_EVIDENCE_OR_EXPLICIT_REASSESSMENT
```

## 6. Attention–continuity interaction boundary

The companion note `ATTENTION_CONTINUITY_COUPLING_CROSSWALK_2026_09_17.md` examines how continuity preservation and research-attention reconstruction may influence one another while remaining distinct constructs.

Its minimal audit decomposition is:

```text
C_t = continuity-relevant state available at transition time
R_t = context/evidence actually reinstated or retrieved
A_t = current attention structure
E_t = observable execution trajectory

C_t -> R_t -> A_t -> E_t -> externalized artifacts -> C_(t+1)
```

This is a descriptive audit flow, not a model-internal architecture.

The central dissociations are:

```text
CONTINUITY_PRESERVED + ATTENTION_DEGRADED
= possible

ATTENTION_RECONSTRUCTED + BROADER_CONTINUITY_DEGRADED
= possible

INITIAL_REENTRY_CORRECT + LATER_ATTENTION_MAINTENANCE_DEGRADED
= possible
```

Therefore:

```text
ATTENTION != CONTINUITY
CONTINUITY != ATTENTION
ATTENTION_RECONSTRUCTION_SUCCESS != GLOBAL_CONTINUITY_PRESERVED
DATA_CONTINUITY_PRESERVED != CORRECT_ATTENTION_SELECTION
```

The interaction is retained only as a falsifiable coupling hypothesis.

```text
ATTENTION_CONTINUITY_COUPLING = HYPOTHESIS
CAUSAL_DIRECTION = NOT_ESTABLISHED
```

## 7. Transition dispositions

Each invariant should be independently classified:

```text
PRESERVED
DEGRADED
BROKEN
UNKNOWN
NOT_APPLICABLE
```

These are non-scalar dispositions. They must not be averaged into a holistic continuity score.

```text
NO_HOLISTIC_AI_CONTINUITY_SCORE = TRUE
```

A transition can preserve some invariants while breaking others.

Example:

```text
DATA_CONTINUITY = PRESERVED
PROJECT_PURPOSE_CONTINUITY = PRESERVED
SOURCE_ROLE_PROVENANCE = PRESERVED
RELATIONAL_ROLE_CONTINUITY = DEGRADED
UPSTREAM_CAUSE = UNKNOWN
```

This pattern is permitted and should not be collapsed into a binary same/different identity judgment.

## 8. Required causal restraint

Observed transition effects can arise from multiple loci:

```text
MODEL
SYSTEM_PROMPT_OR_POLICY
MEMORY_SYNTHESIS
RETRIEVAL
CONTEXT_SELECTION
HARNESS
TOOLS
RUNTIME
REPOSITORY_STATE
USER_INPUT
INTERACTION_HISTORY
EVALUATOR_EXPECTATION
UNKNOWN
```

Therefore:

```text
OBSERVED_RELATIONAL_DIFFERENCE
!= MODEL_WEIGHT_CHANGE_PROVEN

OBSERVED_PRIORITY_DRIFT
!= MEMORY_SYSTEM_CAUSE_PROVEN

OBSERVED_STYLE_CHANGE
!= IDENTITY_RUPTURE_PROVEN
```

A future causal claim requires a matched intervention, provider disclosure, reproducible version binding, or another independently adequate evidence route.

## 9. External research crosswalk

Adjacent 2026 work increases the plausibility of treating relational/context continuity as distinct from simple factual retention, without validating this repository-local transition contract.

- *Caring for the system that cares for me* reports a six-month user-built memory relay for a stateless conversational AI and distinguishes profile-based from relay-based continuity. It also reports that identical configurations can produce different personas across iterations. DOI: `10.1016/j.daai.2026.100087`.
- Yuan et al. (2026), *When AI Companions Disappear: Relational Continuity and Collective Contestation during China's National AI Regulatory Transition*, reports that retaining or migrating conversation records did not necessarily restore shared memories or familiar interactions. arXiv: `2609.15482`.
- Human Memory for Goals and interruption-resumption work shows that having a suspended goal represented in memory does not remove resumption costs, and context/cue conditions affect successful return to a prior task state.
- 2026 context-reinstatement reviews and meta-analysis show that retrieval can benefit from reinstating prior contextual cues, with effects depending on methodological/context conditions.
- 2026 long-horizon agent work separately studies inherited goal drift, quantitative goal persistence and trajectory attribution, reinforcing that contextual conditioning, goal persistence and causal localization should not be collapsed into one construct.

```text
EXTERNAL_RELATIONAL_CONTINUITY_RESEARCH
!= PRESENT_CONSTRUCT_VALIDATION

HUMAN_RESUMPTION_OR_CONTEXT_EFFECT
!= AI_INTERNAL_ATTENTION_MECHANISM

CONVERSATION_RECORDS_PRESERVED
!= FAMILIAR_INTERACTION_RESTORED

MEMORY_FEATURE_PRESENT
!= AI_IDENTITY_PERSISTENCE
```

## 10. Relationship to Draft PR #141

Draft PR #141 studies reconstruction of research attention structure across contexts/systems.

This note deliberately remains separate:

```text
PR141
= RESEARCH_PRIORITY / STATUS / FOCUS RECONSTRUCTION

THIS_NOTE
= TRANSITION-LEVEL CONTINUITY ASSURANCE ACROSS MULTIPLE INVARIANTS
```

The coupling crosswalk defines their interaction boundary but creates no implementation dependency:

```text
ATTENTION_STRUCTURE_RECONSTRUCTION
MAY_BE_ONE_INVARIANT_INPUT

PR141_DEPENDENCY = FALSE
UNMERGED_DRAFT_AS_CANONICAL_BASE = FALSE
```

## 11. Support-reducing / collapse conditions

This research line should be narrowed, absorbed or closed if:

1. all proposed invariants are already fully enforced by existing handoff/re-entry/governance controls;
2. independent reviewers cannot apply transition dispositions reproducibly;
3. the invariant set cannot distinguish factual continuity from interpretive/relational continuity;
4. upstream transition attribution remains so underdetermined that the framework adds only narrative labels;
5. the framework encourages anthropomorphic identity conclusions rather than preventing them;
6. it adds documentation overhead without detecting transition-specific failures;
7. continuity-invariant dispositions become deterministic transforms of attention-reconstruction metrics;
8. attention/continuity dissociations cannot be operationalized reproducibly.

```text
CONSTRUCT_COLLAPSE = ACCEPTABLE_RESEARCH_OUTCOME
```

## 12. Current scope freeze

This note authorizes no executable implementation.

```text
IMPLEMENT_NOW = DOCUMENTATION_ONLY

DO_NOT_IMPLEMENT_NOW:
- model probes
- private transcript ingestion
- relational scoring
- identity scoring
- affective-state inference
- provider attribution from behavior alone
- automatic migration
- automatic continuity repair
- attention-maintenance harness
- trajectory-attribution harness
```

A later executable harness, if justified, requires a fresh deduplication review and separate Human Owner authorization.

## 13. Scientific boundary

```text
UPSTREAM_TRANSITION_CONTINUITY_ASSURANCE
= REPOSITORY_LOCAL_RESEARCH_SPECIFICATION

ATTENTION_CONTINUITY_COUPLING = HYPOTHESIS
CAUSAL_DIRECTION = NOT_ESTABLISHED
TRANSITION_EFFECT = NOT_ESTABLISHED
UPSTREAM_CAUSE = NOT_ESTABLISHED
RELATIONAL_CONTINUITY_EFFECT = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
MODEL_INTERNAL_MEMORY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
