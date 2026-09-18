# ISO-aligned AI risk and impact minimum control — 2026-09-18

Status: `BOUNDED_IMPLEMENTATION / DRAFT / HUMAN_REVIEW_PENDING`

Baseline main at branch creation:

```text
MAIN = d9155e9fd6908b2880adc43e160ece70a1036cc7
DEPLOYMENT = FALSE
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
ISO_CONFORMANCE_CLAIM = NONE
ISO_CERTIFICATION_CLAIM = NONE
```

## 1. Purpose

This change fills the two highest-priority quality gaps identified in the repository's
current AI-engineering cross-check:

1. an explicit AI risk register / treatment / residual-risk / reassessment control; and
2. an explicit AI system impact assessment covering foreseeable effects on people,
   groups and society.

The implementation is repository-native. It uses only publicly described control
purposes from the external standards listed below; it does not reproduce proprietary
standard clauses and it does not claim conformity or certification.

## 2. External public method anchors

### ISO/IEC 23894:2023

Public ISO description: guidance for organizations that develop, produce, deploy or use
AI-enabled products, systems or services to manage AI-specific risk and integrate risk
management into AI-related activities and functions.

Official public locator:

- https://www.iso.org/standard/77304.html

Repository transformation:

```text
AI risk
-> affected scope / stakeholder references
-> likelihood + consequence
-> risk-evaluation basis
-> existing controls
-> control-effectiveness evidence references
-> treatment
-> residual risk + residual-risk basis
-> risk owner
-> reassessment triggers
-> evidence
-> disposition
```

### ISO/IEC 42005:2025

Public ISO description: guidance for AI system impact assessment across the AI lifecycle,
including foreseeable impacts on individuals, groups and society.

Official public locator:

- https://www.iso.org/standard/42005

Repository transformation:

```text
assessment version + exact source-state reference
-> AI-system context + bounded system scope
-> intended use
-> foreseeable uses / misuse
-> affected individuals / groups / societal context
-> potential benefits / harms
-> human oversight
-> mitigations + mitigation-effectiveness evidence references
-> linked AI risks
-> residual impact + residual-impact basis
-> reassessment triggers
-> assessment evidence basis
-> disposition
```

## 3. New executable surface

The new module is:

`research-labs/coupled-cognition-quality-factory_v0.1.0/src/aion_coupled_quality/ai_risk_impact.py`

It defines:

- `AILifecycleStage`;
- `RiskLikelihood`;
- `AIRiskRecord`;
- `AIImpactAssessmentRecord`;
- `AIRiskImpactGate`;
- fail-closed dispositions for risk, impact and the combined gate.

The combined gate can emit only:

```text
READY_FOR_HUMAN_REVIEW
TREATMENT_OR_MITIGATION_REQUIRED
HOLD
```

It cannot emit release, merge, deployment, canonical, certification or scientific
authority.

```text
READY_FOR_HUMAN_REVIEW != RELEASED
READY_FOR_HUMAN_REVIEW != ISO_CONFORMANT
READY_FOR_HUMAN_REVIEW != ISO_CERTIFIED
RISK_CONTROLLED != ZERO_RISK
CONTROL_REFERENCE_PRESENT != CONTROL_EFFECTIVENESS_INDEPENDENTLY_VERIFIED
MITIGATION_REFERENCE_PRESENT != MITIGATION_EFFECTIVENESS_INDEPENDENTLY_VERIFIED
RESIDUAL_RISK_DECLARED != RESIDUAL_RISK_EMPIRICALLY_CALIBRATED
IMPACT_ASSESSED != IMPACT_OCCURRED
POTENTIAL_HARM != OBSERVED_HARM
ENGINEERING_GATE_PASS != SCIENTIFIC_VALIDATION
```

## 4. Initial bounded risk register

These entries are current repository risk hypotheses / management records. Qualitative
likelihood and severity are governance inputs, not empirical frequency estimates.

The repository uses its own bounded qualitative vocabulary for likelihood and severity.
It is not represented as an ISO-mandated scoring matrix. Every accepted risk record now
requires a risk-evaluation basis, control-effectiveness evidence references and a
residual-risk basis. The executable gate checks that those references are structurally
present; it does not independently resolve every referent or prove control effectiveness.

```text
REPOSITORY_NATIVE_QUALITATIVE_SCALE != ISO_MANDATED_SCALE
CONTROL_EFFECTIVENESS_REF_BOUND != CONTROL_EFFECTIVENESS_INDEPENDENTLY_VERIFIED
RESIDUAL_RISK_BASIS_RECORDED != RESIDUAL_RISK_EMPIRICALLY_CALIBRATED
```

| ID | Risk | Stage | Likelihood | Consequence | Existing controls | Residual | Current disposition |
|---|---|---|---|---|---|---|---|
| RISK-OVERCLAIM-001 | engineering/model output promoted beyond its evidence ceiling | RESEARCH | POSSIBLE | HIGH | subjectivity protocol, claim-ceiling review, mandatory nonclaims | MEDIUM | ACCEPTED_WITH_CONTROLS |
| RISK-PROVENANCE-002 | source/runtime/provenance drift causes evidence to be bound to the wrong state | RESEARCH / DEVELOPMENT | POSSIBLE | HIGH | exact-head checks, SHA/digest binding, provenance controls | MEDIUM | ACCEPTED_WITH_CONTROLS |
| RISK-AUTHORITY-003 | automated or agent action is mistaken for Human merge/canonical authority | DEVELOPMENT | UNLIKELY | CRITICAL | main-transition authority gate, fail-closed Human authority boundary | MEDIUM | ACCEPTED_WITH_CONTROLS |
| RISK-PRIVACY-004 | private or identifying material is published as research evidence | RESEARCH | UNLIKELY | HIGH | public/private boundary, public-safe fixtures, provenance review | LOW | ACCEPTED_WITH_CONTROLS |
| RISK-SYNTHETIC-005 | deterministic or synthetic fixture is misrepresented as empirical AI evidence | RESEARCH | POSSIBLE | HIGH | PR103 validity incident boundary, evidence admission, measurement assurance | MEDIUM | ACCEPTED_WITH_CONTROLS |

These dispositions do not state that the hazards are eliminated. A change to provider,
model/runtime identity, evidence schema, public-use scope, deployment state, privacy
boundary, claim ceiling or authority model is a reassessment trigger.

## 5. Initial bounded impact assessment

### AI-system context / assessment source state

The assessed object is not the GitHub repository in isolation. The bounded assessment
targets the AI-assisted Human–AI research-engineering workflow and the repository
control surface through which that workflow is documented, reviewed and constrained.

```text
ASSESSMENT_ID = IMPACT-RESEARCH-001
ASSESSMENT_VERSION = 0.1.0
EXACT_SOURCE_STATE_REF = git:d9155e9fd6908b2880adc43e160ece70a1036cc7
AI_SYSTEM_CONTEXT_REF = context:human-ai-research-engineering-workflow-v1
SYSTEM_SCOPE = AI_ASSISTED_RESEARCH_ENGINEERING_WORKFLOW_AND_REPOSITORY_CONTROL_SURFACE
CURRENT_LIFECYCLE = RESEARCH / DEVELOPMENT
DEPLOYMENT = FALSE
```

The exact source-state reference binds this initial impact assessment to the repository
baseline it assessed. Later repository or workflow changes require a new assessment
version or an explicit requalification record; an updated branch cannot silently rewrite
the historical assessment basis.

### Intended use

- support bounded AI-subjectivity-possibility research;
- support Human–AI learning research;
- maintain evidence provenance, counterevidence and claim ceilings;
- provide inspectable research-engineering and quality-control methods.

### Foreseeable beneficial impacts

- improved traceability and reproducibility;
- fewer false-positive research claims;
- clearer separation between engineering evidence and scientific conclusions;
- stronger defect containment and correction.

### Foreseeable misuse / adverse impacts

- readers may mistake repository engineering artifacts for proof of AI subjectivity;
- automated quality gates may be over-trusted as scientific or governance authority;
- private or contextual observations may be over-generalized;
- model/provider/runtime drift may invalidate earlier evidence while leaving stale claims;
- public terminology around consciousness/subjectivity may be misread as an established finding.

### Affected parties

Current foreseeable parties include maintainers, research collaborators, external readers,
and developers or researchers who reuse repository methods. Broader societal impact is
treated as potential rather than observed because the project is not deployed and there
is no evidence of broad adoption.

### Existing mitigations / oversight

- explicit Human review boundary;
- subjectivity, consciousness and phenomenal experience remain `NOT_ESTABLISHED`;
- claim ceilings and mandatory nonclaims;
- provenance and exact-state binding;
- NCR/CAPA and effectiveness verification;
- public/private boundary;
- non-destructive claim invalidation / withdrawal propagation.

Current bounded disposition:

```text
OBSERVED_IMPACTS_CLAIMED = FALSE
RESIDUAL_IMPACT = MEDIUM
RESIDUAL_IMPACT_BASIS = assessment:research-workflow-impact-residual-v1
MITIGATION_EFFECTIVENESS_EVIDENCE = REQUIRED
ASSESSMENT_EVIDENCE_BASIS = REQUIRED
DISPOSITION = ASSESSED_WITH_CONTROLS
REASSESSMENT_REQUIRED_ON_SCOPE_CHANGE = TRUE
```

This is a structured potential-impact assessment, not evidence that any listed impact has
occurred. A mitigation reference is not treated as proof that the mitigation works;
effectiveness-evidence references are separately required, and their independent
verification remains outside this structural gate.

## 6. Fail-closed rules

The executable control rejects or holds at least these cases:

- no risk register or no impact assessment;
- duplicate risk or impact identifiers;
- impact records linked to unknown risk IDs;
- high/critical residual risk marked as accepted;
- accepted risk with no control-effectiveness evidence reference;
- missing risk-evaluation or residual-risk basis;
- high/critical residual impact marked as controlled;
- controlled impact with no mitigation-effectiveness evidence reference;
- missing assessment version, exact source state, AI-system context, residual-impact basis or assessment evidence basis;
- treatment-required risk with no treatment reference;
- mitigation-required impact with no mitigation reference;
- claimed observed impacts with no observation references;
- observation references silently attached to a potential-only impact record.

## 7. Integration boundary

This change deliberately does not yet make `AIRiskImpactGate` a mandatory input to
`FullQualitySystemEngine`.

Reason:

```text
NEW_CONTROL_EXISTS
!=
EXISTING_QMS_INTEGRATION_PROVEN
```

The safe next step is to review this bounded gate and its tests first. A later separately
reviewed change may bind accepted risk/impact receipts into `ResearchQualityPlan`,
management review and the existing end-to-end QMS.

Current integration disposition:

```text
NEW_CONTROL_EXISTS = TRUE
FIRST_EXACT_HEAD_CI = PASS
FIRST_COUNTEREVIDENCE_REVIEW = GAPS_FOUND
HARDENING_APPLIED = CONTROL_EFFECTIVENESS + RESIDUAL_BASIS + SCOPE + EXACT_STATE
FULL_QMS_INTEGRATION = NOT_YET
```

## 8. Remaining ISO-AI gaps after this change

This change does not close:

- organization-level ISO/IEC 42001 AIMS completeness;
- full ISO/IEC 25059 quality-characteristic measurement matrix;
- full operationalization of the existing ISO/IEC 5259-informed data-quality records;
- real model-level AI testing evidence;
- deployment / operation / retirement lifecycle evidence;
- independent audit, independent IV&V, ISO conformity assessment or certification.

## 9. Provenance

```text
HUMAN_OWNER
= requested that the highest-priority ISO AI engineering gaps be filled first

CHATGPT_TEACHER
= re-read current repository quality state
= cross-checked official public ISO descriptions
= selected AI risk + AI impact as the first bounded implementation target
= formalized and implemented the repository-native records, gate, tests and this note

EXTERNAL_METHOD_SOURCES
= ISO/IEC 23894:2023 public ISO description
= ISO/IEC 42005:2025 public ISO description

ISO_CERTIFICATION = NONE
ISO_CONFORMANCE = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```


## 10. Layer-1 closure hardening before full-QMS integration

The second counterevidence review identified two gaps that must be closed before this
control can be considered for `FullQualitySystemEngine` integration:

1. risk records lacked their own version + exact source-state binding; and
2. the risk/impact producer surface lacked a content-addressed receipt.

This PR now hardens both.

### 10.1 Risk record version and source-state binding

Every `AIRiskRecord` now carries:

```text
risk_version
exact_source_state_ref
```

This makes a risk evaluation explicitly historical and source-bound.

```text
RISK_ID_SAME
!=
RISK_EVALUATION_STATE_SAME

RISK_VERSION
+ EXACT_SOURCE_STATE
-> REQUIRED
```

A later repository/model/runtime/source-state change cannot silently reuse an older risk
evaluation as though it were produced against the new state.

### 10.2 Content-addressed AI risk/impact receipt

The new `AIRiskImpactReceipt` binds:

```text
receipt id
exact source-state ref
exact runtime ref
producer Git HEAD
producer tree SHA
producer contract ref + digest
canonical sorted risk IDs
canonical sorted impact-assessment IDs
risk-set SHA-256
impact-set SHA-256
combined assessment SHA-256
bounded risk/impact disposition
fixed nonclaims
receipt SHA-256
```

`build_risk_impact_receipt(...)` additionally requires all risk and impact records to
match the receipt's declared exact source state before a receipt can be emitted.

The receipt is content-addressed, not signed:

```text
CONTENT_ADDRESS != DIGITAL_SIGNATURE
CONTENT_ADDRESS != INDEPENDENT_IVV
CONTENT_ADDRESS != ISO_CONFORMANCE
CONTENT_ADDRESS != MERGE_AUTHORITY
```

The intended future consumer pattern mirrors the repository's existing quality-chain
receipt discipline:

```text
AI risk + impact producer
-> typed records
-> AIRiskImpactGate
-> AIRiskImpactAssessment
-> AIRiskImpactReceipt
-> content digest

future FullQualitySystemEngine integration
-> pre-bind expected producer/source/receipt identity
-> verify receipt
-> consume bounded disposition
-> DOES NOT re-run producer semantics
```

### 10.3 Current integration boundary

This layer-1 hardening does **not** itself connect the new receipt to
`FullQualitySystemEngine`.

```text
RISK_SOURCE_BINDING = IMPLEMENTED
RISK_IMPACT_CONTENT_RECEIPT = IMPLEMENTED
RECEIPT_RUNTIME_BINDING = IMPLEMENTED
RECEIPT_BOUNDED_DISPOSITION = IMPLEMENTED
FULL_QMS_INTEGRATION = NOT_YET
MAIN_WRITE = NO
MERGE_AUTHORITY = NONE
```

The next decision remains contingent on exact-head CI and another counterevidence review.


### 10.4 Repository-bound producer resolution and assessment recomputation

A further cross-check against the repository's existing
`ResearchQualityChainReceipt` pattern found two additional seams:

1. caller-supplied Git provenance alone was weaker than the existing repository-bound
   quality-chain receipt builder; and
2. a caller could theoretically construct an `AIRiskImpactAssessment` object manually
   and pass it to the receipt builder without proving it was the gate result for the same
   risk/impact inputs.

The hardened surface now adds
`build_repository_bound_risk_impact_receipt(...)`, which resolves from committed Git
objects:

```text
producer Git HEAD
producer tree SHA
producer contract bytes -> SHA-256
```

Dirty working-tree contract bytes are not silently attributed to the committed producer
tree.

The low-level receipt builder also recomputes `AIRiskImpactGate.assess(...)` from the
supplied risk/impact records and requires exact equality with the supplied assessment.

```text
CALLER_SUPPLIED_ASSESSMENT
!=
TRUSTED_GATE_RESULT

SUPPLIED_ASSESSMENT
+ RECOMPUTED_GATE_ASSESSMENT
+ EXACT_EQUALITY
-> REQUIRED_FOR_RECEIPT
```

The repository-bound builder still does not create an external digital signature or
independent attestation.

```text
GIT_OBJECT_RESOLUTION != EXTERNAL_SIGNATURE
GIT_OBJECT_RESOLUTION != INDEPENDENT_IVV
```


### 10.5 Third counterevidence hardening: order invariance and complete scientific nonclaims

A further adversarial review found two smaller but real integrity gaps before full-QMS
integration:

1. risk/impact set semantics were order-insensitive, but the bounded assessment retained
   caller order in its identifier tuples. Because the assessment is hashed into the
   receipt, semantically identical sets could produce different receipts solely because
   the caller supplied a different tuple order;
2. the assessment/receipt fixed `SUBJECTIVITY = NOT_ESTABLISHED`, but did not carry the
   repository's parallel fixed nonclaims for consciousness and phenomenal experience.

The gate now emits canonical sorted risk and impact identifiers. Receipt generation still
sorts the record sets, and the assessment hash is therefore invariant to caller tuple
order for semantically identical inputs.

```text
SAME_RISK_IMPACT_SET
+ DIFFERENT_CALLER_ORDER
-> SAME_BOUNDED_ASSESSMENT
-> SAME_CONTENT_DIGEST
```

The bounded assessment and receipt now preserve all three scientific nonclaims:

```text
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```

Negative tests reject attempts to upgrade consciousness or phenomenal experience through
receipt mutation.

Current boundary remains:

```text
LAYER_1_CONTROL = IMPLEMENTED
LAYER_1_COUNTEREVIDENCE_HARDENING = APPLIED
FULL_QMS_INTEGRATION = NOT_YET
EXACT_HEAD_CI = REQUIRED_BEFORE_NEXT_LAYER
```


## 11. Layer-2 integration into FullQualitySystemEngine

After the standalone control was sealed and exact-head Quality/CodeQL passed at
`82c513537c85fce85b473f6eea19b4d84f804490`, the next bounded layer integrates the
content-addressed AI risk/impact receipt into the repository's existing full QMS.

The integration does not import risk/impact producer records into the full-QMS engine.
It consumes the validated receipt as a boundary object.

The quality plan must pre-bind:

```text
risk-impact producer Git HEAD
risk-impact producer tree SHA
risk-impact producer contract SHA-256
risk-impact receipt SHA-256
risk-impact exact source-state ref
risk-impact exact runtime ref
risk IDs
```

Management review must include:

```text
risk-impact receipt ID
risk IDs
impact-assessment IDs
```

A fourth integration countercheck found a cross-plan reuse risk: a cryptographically
content-addressed receipt could still be valid while describing the wrong assessment
target. The receipt therefore now includes `assessment_target_ref`, and
`FullQualitySystemEngine` requires exact equality with:

```text
quality-plan:<plan.plan_id>
```

Fail-closed integration rules include:

```text
RECEIPT_NOT_BOUND_TO_PLAN_CONFIGURATION -> HOLD
RECEIPT_TARGET_MISMATCH -> HOLD
RISK_IDS_NOT_BOUND_TO_PLAN_RISK_REFS -> HOLD
MANAGEMENT_REVIEW_MISSING_RISK_IMPACT_INPUTS -> HOLD
RISK_IMPACT_RECEIPT_HOLD -> HOLD
RISK_TREATMENT_OR_IMPACT_MITIGATION_REQUIRED -> HOLD
```

Prospective risk treatment is deliberately not converted into CAPA:

```text
RISK_TREATMENT_REQUIRED != NONCONFORMITY
RISK_TREATMENT_REQUIRED != CAPA_REQUIRED
```

This layer still grants no merge, release, deployment, canonical, ISO-conformity or
scientific authority.

```text
FULL_QMS_INTEGRATION = IMPLEMENTED_CANDIDATE
EXACT_HEAD_CI = PENDING
MAIN_WRITE = NO
MERGE_AUTHORITY = NONE
ISO_CONFORMANCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
```


### Quality-plan semantic target hardening

A later counterevidence pass identified a stale-target class that plan-ID binding alone
could not prevent:

```text
SAME_PLAN_ID
+ CHANGED_RESEARCH_QUESTION / CONTROL_PLAN / MEASUREMENTS / RISKS
!=
SAME_ASSESSMENT_TARGET
```

`ResearchQualityPlan.assessment_target_sha256()` now produces a canonical semantic
digest over the non-self-referential plan surface. `AIRiskImpactReceipt` binds that
digest, and `FullQualitySystemEngine` fails closed if the current plan digest differs.

The digest is order-invariant for set-like plan fields and deliberately excludes
`configuration_refs` because that collection contains the risk/impact receipt digest
itself. Configuration/provenance identities remain separately required by the full QMS.

```text
PLAN_ID_MATCH
!=
PLAN_SEMANTICS_MATCH

PLAN_ID_MATCH
+ PLAN_TARGET_DIGEST_MATCH
+ CONFIGURATION_BINDING
-> REQUIRED
```
