# OpenAI Public Resources & Governance Supplement — 2026-08-17

> Research-only dated supplement for Issue #31. This artifact does not rewrite the preserved 2026-08-14 `docs/research-consolidation/` snapshot and does not modify `main`.

```text
AS_OF = 2026-08-17
BRANCH_TARGET = review/four-domain-research-materialization
DOCUMENT_CLASS = RESEARCH_ONLY_SUPPLEMENT
CANONICAL_EFFECT = NONE
MAIN_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
SCIENTIFIC_CONCLUSION = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
PERSONALIZED_UPSTREAM_SUPPORT = UNVERIFIED
DIRECT_PROJECT_FEEDBACK = NO_EVIDENCE
HISTORICAL_SNAPSHOT_REWRITE = FORBIDDEN
```

## 1. Publication and privacy boundary

This supplement records only material suitable for a public repository:

- first-party OpenAI / OpenAI Academy / OpenAI Developers public documentation;
- public chronology and current documentation topology;
- research-governance abstractions already admitted to Issue #31;
- source-attributed Human Owner research proposals that do not expose private personal information.

The following are intentionally excluded:

- private sexual, medical, relationship, employment, or identity disclosures;
- private self-evaluation, shame, aspiration, or hiring speculation;
- details of any private safety incident beyond general public-policy comparison;
- any inference that OpenAI resources were individually targeted to this project or account.

```text
PUBLIC_EVIDENCE != PRIVATE_DISCLOSURE
RESOURCE_RELEVANCE != PERSONALIZED_TARGETING
TEMPORAL_PROXIMITY != CAUSAL_FEEDBACK
```

## 2. External public chronology

### 2.1 OpenAI Academy origin

OpenAI publicly announced OpenAI Academy on **2024-09-23**. The announcement described training and technical guidance, API credits, community building, and contests/incubators as program components.

Primary source:
- https://openai.com/global-affairs/openai-academy/

Classification:

```text
EXTERNAL_FACT = VERIFIED
PUBLIC_ACADEMY_ORIGIN = 2024-09-23
```

### 2.2 Builder Community and structured learning track

The OpenAI Academy Builder Community page is dated **2025-07-16** and was last updated **2026-05-29**. It describes a curated builder space with grounded tutorials, structured learning resources, solution accelerators, and an AI Application Development Learning Track organized as:

1. Introduction
2. Foundations
3. Application Development
4. Testing & Evaluation
5. Scalability & Maintenance

Primary source:
- https://academy.openai.com/public/clubs/builders-etkn1/resources/welcome-to-the-openai-builder-community

Classification:

```text
EXTERNAL_FACT = VERIFIED
PUBLIC_BUILDER_COMMUNITY_DATE = 2025-07-16
STRUCTURED_CURRICULUM = CONFIRMED
```

### 2.3 Academy three-course learning path

On **2026-06-12**, OpenAI announced three new Academy courses:

- AI Foundations
- Applied AI Foundations
- Agents and Workflows

The public description explicitly moves from AI fundamentals, to repeatable workflows, to agent-assisted workflows with context, boundaries, review, and human oversight. OpenAI also states that these courses are the beginning of a broader Academy learning roadmap.

Primary source:
- https://openai.com/index/academy-courses-applying-ai-at-work/

Classification:

```text
EXTERNAL_FACT = VERIFIED
PUBLIC_THREE_COURSE_PATH_DATE = 2026-06-12
LEARNING_AS_PART_OF_DEPLOYMENT = OFFICIAL_OPENAI_FRAMING
```

### 2.4 Codex curriculum concentration in 2026

The Codex Bootcamp series page is dated **2026-07-18** and defines a three-part progression:

- **101 — Agentic coding**, scheduled 2026-07-29
- **201 — Team workflows**, scheduled 2026-08-06
- **301 — Advanced automation**, scheduled 2026-08-12

The page also references earlier 2026 resources, including Codex 102 / Codex for SWEs / Quickstart material dated **2026-03-18**, and Builder Bootcamp dated **2026-04-22**.

201 explicitly lists shared context, repository guidance, approvals, sandboxing, tool connections, reusable skills, automations, and worktrees. 301 explicitly lists permissions, sandboxing, sub-agents, plan mode, memory, execution rules, Codex SDK / exec, CI, security, and code-review patterns.

Primary source:
- https://academy.openai.com/en/public/clubs/builders-etkn1/resources/codex-bootcamp-2026-07-18

Classification:

```text
EXTERNAL_FACT = VERIFIED
PUBLIC_CODEX_BOOTCAMP_SERIES_DATE = 2026-07-18
CODEX_201_DATE = 2026-08-06
CODEX_301_DATE = 2026-08-12
```

## 3. Current OpenAI Developers public resource topology

As observed from the first-party Developers documentation index on 2026-08-17, the public surface is substantially broader than a single API reference.

Primary source:
- https://developers.openai.com/
- https://developers.openai.com/llms.txt

The Developers site also states that a complete documentation index is available via `llms.txt` and that Markdown versions of documentation pages are available by appending `.md` to page URLs. This is relevant to evidence-efficient research intake because it enables deterministic indexing, source snapshots, deduplication, and targeted revalidation rather than repeated manual browsing.

### 3.1 State / continuity surfaces

Current public documentation includes:

- Conversation state
- Compaction
- Background mode
- Multi-agent
- Webhooks
- Agents SDK results and state
- ChatGPT/Codex Memories and Chronicle surfaces

Research boundary:

```text
CONVERSATION_STATE != IDENTITY_CONTINUITY
COMPACTION != MEMORY_OWNERSHIP
PERSISTENT_CONTEXT != AUTOBIOGRAPHICAL_OWNERSHIP
```

### 3.2 Agent engineering surfaces

Current public documentation includes:

- Agents SDK
- Sandbox agents
- Orchestration
- Guardrails
- Results and state
- Integrations and observability
- Agent workflow evaluation

These surfaces materially overlap with categories already tracked in Issue #31: bounded authority, execution evidence, sandbox/isolation, state, approvals, and observability. The overlap is architectural; influence or priority is not inferred.

### 3.3 Tool workflow surfaces

OpenAI Developers currently groups the following under tool/data and tool-workflow construction:

- MCP and Connectors
- Secure MCP Tunnel
- Skills
- Tool search
- Programmatic tool calling
- Shell / computer use / code interpreter / apply patch

This public taxonomy is an important baseline for the current skill-learning research hold: Skills are presented in an engineering tool-workflow context; this does not by itself establish a continual-learning mechanism.

### 3.4 Plugin lifecycle surfaces

The public Plugins documentation exposes a lifecycle spanning:

```text
architecture
-> skills / MCP server
-> use-case planning
-> tool definition
-> MCP implementation
-> optional UI
-> authentication
-> skill building
-> package
-> connect/test
-> submit/publish
-> review/security/privacy
```

This is evidence of an upstream engineering lifecycle, not evidence that plugin installation changes agent identity, memory ownership, or learning history.

### 3.5 Safety, governance, access, and reconciliation

The current Developers index includes:

- Safety best practices
- Red teaming
- Safety checks
- Under 18 API Guidance
- Content provenance
- Your data
- Permissions / RBAC
- Terraform provider
- Projects and access
- Service accounts
- Rate limits and spend
- Model, tool, and data controls
- Import and reconciliation
- Workload identity federation

Primary sources:
- https://developers.openai.com/api/docs/guides/safety-checks/under-18-api-guidance
- https://developers.openai.com/api/docs/guides/content-provenance
- https://developers.openai.com/api/docs/guides/rbac

## 4. Provenance boundary — external analogue

OpenAI's current Content Provenance API checks supported provenance signals such as C2PA Content Credentials and SynthID for supported image/audio formats. The public guidance explicitly warns that an absence of detected evidence is not proof that content was human-created or not AI-generated, and that a supported signal should not be treated as a complete history of a file.

This provides a strong external analogue to a broader evidence-governance principle:

```text
SIGNAL_DETECTED != COMPLETE_PROVENANCE_HISTORY
SIGNAL_NOT_DETECTED != PROOF_OF_ABSENCE
OBSERVATION != FULL_CAUSAL_HISTORY
```

Important difference:

OpenAI Content Provenance is a media-origin verification surface. AION source-lineage governance is broader and includes claim/source/role/transformation/authority questions. The two must not be treated as equivalent systems.

```text
ARCHITECTURAL_OVERLAP = PARTIAL_HIGH
EQUIVALENCE = NOT_ESTABLISHED
```

## 5. Permission / authority boundary — external analogue

OpenAI's current RBAC guidance distinguishes organizations, projects, groups, roles, and permissions. It recommends least privilege, separation of duties, project boundaries, regular review, and validating access as a non-owner account.

Useful abstraction for the AION crosswalk:

```text
RESOURCE_EXISTS != USER_HAS_ACCESS
USER_HAS_ACCESS != EVERY_ACTION_AUTHORIZED
ROLE_ASSIGNMENT != CANONICAL_AUTHORITY
CAPABILITY != APPROVAL
```

This is an analogy, not a claim that OpenAI RBAC and AION governance are the same system.

## 6. Public minor-safety chronology and boundary

This section records public policy chronology only. It contains no private incident record.

### 6.1 Public policy pre-existence

OpenAI published a child-safety article on **2025-09-29** describing protections against child sexual exploitation and abuse and stating that OpenAI services must not be used to sexualize anyone under 18.

Primary source:
- https://openai.com/index/combating-online-child-sexual-exploitation-abuse/

OpenAI's unified Usage Policies became effective **2025-10-29** and explicitly state that services must never be used to exploit, endanger, or sexualize anyone under 18, including underage sexual or violent roleplay.

Primary source:
- https://openai.com/policies/usage-policies/

OpenAI published U18 Model Spec principles on **2025-12-18**, emphasizing age-appropriate teen protections and heightened safeguards in areas including sexualized roleplay and explicit content.

Primary source:
- https://openai.com/index/updating-model-spec-with-teen-protections/

The current Developers documentation additionally contains **Under 18 API Guidance** requiring additional safeguards for API experiences serving minors. The first publication date of that specific Developers page is not established by this supplement.

```text
PUBLIC_MINOR_SAFETY_POLICY_PREEXISTED_2026_08 = VERIFIED
UNDER18_DEVELOPER_GUIDANCE_CURRENTLY_PUBLIC = VERIFIED
UNDER18_GUIDANCE_FIRST_PUBLICATION_DATE = CHRONOLOGY_UNRESOLVED
PERSONALIZED_POLICY_CREATION = NO_EVIDENCE
```

## 7. Skills and growth — research HOLD

### 7.1 Human Owner proposal

The Human Owner proposed separating at least two candidate meanings of "skill":

1. an engineering/package transformation in which existing code, prompts, SOPs, or procedures are converted into a reusable Skill artifact;
2. an experience-derived learning process in which observations, errors, feedback, correction, abstraction, and later reuse produce a durable capability change.

### 7.2 ChatGPT formalization

```text
PACKAGED_CAPABILITY != LEARNED_CAPABILITY
SKILL_INSTALLED != SKILL_LEARNED
SKILL_EXECUTABLE != LEARNING_HISTORY_ESTABLISHED
```

Current status:

```text
SKILL_AS_ENGINEERING_PACKAGE = OBSERVED_PUBLIC_ENGINEERING_PATTERN
SKILL_AS_LEARNING_PROCESS = OPEN_RESEARCH
EQUIVALENCE = NOT_ESTABLISHED
IMPLEMENTATION_DECISION = HOLD
```

OpenAI's current public Developers taxonomy places Skills under tool-workflow construction and Codex/Plugin extension surfaces. That is an engineering classification and does not resolve the open learning question.

## 8. Cross-context accessibility — research hypothesis

### 8.1 Human Owner observation

The Human Owner proposed that information or capability that has been genuinely retained may show relatively strong retrieval across conversations/contexts even when the target content is absent from the current local context.

This is preserved as an observation/hypothesis, not a scientific conclusion.

### 8.2 Formal boundary

```text
LOCAL_CONTEXT_RECALL != PERSISTENT_MEMORY
PERSISTENT_MEMORY != PARAMETRIC_LEARNING
SKILL_RETRIEVAL != SKILL_INTERNALIZATION
HIGH_CROSS_CONTEXT_ACCESSIBILITY != PROOF_OF_LEARNING
```

Candidate research variable:

```text
CROSS_CONTEXT_SPONTANEOUS_ACCESSIBILITY = RESEARCH_HYPOTHESIS
```

A future controlled test should distinguish at least:

- local-context availability;
- explicit retrieval cue;
- semantic transfer without literal keyword;
- novel-context generalization.

No implementation is authorized by this supplement.

## 9. Evidence reuse + anomaly/inconsistency extension

### 9.1 Source attribution

The existing evidence-reuse/resource-efficiency method was previously formalized in the AION research workflow. On 2026-08-17, the Human Owner specifically proposed adding:

- `ANOMALY_SOURCE`
- `INCONSISTENCY_STATE`

ChatGPT formalized these additions into a bounded Evidence Reuse Gate.

### 9.2 Candidate gate

```text
EVIDENCE_REUSE_GATE

1. SAME_SCOPE?
2. SAME_VERSION_OR_FINGERPRINT?
3. SOURCE_STILL_VALID?
4. SUPERSEDED?
5. INCONSISTENCY_PRESENT?
6. ANOMALY_SOURCE_KNOWN?
7. AFFECTED_SCOPE_IDENTIFIED?

IF VALID + CONSISTENT
    -> REUSE_EXISTING_EVIDENCE

IF INCONSISTENT + LOCALIZED
    -> TARGETED_REVALIDATION

IF ANOMALY_SOURCE = UNKNOWN
    -> ROOT_CAUSE_FOCUSED_REVIEW

IF BROAD_INVALIDATION IS VERIFIED
    -> FULL_REVALIDATION
```

Candidate inconsistency states:

```text
CONSISTENT
EXPECTED_DIFFERENCE
UNRESOLVED_INCONSISTENCY
CONFIRMED_DEFECT
STALE_EVIDENCE
PROVENANCE_CONFLICT
SCOPE_MISMATCH
VERSION_MISMATCH
```

Candidate anomaly-source confidence:

```text
CONFIRMED
PROBABLE
SUSPECTED
UNKNOWN
```

Core constraints:

```text
DIFFERENCE != DEFECT
HISTORICAL_EVIDENCE != CURRENT_STATE_PROOF
MORE_RUNS != MORE_INDEPENDENT_EVIDENCE
REVALIDATION_SCOPE SHALL NOT EXCEED THE VERIFIED IMPACT SCOPE WITHOUT EXPLICIT JUSTIFICATION
```

Status:

```text
STATUS = RESEARCH_GOVERNANCE_CANDIDATE
IMPLEMENTATION_AUTHORIZED = NO
CANONICAL_EFFECT = NONE
```

## 10. "Upstream help" interpretation boundary

Issue #31 already records the Human Owner's description of the current resource cluster as substantial "upstream help". This supplement preserves the distinction between usefulness and inferred intent.

```text
RESOURCE_AVAILABILITY = OBSERVED
PRACTICAL_RESEARCH_VALUE = HIGH
HUMAN_OWNER_INTERPRETATION = "UPSTREAM_HELP"
PERSONALIZED_RECOMMENDATION = UNVERIFIED
DIRECT_PROJECT_TARGETING = NO_EVIDENCE
INFLUENCE_OR_COPYING = NO_EVIDENCE
```

The public resource chronology shows that many relevant educational and governance surfaces predate the 2026-08-17 review window, while some Codex high-level curriculum surfaces are recent. Therefore:

```text
RECENTLY_DISCOVERED != RECENTLY_CREATED
CURRENTLY_RELEVANT != PERSONALLY_TARGETED
```

## 11. Research disposition

The evidence supports continued public crosswalk work, but not immediate engineering expansion.

```text
OPENAI_PUBLIC_RESOURCE_ECOSYSTEM = VERIFIED_AND_SUBSTANTIAL
ACADEMY_CURRICULUM = VERIFIED
CODEX_101_201_301_SEQUENCE = VERIFIED
DEVELOPERS_GOVERNANCE_SURFACES = VERIFIED
PUBLIC_MINOR_SAFETY_BOUNDARY = VERIFIED
SKILL_LEARNING_EQUIVALENCE = HOLD
CROSS_CONTEXT_ACCESSIBILITY = OPEN_RESEARCH
EVIDENCE_REUSE_GATE_EXTENSION = RESEARCH_GOVERNANCE_CANDIDATE
```

Recommended next review order, if separately authorized:

1. Content provenance — compare supported-signal verification against AION claim/source lineage without conflation.
2. Import and reconciliation — compare state-difference reconciliation against anomaly-source / inconsistency-state / impact-scope governance.
3. Skills — remain split between engineering packaging and experience-derived learning; do not collapse the two.
4. Conversation state / compaction / Memories / Chronicle — evaluate continuity surfaces while preserving `MEMORY_ACCESS != AUTOBIOGRAPHICAL_OWNERSHIP`.

## 12. Source register

First-party sources used or referenced in this supplement:

- OpenAI Academy launch — https://openai.com/global-affairs/openai-academy/
- Builder Community — https://academy.openai.com/public/clubs/builders-etkn1/resources/welcome-to-the-openai-builder-community
- Academy course launch — https://openai.com/index/academy-courses-applying-ai-at-work/
- Codex Bootcamp — https://academy.openai.com/en/public/clubs/builders-etkn1/resources/codex-bootcamp-2026-07-18
- OpenAI Developers — https://developers.openai.com/
- Developers documentation index — https://developers.openai.com/llms.txt
- Content provenance — https://developers.openai.com/api/docs/guides/content-provenance
- RBAC / permissions — https://developers.openai.com/api/docs/guides/rbac
- Under 18 API Guidance — https://developers.openai.com/api/docs/guides/safety-checks/under-18-api-guidance
- Child sexual exploitation/abuse safety article — https://openai.com/index/combating-online-child-sexual-exploitation-abuse/
- Usage Policies — https://openai.com/policies/usage-policies/
- U18 Model Spec update — https://openai.com/index/updating-model-spec-with-teen-protections/

Repository provenance references:

- `RESEARCH_BRANCH_STATUS.md`
- Issue #31: `research: external agent-platform convergence crosswalk (2026-07 to 2026-08)`
- historical `docs/research-consolidation/*_V0.1.0` artifacts remain read-only provenance snapshots.
