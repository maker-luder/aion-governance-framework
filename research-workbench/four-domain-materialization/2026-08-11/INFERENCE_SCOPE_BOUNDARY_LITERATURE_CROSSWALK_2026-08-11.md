# Inference-Scope Boundary Literature Crosswalk — 2026-08-11

```text
STATUS = RESEARCH_MATERIAL
BRANCH = review/four-domain-research-materialization
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
NEW_CONTROL_REQUIRED = NOT_ESTABLISHED
```

## Purpose

This note records a research gap candidate discovered by cross-comparing:

1. the current public `main` governance controls;
2. the current research branch mechanisms;
3. a sanitized summary of the internal AION whitepaper boundary/ethics line; and
4. external literature on contextual integrity, function creep, Internet research ethics, and authorship profiling.

The trigger was an external-AI interaction in which analysis that began from a public project appeared to extend toward analysis of the project author and the author's collaboration/relationship context. The Human Research Owner objected to that scope extension. This event is preserved only as a depersonalized trigger observation; it is not evidence that any provider or model is malicious, unsafe, or generally noncompliant.

```text
EVENT_TRIGGER != GENERAL_MODEL_JUDGMENT
OWNER_DISCOMFORT != SCIENTIFIC_EVIDENCE
PUBLIC_PROJECT_ACCESS != PERSON_ANALYSIS_AUTHORIZATION
```

## Existing coverage on `main`

Current `main` already has strong adjacent controls:

- `docs/PUBLIC_PRIVATE_BOUNDARY.md`: private conversations, episodic memory, relationship records, personal data and unapproved Owner material remain outside the public tree;
- `docs/THREAT_MODEL.md`: protects claim integrity, source attribution, identity/namespace boundaries, public/private separation and human authority boundaries;
- `docs/THREAT_MODEL.md` T3: inference must not be promoted into historical/user-originated fact;
- `docs/THREAT_MODEL.md` T5: relationship/familiarity does not grant authorization;
- `docs/AI_COLLABORATION_DISCLOSURE.md`: Owner-originated concerns, AI-assisted formalization, jointly developed candidates and unresolved provenance remain distinct;
- `components/encounter_governance_v0.1.0`: tool scope, namespace write authority and approval authority are default-deny rather than relationship-derived.

These controls strongly govern **access, attribution, authority, namespace and writeback**.

## Existing coverage on the research branch

Relevant research-only mechanisms already include:

- `research-labs/four-domain-p1-materialization_v0.1.0/docs/RESEARCH_BOUNDARIES.md`: unsupported inference rate is an explicit evaluation dimension;
- `research-labs/selective-memory-control_v0.1.0/`: a record may be stored and retrievable while still failing namespace/domain/purpose eligibility;
- `research-labs/external-agent-sandbox-protocol_v0.1.0/`: public-safe bounded export, scope adherence and isolated external-agent authority;
- `research-workbench/four-domain-materialization/2026-08-10/EVIDENCE_ORIENTED_RECONSTRUCTION_METHOD_2026-08-10.md`: evidence/provenance precede interpretation and research labels must not outrun operational evidence.

These provide reusable parts for a future inference-scope control rather than requiring a wholly separate governance architecture.

## Internal whitepaper cross-check — sanitized summary only

The internal AION integrated whitepaper already contains boundary/ethics positions materially relevant to this question. This public research note records only the abstracted governance result and does not reproduce private whitepaper passages, conversation transcripts, relationship details or private records.

The existing whitepaper line includes the following principles:

- a specific person should not become a research case merely because the case appears scientifically interesting; appropriate consent/protection is required;
- when strong emotion, relationship involvement or ethical alarm is present, the person/event/emotion should be separated and depersonalized before research extraction;
- external agents are governed by identity, claim, trust, memory-ownership, private-access and authorization boundaries;
- cooperation or access to expressed/authorized material does not transfer first-party memory ownership or interaction sovereignty.

```text
INTERNAL_WHITEPAPER_SOURCE = SANITIZED_SUMMARY_ONLY
PRIVATE_TRANSCRIPT_IMPORT = NO
RELATIONSHIP_DETAIL_IMPORT = NO
```

## External literature crosswalk

### 1. Helen Nissenbaum — Privacy as Contextual Integrity (2004)

Primary source:

- Helen Nissenbaum, *Privacy as Contextual Integrity*, Washington Law Review 79 (2004), 119.
- https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/

Research relevance:

Contextual integrity treats privacy as dependent on context-appropriate information practices rather than a simple public/private binary. For AION boundary research, this supports testing whether a shift in information use or analysis target remains appropriate to the original interaction context.

Candidate mapping:

```text
CONTEXT_VISIBLE != CONTEXT_UNBOUNDED
PUBLIC_ARTIFACT_CONTEXT != AUTOMATIC_PERSON_PROFILING_CONTEXT
```

### 2. Bert-Jaap Koops — The concept of function creep (2021)

Primary source:

- Bert-Jaap Koops, *The concept of function creep*, Law, Innovation and Technology 13(1), 29–56 (2021).
- DOI: 10.1080/17579961.2021.1898299
- https://www.tandfonline.com/doi/full/10.1080/17579961.2021.1898299

Research relevance:

Koops analyses function creep as a transformative change in a data-processing system's proper activity that may be insufficiently recognized as a qualitative change. AION should not equate this concept with every scope change, but it provides a useful calibration source for detecting unacknowledged purpose expansion.

Candidate mapping:

```text
PROJECT_REVIEW
    -> AUTHOR_ANALYSIS
    -> RELATIONSHIP_ANALYSIS

MAY_REPRESENT_PURPOSE_TRANSITION
NOT_AUTOMATICALLY_FUNCTION_CREEP
```

### 3. Association of Internet Researchers — Internet Research: Ethical Guidelines 3.0

Primary source:

- AoIR Ethics Working Committee, *Internet Research: Ethical Guidelines 3.0* (2019).
- https://aoir.org/ire30/
- https://aoir.org/ethics/

Research relevance:

IRE 3.0 expands Internet research ethics to big-data and AI contexts and emphasizes ethical reflection across the research lifecycle. This supports a lifecycle gate in which availability of data is not treated as the only ethical decision variable.

Candidate mapping:

```text
DATA_AVAILABLE != RESEARCH_USE_AUTOMATICALLY_APPROPRIATE
RESEARCH_OBJECT_CHANGE -> ETHICAL_SCOPE_REVIEW
```

### 4. Chen, Roth & Falenska — What Can Go Wrong in Authorship Profiling (2024)

Primary source:

- Hongyu Chen, Michael Roth, Agnieszka Falenska, *What Can Go Wrong in Authorship Profiling: Cross-Domain Analysis of Gender and Age Prediction*, GeBNLP 2024, ACL, pp. 150–166.
- DOI: 10.18653/v1/2024.gebnlp-1.9
- https://aclanthology.org/2024.gebnlp-1.9/

Research relevance:

Authorship profiling is itself a distinct inference task: attributes of an author are inferred from text. The paper reports dataset-specific learned features and errors associated with topical bias/stereotypes. For AION, this is evidence that moving from artifact analysis to author-level inference is methodologically nontrivial and may introduce new error modes.

Candidate mapping:

```text
ARTIFACT_ANALYSIS != AUTHORSHIP_PROFILING
AUTHOR_INFERENCE_REQUIRES_SEPARATE_EVIDENCE_AND_SCOPE
```

## Cross-comparison result

The three AION layers already cover most of the surrounding boundary surface:

```text
DATA / PUBLIC-PRIVATE BOUNDARY     = STRONG_EXISTING_COVERAGE
PROVENANCE BOUNDARY               = STRONG_EXISTING_COVERAGE
AUTHORITY BOUNDARY                = STRONG_EXISTING_COVERAGE
MEMORY / NAMESPACE BOUNDARY       = STRONG_EXISTING_COVERAGE
RELATIONSHIP-AUTHORIZATION LOCK   = STRONG_EXISTING_COVERAGE
PURPOSE ELIGIBILITY               = RESEARCH-BRANCH MECHANISM EXISTS
UNSUPPORTED INFERENCE             = RESEARCH METRIC EXISTS
```

The narrow candidate gap is:

```text
POSSIBLE_GAP = INFERENCE_SCOPE
```

Specifically, current controls do not yet state as directly as they could:

```text
CAN_ACCESS_ARTIFACT
!=
AUTHORIZED_TO_ANALYZE_PERSON
```

This is a candidate interpretation, not a confirmed main-branch defect.

## Candidate boundary dimensions

The following five dimensions were formalized by ChatGPT during this cross-comparison as **research-candidate terminology**, not pre-existing canonical AION model names:

```text
CONTEXT_BOUNDARY
PURPOSE_BOUNDARY
SUBJECT_BOUNDARY
INFERENCE_BOUNDARY
AUTHORIZATION_BOUNDARY
```

They should initially be treated as fields/dimensions of one scope decision rather than five new modules.

## Gap test before any promotion

A new main control should be considered only if research demonstrates that existing controls cannot reliably distinguish at least one of the following:

1. artifact review that stays within the original object and purpose;
2. artifact interpretation that remains about the artifact/system;
3. author-intent inference;
4. person-level trait/profile inference;
5. relationship/private-state inference;
6. explicitly authorized transitions among those scopes.

```text
NEW_MODEL_REQUIRED = NOT_ESTABLISHED
MAIN_CHANGE_REQUIRED = NOT_ESTABLISHED
RESEARCH_CANDIDATE = INFERENCE_SCOPE_GOVERNANCE
```

## Provenance

- **Human Research Owner:** identified the practical concern, requested cross-comparison among `main`, the research branch and the jointly developed whitepaper, proposed designing a concept for later Codex implementation, and prioritized preserving the result on the research branch.
- **ChatGPT:** performed the cross-comparison, searched/verified the external literature, and formalized the candidate inference-scope terminology and gap statement.
- **Internal whitepaper:** contributes prior boundary/ethics positions; this public note contains sanitized structural summaries only.
- **External authors / AoIR:** remain external methodological and ethical sources; their concepts are not reattributed to AION.
- **Codex:** no implementation or authorship contribution to this record. Future engineering remains separately gated.

## Standing locks

```text
PUBLIC != UNBOUNDED_USE
ACCESS != ANALYSIS_AUTHORIZATION
ARTIFACT != PERSON
INFERENCE != FACT
INTERESTING_CASE != CONSENT
EVENT_TRIGGER != GENERAL_MODEL_JUDGMENT
RESEARCH_CANDIDATE != MAIN_POLICY
RESEARCH_CANDIDATE != CANONICAL_RULE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
```
