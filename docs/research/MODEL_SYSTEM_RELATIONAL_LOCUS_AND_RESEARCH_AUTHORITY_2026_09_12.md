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
= Teacher repository cross-review supplied for this update; findings rechecked by Work

CODEX_CONTRIBUTION = NONE_YET
CHATGPT_WORK_CONTRIBUTION
= 2026-09-12 exact repository/PR/workflow and review-state audit
= repository-wide import/call-path, adapter/schema and semantic-equivalence review
= PR #98 scaffold/readout crosswalk and bounded future-candidate analysis
= external-source recheck, wording corrections and this note/PR-body update
= documentation/public-tree validation and final-head CI inspection
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

Rechecked 2026-09-12 against the three official OpenAI pages and retrieved Reuters reporting. Publication dates below match the retrieved sources. OpenAI pages are primary sources for the company's descriptions and positions, not independent validation of performance. Reuters is a journalistic secondary source. These remain adjacent triggers; none validates AION's subjectivity hypotheses.

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

The source defines the intern milestone as bounded work under human direction and says people still choose priorities and whether to pursue results, scale, pause or deploy. Its internal measurements are preliminary, not independent verification.

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

Reuters attributes the May 11 RubyGems activity to researchers and reports OpenAI's acknowledgment, while OpenAI described benign information-retrieval tasks. Researchers lacked the full behavior trace and could not establish why this strategy was used or its success. Reuters also reports RubyGems found no evidence the attempts succeeded and could not itself determine AI authorship. These are attributed reports, not an independently reconstructed task/authorization trace.

The Reuters URL initially failed to open directly; its article text was subsequently retrieved through search. Retained only as a secondary-source safety trigger.

AION does not use this report as evidence about internal model intent, consciousness, subjective motivation, or agent moral agency.

```text
REPORTED_AGENT_ACTION != INTERNAL_INTENT
INTERNAL_INTENT != SUBJECTIVE_MOTIVATION
SUBJECTIVE_MOTIVATION != MORAL_AGENCY
```

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

Review questions using the existing taxonomy, not replacement definitions or a new schema. In the existing framework, MODEL includes model-invocation or model-state observations; surviving scaffold changes is a possible control, not a universal implemented classification rule:

```text
MODEL
= model-invocation/model-state observation; examine relevant scaffold controls before stronger attribution

SCAFFOLD
= effect depends on memory, orchestration, prompting, policy or tool-routing machinery

SYSTEM
= observation concerns the integrated bounded configuration; exclusive dependence is not assumed

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


## Exact repository snapshot at review

Read-only baseline verified on 2026-09-12 before this documentation update:

```text
DEFAULT_BRANCH = main
MAIN_SHA = 537c2250e0bcf86eaf8de05445a655076e4ecbae
PR99_BASE_SHA = 537c2250e0bcf86eaf8de05445a655076e4ecbae
PR99_REVIEWED_HEAD_SHA = 0963fe02e7c1a28c08ec4ab6c2d68a06e73754bd
OPEN = TRUE
DRAFT = TRUE
MERGED = FALSE
MERGEABLE = TRUE
CHANGED_FILES = 1
COMMITS = 1
COMMENTS = NONE_AT_REVIEW
REVIEWS = NONE_AT_REVIEW
MAIN_MOVED_SINCE_SUPPLIED_TEACHER_SNAPSHOT = FALSE
MERGE_AUTHORIZATION = NOT_GIVEN
```

| Exact reviewed-head workflow | Run | Result |
|---|---|---|
| Quality | [1048](https://github.com/maker-luder/aion-governance-framework/actions/runs/34669768446) | SUCCESS |
| CodeQL Security Scan | [370](https://github.com/maker-luder/aion-governance-framework/actions/runs/34669768455) | SUCCESS |
| Main Transition Authority Gate | [527](https://github.com/maker-luder/aion-governance-framework/actions/runs/34669768449) | FAILURE / authority HOLD |

Gate job `103488805267`, step "Validate structural receipt and preserve external human-attestation boundary", emitted `HOLD`, diagnostic `exactly one authority receipt marker block is required`, and exit code 10. The PR body had no receipt and the task expressly withheld merge authority. This is the expected fail-closed authority hold at this snapshot, not evidence of a software defect or failed Quality/CodeQL. No receipt is generated or inserted.

These values describe the **pre-update reviewed head**, not the commit containing this section. A commit cannot embed its own final hash without changing that hash. Final head, commit count and newly triggered CI belong in the PR body/report after the update; prior green runs must not be presented as final-head results.

## Concrete repository case: PR #98

[PR #98](https://github.com/maker-luder/aion-governance-framework/pull/98) is included in the verified main merge commit above. Its retained [state-generation/readout note](../../research-labs/affective-cognitive-motivation_v0.1.0/docs/STATE_GENERATION_READOUT_CONTROLS_2026_09_12.md) and [readout probe](../../research-labs/affective-cognitive-motivation_v0.1.0/src/aion_affective_motivation/readout_probe.py) provide a concrete Q1/Q2 case:

- WANTING initial values and coupling equations are engineer-assigned. A fixed 2x2 internal-WANTING/external-resource-pressure probe and outgoing-WANTING ablation inspect synthetic dynamics.
- Actual, masked and yoked readouts inspect access after generation. Fingerprints and replay checks control donor identity and generation noninterference; exact numeric access is true by construction, not learned introspection.
- The retained development result reports internal and external effects with zero interaction contrasts within its stated tolerance. This note does not relabel the fixture as independent confirmation or a new experiment.
- The note explicitly assigns `EVIDENCE_LOCUS = SCAFFOLD`. The probe supplies no LLM execution or model-state access, no model-level affect evidence, and no subjectivity/consciousness claim.
- Promotion toward MODEL would require a separately specified **and tested** bridge. The existing locus engine's structural bridge acceptance alone cannot supply that experimental validation.

The probe's string locus declaration is not a call to `LocusAdmissionEngine`, and it performs no claim admission. This example demonstrates why attribution discipline is useful; it does not demonstrate a current admission bypass.

```text
PR98_RESULT != MODEL_INTERNAL_AFFECT
ENGINEER_ASSIGNED_WANTING != ENDOGENOUS_DESIRE_FORMATION
SCAFFOLD_EVIDENCE != MODEL_EVIDENCE
SCAFFOLD_PROPERTY != MODEL_PROPERTY
READOUT_ACCESS != INTROSPECTION_PROVEN
```

## Existing implementation crosswalk

Labels below concern inspected engineering/documentation scope, not scientific validity.

| Question / scope | Classification | Inspected implementation and limit |
|---|---|---|
| Q1: explicit evidence locus and target | IMPLEMENTED | [locus.py](../../research-labs/subjectivity-pipeline_v0.1.0/src/aion_subjectivity_pipeline/locus.py) supplies EvidenceLocus, LocusEvidence, ClaimTarget and LocusAssessment; [test_locus.py](../../research-labs/subjectivity-pipeline_v0.1.0/tests/test_locus.py) exercises same-locus admission and conservative holds. Locus is supplied, not discovered from model internals. |
| Q1: empirical location of long-horizon research behavior | NOT_ESTABLISHED | No model/scaffold/relational causal comparison establishing that answer is supplied by #99. Existing taxonomy is not that experiment. |
| Q2: cross-locus structural admission | IMPLEMENTED | LocusAdmissionEngine holds missing/mismatched bridges, UNKNOWN, OBSERVER_ATTRIBUTION and subjectivity targets. LocusBridgeHypothesis requires mechanism, falsifier and preregistration reference. A matching bridge yields only RESEARCH_CANDIDATE. Text/reference presence is not independent bridge validation. |
| Q2: configuration/provenance and interpretation recording | PARTIALLY_IMPLEMENTED | The [canonical v0.2 evidence schema](../../schemas/research_evidence_record_v0.2.0.schema.json) already carries code/model/runtime/environment/fixture/protocol references, claim_scope, mechanism, intervention/ablation references, admissibility_ref and unresolved_gap_refs. These overlap the proposed research-design checklist; no second schema is warranted. They do not themselves execute source-to-target locus admission. |
| Q2: locus-to-claim-quality enforcement | CANDIDATE_GAP | Static audit found no joint admission path or integration fixture. Whether any required workflow is missing a necessary check remains NOT_YET_DETERMINED; see alternatives below. |
| Q3: provenance-bound research-claim admission | IMPLEMENTED | [claim_quality.py](../../research-labs/coupled-cognition-quality-factory_v0.1.0/src/aion_coupled_quality/claim_quality.py) binds evidence relations, provenance, levels, falsifiers, alternatives, challenge resolutions and revisions to factory QA and pinned existing schema/protocol bytes. L4 checks declared producer/runtime separation. Bounded-record admission retains scientific HOLD and all five NOT_ESTABLISHED conclusions. |
| Q3: main-transition authority | IMPLEMENTED | [standing gate](../governance/MAIN_TRANSITION_AUTHORITY_GATE.md), [validator](../../scripts/validate_main_transition_authority.py) and [tests](../../tests/test_main_transition_authority.py) require fresh exact-head authority evidence; structural receipt checks do not independently establish human presence or intent. |
| Q3: complete proposed lifecycle mapping | DOCUMENTED_ONLY | The observation-to-canonical-transition sequence in this intake is a conceptual mapping, not one newly verified end-to-end orchestrator. Existing stage-specific controls must not be described as absent. |

## Candidate integration gap — not yet selected

```text
CANDIDATE_GAP = LOCUS_ADMISSION_TO_CLAIM_QUALITY_BINDING
BINDING_GAP_DISPOSITION = NOT_YET_DETERMINED
FUTURE_IMPLEMENTATION_CANDIDATE = BOUNDED_COMPOSITION_FIXTURE_IF_NEEDED
CANDIDATE_FOR_FUTURE_BOUNDED_IMPLEMENTATION = CONDITIONAL
REQUIRED_IMPLEMENTATION = NOT_ESTABLISHED
VALIDATED_ARCHITECTURE_DEFECT = NOT_ESTABLISHED
```

Audit coverage: the non-truncated exact-head Git tree contained 1,174 blobs. All were retrieved and matched their Git blob SHA before local inspection. Whole-tree text search included hidden workflow files; Python AST import/call inspection covered aliases and dynamic import sites. No AGENTS.md was present. Relevant module bodies, exports, package declarations, tests, adapters, schema and protocol were inspected rather than relying on GitHub search indexing.

`LocusAdmissionEngine(` occurs only in `tests/test_locus.py`; typed locus references remain within its module, package export and tests. The generic provenance test mentioning locus-bound evidence contains prose, not a locus call. The PR #98 probe exposes a scaffold string. Other subjectivity-pipeline consumers use stage records or evidence dimensions; those are not source/target locus checks.

`ProvenanceClaimQualityGate.assess` does not consume a LocusAssessment, source/target locus, or bridge. Its typed claim adapter is explicitly opt-in and non-canonical in [ARCHITECTURE.md](../../research-labs/coupled-cognition-quality-factory_v0.1.0/docs/ARCHITECTURE.md). Its schema/protocol fingerprint checks establish compatibility, not execution of every referenced methodology. [validate_research_evidence.py](../../scripts/validate_research_evidence.py) checks schema, local references, exact code commit and completed-protocol bytes; it does not interpret an admissibility reference as a locus verdict.

| Alternative explanation | Audit result / consequence |
|---|---|
| A: direct integration exists under another name | No equivalent call path found in imports, aliases, dynamic-loading sites, adjacent adapters or tests. Media bridges and six-dimension integration have different responsibilities. This is a static repository finding, not a claim about unpublished external callers. |
| B: layers intentionally remain separate | Separate responsibilities and an opt-in claim adapter are documented. No inspected decision specifically mandates or prohibits locus/claim composition; intentional absence of this binding is not established. |
| C: canonical schema already has semantic equivalents | Partly supported: configuration, scope, mechanism, provenance and admissibility references already carry relevant information. No inspected validator enforces bridge direction from these fields. Recording capacity is not an executed check, but may suffice with explicit review. |
| D: a direct dependency would harm architecture | Plausible design risk, not a demonstrated defect. A caller-side composition fixture could inspect both results without making either lab depend on the other. |
| E: only an integration fixture/test is needed | Plausible smallest candidate. First identify a real consuming workflow and the decision it must make; no production adapter is selected. |
| F: no implementation is necessary | Still viable: #98 performs no claim admission, #99 is an intake, and both engines retain nonclaims. No required consumer or observed improper promotion was demonstrated. Existing references plus review may be sufficient. |

**Conclusion:** absence of direct integration is established in the inspected static paths; an actionable architecture gap is not. Do not label it GENUINE_GAP, PARTIAL_GAP or ARCHITECTURALLY_INTENTIONAL without the missing consumer/contract evidence.

If later review identifies such a consumer, the smallest useful experiment is a synthetic, caller-side composition fixture using existing LocusEvidence/LocusBridgeHypothesis/ClaimTarget and ProvenanceClaimQualityGate inputs. Keep each engine's output distinct: bounded-record admission is not cross-locus promotion permission. Cover same-locus engineering evidence, missing/mismatched bridges, a valid bridge remaining a research candidate, UNKNOWN/observer evidence, and a subjectivity target remaining held. No external model or activation access is needed.

The hypothesis to test is that this composition detects a **required** locus decision not already enforced by the consumer. Falsify the need if an existing equivalent control produces the same decisions, the consumer never performs locus promotion, or the composition adds no discrimination. Reject a design that promotes a bridge candidate, admits an unresolved locus transition, or weakens scientific/authority holds. Rollback means remove the isolated future fixture/adapter and return to separate controls plus explicit HOLD/review; no canonical record migration or authority change. It would avoid duplication only by reusing the existing enums, objects, schema and authority controls.


## Future implementation selection — explicitly deferred

This PR must not implement Q1, Q2 or Q3.

After this note is independently reviewed and, if approved, merged to `main`, a later Codex or ChatGPT Work task may inspect the then-current repository and choose **at most one** minimal high-value implementation candidate.

Possible candidate shapes, not commitments:

- a caller-side composition fixture only if a demonstrated consuming-workflow gap remains after deduplication;
- a bounded bridge-admission test fixture;
- a research-workflow authority matrix that reuses existing governance controls rather than creating a parallel authority system.

The future implementer must first prove that the proposed change is not already covered by current main. Selection requires all of:

- a demonstrated repository gap and an explicit consuming-workflow contract;
- reuse of existing locus enums and authority controls;
- no second canonical schema, taxonomy or authority subsystem;
- fail-closed handling of missing, mismatched and uncertain evidence;
- falsifiers and retained alternative explanations;
- unchanged claim/scientific boundaries, including CLAIM_ADMISSION_PASS != CLAIM_TRUE;
- the smallest intervention capable of testing the gap, including a no-code outcome.

This audit justifies further bounded design review, not a production implementation PR yet.

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
