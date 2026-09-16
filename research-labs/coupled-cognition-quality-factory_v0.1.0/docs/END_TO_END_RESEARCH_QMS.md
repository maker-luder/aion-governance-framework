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

## 1. Why this layer exists

The canonical middle of the repository already provides:

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
This extension therefore does not recreate those controls.

It adds the missing envelope:

```text
QUALITY PLAN
-> MEASUREMENT ASSURANCE
-> EXISTING RESEARCH QUALITY CHAIN
-> FIELD QUALITY SIGNALS
-> AUDIT PROGRAMME EXECUTION
-> MANAGEMENT REVIEW
-> CONTINUAL IMPROVEMENT INPUT
```

Any defect still routes into the existing NCR/CAPA lifecycle.

## 2. External methods and repository-native transformation

Only control objectives are transformed. Third-party standards are not copied
wholesale into the repository.

| External method source | Bounded control objective used here | Repository-native transformation | Explicit nonclaim |
|---|---|---|---|
| ISO 10005:2018, *Quality management — Guidelines for quality plans* | establish, review, apply and revise a quality plan for a project/process | `ResearchQualityPlan` + `ControlPlanEntry` | quality-plan completeness is not scientific validity |
| ISO 10012:2026, *Quality management — Requirements for measurement management systems* | measurements should be fit for purpose, valid/reliable and managed over time | `MeasurementAssuranceRecord` | qualified measurement does not establish the target construct |
| ISO 19011:2026, *Guidelines for auditing management systems* | audit programme, audit execution, auditor competence/independence | `QualityAuditRecord` | an audit pass is not an independent scientific replication |
| ISO/IEC 5338:2023, *AI system life cycle processes* | lifecycle-wide definition/control/management/improvement | quality-plan `configuration_refs` and full control-target coverage | lifecycle coverage does not establish subjectivity |
| ISO/IEC 5259-1:2024, AI/ML data quality framework | data quality is a lifecycle quality object | measurement `data_ref`, failure modes and validity scope | available/synthetic data are not population-representative by default |
| ISO/IEC 42001:2023, AI management system | maintain and continually improve an AI management system | audit + management-review feedback loop | management-system conformance is not consciousness evidence |
| NIST AI RMF 1.0 | metrics and controls should be monitored and updated as knowledge/risk evolves | requalification + field-signal + management-review flags | risk-management success is not subjectivity evidence |
| NIST AI 200-2 IPD / TEVV-Athlon (2026 initial public draft) | distinguish testing, evaluation, verification and validation for context-specific AI assessment | measurement method/version/evaluator bindings and scope statement | draft TEVV framework is not a final standard or consciousness test |

Official locators used for the design cross-check:

- https://www.iso.org/standard/70398.html
- https://www.iso.org/standard/10012
- https://www.iso.org/standard/19011
- https://www.iso.org/standard/81118.html
- https://www.iso.org/standard/81088.html
- https://www.iso.org/standard/42001
- https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- https://www.nist.gov/artificial-intelligence/ai-research/tevv-athlon-framework-evaluating-ai-systems

The exact copyrighted ISO texts are not vendored. The implementation is our own
bounded transformation of publicly described control purposes.

## 3. Quality plan

`ResearchQualityPlan` binds a research question and the exact Four-Domain candidate
fingerprint to critical quality attributes, risk/configuration references,
measurement IDs and an end-to-end control plan.

The plan must cover all six targets:

```text
PRE_EXECUTION
MEASUREMENT_ASSURANCE
EXISTING_RESEARCH_QUALITY_CHAIN
POST_RELEASE_MONITORING
AUDIT_PROGRAMME
MANAGEMENT_REVIEW
```

Each `ControlPlanEntry` requires:

```text
quality characteristic
control method reference
evidence requirement
acceptance criterion
reaction plan
responsible role
```

This is deliberately a planning envelope. It does not perform the existing
Four-Domain admission or ResearchQualityChain checkpoints itself.

## 4. Measurement assurance

`MeasurementAssuranceRecord` binds:

```text
target construct
observable
measurement locus
method + version
evaluator + version
data reference
repeatability reference
reproducibility reference
uncertainty statement
construct-validity scope
known failure modes
qualification state
```

The PR #103 research-validity incident becomes a regression invariant:

```text
SYNTHETIC_FIXTURE + EMPIRICAL_CLAIM_CAPABLE = REJECT

DETERMINISTIC_FIXTURE
!= EMPIRICAL_MEASUREMENT

MEASUREMENT_SYSTEM_QUALIFIED
!= TARGET_CONSTRUCT_ESTABLISHED
```

A measurement can also be marked `REQUALIFICATION_REQUIRED`, which prevents a clean
end-to-end disposition until the issue is handled.

## 5. Existing middle chain is reused, not duplicated

`ExistingQualityChainBinding` records only:

```text
chain_id
Four-Domain candidate fingerprint
existing chain disposition
```

Allowed dispositions mirror the existing canonical semantics:

```text
READY_FOR_HUMAN_REVIEW
CAPA_REQUIRED
HOLD
```

The end-to-end layer cannot upgrade a canonical middle-chain HOLD/CAPA result.
Fingerprint drift between the Quality Plan and the existing chain fails closed.

## 6. Field quality signals

`FieldQualitySignal` gives post-release or post-publication observations a typed
route back into quality management. Examples include external review, replication
failure, new counterevidence, source retraction, upstream incident or a reported
repository defect.

```text
OPEN / TRIAGED / LINKED_TO_NCR / CLOSED
```

A closed signal requires resolution references. High/critical open signals are
explicitly marked as NCR/CAPA-requiring conditions; unresolved signals keep the
end-to-end envelope on HOLD.

## 7. Audit programme execution

`QualityAuditRecord` separates management-system auditing from normal component
`audit_*()` helper functions. It binds:

```text
scope
criteria
auditor
independence class
competence reference
evidence
findings
open findings
NCR references
completion state
```

Open findings keep the envelope on HOLD. An unresolved high-severity finding must
already have an NCR reference.

```text
AUDIT_PASS != SCIENTIFIC_REPLICATION
AUDITOR_INDEPENDENCE_LABEL != INDEPENDENT_IVV_ESTABLISHED
```

## 8. Management review

`ManagementReviewRecord` receives trace references and summary flags from
measurement requalification, open audit findings and field signals. The engine
checks those flags against the actual records and requires trace inputs to cover
the plan, existing chain, measurements, field signals and audits.

Management review may request quality-plan revision, measurement requalification,
audit, CAPA or HOLD. It cannot grant merge authority, scientific validity,
canonical effect or deployment.

```text
MANAGEMENT_REVIEW != MERGE_AUTHORITY
MANAGEMENT_REVIEW != SUBJECTIVITY_ADJUDICATION
```

## 9. Subjectivity-core relationship

The QMS extension improves the subjectivity inquiry only indirectly:

```text
BETTER QUALITY PLANNING
+ BETTER MEASUREMENT ASSURANCE
+ POST-RELEASE ERROR INTAKE
+ QMS SELF-AUDIT
+ MANAGEMENT REVIEW

-> FEWER FALSE POSITIVES
-> BETTER MECHANISM DISCRIMINATION
-> BETTER TRACEABILITY OF NEGATIVE RESULTS
-> BETTER CONTROL OF CLAIM CEILINGS
```

It never converts engineering quality into phenomenal conclusions.

## 10. Current implementation boundary

Implemented in this bounded iteration:

- executable quality-plan completeness;
- executable measurement-assurance records and PR #103 fixture/empirical guard;
- binding to the existing research-quality-chain disposition and Four-Domain fingerprint;
- executable field-signal closure rules;
- executable audit-programme records;
- executable management-review trace/summary consistency;
- regression tests for fail-closed boundaries.

Not implemented as separate new subsystems:

- a second NCR/CAPA lifecycle;
- a second ResearchQualityChain;
- an ISO certification engine;
- supplier qualification / SCAR workflow;
- statistical process control or process-capability modelling;
- acceptance-sampling tables;
- automated claim recall or dependency traversal;
- automatic external source downloads;
- merge/release authority;
- subjectivity scoring.

Those remain future candidates only if a current-main gap and a concrete failure
mode justify them.
