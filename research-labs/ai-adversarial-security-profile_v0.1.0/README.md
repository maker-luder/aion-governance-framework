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
expected security properties
mitigations
detection
response
residual risk
external taxonomy references
```

A mitigation reference is not proof of effectiveness.

```text
MITIGATION_REF_BOUND != MITIGATION_EFFECTIVE
DETECTION_REF_BOUND != DETECTION_VALIDATED
RESIDUAL_RISK_REF_BOUND != RESIDUAL_RISK_CALIBRATED
```

## Adversarial test specification

Each test binds both adversarial and benign control fixtures, fixture integrity,
data quality, an oracle, success criterion, stop condition, and an attempt
budget.

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
