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
