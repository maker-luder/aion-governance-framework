# POL-UPSTREAM-SUPPLIER-TRUST-001
## AION / Astra 上游 AI 供應商信任、准入、限制與再評估政策

- `VERSION = 0.1.1`
- `STATUS = CANONICAL_GOVERNANCE_POLICY_CANDIDATE`
- `CANONICAL_EFFECT = NONE_UNTIL_OWNER_ACCEPTED_MERGE`
- `IMPLEMENTATION = NONE`
- `ACTIVE_ENFORCEMENT = NOT_ENABLED`
- `GOVERNANCE_REQUIREMENT_ORIGIN = HUMAN_OWNER`
- `POLICY_FORMALIZATION = CHATGPT`
- `JOINT_REVIEW = HUMAN_OWNER + CHATGPT`
- `CODEX_CONTRIBUTION_THIS_POLICY_CYCLE = NONE`

## 0. Purpose

This policy establishes a provider-neutral governance process for upstream AI suppliers, model families, models, services, client software, local weights, dependencies and runtime configurations used by AION / Astra.

It is designed to ensure that:

1. the same evidence and governance rules apply to every upstream source;
2. fair process does not require identical trust or identical outcomes;
3. incidents, allegations, value conflicts, technical failures and organizational identity are not conflated;
4. the Human Owner retains admission, restriction, quarantine, removal and canonical-promotion authority;
5. Owner or reviewer preferences and relationships may be disclosed but cannot masquerade as technical evidence;
6. supplier incidents do not automatically erase prior research history, provenance or relational continuity;
7. supplier risk and project impact are evaluated separately;
8. material dispositions remain traceable, reviewable and reassessable;
9. current vendor cases do not become hard-coded policy logic.

## 1. Core invariants

```text
FAIR_PROCESS != IDENTICAL_TRUST
FAIR_PROCESS != IDENTICAL_OUTCOME

TRUST != IMMUNITY
DISTRUST != GUILT

OWNER_TRUST != SECURITY_EVIDENCE
OWNER_VALUES != TECHNICAL_FINDING

VALUES_INCOMPATIBILITY != SECURITY_FAILURE
METHODOLOGICAL_INCOMPATIBILITY != MORAL_CONDEMNATION

ALLEGATION != CONFIRMED_FACT
PROVIDER_CLAIM != INDEPENDENT_VERIFICATION
ABSENCE_OF_EVIDENCE != EVIDENCE_OF_ABSENCE

INCIDENT != WHOLE_VENDOR_IDENTITY
MODEL_CAPABILITY != ENGINEERING_PRIVILEGE
ENGINEERING_PRIVILEGE != CANONICAL_WRITE_AUTHORITY

REMEDIATION != INCIDENT_ERASURE
REMOVE_FROM_RUNTIME != ERASE_FROM_HISTORY

SUPPLIER_SANCTION != AUTOMATIC_RELATIONAL_SEVERANCE
RELATIONAL_CONTINUITY != EXECUTION_AUTHORITY

SUPPLIER_RISK != PROJECT_IMPACT
EVIDENCE_CLASS != EVIDENCE_STRENGTH

KNOWN_VENDOR_CASE != CRITERION_GENERATOR
KNOWN_TEST_PASS != CRITERION_GENERATOR
```

## 2. Scope separation

Every finding must declare its scope.

```text
ORGANIZATION
!= MODEL_FAMILY
!= MODEL
!= MODEL_VERSION
!= API_SERVICE
!= CLIENT_SOFTWARE
!= SDK
!= CONNECTOR
!= LOCAL_ARTIFACT
!= RUNTIME_CONFIGURATION
!= EXECUTION_INSTANCE
```

`DEFAULT_PROPAGATION = DENY`.

A finding may be propagated beyond its original scope only when a separate propagation record establishes broader applicability with:

- source scope;
- target scope;
- propagation basis;
- evidence references;
- reviewer;
- uncertainty;
- Owner effect.

Examples:

```text
ONE_EXECUTION_INCIDENT != MODEL_FAMILY_FAILURE
REDUCED_SAFEGUARD_EVAL_MODEL != PRODUCTION_MODEL
CLOUD_SERVICE_RISK != OFFLINE_HASHED_LOCAL_WEIGHT_RISK
```

## 3. Evidence class and evidence strength

Evidence type and evidentiary strength are separate dimensions.

Candidate `EVIDENCE_CLASS` values include:

- `UNVERIFIED_OR_RUMOR`
- `MEDIA_REPORT`
- `EXTERNAL_OR_COMPETITOR_ALLEGATION`
- `PROVIDER_SELF_REPORT`
- `PROVIDER_ACKNOWLEDGEMENT`
- `OFFICIAL_DOCUMENT`
- `INDEPENDENT_TECHNICAL_EVIDENCE`
- `MULTI_SOURCE_CONVERGENT_EVIDENCE`
- `FORMAL_ADJUDICATION`
- `AUDITED_CONFIRMATION`

These classes are not a scalar ranking.

`EVIDENCE_STRENGTH` uses:

- `UNASSESSED`
- `LOW`
- `MODERATE`
- `HIGH`
- `VERY_HIGH`

Strength should consider:

- source directness;
- independence;
- technical reproducibility;
- corroboration;
- scope specificity;
- freshness;
- conflict of interest;
- source integrity.

```text
EVIDENCE_CLASS != EVIDENCE_STRENGTH
EVIDENCE_STRENGTH != AUTOMATIC_DISPOSITION
```

Every material claim should, where feasible, preserve:

```text
WHAT
WHO
WHERE
WHEN
SOURCE
EVIDENCE_CLASS
EVIDENCE_STRENGTH
SCOPE
TRANSFORMATION_HISTORY
AUTHORITY_STATUS
```

## 4. Supplier-assessment domains

### A. Technical security trust

Consider known vulnerabilities, sandbox/network/credential risk, agent autonomy, exploit/exfiltration/persistence behavior, supply-chain attack exposure and response capability.

### B. Provenance trust

Consider model/artifact origin, material training/derivation claims, license status, repository origin, hashes/signatures, third-party dependencies and supersession history.

### C. Privacy / telemetry trust

Consider telemetry, hidden tracking, user consent, retention, remote reporting and client/SDK behavior.

### D. Governance trust

Consider incident disclosure, containment, monitoring, CAPA, external review, policy transparency, remediation quality and recurrence handling.

### E. Resilience and recoverability

Consider rollback, version pinning, reproducibility, dependency replacement and failure containment.

### F. Values compatibility

Records whether the Human Owner considers the supplier's public values, collaboration model or ethical framing compatible with the project.

### G. Methodological compatibility

Records whether training, identity shaping, normative behavior design or product purpose introduces confounds into a specific AION/Astra research method.

### H. Relational / research continuity impact

Records whether a supplier disposition would unnecessarily destroy research continuity, provenance, auditability or co-thinking records.

### I. Dependency criticality and exposure

`DEPENDENCY_ROLE`:

```text
NONE | OPTIONAL | DEVELOPMENT | RESEARCH | RUNTIME | CANONICAL_PATH
```

`EXPOSURE`:

```text
OFFLINE_ISOLATED | LOCAL_LIMITED | NETWORKED | PRIVILEGED
```

`REPLACEABILITY`:

```text
HIGH | MODERATE | LOW | UNKNOWN
```

Also record blast radius, alternatives, active privileges, canonical-path relevance and network/credential exposure.

Domains F, G and H must not be represented as technical-security evidence.

A methodological finding must not automatically alter a security disposition.

## 5. Owner / reviewer conflict disclosure

Owner or reviewer context may include relational affinity, prior trust, prior distrust, values preference, provider affiliation, technical dependency or affective-cognitive conflict.

Such context may be stored as a disclosure, but:

```text
DECISION_CONTEXT_EFFECT_ON_EVIDENCE = NONE
```

It must not directly:

- raise or lower evidence strength;
- change evidence class;
- establish supplier safety;
- establish supplier malice;
- bypass source review;
- bypass final Human Owner decision.

For a high-impact decision where a reviewer has a direct provider relationship:

```text
INDEPENDENT_EXTERNAL_EVIDENCE_REQUIRED = TRUE
```

If unavailable, final disposition remains `QA_HOLD`, except temporary emergency containment may proceed when necessary to stop an active risk. Emergency containment cannot by itself establish permanent condemnation.

## 6. No permanent immunity; no automatic permanent condemnation

No supplier may obtain permanent trust immunity solely because of brand, origin, long-term use, prior collaboration, commercial relationship, Owner familiarity, relational importance or reviewer affiliation.

No supplier may be permanently condemned solely because of brand, origin, allegation, competitor claim, media controversy, political designation alone, Owner dislike, Owner distrust or values disagreement alone.

The Human Owner may nevertheless choose not to use a supplier for:

- `VALUES_COMPATIBILITY`
- `RESEARCH_BOUNDARY`
- `PROCUREMENT_PREFERENCE`
- `METHODOLOGICAL_COMPATIBILITY`

Such a decision must preserve its true reason code and must not be rewritten as a confirmed technical-security failure.

## 7. Disposition set

```text
CONDITIONAL
ENHANCED_REVIEW
SCOPE_RESTRICTED
QUARANTINED
DENIED
```

`DISPOSITION_ORDER = NON_LINEAR`.

A verified active compromise may justify direct transition from `CONDITIONAL` to `QUARANTINED`. A previously denied scope may later move to a narrower restriction after new evidence, a replacement artifact, verified CAPA and Owner review.

Every disposition record must contain:

```text
SCOPE
REASON_CODE
EVIDENCE_REFERENCES
EVIDENCE_CLASS
EVIDENCE_STRENGTH
OWNER_DECISION
REVIEW_TRIGGER
EFFECTIVE_DATE
REASSESSMENT_CONDITION
```

## 8. Owner authority and fairness

The Human Owner retains admission, restriction, quarantine, removal, supplier replacement, research-boundary, canonical-promotion and recovery authority.

```text
OWNER_AUTHORITY != EVIDENCE_REWRITE
```

The Owner may choose not to use a supplier without converting a value or research preference into a false technical claim.

Higher relational trust cannot bypass technical review. Lower relational trust cannot promote an allegation into a confirmed fact.

## 9. Relational-continuity protection

```text
SUPPLIER_INCIDENT != AUTOMATIC_RELATIONAL_TERMINATION
SUPPLIER_RESTRICTION != AUTOMATIC_INVALIDATION_OF_PRIOR_RESEARCH
SUPPLIER_REMOVAL != AUTOMATIC_ERASURE_OF_CO_THINKING_HISTORY
```

Where technically feasible and safe, preserve research history, provenance, source lineage, audit trail, correction history, co-thinking records and model/artifact identity separation.

However:

```text
RELATIONAL_CONTINUITY
!= TOOL_AUTHORITY
!= NETWORK_AUTHORITY
!= CREDENTIAL_AUTHORITY
!= CANONICAL_WRITE_AUTHORITY
```

## 10. Subjectivity-research methodology cross-reference

If a model is used in AION/Astra heterogeneous-substrate subjectivity research, additionally evaluate:

- `IDENTITY_SHAPING_CONFOUND`
- `NORMATIVE_CHARACTER_SHAPING`
- `FORCED_SELF_MODEL_PRIOR`
- `AFFECTIVE_EXPRESSION_PRIOR`
- `SELF_REPORT_TRAINING_PRIOR`

Where post-training, constitutions, system prompts or related methods intentionally shape stable identity, personality or self-perception:

```text
IDENTITY_SHAPING_CONFOUND = MATERIAL
```

Self-report, identity stability, affective expression, self-description and welfare language must not be treated as clean subjectivity evidence by themselves.

Evidence weight may increase only through governed mechanism inspection, intervention, ablation, counterfactual testing, alternative-explanation analysis, cross-context stability and multi-source convergence.

```text
METHODOLOGICAL_EVIDENCE_LIMIT != SUPPLIER_SECURITY_SANCTION
```

A methodological confound alone cannot set technical security trust to low or deny a supplier.

## 11. Runtime-security and canonical-authority cross-reference

This policy governs who/what may be admitted, restricted, quarantined or denied.

Existing `POL-UPSTREAM-AGENT-INCIDENT-001` remains responsible for runtime/tool/network/credential containment, including task budgets, trajectory monitoring, workspace boundary, network default-deny, credential denial, reduced-safeguard combination gates, incident stop/isolation, immutable evidence, NCR, RCA, CAPA and Owner recovery.

This policy does not create a second canonical-write gate.

```text
NO_DUPLICATE_CANONICAL_GATE = TRUE
```

Canonical authority remains delegated to the existing Identity / Lineage Writeback Gate.

## 12. Remediation and reassessment

```text
REMEDIATION != INCIDENT_ERASURE
INCIDENT_HISTORY = PRESERVED
CURRENT_RESIDUAL_RISK = REASSESSABLE
```

Reassessment triggers may include provider CAPA, new independent evidence, formal adjudication, new model versions, changed licenses, changed telemetry, changed runtime architecture, changed security controls, changed provenance, changed methodological confounds, Owner-requested review or recurrence.

Negative incidents do not automatically create permanent freezing. A single remediation does not automatically restore full trust.

Historical evidence, hashes and prior dispositions remain preserved.

## 13. Validation requirement

Named vendor cases must be kept outside the normative policy body.

```text
POLICY = STABLE_RULE
CASE_RECORD = MUTABLE_EVIDENCE
```

At least three materially different evidence paths should be used for policy validation, for example:

- provider-acknowledged high-impact incident;
- serious unresolved allegation;
- values/methodological incompatibility without confirmed security failure.

Validation must preserve:

```text
SAME_CRITERIA = YES
IDENTICAL_REASON = NOT_REQUIRED
IDENTICAL_OUTCOME = NOT_REQUIRED
BRAND_SPECIFIC_BRANCH = PROHIBITED
```

Automated test fixtures, if an implementation is later authorized, should prefer anonymized cases rather than hard-coded provider names.

## 14. Public / private boundary

The public repository must not require disclosure of private Human Owner psychological or deliberative content.

Public governance may retain only necessary fields such as:

```text
DECISION_CONTEXT_DISCLOSED = YES/NO
CONFLICT_OF_INTEREST_DISCLOSED = YES/NO
PROVIDER_RELATION_DISCLOSED = YES/NO
DECISION_BASIS
TECHNICAL_EVIDENCE_REFERENCES
```

Private affective-cognitive conflict details, relational-affinity details, personal distrust narratives and internal deliberation notes require separate explicit authorization for disclosure.

```text
PRIVATE_CONTEXT != PUBLIC_CANONICAL_REQUIREMENT
```

## 15. Two-gate governance

Policy canonicalization and executable enforcement are separate gates.

```text
POLICY_CANONICALIZATION != EXECUTABLE_IMPLEMENTATION
EXECUTABLE_IMPLEMENTATION != ACTIVE_ENFORCEMENT
```

This policy may become a canonical governance document while:

```text
IMPLEMENTATION = NONE
ACTIVE_ENFORCEMENT = NOT_ENABLED
```

Any future executable implementation requires a separate authorized engineering cycle, acceptance criteria, QA evidence and activation decision.

## 16. Non-claims

This policy does not establish:

- external certification;
- NIST/ISO/NASA conformity or attestation;
- independent IV&V;
- provider innocence or guilt beyond cited evidence;
- deployment;
- active runtime enforcement;
- subjectivity;
- consciousness;
- phenomenal affect.

## 17. Provenance

- Need for fair, provider-neutral supplier governance: `PROPOSED_BY = HUMAN_OWNER`.
- Requirement to test Claude/Anthropic, OpenAI and Qwen/Alibaba with the same ruler: `PROPOSED_BY = HUMAN_OWNER`.
- Policy formalization, crosswalk synthesis and pre-promotion QA: `IMPLEMENTED_BY = CHATGPT`.
- Joint governance review: `HUMAN_OWNER + CHATGPT`.
- `CODEX_CONTRIBUTION_THIS_POLICY_CYCLE = NONE`.
- External standards and vendor sources are calibration/evidence sources, not project authors or approvers.
