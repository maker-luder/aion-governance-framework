# Executable Four-Domain standards crosswalk

Status: `BOUNDED_IMPLEMENTATION / STRUCTURALLY_TESTED / SCIENTIFIC_HOLD`

This extension materializes the candidate implementation classes specified by
merged PR #102 without turning an external standard into subjectivity evidence.

```text
IMPLEMENTATION_BASE_COMMIT_SHA = d95bc2625e71f1c85a725aaba78cb0feccfc0668
IMPLEMENTATION_BASE_TREE_SHA = 77470062979df1db2f17c3a2a396891d1e910f98
ORIGINAL_SPECIFICATION_REVIEW = PR #102 @ 3ce4f759caf662a53f0d1f3a54709bc482d7df5e
CURRENT_SPECIFICATION_STATUS = MERGED
HISTORICAL_SYNCED_MAIN_COMMIT_SHA = 6e0ae579da9d09b3ba4041d52a7e9833ceb10ca1
PR102_USED_AS_IMPLEMENTATION_BASE = FALSE
```

The existing Four-Domain and research-quality-chain structures from merged PR
#100 remain canonical antecedents. This is a minimal extension that adds:

1. an external-standard source registry whose declared SHA-256 is recomputed
   from the supplied source payload before admission;
2. explicit contribution roles: vocabulary, process control, evidence quality,
   technical method, and claim limit;
3. complete bindings across human construct, ontology-neutral machine question,
   engineering operation, and governance interpretation, with every declared
   source required to have at least one Four-Domain binding;
4. a required subjectivity-confound register that rejects human-to-machine
   equivalence and human constructs as subjectivity proxies, and requires unique
   competing explanations;
5. distinct TEST, EVALUATION, VERIFICATION, and VALIDATION definitions;
6. an audit fingerprint that binds all claim-boundary fields, including
   consciousness, phenomenal experience, moral status, scientific disposition,
   canonical effect, and deployment state.

The registry fails closed on duplicate sources or bindings, unknown or unbound
source references, source-content hash mismatch, incomplete TEVV vocabulary,
missing Four-Domain fields, missing process/evidence roles, or absent/invalid
confound records.

```text
DECLARED_HASH_FORMAT != CONTENT_BINDING
SOURCE_CONTENT_HASH = RECOMPUTED_BEFORE_ADMISSION
AUDIT_FINGERPRINT = CLAIM_BOUNDARY_COMPLETE
MODEL_INVOKED = FALSE
EVIDENCE_ADMISSIBILITY = PROCESS_CONTROL_ONLY
STANDARD_CONFORMANCE != SCIENTIFIC_VALIDATION
PROCESS_CONTROL != SUBJECTIVITY_EVIDENCE
HUMAN_CONSTRUCT != MACHINE_ONTOLOGY
TEVV_TERMS_ARE_NOT_SYNONYMS
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation ships only synthetic fixture tests. Populating the registry
with external standards requires exact authoritative locators, version/date,
access date, source payload, immutable content hash, and independent source
review. The registry verifies binding integrity; it does not independently
establish the authority, truth, or completeness of an external standard.

## 2026-09-19 governance / assurance operationalization update

This update records a repository-level interpretation that emerged from a live
cross-read of the current standards surfaces and the already-merged quality,
TEVV, security, provenance and claim-admission controls.

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_OBJECT

AI_GOVERNANCE_STANDARDS
= METHOD_REFERENCE
+ RISK_AND_IMPACT_DISCIPLINE
+ TEVV_DISCIPLINE
+ QUALITY_ASSURANCE
+ SECURITY_ASSURANCE
+ CLAIM_AND_AUTHORITY_CONTROL

AI_GOVERNANCE_STANDARDS
!= NEW_RESEARCH_AXIS
!= SUBJECTIVITY_EVIDENCE
!= CONSCIOUSNESS_EVIDENCE
!= CERTIFICATION_CLAIM
```

The practical value is therefore not to reframe the repository as an
"AI-governance project". The value is to use external governance and assurance
methods as a **supporting control layer** around high-risk research claims.

The repository already contains most of the needed implementation surfaces:

- this executable standards registry and Four-Domain binding;
- the bounded AI risk / impact control;
- the AI TEVV profile and content-addressed TEVV receipt;
- the AI adversarial-security profile and content-addressed security receipt;
- `FullQualitySystemEngine` and its end-to-end QMS bindings;
- provenance and claim-admission controls;
- exact-head CI / transition-authority controls.

Therefore:

```text
NEW_PARALLEL_GOVERNANCE_ENGINE = NOT_JUSTIFIED
ORCHESTRATE_EXISTING_CONTROLS = PREFERRED
DUPLICATE_CONTROL_SURFACE = AVOID
```

### External standards / framework status recheck

The following status snapshot was rechecked against first-party ISO and NIST
sources on 2026-09-19. It is intentionally version- and date-bound.

| Source | Status observed 2026-09-19 | Repository use | Boundary |
|---|---|---|---|
| ISO/IEC 42001:2023 | published international standard | AIMS / lifecycle management-system reference | no claim of ISO/IEC 42001 conformity or certification |
| ISO/IEC 23894:2023 | published international standard | AI risk-management method reference | guidance use does not establish complete risk control |
| ISO/IEC 42005:2025 | published international standard | AI system impact-assessment reference | impact assessment does not adjudicate subjectivity |
| ISO/IEC 42006:2025 | published international standard | audit/certification-body context only | the repository is not a certification body and does not claim certification |
| ISO/IEC TS 42119-2:2025 | published technical specification | risk-based AI testing-method reference | testing guidance does not establish validation or scientific truth |
| ISO/IEC DTS 42119-3.2 | under development / approval phase | future verification/validation-method watch item | draft status must not be represented as a final standard |
| ISO/IEC 25059:2023 | published; ISO page notes replacement work is advanced | AI quality-model reference | quality characteristics are not consciousness indicators |
| ISO/IEC AWI 42003 | under development | implementation-guidance watch item for ISO/IEC 42001 | not yet a published standard |
| NIST AI RMF 1.0 | published voluntary framework; revision in progress | `GOVERN / MAP / MEASURE / MANAGE` lifecycle crosswalk | voluntary framework, not certification |
| NIST AI 600-1 | published GenAI profile | GenAI risk / human-AI configuration / provenance / red-team method reference | profile use does not establish repository conformance |
| NIST AI 200-2 TEVV-Athlon | initial public draft; comment period closes 2026-10-06 | TEVV terminology and process-design watch item | draft, not a final standard |

First-party status references:

- https://www.iso.org/standard/42001
- https://www.iso.org/standard/77304.html
- https://www.iso.org/standard/42005
- https://www.iso.org/standard/42006
- https://www.iso.org/standard/84127.html
- https://www.iso.org/standard/85072.html
- https://www.iso.org/standard/80655.html
- https://www.iso.org/standard/91021.html
- https://www.nist.gov/itl/ai-risk-management-framework
- https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- https://www.nist.gov/artificial-intelligence/ai-research/tevv-athlon-framework-evaluating-ai-systems

### Operational use inside this repository

A future research or engineering change should not mechanically run every
standard-derived control. It should first determine applicability and then route
through the existing controls.

```text
0. LIVE_STATE_AND_SOURCE_FRESHNESS
   -> re-read current main / target head
   -> re-check authoritative source status
   -> do not trust a stale version/status label

1. SOURCE_INTAKE
   -> exact identifier
   -> issuing body
   -> version/date
   -> authoritative locator
   -> access date
   -> lawful reviewed payload
   -> SHA-256 content binding
   -> explicit contribution role

2. FOUR_DOMAIN_TRANSLATION
   -> HUMAN_CONSTRUCT_USE
   -> MACHINE_QUESTION_USE
   -> ENGINEERING_OPERATION_USE
   -> GOVERNANCE_INTERPRETATION_USE
   -> PERMITTED_CLAIM
   -> PROHIBITED_PROMOTION

3. CONFOUND_CONTROL
   -> preserve competing explanations
   -> reject human-construct == machine-ontology equivalence
   -> reject standard citation as a subjectivity proxy

4. RISK_AND_IMPACT_ROUTE
   -> map applicable AI risks / affected actors / residual-risk basis
   -> bind impact-assessment context where relevant
   -> no universal applicability by default

5. TEVV_ROUTE
   -> TEST
   -> EVALUATION
   -> VERIFICATION
   -> VALIDATION
   kept semantically distinct
   -> bind metrics, criteria, evaluator context and generalizability limits

6. SECURITY_ROUTE
   -> threat applicability
   -> bounded adversarial test design
   -> security receipt
   -> no SECURITY_PASS claim without empirical evidence

7. FULL_QMS_COMPOSITION
   -> bind exact target / source state
   -> bind data-quality / risk / TEVV / security receipts
   -> retain NCR/CAPA and management-review paths
   -> fail closed on missing or mismatched bindings

8. CLAIM_AND_AUTHORITY_ROUTE
   -> derive the maximum supported claim
   -> preserve negative / null / contradictory results
   -> separate structural admissibility from truth
   -> require the repository's human authority path for main transition

9. POST_CHANGE_REVALIDATION
   -> exact-head CI
   -> affected-control review
   -> source-status / dependency-change triggers
   -> NCR/CAPA when a control failure or nonconformity is identified
```

This is an orchestration procedure over existing surfaces, not a new autonomous
authority layer.

```text
AUTOMATION != AUTHORITY
PASSING_PIPELINE != SCIENTIFIC_TRUTH
FULL_QMS_PASS != SUBJECTIVITY_ESTABLISHED
STANDARD_MAPPING_PASS != STANDARD_CONFORMANCE
```

### Minimal implementation gap: standards lifecycle freshness

The current `ExternalStandardSource` already binds:

- standard identifier;
- issuing body;
- version/date;
- locator;
- access date;
- contribution roles;
- source-content SHA-256.

It does **not** currently represent the observed lifecycle status of the source
as a typed field. That matters because several relevant sources are actively
moving:

- NIST AI RMF 1.0 is under revision;
- NIST AI 200-2 TEVV-Athlon is an initial public draft;
- ISO/IEC DTS 42119-3.2 is under development;
- ISO/IEC AWI 42003 is under development;
- ISO/IEC 25059:2023 has advanced replacement work noted by ISO.

A future minimal executable extension may therefore add a bounded lifecycle
record such as:

```text
StandardLifecycleStatus
= PUBLISHED
| UNDER_REVISION
| INITIAL_PUBLIC_DRAFT
| UNDER_DEVELOPMENT
| SUPERSEDED
| WITHDRAWN

status_observed_on
status_source_locator
revalidation_trigger
```

Candidate fail-closed rules:

```text
DRAFT_AS_FINAL_STANDARD -> REJECT
SUPERSEDED_SOURCE_USED_AS_CURRENT_WITHOUT_JUSTIFICATION -> REJECT
MISSING_STATUS_PROVENANCE -> REJECT
STATUS_CHANGE_AFTER_RECORDED_REVIEW -> REVALIDATION_REQUIRED
```

This should be implemented only if a fresh code-level review confirms that the
same lifecycle semantics are not already owned elsewhere.

```text
DOCUMENTATION_CHANGE_2026_09_19 = YES
EXECUTABLE_CHANGE_2026_09_19 = NO
NEW_RESEARCH_AXIS = NO
NEW_GOVERNANCE_AUTHORITY = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
```
