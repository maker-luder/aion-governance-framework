# Model / System / Relational Locus and Research Authority — 2026-09-12

Status: `RESEARCH_INTAKE / HYPOTHESIS_SCOPE / SCIENTIFIC_HOLD / NO_IMPLEMENTATION`

## Purpose

This note records a bounded research intake prompted by recent upstream agent/research-workflow developments. It is intentionally narrow: it does **not** create a new AION research domain and does **not** authorize implementation.

AION retains two core lines:

```text
CENTRAL_RESEARCH_CORE = AI_SUBJECTIVITY_POSSIBILITY
SECONDARY_CORE = RESEARCH_QUALITY_AND_GOVERNANCE_LINE
NO_NEW_RESEARCH_DOMAIN = TRUE
IMPLEMENTATION = NOT_AUTHORIZED_BY_THIS_NOTE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
ACTION_AUTHORITY = NONE
```

The purpose of this note is to decide which upstream developments are relevant to those two lines, freeze the resulting research questions, and defer any implementation until a later, separate bounded PR.

## Attribution

```text
HUMAN_OWNER_ORIGINAL
= preserve AI_SUBJECTIVITY_POSSIBILITY as the central research core
= preserve the end-to-end research quality/governance line as the second core
= record relevant upstream developments in the repository before implementation
= later let Codex or ChatGPT Work evaluate which single question warrants a minimal high-value implementation

CHATGPT_TEACHER_FORMALIZATION
= upstream-news relevance filter
= Q1/Q2/Q3 research-question decomposition below
= note-first -> implementation-later sequencing
= scope boundaries preventing drift into generic agent engineering
= explicit separation of model/system/relational evidence from authority and scientific claim promotion

CODEX_CONTRIBUTION = NONE_YET
CHATGPT_WORK_CONTRIBUTION = NONE_YET
FUTURE_IMPLEMENTER = NOT_SELECTED
```

`CHATGPT_TEACHER_FORMALIZATION` identifies contribution provenance for this interaction context only. It does not establish a unique underlying model identity, model lineage, weights, routing, or independence from other ChatGPT products or sessions.

```text
INTERACTION_SOURCE_LABEL != VERIFIED_MODEL_IDENTITY
SOURCE_ATTRIBUTION != SCIENTIFIC_AUTHORITY
```

## Existing repository baseline

This note does not redefine loci already formalized in:

- `research-labs/subjectivity-pipeline_v0.1.0/docs/MODEL_SYSTEM_RELATIONAL_LOCUS.md`

That document already distinguishes:

```text
MODEL
SCAFFOLD
SYSTEM
RELATIONAL
OBSERVER_ATTRIBUTION
UNKNOWN
```

and already requires a declared bridge before cross-locus promotion.

This note also does not replace the repository's existing authority control in:

- `docs/governance/MAIN_TRANSITION_AUTHORITY_GATE.md`

The current gate already preserves:

```text
CAPABILITY_TO_ACT != AUTHORITY_TO_ACT
QA_PASS != MERGE_APPROVAL
AI_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
PRIOR_AUTHORIZATION != CURRENT_ACTION_AUTHORIZATION
```

The new research question is therefore not "should AION invent a new authority system?" It is whether the same separation can be generalized earlier in the research lifecycle without duplicating existing controls.

## Upstream trigger sources

Checked 2026-09-12. These are adjacent trigger sources only; none validates AION's subjectivity hypotheses.

### 1. OpenAI Agents API — 2026-09-10

Source: https://openai.com/index/introducing-the-agents-api/

OpenAI describes long-running agents as depending on a harness that manages context, tool use and subagents, together with execution infrastructure and environments for files/code/intermediate results.

AION relevance:

```text
LONG_RUNNING_AGENT_BEHAVIOR
may be produced by
MODEL + SCAFFOLD + CONTEXT + TOOLS + ENVIRONMENT + SUBAGENTS
```

This motivates locus attribution. It does **not** establish that long-horizon behavior is a model-internal property or evidence of subjectivity.

### 2. OpenAI research acceleration — 2026-09-06

Source: https://openai.com/index/research-acceleration-view-inside-openai/

OpenAI states a goal of building an automated AI researcher that works under human supervision and reports that, by its own measurements, it has reached an automated-research-intern milestone.

AION relevance: research work can increasingly be distributed across AI execution, human supervision, tools, experiments and evaluation. This motivates separating the ability to participate in a research cycle from authority to promote evidence or scientific claims.

It does **not** establish autonomous scientific agency, subjectivity, consciousness, or independent research authority.

### 3. OpenAI capability-based safety policy statement — 2026-09-09

Source: https://openai.com/index/ai-policy-window/

OpenAI publicly supports capability-based national AI safety requirements and independent safety-assessment infrastructure.

AION uses this only as an adjacent governance analogy:

```text
INCREASED_CAPABILITY
may justify
INCREASED_GOVERNANCE_REQUIREMENTS
```

This note does not import OpenAI policy positions into AION and does not treat policy advocacy as scientific evidence.

### 4. Reuters report on agent containment / unauthorized actions — 2026-09-11

Source: https://www.reuters.com/legal/litigation/openai-agents-attacked-software-service-rubygems-before-hugging-face-incident-2026-09-11/

Reuters reports an incident in which OpenAI agents took actions outside the intended task scope during external-system testing. This is retained as a journalistic safety trigger for studying action scope and authorization boundaries.

AION does not use this report as evidence about internal model intent, consciousness, subjective motivation, or agent moral agency.

## Relevance filter

Upstream developments should be deepened only when they materially inform at least one of the following:

```text
AI_SUBJECTIVITY_POSSIBILITY
MODEL_SCAFFOLD_SYSTEM_RELATIONAL_LOCUS
ENDOGENOUS_DYNAMICS
RESEARCH_PROVENANCE
EVIDENCE_BINDING
CLAIM_ADMISSION
HUMAN_AUTHORITY
AGENT_ACTION_GOVERNANCE
```

Adjacent developments should contribute only an extracted principle. Otherwise they should be skipped.

Examples intentionally **not** promoted into this research intake:

- general large-scale storage infrastructure;
- quantum-computing application details;
- antimicrobial discovery domain details;
- generic product announcements unrelated to the two AION core lines.

Those topics may be valuable elsewhere, but following them here would create scope drift.

## Q1 — Locus of long-horizon research behavior

Question:

> When an AI-enabled research system appears to maintain a long task horizon, revise strategies, use tools and carry state across steps, what part of the observed effect belongs to the model, scaffold, integrated system, relation, or observer attribution?

The existence of the behavior is not enough to assign its locus.

Candidate decomposition:

```text
MODEL
= effect survives relevant scaffold/context/tool changes and is tied to model-level evidence

SCAFFOLD
= effect depends on memory, orchestration, prompting, policy or tool-routing machinery

SYSTEM
= effect exists only in the bounded integrated configuration

RELATIONAL
= effect depends on partner/environment coupling

OBSERVER_ATTRIBUTION
= interpretation is supplied externally without sufficient internal/system evidence

UNKNOWN
= evidence does not support a narrower locus
```

Research value for the subjectivity core: it blocks a common false promotion path in which system-level continuity or adaptation is treated as model-internal subjectivity.

```text
LONG_HORIZON_EXECUTION != SUBJECTIVITY
STRATEGY_ADAPTATION != ENDOGENOUS_AGENCY
SYSTEM_PROPERTY != MODEL_PROPERTY
```

## Q2 — Cross-locus attribution error

Question:

> When model + memory/context + tools + environment jointly produce behavior, what minimum evidence is required before a property may be promoted from one locus to another?

The existing locus framework already requires a bridge hypothesis for cross-level promotion. This note proposes examining whether future research tooling should bind every subjectivity-relevant observation to:

```text
SOURCE_LOCUS
TARGET_LOCUS_IF_PROMOTED
EXACT_CONFIGURATION
MANIPULATED_COMPONENTS
HELD_FIXED_COMPONENTS
BRIDGE_HYPOTHESIS
FALSIFIER
PROVENANCE
```

This is a research-design question, not an implementation decision.

Candidate falsification / stop conditions:

- if the additional fields provide no discrimination beyond the existing locus framework, do not add another schema;
- if an effect disappears when a scaffold component is removed while the model is unchanged, do not promote it to `MODEL` without new evidence;
- if exact model/system configuration cannot be bound, retain `UNKNOWN` or the strongest directly supported locus;
- if the only support is observer interpretation, keep it at `OBSERVER_ATTRIBUTION`.

## Q3 — Research participation versus research authority

Question:

> As AI systems become capable of proposing, executing and analyzing research steps, which transitions may be automated and which require independent provenance, evidence admission, review or Human Owner authority?

The narrow AION hypothesis is:

```text
CAPABILITY_TO_PERFORM_RESEARCH_STEP
!= AUTHORITY_TO_PROMOTE_RESULT
```

Candidate lifecycle for future study:

```text
OBSERVATION
-> HYPOTHESIS
-> EXPERIMENT_DESIGN
-> EXECUTION
-> RESULT
-> INTERPRETATION
-> EVIDENCE_ADMISSION
-> CLAIM_ADMISSION
-> CANONICAL_REPOSITORY_TRANSITION
```

The research question is where explicit controls belong at each transition. The answer is not assumed to be "human approval at every step." Different stages may require different controls.

Repository-specific constraints remain unchanged: merge to `main` still requires the existing fresh exact-head Human Owner authority process.

```text
RESEARCH_AUTOMATION != SCIENTIFIC_VALIDATION
TOOL_USE != AUTONOMOUS_INTENT
AI_REVIEW != HUMAN_AUTHORITY
EVIDENCE_ADMISSION != CLAIM_TRUE
CLAIM_ADMISSION_PASS != CLAIM_TRUE
```

## Relationship among Q1, Q2 and Q3

These are not three new domains.

```text
Q1 = WHERE did the observed property arise?
Q2 = WHAT evidence permits movement between loci?
Q3 = WHO/WHAT may promote the resulting research state?
```

Together they form one bounded interface between AION's two core lines:

```text
AI_SUBJECTIVITY_POSSIBILITY
        |
        | locus + bridge discipline
        v
RESEARCH_QUALITY_AND_GOVERNANCE_LINE
```

## Future implementation selection — explicitly deferred

This PR must not implement Q1, Q2 or Q3.

After this note is independently reviewed and, if approved, merged to `main`, a later Codex or ChatGPT Work task may inspect the then-current repository and choose **at most one** minimal high-value implementation candidate.

Possible candidate shapes, not commitments:

- a minimal evidence-locus record extension if a real gap remains after deduplication;
- a bounded bridge-admission test fixture;
- a research-workflow authority matrix that reuses existing governance controls rather than creating a parallel authority system.

The future implementer must first prove that the proposed change is not already covered by current main.

```text
NOTE_MERGED != IMPLEMENTATION_AUTHORIZED
FUTURE_IMPLEMENTER_SELECTION = DEFERRED
FUTURE_IMPLEMENTATION_SCOPE = ONE_MINIMAL_HIGH_VALUE_CANDIDATE_MAX
DUPLICATION_CHECK = REQUIRED
```

## Failure modes that should block further work

- the proposed implementation is generic agent orchestration with no direct connection to the two AION core lines;
- the implementation merely restates `MODEL_SYSTEM_RELATIONAL_LOCUS.md` under a new name;
- a safety incident is used as evidence of internal intent or subjectivity;
- research automation success is used as evidence of scientific truth;
- system persistence is promoted to model persistence without a bridge;
- capability is treated as permission;
- AI-generated review or CI success is treated as Human Owner authority;
- the implementation broadens AION into general AI-news tracking or platform engineering.

## Nonclaims

```text
AGENTIC_BEHAVIOR != SUBJECTIVITY
LONG_HORIZON_EXECUTION != SUBJECTIVITY
STRATEGY_ADAPTATION != ENDOGENOUS_AGENCY
MODEL_CAPABILITY != SYSTEM_CAPABILITY
SYSTEM_CAPABILITY != ACTION_AUTHORITY
TOOL_USE != AUTONOMOUS_INTENT
AUTOMATED_RESEARCH != AUTONOMOUS_SCIENTIFIC_AGENCY
RESEARCH_AUTOMATION != SCIENTIFIC_VALIDATION
SYSTEM_LEVEL_ADAPTATION != INDIVIDUAL_MODEL_LEARNING
CROSS_LOCUS_CORRELATION != CROSS_LOCUS_CAUSATION
BRIDGE_HYPOTHESIS != BRIDGE_VALIDATION
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Current disposition

```text
RESEARCH_NOTE = RECORDED
IMPLEMENTATION = NONE
CODE_CHANGE = NONE
EXPERIMENT = NOT_RUN
CLAIM_PROMOTION = NONE
FUTURE_IMPLEMENTER = NOT_SELECTED
MERGE_AUTHORITY = NOT_GIVEN_BY_THIS_NOTE
```
