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
