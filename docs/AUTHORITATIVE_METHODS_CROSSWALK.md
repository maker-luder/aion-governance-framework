# Authoritative Methods Crosswalk

Status: `PUBLIC_METHODS_CROSSWALK_CANDIDATE`

This document maps public standards, authoritative guidance, and open-science methods into the AION/Astra governance framework. A mapping means **methodological influence or compatibility**, not certification, endorsement, compliance, or achievement of an external level.

## Crosswalk

| External source | Relevant concept | AION/Astra convergence | Claim boundary |
|---|---|---|---|
| NIST AI RMF 1.0 + NIST AI 600-1 Generative AI Profile | Lifecycle risk management and trustworthiness considerations in design, development, use, and evaluation | Keep risk review attached to requirement, design, implementation, test, deployment, and research-claim stages; explicitly record context, affected actors, evidence and residual risk | No claim of NIST certification or formal conformance |
| NIST AI TEVV | Reliable measurements, testbeds, metrics, limitations, context-sensitive evaluation | Separate observation, metric, protocol, result, interpretation and limitation; require fresh execution evidence and context before PASS | Internal testing is not independent IV&V |
| NIST AI 100-2 E2025 | Adversarial ML taxonomy using lifecycle stage, attacker goal/objective, capability and knowledge | Extend threat records with structured adversary fields; cover poisoning, evasion, privacy, misuse and evidence/provenance manipulation relevant to GenAI | Taxonomy use does not establish completeness against every attack |
| NIST SP 800-218 SSDF | Secure development practices integrated through the SDLC | Preserve secure-development review from requirements through release; connect NCR/CAPA and root-cause correction to software-security findings | Project does not claim SSDF certification |
| W3C PROV-O / PROV-DM | Interoperable provenance via Entity, Activity, Agent and derivation/attribution/association relations | Map project artifacts, research runs and actors into a lightweight provenance vocabulary; keep authorship/source attribution distinct from approval authority | AION-specific roles remain project extensions, not W3C-defined roles |
| SLSA v1.2 provenance | Verifiable information about where, when and how software artifacts were produced | Treat build source, builder/workflow identity, commit, inputs, dependencies and artifact digest as release evidence; plan attestation verification | Do not claim a SLSA level until all applicable requirements are independently checked |
| GitHub Artifact Attestations | Cryptographically signed build provenance and optional SBOM association | Candidate release-hardening path for public build artifacts, with verification instructions and digest binding | Attestation proves declared build provenance/integrity properties, not semantic correctness or subjectivity |
| SPDX 3.0 | Open standard for SBOMs and software/data/AI/security metadata | Use SPDX-compatible inventory as the preferred future machine-readable dependency/license manifest | SPDX-format output is not a license-compatibility opinion |
| OpenSSF Scorecard | Automated indicators of open-source project security posture | Optional repository hardening feedback signal, recorded as an input to review rather than a gate by itself | A score is not certification and must not override project evidence |
| OWASP GenAI / LLM Top 10 | GenAI application security risks such as prompt injection, supply-chain risk, sensitive-information disclosure and excessive agency | Cross-reference runtime/tool/memory/prompt threat scenarios and default-deny controls | Community risk list supplements rather than replaces NIST taxonomy and project-specific threat modeling |
| Center for Open Science preregistration practices | Precommit study plans and distinguish confirmatory from exploratory analysis | For subjectivity experiments, freeze hypothesis, alternatives, outcomes, exclusion rules, protocol and analysis plan before confirmatory execution; label deviations and exploratory follow-ups | Preregistration improves transparency; it does not guarantee a correct hypothesis or valid result |

## New convergence methods

### 1. Multi-hypothesis evidence matrix

Every subjectivity-related observation should be evaluated against at least one non-subjective alternative explanation. Candidate alternatives include prompt conditioning, retrieval effects, imitation, stochastic variation, evaluator cueing, state leakage, implementation artifacts and test-fixture contamination.

A positive-looking observation is therefore not enough. The evidence record asks both:

- what hypothesis would this result support; and
- what competing explanations remain compatible with it.

### 2. Claim ladder

The project uses a deliberately conservative evidence ladder:

- `L0_OBSERVATION` — an output/event was observed.
- `L1_REPEATABLE_BEHAVIOR` — the behavior is reproducible under a specified protocol.
- `L2_STATE_ASSOCIATION` — a represented internal state is reliably associated with the behavior.
- `L3_INTERVENTION_SENSITIVE_MECHANISM` — controlled intervention on the candidate mechanism changes outcomes as preregistered.
- `L4_ROBUST_REPLICATION` — the finding survives meaningful context/model/run variation and independent or separated replication where feasible.
- `L5_SUBJECTIVITY_NOT_AUTOMATICALLY_ESTABLISHED` — even strong mechanism evidence is not, by itself, proof of phenomenal experience or subjectivity.

The ladder prevents a category error from `behavior -> mechanism -> phenomenal experience`.

### 3. Negative controls and perturbation tests

Where safe and governed, evaluation should include:

- negative controls expected not to produce the target effect;
- matched synthetic fixtures;
- context-order perturbations;
- memory-present / memory-absent comparisons;
- correction-before / correction-after comparisons;
- provenance-preserved / provenance-redacted comparisons where privacy permits;
- repeated runs with recorded environment and model/version identifiers.

Controlled/random model ablation remains separately governance-held and is not activated by this document.

### 4. Longitudinal continuity matrix

Continuity is measured dimension by dimension rather than treated as one binary identity claim:

`FACTUAL | PROJECT | ROLE | INTERPRETIVE | RELATIONAL_STYLE | CORRECTION_RECOVERY`

A run may pass some dimensions and fail others. No combination automatically establishes personal identity, consciousness, or phenomenal continuity.

### 5. Evidence card

Every material research claim should be capable of producing a machine-readable evidence card containing:

`claim_id, claim_level, hypothesis, alternatives, preregistration_status, protocol_ref, protocol_hash, code_commit, environment, input_fixture_refs, output_evidence_refs, result, limitations, reviewer_status, independent_validation_status, canonical_effect`

This separates the **claim** from the **evidence chain** used to support it.

## Public-source references

- NIST AI 600-1, *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*.
- NIST AI TEVV program materials.
- NIST AI 100-2 E2025, *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations*.
- NIST SP 800-218, *Secure Software Development Framework (SSDF) Version 1.1*.
- W3C Recommendation, *PROV-O: The PROV Ontology*.
- SLSA v1.2, *Provenance*.
- GitHub Docs, *Artifact attestations*.
- SPDX Specification 3.0.
- OpenSSF Scorecard.
- OWASP GenAI Security Project, *Top 10 for LLM Applications 2025*.
- Center for Open Science, *Preregistration* resources.

Where a source changes over time, the implementation should record the consulted source version/date rather than silently treating external guidance as immutable.
