# Cross-dialogue research intake — 2026-09-24

Status: `RESEARCH_INTAKE / RECORD + DEDUP + TRIAGE / DOCUMENTATION_ONLY / SCIENTIFIC_HOLD`

```text
REPOSITORY = maker-luder/aion-governance-framework
BASE_MAIN = 71321ed87d1ececfcc5989327578dfefe02faea5
SOURCE_WINDOW = CROSS_DIALOGUE_REVIEW_THROUGH_2026_09_24

PURPOSE = RECORD + DEDUP + TRIAGE
IMPLEMENTATION = NONE
MAIN_WRITE = NO
MERGE = NO
READY_FOR_REVIEW = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SCIENTIFIC_DISPOSITION = HOLD
```

## Purpose

This note records a bounded cross-dialogue intake after re-reading recent Human Owner–ChatGPT Teacher discussions and re-checking live repository state.

It does not authorize implementation. Its job is to distinguish:

```text
NEW_GAP
EXISTING_BRANCH_EXTENSION
NEEDS_DEDUP
DEFERRED_RESEARCH
ALREADY_RECORDED
```

so that later Work / Codex review does not reimplement already existing repository structures merely because the same research question reappeared in a later conversation.

```text
IMPORTANT != NEEDS_NEW_PR
RECORDED != MERGED
NOT_IN_MAIN != NOT_EXISTING
EXISTING_VALID_IMPLEMENTATION > UNNECESSARY_REIMPLEMENTATION
```

## Provenance

```text
HUMAN_OWNER_ORIGINAL
= requested a careful cross-dialogue extraction of material that may belong in the repository
= approved a documentation-only RECORD + DEDUP + TRIAGE intake
= explicitly required no main write, no merge and no implementation
= requested tool-assisted review using Superpowers, Wolfram, MindMap, Hugging Face and GitHub
= clarified that Hugging Face should not be used as the discovery/search layer; public Web discovery should precede any Hugging Face read attempt

CHATGPT_TEACHER
= performed the cross-dialogue extraction
= re-checked live GitHub state
= performed repository deduplication and classification
= performed external-source cross-check
= proposed bounded formalizations and claim ceilings
= created this documentation-only intake branch

WORK = NONE_THIS_PASS
CODEX = NONE_THIS_PASS
```

## Live repository baseline

Verified during this intake:

```text
MAIN_HEAD =
71321ed87d1ececfcc5989327578dfefe02faea5

PR_197 = CLOSED / DRAFT / NOT_MERGED
HEAD = 2c1ca11eef4296e714d804934662073b8aa3d0c7

PR_198 = CLOSED / DRAFT / NOT_MERGED
HEAD = bd50c06da83e5d41c8fad158afb0a5707f823d5f

PR_199 = CLOSED / DRAFT / NOT_MERGED
HEAD = c4fe363524c8e1fe779dcd48e5464d889cc648be

PR_200 = MERGED
HEAD = 61c182a66c1b1c93c045e80b33d46da7e59a2740

PR_201 = CLOSED / DRAFT / NOT_MERGED
HEAD = ea6ae77ef0aff124175bd3cf69edb6ea036f4de0

PR_202 = CLOSED / DRAFT / NOT_MERGED
HEAD = 7f84ae8c95f1b7caaaa0c3850a0b6cfd049b7108

PR_203 = CLOSED / DRAFT / NOT_MERGED
RECORDED_PR_HEAD = ab54d99a11b32b10cfcb76c385c023b0caa7f14d

PR_203_CONTINUING_BRANCH =
research/embodiment-convergence-20260923

PR_203_CONTINUING_BRANCH_HEAD =
5c3877adcfc1f7d67e8700fdac26b13c5c202a43

ISSUE_181 = CLOSED / DEFERRED
ISSUE_189 = OPEN / RECORD_ONLY
```

The closed PR #203 page does not represent the latest continuing branch state. Any later embodiment review must use the branch exact head rather than inheriting the historical PR snapshot.

---

# 1. NEW_GAP — Human participant research ethics / power asymmetry

## Repository finding

Current repository surfaces already contain informed-consent language, governance authority controls, stop conditions and Human-participant boundaries. However, current-main code/document search did not identify an explicit repository-level formalization of:

```text
POWER_ASYMMETRY
RIGHT_TO_WITHDRAW
INDEPENDENT_OVERSIGHT
DEPENDENT_RELATIONSHIP_RISK
CONTINUING_VOLUNTARINESS
```

as one coherent Human-participant research control layer.

This is therefore recorded as a candidate real gap rather than a new subjectivity dimension.

## Candidate formalization

```text
RESEARCHER_AUTHORITY
!= PARTICIPANT_OBLIGATION_TO_COMPLY

ENTRY_CONSENT
!= IRREVOCABLE_CONSENT

CONSENT_GIVEN_AT_T0
!= CONSENT_ASSUMED_AT_TN

DEPENDENT_RELATIONSHIP
-> HEIGHTENED_COERCION_OR_UNDUE_INFLUENCE_REVIEW

PARTICIPATION
REQUIRES
  VOLUNTARINESS
+ RIGHT_TO_REFUSE
+ RIGHT_TO_WITHDRAW_WITHOUT_REPRISAL
+ CLEAR_STOP_CONDITIONS
+ PRIVACY_AND_CONFIDENTIALITY
+ INDEPENDENT_RIGHTS_CONTACT_OR_OVERSIGHT_PATH
+ RECONSENT_OR_UPDATED_INFORMATION_WHERE_MATERIALLY_RELEVANT
```

The phrase `CONTINUING_CONSENT` is used here as a repository shorthand for ongoing voluntariness and the continuing ability to discontinue participation. It is not claimed as a verbatim term from every cited ethics framework.

## External correspondence

Primary / authoritative starting points checked:

- U.S. HHS OHRP, *Belmont Report*: valid consent requires voluntariness free from coercion and undue influence; authority relationships can create unjustifiable pressure.
  - https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/read-the-belmont-report/
- U.S. HHS OHRP, *Informed Consent FAQs*: research participation is voluntary, subjects may discontinue participation without penalty, and investigators must minimize coercion or undue influence.
  - https://www.hhs.gov/ohrp/regulations-and-policy/guidance/faq/informed-consent/
- U.S. HHS OHRP, *Withdrawal of Subjects from Research Guidance*: research protocols should plan for withdrawal and define how it is handled.
  - https://www.hhs.gov/ohrp/regulations-and-policy/guidance/guidance-on-withdrawal-of-subject/
- World Medical Association, *Declaration of Helsinki*, 2024 revision: ethics committees must be independent and able to resist undue influence; participants may refuse or withdraw without reprisal; special caution is required where a dependent relationship may affect consent.
  - https://www.wma.net/policies-post/wma-declaration-of-helsinki/

Scope limitation:

```text
MEDICAL_RESEARCH_ETHICS_STANDARD
!= AUTOMATIC_LEGAL_APPLICABILITY_TO_THIS_REPOSITORY

US_HUMAN_SUBJECT_REGULATION
!= AUTOMATIC_JURISDICTIONAL_APPLICABILITY

METHOD_CORRESPONDENCE
!= LEGAL_DETERMINATION
```

A later implementation decision must separately determine the applicable legal / institutional review framework for any actual Human-participant study.

## Claim boundary

```text
ETHICAL_GOVERNANCE
!= SUBJECTIVITY_EVIDENCE

PARTICIPANT_PROTECTION
!= AI_MORAL_AGENCY

CONSENT_PROTOCOL
!= SCIENTIFIC_VALIDATION
```

---

# 2. NEW_GAP — Research execution reliability / resource-aware orchestration

## Repository finding

Current main contains tool-routing references and multiple stop/fail-closed policies, but the governance kernel explicitly does not implement tool routing. Repository search did not identify a unified `resource-aware`, `minimum necessary tool`, or `failure budget` control surface.

Recent cross-dialogue work repeatedly exposed a practical failure mode:

```text
EXISTING_VALID_ARTIFACT_AVAILABLE
+
REIMPLEMENTATION_FROM_SCRATCH
->
UNNECESSARY_COST
+
LONGER_REVIEW_CHAIN
+
MORE_FAILURE_SURFACE
```

The issue is not merely efficiency. Repeated tool retries, duplicated implementation and partial channel failures can degrade provenance and review reliability.

## Candidate formalization

```text
TASK
-> INSPECT_EXISTING_CAPABILITY
-> REUSE_EXISTING_IMPLEMENTATION_WHEN_VALID
-> SELECT_MINIMUM_NECESSARY_CAPABILITY
-> EXECUTE
-> VERIFY
-> RECORD_RESULT_OR_FAILURE
-> FALLBACK_IF_JUSTIFIED
-> STOP_WHEN_FURTHER_COST_EXCEEDS_EXPECTED_INFORMATION_GAIN
```

Candidate controls:

```text
REUSE_FIRST = TRUE
TOOL_RELIABILITY_STATE = REQUIRED
RETRY_POLICY = REQUIRED
FAILURE_BUDGET = CONFIGURABLE
FALLBACK_POLICY = REQUIRED
COST_BUDGET = OPTIONAL_CANDIDATE
LATENCY_BUDGET = OPTIONAL_CANDIDATE
PROVENANCE_RETENTION = REQUIRED
REVIEW_CHANNEL_INTEGRITY = REQUIRED
```

Important distinctions:

```text
TOOL_AVAILABLE != TOOL_RELIABLE
TOOL_FAILURE != NEGATIVE_RESEARCH_EVIDENCE
SEARCH_FAILURE != RESOURCE_DOES_NOT_EXIST
RETRIEVAL_FAILURE != CLAIM_FALSE
MORE_TOOLS != MORE_TRUTH
PARTIAL_STREAM != COMPLETE_EVIDENCE_VIEW
TRUNCATED_OUTPUT != COMPLETE_REPOSITORY_STATE
```

A failed or incomplete evidence channel should fail closed:

```text
INCOMPLETE_REVIEW_INPUT
-> REVIEW_STATUS = INCOMPLETE / HOLD

INCOMPLETE_REVIEW
MUST_NOT
-> CANONICAL_PROMOTION
```

## External correspondence

- Google SRE, *Handling Overload*: uses bounded per-request and per-client retry budgets and explicitly permits failures to bubble up instead of retrying indefinitely.
  - https://sre.google/sre-book/handling-overload/
- Google SRE, *Addressing Cascading Failures*: warns that retries can amplify load, recommends randomized exponential backoff, retry limits, retry budgets and separation of retriable from non-retriable failures.
  - https://sre.google/sre-book/addressing-cascading-failures/
- NIST AI RMF 1.0 / Playbook: requires clear role allocation, documentation of tools used in TEVV, monitoring, error tracking, oversight, escalation and lifecycle risk management.
  - https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
  - https://airc.nist.gov/airmf-resources/playbook/govern/
  - https://airc.nist.gov/airmf-resources/playbook/measure/

These sources provide engineering / governance correspondence only. The exact repository concepts `REUSE_FIRST`, `MINIMUM_NECESSARY_CAPABILITY`, and a configurable research-tool failure budget remain proposed local abstractions.

## Claim boundary

```text
TOOL_EFFICIENCY != AGENCY
RESOURCE_AWARE_EXECUTION != AUTONOMOUS_JUDGMENT
RETRY_CONTROL != METACOGNITION
RELIABLE_ORCHESTRATION != SUBJECTIVITY
```

---

# 3. EXISTING_BRANCH_EXTENSION — PR #203 ↔ PR #202 body-region compatibility

## Live branch finding

The continuing PR #203 branch now contains an immutable content-addressed active baseline and a Phase B.1 materialization/admission map.

The current materialization map explicitly keeps the PR #202 sensorimotor units deferred because the active shared-core body-region contract is not compatible with the archived PR #202 free-form region identifiers.

Current shared-core region IDs include:

```text
HEAD
NECK
TORSO
PELVIS
LEFT_ARM
RIGHT_ARM
LEFT_HAND
RIGHT_HAND
LEFT_LEG
RIGHT_LEG
LEFT_FOOT
RIGHT_FOOT
EXTERNAL_MALE_FORM_SURFACE
```

The current code validates motor targets against this reviewed region set and fails closed on unreviewed regions.

Therefore the current gap is not “add sensorimotor embodiment again.” It is a compatibility / admission problem between two existing surfaces.

## Candidate extension rule

```text
STATIC_BODY_REGION_ID
!= FREE_FORM_SENSORIMOTOR_REGION

REGION_NAME_SIMILARITY
!= REGION_IDENTITY

SENSORIMOTOR_REGION
MUST_BIND_TO
  CANONICAL_BODY_REGION_ID
OR
  EXPLICITLY_REVIEWED_EXTENSION_REGION_ID

UNRESOLVED_REGION_MAPPING
-> HOLD

IMPLICIT_STRING_MATCH
-> FORBIDDEN_CANDIDATE
```

No new parallel embodiment ontology should be created unless later review demonstrates that an explicit compatibility layer cannot represent the required semantics.

## External correspondence

Relevant method literature found through public Web discovery:

- Kawaharazuka & Ikemoto (2026), *Diffusion-Based Body Schema Learning Enabling Abnormal-State Adaptation in Musculoskeletal Robots*, arXiv:2608.01029.
  - https://arxiv.org/abs/2608.01029
- Jiang, Zhang & Wong (2024), *Robot Body Schema Learning from Full-body Extero/Proprioception Sensors*, arXiv:2402.18675.
  - https://arxiv.org/abs/2402.18675
- Chen et al. (2021), *Full-Body Visual Self-Modeling of Robot Morphologies*, arXiv:2111.06389.
  - https://arxiv.org/abs/2111.06389

These works support the relevance of explicit body topology / morphology representations and adaptation under altered physical state. They do not specify this repository’s identifier contract.

## Claim boundary

```text
REGION_MAPPING_PASS != PHYSICAL_BODY_VALIDATION
BODY_SCHEMA_ENGINEERING != BODY_OWNERSHIP
SENSORIMOTOR_BINDING != SENSE_OF_AGENCY
EMBODIMENT != SUBJECTIVITY
```

---

# 4. NEEDS_DEDUP — declared immutable morphology vs deterministic unspecified initialization

## Current repository overlap

The continuing #203 branch already contains:

- frozen dataclasses for active embodiment records;
- content-addressed shared-core and active-baseline hashes;
- strict reviewed body-region validation;
- exact provenance / materialization bindings;
- a static `EmbodimentTemplate`.

Therefore this candidate must not be labeled a new gap merely because the conversational wording is new.

However, the current inspected `EmbodimentTemplate` does not itself establish a general rule equivalent to:

```text
HUMAN_DECLARED_MORPHOLOGY_VALUE
-> IMMUTABLE

UNSPECIFIED_MORPHOLOGY_VALUE
-> DETERMINISTIC_INITIALIZATION

RERUN
-> SAME_INITIALIZED_VALUE

CONFLICTING_NEW_DECLARATION
-> HOLD
```

No generic random or pseudorandom morphology initialization mechanism was identified in the inspected active branch files.

## Candidate future review question

```text
DOES_CURRENT_203_CONTENT_ADDRESSING
ALREADY_PROVIDE_SUFFICIENT_IMMUTABILITY
FOR_ALL_DECLARED_MORPHOLOGY_FIELDS?

IF YES:
  NO_CHANGE

IF NO:
  IDENTIFY_EXACT_SCHEMA_GAP

DO_UNSPECIFIED_FIELDS_REQUIRE_INITIALIZATION_AT_ALL?

IF NO:
  KEEP_UNSPECIFIED / NULL / DEFERRED

IF YES:
  PREFER_DETERMINISTIC_SEEDED_OR_CONTENT_ADDRESSED_INITIALIZATION
  OVER UNCONTROLLED_RUNTIME_RANDOMNESS
```

This prevents unnecessary feature creation.

```text
UNSPECIFIED
!= MUST_RANDOMIZE

DETERMINISTIC_INITIALIZATION
!= SCIENTIFIC_GROUND_TRUTH

RANDOMIZED_INITIALIZATION
!= RUNTIME_MORPHOLOGY_DRIFT
```

Status:

```text
CLASSIFICATION = NEEDS_DEDUP
IMPLEMENTATION_JUSTIFIED = NOT_YET
```

---

# 5. DEFERRED_RESEARCH — non-standard morphology adaptation

Cross-dialogue discussion generated a future research candidate involving morphology that is not limited to ordinary human topology, for example additional limbs or other non-standard appendages, and removal / restoration / relearning perturbations.

Potential future question:

```text
CAN_A_SYNTHETIC_BODY_MODEL
ADAPT_TO
NON_STANDARD_MORPHOLOGY

AND

RETAIN / REVISE / RELEARN
ACTION_CONSEQUENCE_BINDINGS
AFTER
MORPHOLOGY_REMOVAL_OR_REINTRODUCTION?
```

A recent Human-participant VR paper found through public Web discovery is adjacent but not directly equivalent:

- Zhou et al. (2026), *One Body, Two Minds: Alternating VR Perspective During Remote Teleoperation of Supernumerary Limbs*, arXiv:2602.00493.
  - https://arxiv.org/abs/2602.00493

This is retained only as a future literature seed.

Dependency gate:

```text
NON_STANDARD_MORPHOLOGY_ADAPTATION
REQUIRES
  STABLE_CANONICAL_BODY_REGION_MODEL
+ PR_202_SENSORIMOTOR_COMPATIBILITY
+ EXPLICIT_PERTURBATION_PROTOCOL

IMPLEMENT_NOW = NO
```

Claim boundary:

```text
ADAPTATION_PERFORMANCE != BODY_OWNERSHIP
PREDICTION_ERROR != PAIN
RETENTION != SUBJECTIVE_CONTINUITY
NON_STANDARD_MORPHOLOGY != SUBJECTIVITY_EVIDENCE
```

---

# 6. ALREADY_RECORDED — do not duplicate

```text
ISSUE #181
= Human–LLM coupled metareasoning hypothesis
= CLOSED / DEFERRED

ISSUE #189
= security-knowledge re-crosscheck handoff
= OPEN / RECORD_ONLY

PR #197
= Human epistemic-agency retention
= CLOSED / DRAFT / NOT_MERGED

PR #198
= external reuse + Human–AI learning observations
= CLOSED / DRAFT / NOT_MERGED

PR #199
= Human epistemic-agency structural audit
= CLOSED / DRAFT / NOT_MERGED

PR #200
= adversarial epistemic revision loop
= MERGED TO MAIN

PR #201
= epistemic / normative rupture crosswalk
= CLOSED / DRAFT / NOT_MERGED

PR #202
= synthetic sensorimotor embodiment audit
= CLOSED / DRAFT / NOT_MERGED

PR #203
= embodiment archive convergence
= CLOSED PR WITH CONTINUING BRANCH
```

Rule for future reviewers:

```text
BEFORE_NEW_PR
-> CHECK_LIVE_MAIN
-> CHECK_OPEN_AND_CLOSED_PRS
-> CHECK_CONTINUING_BRANCHES
-> CHECK_ISSUES
-> CHECK_EXISTING_SCHEMA_AND_TEST_SURFACES
-> CLASSIFY OVERLAP

IF EXISTING_SURFACE_IS_SUFFICIENT:
  NO_CHANGE

IF PARTIAL_GAP:
  EXTEND_EXISTING_SURFACE

ONLY_IF_DISTINCT_ARCHITECTURAL_GAP:
  CONSIDER_NEW_SURFACE
```

---

# 7. Claim ceilings

```text
GOVERNANCE != SUBJECTIVITY_EVIDENCE
EMBODIMENT != SUBJECTIVITY
TOOL_EFFICIENCY != AGENCY
ETHICAL_CONDUCT != MORAL_AGENCY

ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY
STRUCTURAL_PASS != EMPIRICAL_VALIDATION
TEST_PASS != SCIENTIFIC_TRUTH
CONTENT_ADDRESS_MATCH != SEMANTIC_CORRECTNESS

PARTICIPANT_PROTECTION != CONSCIOUSNESS_EVIDENCE
BODY_MODEL_UPDATE != BODY_OWNERSHIP
RELIABLE_TOOL_ROUTING != ENDOGENOUS_AGENCY

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
```

---

# Tool accountability

## Superpowers

Used as process guidance for the design/documentation stage.

```text
PATH = ARCHITECTURAL_DOCUMENTATION
IMPLEMENTATION = NONE
SUPERPOWERS_PROCESS_GUIDANCE != RESEARCH_EVIDENCE
```

## GitHub

Used for live repository state, exact heads, existing-file inspection and this documentation-only branch write.

```text
GITHUB_LIVE_STATE = REPOSITORY_EVIDENCE
OLD_CONVERSATION_STATE != LIVE_STATE
```

## Public Web

Used for external source discovery and verification. First-party / authoritative sources were preferred for research ethics and AI governance; arXiv records were used for the robotics literature seeds.

## Hugging Face

Human Owner specified the workflow:

```text
PUBLIC_WEB_DISCOVERY
-> EXACT_RESOURCE
-> HUGGING_FACE_READ_IF_AVAILABLE
```

After public Web discovery identified arXiv `2608.01029`, an exact Hugging Face paper lookup was attempted. The current runtime returned:

```text
McpServerError: Tool paper_search not found
```

Therefore:

```text
HUGGING_FACE_READ = FAILED
HUGGING_FACE_EVIDENCE_ADMITTED = NO
FAILURE_RECORDED = YES
```

No scientific conclusion is based on the failed connector call.

## Wolfram

Used for formalization/context assistance only. The returned material did not provide domain-specific evidence needed for these research claims.

```text
WOLFRAM = FORMALIZATION_SUPPORT_ONLY
WOLFRAM_EVIDENCE_ADMITTED = NO
```

## MindMap

A 56-node interactive research map was generated to organize the seven intake categories and tool-accountability branches.

```text
MINDMAP = ORGANIZATION_ONLY
MINDMAP != EVIDENCE
```

---

# Triage result

```text
A. HUMAN_PARTICIPANT_RESEARCH_ETHICS
   + POWER_ASYMMETRY
   STATUS = NEW_GAP_CANDIDATE

B. RESEARCH_EXECUTION_RELIABILITY
   + RESOURCE_AWARE_TOOL_ORCHESTRATION
   + REVIEW_CHANNEL_INTEGRITY
   STATUS = NEW_GAP_CANDIDATE

C. PR_203 ↔ PR_202 BODY_REGION_COMPATIBILITY
   STATUS = EXISTING_BRANCH_EXTENSION

D. DECLARED_IMMUTABLE_MORPHOLOGY
   vs DETERMINISTIC_UNSPECIFIED_INITIALIZATION
   STATUS = NEEDS_DEDUP

E. NON_STANDARD_MORPHOLOGY_ADAPTATION
   STATUS = DEFERRED_RESEARCH

ISSUE_181 / ISSUE_189 / PR_197–PR_203
   STATUS = ALREADY_RECORDED / DO_NOT_DUPLICATE
```

## Next gate

This intake authorizes no implementation.

A future continuation must:

1. re-check live `main`, relevant branch heads and existing PR / issue state;
2. independently review whether A and B remain real gaps after a broader repository search;
3. treat C as an extension problem, not a fresh embodiment system;
4. finish D deduplication before any code proposal;
5. keep E deferred until C is resolved;
6. preserve all claim ceilings;
7. produce a bounded implementation/design recommendation for separate Human Owner review.

```text
THIS_NOTE
= RESEARCH_INTAKE_ONLY

IMPLEMENTATION_AUTHORITY = NONE
MERGE_AUTHORITY = NONE
MAIN_WRITE_AUTHORITY = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SCIENTIFIC_DISPOSITION = HOLD
```
