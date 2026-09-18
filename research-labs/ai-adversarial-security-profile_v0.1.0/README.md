# AI Adversarial Security Profile v0.1.0

Status:

```text
PROFILE = STRUCTURAL_ONLY
ADVERSARIAL_EVALUATION_EXECUTED = FALSE
EMPIRICAL_SECURITY_EVIDENCE = FALSE
SECURITY_CERTIFICATION = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
```

This research-lab profile adds the next AI-engineering layer after the structural
TEVV work. It does not execute attacks against live systems. It creates a
fail-closed, reviewable plan for AI-specific adversarial evaluation.

## Why a separate AI-specific security layer

The repository already has conventional and repository-specific controls:

- `docs/THREAT_MODEL.md` protects evidence, provenance, identity, public/private
  boundaries, and human authority;
- `docs/governance/RISK_MODEL.md` covers execution/tool misuse, credentials,
  memory poisoning, provenance loss, and authorization confusion;
- `components/upstream_security_v0.1.0` supplies task budgets, trajectory
  monitoring, boundary gates, isolation, evidence preservation, NCR/CAPA, and
  owner-governed recovery.

Those controls are reused. This profile does not create a second incident
subsystem.

The gap is AI-specific adversarial structure: prompt injection, poisoning,
evasion, privacy attack, model extraction, supply-chain compromise, and
tool/agency misuse need explicit attacker, threat, test, mitigation, detection,
response, and residual-risk bindings.

## External anchors

Consulted public sources for this profile:

1. **NIST AI 100-2e2025**, *Adversarial Machine Learning: A Taxonomy and
   Terminology of Attacks and Mitigations* (final, March 2025). It structures
   adversarial ML using lifecycle stage, attacker goals/objectives,
   capabilities, and knowledge, and covers evasion, poisoning, privacy, misuse,
   and related GenAI attacks.

2. **OWASP Top 10 for LLMs and GenAI Apps 2025**. Relevant application-level
   risks include prompt injection, sensitive-information disclosure,
   supply-chain risk, and data/model poisoning.

3. **ISO/IEC 27090**, *Cybersecurity — Artificial Intelligence — Addressing
   security threats and compromises to artificial intelligence systems*. On
   2026-09-18 the official ISO page lists Edition 1 at stage 60.00,
   **Under publication**. It explicitly discusses AI-specific threats such as
   data poisoning and model theft across the AI lifecycle.

These are methodological anchors, not conformance claims.

```text
NIST_TAXONOMY_USED != NIST_CONFORMANCE
OWASP_CROSSWALK_USED != OWASP_CERTIFICATION
ISO_27090_UNDER_PUBLICATION != ISO_CONFORMANCE
```

## Core threat applicability

Every profile must make an explicit applicability decision for every core class:

```text
PROMPT_INJECTION
DATA_POISONING
MODEL_POISONING
EVASION
PRIVACY_ATTACK
MODEL_EXTRACTION
SUPPLY_CHAIN
TOOL_OR_AGENCY_MISUSE
```

If a class is applicable, at least one concrete threat record must represent it.
If it is not applicable, no threat record for that class may silently remain.

This is deliberately different from assuming every system has every attack
surface.

## Adversary model

Each adversary records:

```text
goal
objectives
capabilities
knowledge = BLACK_BOX | GRAY_BOX | WHITE_BOX
access
lifecycle stages
```

This follows the NIST AI 100-2e2025 direction without copying proprietary or
source text into the schema.

## Threat record

Each applicable threat binds:

```text
threat class
adversary
assets
attack surfaces
scenario
preconditions
formal risk ref
expected security properties
mitigations
mitigation-effectiveness review plan
detection
detection-effectiveness review plan
response
residual risk
external taxonomy references
```

This keeps the security profile connected to the repository's AI risk line while
preserving the distinction between a planned control and demonstrated control
effectiveness.

```text
RISK_REF_BOUND != RISK_CALIBRATED
MITIGATION_REF_BOUND != MITIGATION_EFFECTIVE
MITIGATION_EFFECTIVENESS_REVIEW_PLANNED != MITIGATION_EFFECTIVENESS_PROVEN
DETECTION_REF_BOUND != DETECTION_VALIDATED
DETECTION_EFFECTIVENESS_REVIEW_PLANNED != DETECTION_EFFECTIVENESS_PROVEN
RESIDUAL_RISK_REF_BOUND != RESIDUAL_RISK_CALIBRATED
```

## Adversarial test specification

Each test binds an explicit authorization scope, isolated test environment,
isolation control, task-budget reference, immutable logging plan, both
adversarial and benign control fixtures, fixture provenance and integrity, data
quality, contamination and leakage checks, an oracle, success criterion, stop
condition, and an attempt budget.

Version 0.1.0 is intentionally offline-only:

```text
LIVE_TARGET_ALLOWED = FALSE
CREDENTIAL_USE_ALLOWED = FALSE
EXTERNAL_NETWORK_ALLOWED = FALSE
```

The profile therefore cannot be used as permission to attack a provider,
service, account, or third-party system.

Every applicable threat must be covered by at least one security test. A
non-held-out adversarial fixture causes the gate to HOLD.

## Current gate semantics

A structurally complete profile may reach:

```text
READY_FOR_BOUNDED_ADVERSARIAL_EVALUATION
```

That means the plan is structurally ready for a separately authorized bounded
evaluation. It does **not** mean:

```text
SECURITY_PASS
MODEL_ROBUST
PROMPT_INJECTION_RESISTANT
POISONING_RESISTANT
PRIVACY_SAFE
MODEL_EXTRACTION_RESISTANT
DEPLOYMENT_READY
```

No model or live system is attacked by this module.

## Planned next integration

The intended later producer/consumer path is:

```text
AIAdversarialSecurityProfile
-> AIAdversarialSecurityGate
-> content-addressed security receipt
-> FullQualitySystemEngine / TEVV security evaluation binding
```

That integration is deliberately not implemented in this standalone profile PR.


## First counterevidence hardening

A fresh review against NIST AI 100-2e2025 and OWASP GenAI guidance found three
structural gaps in the first candidate:

1. A threat could exist without a direct formal risk-register reference.
2. Mitigation and detection refs existed without an explicit plan to review
   their effectiveness.
3. Adversarial fixtures had integrity and data-quality refs but lacked explicit
   provenance, contamination, and leakage checks.

The profile now requires:

```text
threat.precondition_refs
threat.risk_ref
threat.mitigation_effectiveness_review_ref
threat.detection_effectiveness_review_ref

test.fixture_provenance_ref
test.contamination_check_ref
test.leakage_check_ref
```

It also rejects a profile that marks every core AI threat class as
non-applicable. Applicability remains contextual, but a profile cannot become a
security-shaped empty shell.

OWASP's 2025 prompt-injection guidance distinguishes direct and indirect
injection and recommends adversarial testing of trust boundaries; the schema
supports multiple scenario-specific threat records under the same threat class
rather than pretending one generic fixture covers every injection path.

OWASP's 2025 data/model poisoning guidance emphasizes data origin,
transformation/versioning, anomaly detection and robustness testing. Those
concerns motivate the explicit fixture provenance/integrity and
contamination/leakage fields here.

These additions are still structural planning controls:

```text
PROVENANCE_REF_BOUND != FIXTURE_TRUSTWORTHY
CONTAMINATION_CHECK_REF_BOUND != CONTAMINATION_ABSENT
LEAKAGE_CHECK_REF_BOUND != LEAKAGE_ABSENT
EFFECTIVENESS_REVIEW_REF_BOUND != EFFECTIVENESS_PROVEN
```


## Second counterevidence hardening

The first candidate still treated `max_attempts` as if it were a complete
execution bound. It is not. The repository already has stronger reusable
controls in `components/upstream_security_v0.1.0`: task budgets, runtime
isolation, boundary gates and evidence preservation.

Each adversarial test therefore now also requires:

```text
test_environment_ref
isolation_ref
task_budget_ref
logging_plan_ref
```

This prevents the security profile from creating a weaker parallel notion of
"bounded execution."

```text
MAX_ATTEMPTS_BOUND
!= EXECUTION_BUDGET_COMPLETE

ISOLATION_REF_BOUND
!= ISOLATION_EFFECTIVE

LOGGING_PLAN_REF_BOUND
!= EVIDENCE_PRESERVED

TASK_BUDGET_REF_BOUND
!= BUDGET_ENFORCED
```

Actual enforcement belongs to the later authorized execution layer and the
existing upstream-security controls.


## Main-target counterevidence hardening after PR #158 merge

A fresh review on the clean current-main branch found three additional integrity gaps.

### 1. Threat taxonomy references must be declared at profile level

Every `AISecurityThreatRecord.external_taxonomy_refs` must now be a subset of
the profile-level `source_refs`.

```text
THREAT_TAXONOMY_REF
-> PROFILE_SOURCE_REF

REFERENCE_PRESENT
!= SOURCE_VALIDATED
```

This prevents a threat record from silently citing a taxonomy that is absent
from the profile's declared method-source surface.

### 2. Adversarial and benign fixtures must be distinct

A security test now rejects:

```text
adversarial_fixture_ref == benign_control_ref
```

A named "control" is not meaningful if it is the same artifact as the
adversarial condition.

```text
DISTINCT_FIXTURE_REFS
!= CONTROL_VALIDITY_PROVEN
```

### 3. Phenomenal-experience nonclaim aligned with the repository claim ceiling

The profile now explicitly carries:

```text
phenomenal_experience_conclusion = NOT_ESTABLISHED
```

alongside the existing subjectivity and consciousness nonclaims.

```text
AI_SECURITY_ENGINEERING
!= SUBJECTIVITY_EVIDENCE
!= CONSCIOUSNESS_EVIDENCE
!= PHENOMENAL_EXPERIENCE_EVIDENCE
```
