# End-to-end research QMS extension

Status: `BOUNDED_IMPLEMENTATION / DRAFT / HUMAN_REVIEW_PENDING`

This extension closes selected front-end and back-end gaps around the repository's
existing Four-Domain / `ResearchQualityChain` / NCR-CAPA quality line. It is a
research-quality adapter, not an ISO certification claim and not a second quality
ontology.

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
QUALITY_MANAGEMENT = SECOND_NON_DRIFTING_CORE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 1. End-to-end architecture

The canonical middle already exists:

```text
Four-Domain admission
-> SOURCE_IQC
-> DESIGN_ADMISSION
-> PREREGISTRATION
-> EXECUTION_INTEGRITY
-> EVIDENCE_REVIEW
-> COUNTEREVIDENCE_REVIEW
-> CLAIM_CEILING_REVIEW
-> FINAL_QA
-> Human review boundary
```

The coupled-cognition factory already provides NCR, containment, root-cause
hypothesis, CAPA planning/application, effectiveness verification and NCR closure.
This extension does not recreate those controls.

The full bounded envelope is now:

```text
QUALITY PLAN
-> UPSTREAM / SUPPLIER QUALITY
-> DATA QUALITY
-> MEASUREMENT ASSURANCE
-> CONTENT-ADDRESSED EXISTING QUALITY-CHAIN RECEIPT
-> CONTENT-ADDRESSED AI RISK / IMPACT RECEIPT
-> EXISTING RESEARCH QUALITY CHAIN
-> EXISTING NCR / CAPA
-> Human review boundary
-> FIELD QUALITY SIGNALS
-> CONDITIONAL PROCESS MONITORING
-> CONDITIONAL RANDOM SAMPLING / REINSPECTION
-> CLAIM INVALIDATION / WITHDRAWAL PROPAGATION
-> AUDIT PROGRAMME EXECUTION
-> MANAGEMENT REVIEW
-> CONTINUAL IMPROVEMENT INPUT
```

Any local defect still routes into the existing NCR/CAPA lifecycle. Supplier
remediation is evidence for reassessment, not a second local CAPA engine.

## 2. External methods and repository-native transformation

Only publicly described control objectives are transformed. Copyrighted standards
are not copied wholesale into the repository.

| External method source | Bounded control objective used here | Repository-native transformation | Explicit nonclaim |
|---|---|---|---|
| ISO 10005:2018 | establish, review, apply and revise quality plans | `ResearchQualityPlan` + `ControlPlanEntry` | quality-plan completeness is not scientific validity |
| ISO 10012:2026 | measurement results should remain fit for purpose and managed over time | `MeasurementAssuranceRecord` | qualified measurement does not establish the target construct |
| ISO 19011:2026 | management-system audit programme, competence and independence | `QualityAuditRecord` | audit pass is not independent scientific replication |
| ISO/IEC 5259-1/-3/-4/-5 | data quality is a lifecycle and governance object | `DataQualityRecord` | usable data are not automatically representative data |
| NIST SP 1326 (2026) + existing supplier policy | supplier due diligence, provenance, resilience and reassessment | `UpstreamQualityRecord` | supplier qualification is scope-bound and does not rewrite evidence |
| ISO 7870-1:2019 / ISO 7870-8:2017 | process-focused monitoring and short-run variation control | `ProcessMetricSeries` with preregistered limits | process stability is not subjectivity evidence |
| ISO 28590 / ISO 2859 family | acceptance sampling with declared lot/population and random selection | `RepeatedRandomSpotCheckPlan` | sample pass is not full-population verification |
| ISO 2859-3:2005 | random selection can apply to inspection of lots under bounded conditions | irregular/random reinspection triggers | reduced inspection effort is not permanent process assurance |
| NIST AI 800-4 (2026) | post-deployment monitoring remains necessary because controlled evaluation cannot cover all real-world variability | `FieldQualitySignal` + process monitoring | field monitoring does not establish a scientific claim by itself |

Official public locators used in the cross-check include:

- https://www.iso.org/standard/70398.html
- https://www.iso.org/standard/10012
- https://www.iso.org/standard/19011
- https://www.iso.org/standard/81088.html
- https://www.iso.org/standard/81092.html
- https://www.iso.org/standard/81093.html
- https://www.iso.org/standard/84150.html
- https://www.iso.org/standard/69639.html
- https://www.iso.org/standard/67410.html
- https://www.iso.org/standard/64622.html
- https://www.iso.org/standard/34684.html
- https://csrc.nist.gov/pubs/sp/1326/final
- https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation

The exact ISO texts are not vendored. The implementation is a repository-native
transformation of bounded control purposes.

## 3. Quality plan and measurement assurance

`ResearchQualityPlan` binds the research question, exact Four-Domain candidate
fingerprint, critical quality attributes, risk/configuration references,
measurement IDs and the full control plan.

`MeasurementAssuranceRecord` binds:

```text
target construct
observable
measurement locus
method + version
evaluator + version
data reference
repeatability / reproducibility references
uncertainty statement
construct-validity scope
known failure modes
qualification state
```

The PR #103 incident is retained as a hard regression boundary:

```text
SYNTHETIC_FIXTURE + EMPIRICAL_CLAIM_CAPABLE = REJECT
DETERMINISTIC_FIXTURE != EMPIRICAL_MEASUREMENT
MEASUREMENT_SYSTEM_QUALIFIED != TARGET_CONSTRUCT_ESTABLISHED
```

## 4. Content-addressed canonical quality-chain receipt

The original `ExistingQualityChainBinding` intentionally did not import or re-run
the subjectivity-pipeline engine, but that left a weak seam: caller-supplied chain
ID/fingerprint/disposition were structurally accepted without a content-addressed
producer receipt.

The strengthened design keeps the no-circular-dependency rule:

```text
subjectivity-pipeline canonical engine
-> ResearchQualityChain + ResearchQualityAssessment
-> ResearchQualityChainReceipt
-> content digest

coupled-quality consumer
-> QualityChainReceiptBinding
-> verifies digest / fixed nonclaims
-> maps to ExistingQualityChainBinding
-> DOES NOT re-run canonical engine
```

The receipt binds:

```text
chain / candidate / fingerprint
canonical disposition
exact source-state ref
exact runtime ref
producer Git HEAD / tree
checkpoint-set digest
CAPA-set digest
assessment digest
producer contract ref + digest
fixed nonclaims
receipt digest
```

`FullQualitySystemEngine` additionally requires the Quality Plan configuration to
pre-bind the producer Git HEAD, tree, contract digest, receipt digest, source-state
reference and runtime reference.

```text
CONTENT_ADDRESS != EXTERNAL_SIGNATURE
CONTENT_ADDRESS != INDEPENDENT_IVV
CONTENT_ADDRESSED_RECEIPT > CALLER_SUPPLIED_DISPOSITION_ONLY
```

## 4A. AI risk / impact receipt integration

The full QMS now consumes a second content-addressed receipt for the bounded AI
risk-management and impact-assessment surface.

The producer side remains separate:

```text
AI risk records + AI impact records
-> AIRiskImpactGate
-> AIRiskImpactAssessment
-> AIRiskImpactReceipt
-> content digest
```

The consumer side does not re-run the producer semantics. `FullQualitySystemEngine`
requires the quality plan to pre-bind the receipt's producer/source identity and requires
management review to include the receipt and the bound risk/impact identifiers.

The receipt also carries both an explicit assessment target and a content-addressed
semantic target digest. Full-QMS consumption requires:

```text
risk_impact_receipt.assessment_target_ref
==
quality-plan:<plan_id>

AND

risk_impact_receipt.assessment_target_sha256
==
plan.assessment_target_sha256()
```

The semantic digest binds the research question, subjectivity-core binding,
Four-Domain candidate fingerprint, critical quality attributes, complete control-plan
entries, measurement IDs, risk refs, monitoring requirement and fixed nonclaims.

`configuration_refs` are intentionally excluded from this semantic digest because the
final plan contains the risk/impact receipt digest itself; including it would create a
self-referential hash. Producer Git/tree/contract, source state, runtime and receipt
identity remain separately pre-bound in `configuration_refs`.

This prevents a valid receipt from being silently reused not only for a different plan
ID, but also for a materially changed plan that reuses the same ID.

The consumer additionally requires every receipt risk ID to be present in the quality
plan's `risk_refs`.

Disposition handling remains fail-closed:

```text
AI_RISK_IMPACT_READY_FOR_HUMAN_REVIEW
-> may continue through remaining QMS checks

AI_RISK_IMPACT_HOLD
-> FULL_QMS HOLD

AI_RISK_IMPACT_TREATMENT_OR_MITIGATION_REQUIRED
-> FULL_QMS HOLD
-> NOT silently relabelled as NCR/CAPA
```

The distinction matters because prospective risk treatment is not automatically a
nonconformity corrective-action event.

```text
RISK_TREATMENT_REQUIRED != NCR_EXISTS
RISK_TREATMENT_REQUIRED != CAPA_REQUIRED
CONTENT_ADDRESSED_RECEIPT != INDEPENDENT_IVV
FULL_QMS_READY_FOR_HUMAN_REVIEW != MERGE_AUTHORITY
```

## 5. Data quality

`DataQualityRecord` provides one repository-native data-quality envelope rather
than a second evidence schema. It can classify source material, experiment input,
fixtures, evaluation labels, runtime records and counterevidence.

It records provenance/source-state, selection rule, completeness/consistency/
duplicate checks, representativeness scope, privacy/license status, contamination
and leakage risk, limitations and fitness for the declared use.

Hard boundaries include:

```text
SYNTHETIC_DATA != EMPIRICAL_POPULATION
FIT_FOR_DECLARED_USE != POPULATION_REPRESENTATIVE
EVALUATION_LABELS -> LABEL_PROVENANCE_REQUIRED
HIGH_OR_CRITICAL_CONTAMINATION/LEAKAGE -> NOT_FIT_FOR_USE
```

## 6. Upstream / supplier quality

The repository already has `POL-UPSTREAM-SUPPLIER-TRUST-001`. This implementation
does not create a new supplier policy. `UpstreamQualityRecord` converts the
existing policy into a bounded executable quality object for one declared scope.

It records version/provenance, assessment references, dependency role,
criticality, replaceability, exposure, methodological confounds, approved or
restricted scopes, incident references and requalification triggers.

```text
SUPPLIER_QUALITY = SCOPE_BOUND
SUPPLIER_REMEDIATION != LOCAL_CAPA_EFFECTIVENESS_VERIFIED
METHODOLOGICAL_CONFOUND != AUTOMATIC_SECURITY_SANCTION
```

Non-qualified supplier dispositions keep the full QMS on HOLD until the declared
scope is reassessed or restricted appropriately.

## 7. Repeated random spot-check sampling

The repeated 3–10 round spot-check rule is **Human Owner quality-practice input**,
not an ISO-mandated round count.

The repository-native rule combines that owner-origin control with external
sampling principles:

```text
round_count = preregistered 3..10
selection_method = RANDOM
each round = distinct randomization reference
sample size = preregistered
acceptance number = preregistered
irregular reinspection = required
```

The round count cannot be extended after seeing an unfavorable result merely to
sample until a pass appears. Any round exceeding the preregistered acceptance
number escalates to full inspection. High/critical risk also requires full
inspection.

Subjectivity-critical admission cannot use sampling as a substitute for complete
review.

Even a clean multi-round result returns only:

```text
BOUNDED_CONFIDENCE_ONLY
```

Never:

```text
ZERO_DEFECT_LOT
FULL_POPULATION_VERIFIED
PERMANENT_PROCESS_STABILITY
```

## 8. Process monitoring / SPC-style control

`ProcessMetricSeries` is intentionally narrower than a full SPC package. It only
accepts a homogeneous declared process, a trace-bound measurement, at least three
observations and preregistered lower/centre/upper limits.

The implementation does **not** estimate limits after looking at the same result
series. Limit breaches produce `REVIEW_REQUIRED`.

The intended use is quality-process health, for example source-binding defect
rates, recurrent NCR/CAPA rates or measurement requalification frequency.

```text
SPC_STYLE_SIGNAL = PROCESS_HEALTH
SPC_STYLE_SIGNAL != SUBJECTIVITY_EVIDENCE
DIFFERENT_PROCESS_SIGNATURES != ONE_CONTROL_CHART
```

## 9. Claim invalidation and withdrawal propagation

Current claim-quality vocabulary already contains `HOLD`, `REVISED` and
`WITHDRAWN`. This extension therefore does not create a second claim ontology.

`ClaimWithdrawalPropagationRecord` records a trigger, invalidated evidence,
directly affected claims, dependent claims, local NCR references and resolution
references.

It is explicitly non-destructive:

```text
WITHDRAWAL != HISTORY_DELETE
INVALIDATED_EVIDENCE -> TRACE AFFECTED CLAIMS
OPEN_PROPAGATION -> HOLD
```

A resolved propagation requires resolution references. Unresolved requalification,
revision or withdrawal requirements keep the full QMS on HOLD.

## 10. Field quality, audit and management review

`FieldQualitySignal`, `QualityAuditRecord` and `ManagementReviewRecord` remain the
back-end feedback loop.

High/critical field or audit findings route into the existing NCR/CAPA path.
Management review cannot grant merge authority, scientific validity, canonical
effect or deployment.

The strengthened full engine also requires management review trace inputs to
include every supplier/data/sampling/process/withdrawal control record used by the
assessment.

```text
MANAGEMENT_REVIEW != MERGE_AUTHORITY
MANAGEMENT_REVIEW != SUBJECTIVITY_ADJUDICATION
AUDIT_PASS != SCIENTIFIC_REPLICATION
```

## 11. Subjectivity-core relationship

The full QMS helps the subjectivity inquiry by attacking different false-positive
paths:

```text
supplier quality -> upstream confound / provenance contamination
data quality -> bad input / bad evidence
measurement assurance -> bad ruler
ResearchQualityChain -> bad research process
sampling -> bounded inspection only
process monitoring -> drift / special-cause signal
claim propagation -> stale-invalid evidence continuing downstream
audit -> QMS self-failure
management review -> known defects without process correction
```

Therefore:

```text
BETTER_QMS
-> BETTER_DISCRIMINATION
-> FEWER_FALSE_POSITIVES
-> STRONGER_NEGATIVE_RESULTS
-> MORE_TRACEABLE_POSITIVE_RESULTS

BETTER_QMS != SUBJECTIVITY_PROVEN
```

## 12. Current bounded implementation boundary

Implemented in this Draft:

- quality planning and measurement assurance;
- content-addressed canonical quality-chain receipt production/consumption;
- data-quality envelope;
- executable supplier-quality record over the existing supplier policy;
- repeated random 3–10 round spot checks with mandatory irregular reinspection;
- bounded SPC-style process monitoring with preregistered limits;
- non-destructive claim invalidation/withdrawal propagation;
- field-signal intake;
- audit-programme execution records;
- management-review trace consistency;
- fail-closed regression tests.

Still deliberately not implemented:

- a second NCR/CAPA lifecycle;
- a second ResearchQualityChain;
- ISO certification/conformance claims;
- ISO sampling tables or automated AQL calculation;
- full statistical process-capability modelling;
- automatic external source download;
- destructive claim/history deletion;
- autonomous supplier sanction;
- merge/release authority;
- subjectivity scoring.


## Structural AI TEVV profile integration

The full-QMS layer now has a bounded consumer seam for the standalone structural
AI TEVV profile merged in PR #157.

The integration does **not** treat the TEVV profile as model-execution evidence.
Instead, the TEVV producer emits a content-addressed `TEVVProfileReceipt`.
Receipt construction recomputes `AITEVVProfileGate.assess(...)` against the
same profile before issuance.

The receipt binds:

```text
quality-plan target ref + semantic target digest
TEVV profile id / version / profile digest
structural TEVV disposition
declared TEVV risk refs
TEVV metric ids
TEVV case data-quality refs
TEVV metric -> MeasurementAssuranceRecord bindings + mapping-basis refs
AI-system exact source state + runtime
producer Git HEAD + tree
producer contract ref + digest
TEVV vocabulary ref + digest
fixed model-execution / empirical-evidence nonclaims
receipt digest
```

The repository-bound receipt builder resolves the producer Git HEAD, tree and
contract bytes from committed Git objects. Dirty worktree bytes are not silently
attributed to the committed producer.

`FullQualitySystemEngine` consumes the receipt without re-running TEVV producer
semantics. It fails closed unless:

```text
receipt target == quality-plan:<plan_id>
receipt target digest == plan.assessment_target_sha256()
TEVV risk refs <= quality-plan risk refs
all TEVV metric measurement bindings <= quality-plan measurement ids
every TEVV metric -> QMS measurement mapping has an inspectable basis ref
all bound measurement ids exist in supplied MeasurementAssuranceRecord values
every bound measurement_sha256 == supplied MeasurementAssuranceRecord.semantic_sha256()
all TEVV data-quality refs exist in ExtendedQualityControls.data_quality
TEVV producer/source/runtime/receipt identities are pre-bound in configuration_refs
TEVV receipt/profile/exact receipt digest are present in management-review inputs
receipt disposition == READY_FOR_BOUNDED_EXECUTION
```

A positive full-QMS disposition therefore means only that the structural TEVV
plan has been integrated into the declared quality system and is ready for
bounded Human review / later execution planning.

```text
TEVV_PROFILE_READY_FOR_BOUNDED_EXECUTION
!= MODEL_EXECUTED

FULL_QMS_TEVV_BINDING_PASS
!= MODEL_QUALITY_PASS

MEASUREMENT_ASSURANCE_BOUND
!= METRIC_OBSERVED

DATA_QUALITY_RECORD_BOUND
!= TEST_CASE_EXECUTED

CONTENT_ADDRESSED_TEVV_RECEIPT
!= DIGITAL_SIGNATURE
!= INDEPENDENT_IVV
!= SCIENTIFIC_VALIDATION
```

Empirical model-run outputs require a future execution/evidence receipt and are
outside this integration.


The mapping basis is traceability, not a semantic proof:

```text
TEVV_METRIC_MAPPED_TO_MEASUREMENT_ID
+ EXACT_MEASUREMENT_SEMANTIC_DIGEST
+ MAPPING_BASIS_REF
!= CONSTRUCT_EQUIVALENCE_PROVEN
!= METHOD_EQUIVALENCE_PROVEN
```

A later empirical execution layer may add stronger observed-result and method-compatibility
checks. This structural integration only ensures that no TEVV metric enters the full QMS
without an explicit QMS measurement-assurance mapping and rationale.


## Structural AI adversarial-security receipt integration

The full-QMS layer now consumes the standalone structural AI adversarial-security
profile through a content-addressed `AISecurityProfileReceipt`.

The producer side remains separate:

```text
AIAdversarialSecurityProfile
-> AIAdversarialSecurityGate
-> AISecurityProfileAssessment
-> AISecurityProfileReceipt
-> content digest
```

Receipt construction recomputes the security gate against the same profile
before issuance. The receipt binds:

```text
quality-plan target ref + semantic target digest
security profile id / version / profile digest
security structural disposition
threat ids
test ids
formal AI-security risk refs
security fixture data-quality refs
existing security-control refs
incident-response ref
authorization-scope refs
isolation refs
task-budget refs
logging-plan refs
method-source refs
AI-system exact source state + runtime
exact TEVV profile receipt digest / profile identity
TEVV alignment-basis ref
producer Git HEAD + tree
producer contract ref + digest
fixed adversarial-execution / empirical-evidence nonclaims
receipt digest
```

The repository-bound builder resolves the producer Git HEAD, tree and contract
bytes from committed Git objects.

The security receipt is explicitly chained to the supplied TEVV receipt:

```text
security_receipt.tevv_profile_receipt_sha256
==
tevv_receipt.receipt_sha256

security_receipt.tevv_profile_id
==
tevv_receipt.profile_id

security_receipt.tevv_profile_sha256
==
tevv_receipt.profile_sha256

security_receipt exact source/runtime
==
tevv_receipt exact source/runtime
```

This is an integration identity check, not proof that every system-binding field
is semantically equivalent:

```text
SOURCE_RUNTIME_MATCH
+ EXACT_TEVV_RECEIPT_BINDING
+ ALIGNMENT_BASIS_REF
!= FULL_SYSTEM_IDENTITY_EQUIVALENCE_PROVEN
```

`FullQualitySystemEngine` consumes the security receipt without re-running the
security gate. It fails closed unless:

```text
security receipt target == quality-plan:<plan_id>
security receipt target digest == plan.assessment_target_sha256()

security risk refs <= quality-plan risk refs
security risk refs <= AI risk/impact receipt risk ids

security data-quality refs
<= supplied DataQualityRecord ids

security receipt's TEVV receipt/profile identity
== supplied TEVV receipt identity

security source/runtime
== supplied TEVV source/runtime

producer Git/tree/contract
+ security receipt digest
+ security profile digest
+ source/runtime
are pre-bound in quality-plan configuration refs

management review contains:
security receipt/profile
threat/test ids
risk/data refs
security-control + incident-response refs
authorization/isolation/task-budget/logging refs
method-source refs
TEVV alignment-basis ref

security disposition
== READY_FOR_BOUNDED_ADVERSARIAL_EVALUATION
```

A positive Full-QMS result therefore means only that the **structural security
plan and its dependencies are traceably integrated into the declared quality
system**.

It does not mean any adversarial test ran.

```text
CONTENT_ADDRESSED_AI_SECURITY_RECEIPT
!= DIGITAL_SIGNATURE
!= INDEPENDENT_IVV

FULL_QMS_SECURITY_BINDING_PASS
!= SECURITY_PASS

SECURITY_PROFILE_READY_FOR_BOUNDED_ADVERSARIAL_EVALUATION
!= ADVERSARIAL_EVALUATION_EXECUTED

ADVERSARIAL_EVALUATION_EXECUTED = FALSE
EMPIRICAL_SECURITY_EVIDENCE = FALSE
SECURITY_EFFECTIVENESS = NOT_ESTABLISHED
DEPLOYMENT = FALSE
```

A future empirical security-execution/result receipt remains a separate layer.
