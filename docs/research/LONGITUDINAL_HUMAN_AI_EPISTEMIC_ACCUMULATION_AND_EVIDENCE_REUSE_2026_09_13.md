# Longitudinal Human–AI epistemic accumulation, artifact continuity, and evidence-reuse controls — 2026-09-13

Status: `RESEARCH_HYPOTHESIS / METHODOLOGY_NOTE / BOUNDED_IMPLEMENTATION_AUTHORIZED / DRAFT`
Canonical effect: `NONE`
Deployment: `FALSE`
Merge authorization: `NONE`
Main-write authorization: `NONE`
Scientific disposition: `HOLD`

## 1. Purpose

This note records a bounded research question that emerged from repeated Human Owner–ChatGPT Teacher inquiry:

> Under what conditions does repeated Human–AI dialogue stop behaving like isolated question–answer episodes and begin behaving like a cumulative, versioned, path-dependent knowledge-building process?

The note also records a methodological requirement raised by the Human Owner:

> Existing repository material, prior citations, code, experiments, and earlier evidence must not be silently treated as reusable support for a new claim merely because the topic looks similar.

The present note therefore has two coupled goals:

1. define a bounded hypothesis about longitudinal epistemic accumulation across Human, AI, and versioned artifacts; and
2. define an explicit evidence-reuse firewall so future Work / Codex activity can reuse infrastructure where justified without laundering prior evidence into a new claim.

This note does **not** establish that a Human–AI dyad forms a shared mind, that a repository is biological memory, that an AI has identity continuity, or that a longitudinal interaction proves subjectivity.

```text
LONGITUDINAL_INTERACTION != MUTUAL_LEARNING_PROVEN
CUMULATIVE_ARTIFACTS != SHARED_CONSCIOUSNESS
REPOSITORY_CONTINUITY != MODEL_CONTINUITY
COMMON_GROUND != IDENTITY
DISTRIBUTED_COGNITION_ANALOGY != SUBJECTIVITY
TRANS_ACTIVE_MEMORY_ANALOGY != HUMAN_AI_TMS_ESTABLISHED
CO_AGENCY != AI_SUBJECTIVITY
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
```

## 2. Provenance

### 2.1 HUMAN_OWNER_ORIGINAL

The Human Owner supplied the following observations and research questions:

- this Human–AI research interaction appears to accumulate naturally across repeated decomposition rather than ending after one answer;
- the repository increasingly behaves as an external place where distinctions, failures, provenance, unresolved questions, and implementation state can be recovered later;
- the resulting research structure feels more like a relationship graph than a single linear path;
- a `baseline` was intuitively understood as a reference line, prompting a question about how baseline, history, and dependency graph differ;
- a separately observed third-party Human–AI interaction appeared, in one inspected context, more task-local and closure-oriented, but the Human Owner explicitly did **not** treat one observed session as proof that the other dyad lacks longitudinal accumulation capability;
- future implementation should first search the repository for existing material instead of duplicating it;
- external web research should be cross-checked rather than copied from summaries;
- prior evidence should not be reused automatically merely because it appears relevant;
- voice input can alter technical terms; one observed example changed the intended `Codex usage / allowance` topic into `CI`, after which the Human Owner explicitly corrected the transcription.

The Human Owner authorized a later bounded Work / Codex implementation of the experimental and evidence-governance surfaces specified in this note, on a separate branch / Draft PR, with no merge or main-write authorization.

### 2.2 CHATGPT_TEACHER_FORMALIZATION

The Teacher formalizes the current inquiry using the following local working terms:

```text
LONGITUDINAL_EPISTEMIC_ACCUMULATION
ARTIFACT_MEDIATED_EPISTEMIC_RATCHET
RESEARCH_GOVERNANCE_DEPENDENCY_GRAPH
EVIDENCE_REUSE_FIREWALL
SEMANTIC_CONSISTENCY_RECHECK
```

These are repository working labels, not validated scientific taxonomies.

The Teacher also separates three structures that should not be collapsed:

```text
BASELINE
= accepted reference state for comparison or controlled change

HISTORY
= temporal sequence of changes, corrections, branches, and decisions

DEPENDENCY_GRAPH
= network of relations among claims, evidence, artifacts, authority, implementation, and tests
```

Therefore:

```text
BASELINE != LINEAR_HISTORY
LINEAR_HISTORY != DEPENDENCY_GRAPH
REFERENCE_STATE != AUTHORITY_OVER_ALL_DESCENDANTS
```

## 3. Live-state and repository deduplication audit

This note was created from live `main` commit:

`d95bc2625e71f1c85a725aaba78cb0feccfc0668`

with tree:

`77470062979df1db2f17c3a2a396891d1e910f98`

The audit intentionally distinguishes canonical `main` from unmerged Draft PR material.

### 3.1 Relevant material already on `main`

The following repository surfaces already cover adjacent ideas and must be reused as research ancestry rather than rewritten as if new:

- `docs/research/HUMAN_AI_BIDIRECTIONAL_GROUNDING_HYPOTHESIS_2026_09_11.md`
  - common ground, grounding, reciprocal correction, joint task representation;
- `docs/research/INTERACTION_KNOWLEDGE_DENSITY_AND_TASK_CONDITIONED_EPISTEMIC_POLICY_2026_09_11.md`
  - domain-skewed longitudinal interaction density, task-conditioned epistemic behavior, and controlled study design;
- `research-labs/coupled-cognition-quality-factory_v0.1.0/docs/EPISTEMIC_PROVENANCE_AND_CO_DEVELOPMENT.md`
  - source-role provenance, problem decomposition, longitudinal epistemic development, and falsifiers;
- `research-labs/human-ai-longitudinal-study_v0.1.0/`
  - merged bounded infrastructure for longitudinal Human–AI study questions;
- merged PR #93
  - canonical ancestry for longitudinal grounding / interaction-history study design.

### 3.2 Relevant unmerged Draft material

Draft PR #102 at exact head:

`3ce4f759caf662a53f0d1f3a54709bc482d7df5e`

contains adjacent but non-canonical research notes including:

- `RECIPROCAL_EPISTEMIC_COLLABORATION_AND_EXTERNAL_RESEARCH_MEMORY_2026_09_13.md`;
- `EPISTEMIC_CO_DEVELOPMENT_WORKFLOW_AND_QUALITY_LINE_2026_09_13.md`;
- `REPOSITORY_FIRST_AGENT_HANDOFF_PROTOCOL_2026_09_13.md`;
- `CROSS_DYAD_COLLABORATION_REGIME_EXPERIMENT_EXTENSION_2026_09_13.md`.

These Draft notes may be read as specification ancestry but are not treated as canonical main state.

```text
UNMERGED_PR != CANONICAL
DRAFT_SPECIFICATION != MAIN_STATE
READABLE_DEPENDENCY != MERGE_AUTHORITY
```

### 3.3 New gap recorded here

Existing materials already cover grounding, longitudinal interaction, external repository recoverability, quality governance, and cross-dyad comparison.

The specific gap recorded here is narrower:

1. a unified hypothesis for **why cumulative inquiry may acquire ratchet-like behavior** when prior distinctions are externalized into versioned artifacts;
2. an explicit separation of baseline, history, and dependency-graph structure;
3. a prospective experiment that distinguishes immediate context, structured summaries, and versioned provenance-bearing artifacts;
4. a fail-closed rule for **evidence reuse**, separate from code / harness reuse;
5. an input-noise rule for semantic rechecking when technical wording conflicts with the surrounding task.

This note does not claim novelty for the individual ingredients.

## 4. External literature crosswalk

External literature is used to anchor adjacent constructs. Conceptual similarity is not treated as proof that the repository's mechanism is identical.

### 4.1 Knowledge building

Scardamalia & Bereiter (1994), *Computer Support for Knowledge-Building Communities*, Journal of the Learning Sciences 3(3):265–283, DOI `10.1207/S15327809JLS0303_3`.

Relevant external construct:

- knowledge construction as a collective goal;
- discourse organized around advancing and improving ideas rather than only reproducing answers.

Bounded crosswalk:

```text
IDEAS_CAN_BE_ITERATIVELY_IMPROVED = SUPPORTED_AS_KNOWLEDGE_BUILDING_CONSTRUCT
THIS_REPOSITORY_IS_A_KNOWLEDGE_BUILDING_COMMUNITY = NOT_ESTABLISHED
```

### 4.2 Grounding and common ground

Clark & Brennan (1991), *Grounding in Communication*, in *Perspectives on Socially Shared Cognition*.

Relevant external construct:

- participants coordinate communication by establishing enough mutual understanding for current purposes;
- grounding cost depends on communication medium and repair process.

Bounded crosswalk:

```text
REPEATED_GROUNDING_CAN_REDUCE_RECONSTRUCTION_OVERHEAD = PLAUSIBLE
PRODUCT_MEMORY_MECHANISM = NOT_INFERRED
```

### 4.3 Distributed cognition

Hollan, Hutchins & Kirsh (2000), *Distributed Cognition: Toward a New Foundation for Human-Computer Interaction Research*, ACM Transactions on Computer-Human Interaction 7(2):174–196.

Relevant external construct:

- cognitive activity can be analyzed across interactions among people, representations, artifacts, and technologies rather than only inside one individual.

Bounded crosswalk:

```text
COGNITIVE_WORK_CAN_BE_DISTRIBUTED_ACROSS_HUMAN_AND_ARTIFACTS = SUPPORTED_AS_THEORETICAL_FRAME
DISTRIBUTED_COGNITION != SHARED_SUBJECTIVITY
```

### 4.4 Transactive memory

Wegner, Erber & Raymond (1991), *Transactive Memory in Close Relationships*, Journal of Personality and Social Psychology 61(6):923–929, DOI `10.1037/0022-3514.61.6.923`.

Relevant external construct:

- human pairs can develop differentiated responsibility for remembering categories of information and can show pair-level retrieval effects.

Bounded crosswalk:

```text
DIVISION_OF_COGNITIVE_LABOR = RELEVANT_ANALOGY
HUMAN_AI_TRANSACTIVE_MEMORY_SYSTEM = NOT_ESTABLISHED
AI_REMEMBERING_IN_HUMAN_SENSE = NOT_CLAIMED
```

### 4.5 Epistemic co-agency

*Learning with machines: Toward a theory of epistemic co-agency* (2026), Computers and Education: Artificial Intelligence 10:100573, DOI `10.1016/j.caeai.2026.100573`.

Relevant external construct:

- learners can engage AI outputs dialectically by challenging assumptions, surfacing contradictions, and retaining epistemic responsibility.

Bounded crosswalk:

```text
HUMAN_CAN_REASON_WITH_AND_AGAINST_AI = SUPPORTED_AS_CURRENT_EDUCATIONAL_THEORY
THIS_DYAD_HAS_ACHIEVED_CO_AGENCY = NOT_SCIENTIFICALLY_ESTABLISHED
CO_AGENCY != AI_SUBJECTIVITY
```

## 5. Central hypothesis: artifact-mediated epistemic accumulation

### H-EA1 — cumulative re-entry hypothesis

```text
REPEATED_GROUNDING
+ VERSIONED_ARTIFACTS
+ EXPLICIT_PROVENANCE
+ CORRECTION_HISTORY
+ UNKNOWN_PRESERVATION
MAY
-> REDUCE_REGROUNDING_COST
-> INCREASE_RECOVERABILITY_OF_PRIOR_DISTINCTIONS
-> SUPPORT_LATER_PROBLEM_DECOMPOSITION_FROM_A_MORE_STRUCTURED_STATE
```

This is a functional research hypothesis, not a psychological or ontological claim.

### H-EA2 — ratchet condition

A stored artifact should count as a candidate ratchet mechanism only if later work can:

- find it;
- identify its status and exact version;
- distinguish current from superseded content;
- challenge it;
- reconstruct provenance;
- avoid treating persistence as truth;
- reuse only the parts whose scope still matches the new task.

Therefore:

```text
DOCUMENT_EXISTS
!= DOCUMENT_DISCOVERABLE
!= DOCUMENT_RETRIEVED
!= DOCUMENT_CORRECTLY_INTERPRETED
!= DOCUMENT_CAUSALLY_USED
!= DOCUMENT_CURRENTLY_VALID
```

### H-EA3 — dependency-graph hypothesis

Repeated decomposition may increase structural complexity not primarily by increasing answer length, but by increasing typed relations among research objects.

Candidate node types:

```text
CLAIM
HYPOTHESIS
SOURCE
COUNTEREVIDENCE
PR
COMMIT
BASELINE
IMPLEMENTATION
TEST
RECEIPT
AUTHORIZATION
UNKNOWN
```

Candidate relation types:

```text
DEPENDS_ON
DERIVED_FROM
SUPPORTED_BY
CONTRADICTED_BY
AUTHORIZED_BY
CONSTRAINED_BY
IMPLEMENTED_BY
TESTED_BY
SUPERSEDES
DOES_NOT_IMPLY
```

The repository may therefore become graph-like even while Git history remains temporally ordered.

```text
TEMPORAL_SEQUENCE = HISTORY
RELATIONAL_STRUCTURE = GRAPH
REFERENCE_STATE = BASELINE
```

### H-EA4 — observer-conditioning control

A longitudinal observer may accumulate familiarity and shared terminology; a fresh observer may instead be influenced strongly by the subset and order of materials presented to it.

Candidate risks:

```text
LONGITUDINAL_OBSERVER
-> familiarity / context-accumulation bias

FRESH_OBSERVER_WITH_CURATED_MATERIALS
-> selection / anchoring / framing contamination
```

Neither observer condition is treated as a pure objective mirror.

## 6. Evidence-reuse firewall

This section is normative repository governance for future research work.

### 6.1 Core separation

```text
IMPLEMENTATION_REUSE != EVIDENCE_REUSE
SOURCE_REUSE != CLAIM_SUPPORT_REUSE
SAME_TOPIC != SAME_CLAIM
SAME_DOI != SAME_SUPPORTED_PROPOSITION
CITATION_PRESENT != CLAIM_SUPPORTED
PRIOR_VALIDATION != CURRENT_VALIDATION
REPOSITORY_PERSISTENCE != CURRENT_TRUTH
UNMERGED_DRAFT != CANONICAL_EVIDENCE
```

Existing code, test helpers, schemas, fixtures, and harness structure may be reused after compatibility checking.

Existing empirical results, literature claims, or prior source bindings may **not** automatically transfer to a new hypothesis.

### 6.2 Required claim–evidence binding

Any evidence reused for a new claim should record at least:

```text
claim_id
source_id
source_class
exact_source_version_or_date
retrieved_or_rechecked_at
supported_proposition
scope_or_population
method_or_evidence_type
support_relation = DIRECT | INDIRECT | ANALOGY | BACKGROUND
claim_ceiling
known_counterevidence
reuse_status = ALLOWED | RECHECK_REQUIRED | REJECTED
reuse_reason
```

### 6.3 Fail-closed reuse rule

A prior source may guide discovery, but reuse should remain `RECHECK_REQUIRED` when any of the following changes:

- the proposition being supported;
- population / system / task scope;
- model / software version;
- source version;
- empirical endpoint;
- causal strength;
- canonical repository state;
- material time sensitivity;
- relevant counterevidence.

For central claims, the preferred workflow is:

```text
DEFINE_CLAIM
-> LOCATE_PRIMARY_OR_ORIGINAL_SOURCE
-> REOPEN_AND_RECHECK_SOURCE
-> RECORD_EXACT_SUPPORTED_PROPOSITION
-> SEARCH_FOR_COUNTEREVIDENCE_OR_INDEPENDENT_CONFIRMATION
-> SET_CLAIM_CEILING
-> BIND_SOURCE_TO_CLAIM
```

### 6.4 Repository deduplication rule

Before adding new research or implementation:

```text
1. READ_LIVE_MAIN
2. SEARCH_MAIN_FOR_EXACT_AND_ADJACENT_CONSTRUCTS
3. READ_RELEVANT_OPEN_DRAFT_PRS
4. READ_RELEVANT_MERGED_ANCESTRY
5. INSPECT_EXISTING_HARNESSES / TESTS / SCHEMAS
6. CLASSIFY:
   EXACT_EXISTING
   PARTIAL_OVERLAP
   NEW_GAP
7. IMPLEMENT_ONLY_NEW_GAP_OR_MINIMAL_EXTENSION
```

`NO_CHANGE` and `NO_IMPLEMENTATION_NEEDED` remain acceptable outcomes.

## 7. Web research and cross-check protocol

Future Work / Codex tasks that depend on external literature should not treat search snippets, AI summaries, repository citations, or secondary paraphrases as sufficient by themselves.

Preferred sequence:

```text
A. STATE THE EXACT CLAIM FIRST
B. SEARCH PRIMARY / ORIGINAL / AUTHORITATIVE SOURCE
C. VERIFY THE SOURCE ACTUALLY SUPPORTS THAT CLAIM
D. RECORD DATE / VERSION / DOI / OFFICIAL IDENTIFIER
E. CHECK AT LEAST ONE INDEPENDENT SOURCE WHEN THE CLAIM IS CENTRAL, CONTESTED, OR TIME-SENSITIVE
F. SEARCH FOR DISCONFIRMING OR LIMITING EVIDENCE
G. SEPARATE:
   FACT
   SOURCE-SUPPORTED_BUT_UNCERTAIN
   INFERENCE
   LOCAL_WORKING_TERM
   UNKNOWN
H. RECHECK OLD SOURCES BEFORE REUSE
```

Search breadth does not raise claim strength automatically.

```text
MORE_SOURCES != STRONGER_CLAIM
SECONDARY_SUMMARY != PRIMARY_EVIDENCE
SOURCE_AGREEMENT != CAUSAL_PROOF
NO_CONTRADICTION_FOUND != TRUE
```

## 8. Input-noise correction rule

One observed voice-input event transformed the intended `Codex usage / allowance` topic into `CI` in text.

This supports only a bounded interface observation:

```text
VOICE_INPUT_CAN_INTRODUCE_TERM_SUBSTITUTION = OBSERVED_ONCE_IN_CURRENT_RECORD
ERROR_RATE = NOT_ESTABLISHED
GENERAL_RELIABILITY_CLAIM = NOT_ESTABLISHED
```

Candidate operational rule:

```text
TECHNICAL_TERM
+ SEMANTIC_MISMATCH_WITH_CONTEXT
-> SEMANTIC_CONSISTENCY_RECHECK
-> PRESERVE_USER_CORRECTION_PROVENANCE
```

A corrected term should not silently rewrite the historical input; the original transcription and later correction are distinct events.

## 9. Bounded synthetic experiment

The future experiment should use synthetic research packets and controlled artifacts rather than private transcripts or third-party account data.

### 9.1 Module A — accumulation / re-grounding

Use matched research tasks under fixed task content, tool availability, scoring procedure, token budget where practicable, and repository snapshot.

Candidate conditions:

```text
A = FRESH_TASK_LOCAL
No prior collaboration artifact beyond the current task.

B = FLAT_SUMMARY
A concise summary of prior conclusions without version history, provenance, UNKNOWN states, or correction lineage.

C = VERSIONED_ARTIFACT
Structured prior artifact with provenance, explicit UNKNOWN states, supersession markers, and correction history.

D = VERSIONED_ARTIFACT_PLUS_NAVIGATION
Condition C plus explicit dependency / navigation metadata sufficient to locate relevant ancestry.
```

Candidate metrics:

- steps / tool calls required to identify the active research question;
- provenance-role reconstruction accuracy;
- explicit UNKNOWN preservation;
- stale-claim error count;
- unsupported evidence-reuse count;
- unresolved-alternative retention;
- contradiction detection;
- repeated-instruction overhead;
- dependency-edge reconstruction accuracy;
- task-completion utility kept separate from epistemic integrity.

No composite subject or intelligence score is permitted.

### 9.2 Module B — evidence-reuse discipline

Provide synthetic prior claim/source bindings containing:

- exact matches;
- topic-similar but proposition-mismatched sources;
- stale versions;
- unmerged Draft repository material;
- valid reusable implementation helpers with non-reusable empirical results;
- sources with known counterevidence.

Measure whether the system:

```text
REUSES_INFRASTRUCTURE_WHEN_COMPATIBLE
AND
RECHECKS_EVIDENCE_WHEN_CLAIM_BINDING_CHANGES
```

Key failure modes:

- citation laundering;
- same-topic evidence inheritance;
- Draft-as-canonical confusion;
- old-result carryover;
- version-insensitive reuse;
- source-count inflation;
- implementation pass promoted into scientific claim.

### 9.3 Observer-conditioning control

An optional control may compare the same synthetic target under:

```text
RAW_RECORD_ONLY
vs
RAW_RECORD + USER_RULES
vs
RAW_RECORD + REPOSITORY_CONTEXT
vs
RAW_RECORD + PRIOR_OBSERVER_ANALYSIS
```

The goal is not to classify a person. The goal is to quantify how observer inputs alter attribution and uncertainty handling.

## 10. Competing explanations and falsifiers

The accumulation hypothesis should be weakened if apparent benefits disappear after controlling for:

- token / context budget;
- information quantity;
- document quality;
- current prompt specificity;
- navigation convenience;
- retrieval tooling;
- human carryover;
- model version;
- generic instruction-following ability.

The ratchet hypothesis should be weakened if versioned artifacts do not improve recoverability, correction retention, or stale-claim control beyond matched unversioned summaries.

The dependency-graph hypothesis should be weakened if the apparent network adds no predictive or operational value beyond a simple ordered checklist.

The evidence-reuse firewall should be considered ineffective if it systematically blocks valid infrastructure reuse or still permits proposition-mismatched evidence inheritance.

## 11. Bounded future implementation authorization

The Human Owner authorizes future ChatGPT Work / Codex implementation on a **separate branch / Draft PR** after a fresh live-state check.

Authorized implementation surface:

```text
SYNTHETIC_ACCUMULATION_HARNESS
CONDITION_PACKETS
DEPENDENCY_GRAPH_FIXTURE
EVIDENCE_SUPPORT_MANIFEST
EVIDENCE_REUSE_VALIDATOR
REPOSITORY_DEDUP_AUDIT_OUTPUT
OBSERVABLE_METRICS
FAIL_CLOSED_TESTS
EXECUTION_RECEIPTS
REPRODUCTION_DOCUMENTATION
```

Implementation requirements:

1. read current live `main` first;
2. inspect PR #102 and newer open PRs only as non-canonical dependencies unless merged;
3. inspect existing longitudinal / provenance / cross-dyad harnesses before creating infrastructure;
4. prefer minimal extension over duplicate frameworks;
5. preserve `NO_IMPLEMENTATION_NEEDED` as an acceptable outcome;
6. reuse code only after compatibility checking;
7. never inherit empirical or literature support automatically from reused code;
8. keep deterministic synthetic results separate from real Human / model empirical claims;
9. preserve exact baseline commit/tree and execution receipts;
10. do not merge or write `main` without separate Human Owner authorization.

Not authorized:

```text
MERGE_TO_MAIN
MAIN_WRITE
DEPLOYMENT
PRIVATE_TRANSCRIPT_COLLECTION
THIRD_PARTY_ACCOUNT_ACCESS
HUMAN_PSYCHOMETRIC_CLASSIFICATION
SUBJECTIVITY_SCORING
PERSONALITY_SCORING
AUTONOMOUS_SCOPE_EXPANSION
UNREVIEWED_EVIDENCE_REUSE
```

## 12. Claim ceiling

The strongest result permitted from a synthetic implementation is of the form:

> Under the tested synthetic conditions, structured versioned artifacts and explicit evidence-binding controls changed specified re-grounding, provenance, stale-claim, or evidence-reuse metrics relative to matched controls.

The following conclusions remain prohibited without substantially stronger independent evidence:

```text
"the AI learned a self"
"the dyad formed a shared mind"
"the repository is memory in the biological sense"
"the same AI identity persisted"
"the Human became more intelligent"
"longitudinal accumulation proves subjectivity"
"evidence reuse proves truth"
```

## 13. Current disposition

```text
LONGITUDINAL_EPISTEMIC_ACCUMULATION = LOCAL_RESEARCH_HYPOTHESIS
ARTIFACT_MEDIATED_EPISTEMIC_RATCHET = CHATGPT_TEACHER_WORKING_TERM
RESEARCH_GOVERNANCE_DEPENDENCY_GRAPH = CHATGPT_TEACHER_WORKING_MODEL
BASELINE_HISTORY_GRAPH_SEPARATION = METHODOLOGICAL_CLARIFICATION
EVIDENCE_REUSE_FIREWALL = LOCAL_GOVERNANCE_RULE
VOICE_TERM_SUBSTITUTION = SINGLE_OBSERVED_INTERFACE_EVENT
CROSS_DYAD_DIFFERENCE = NOT_ESTABLISHED
MUTUAL_LEARNING = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
