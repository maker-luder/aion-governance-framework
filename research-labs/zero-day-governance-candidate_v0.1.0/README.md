# Zero-Day Governance Candidate v0.1.0

Status: `RESEARCH_ONLY / CANDIDATE_CONCEPT / NOVELTY_NOT_ESTABLISHED / CANONICAL_EFFECT=NONE`

## Scope and non-equivalence

This module studies **Zero-Day Governance** as a candidate research concept proposed by the Human Owner. It is not canonical project terminology, a long-term knowledge rule, a deployment feature, or a cybersecurity assurance claim.

> `ZERO_DAY_GOVERNANCE != ZERO_DAY_EXPLOIT_PREVENTION`

In cybersecurity usage, a zero-day exploit concerns an attack exploiting a software, hardware, or firmware vulnerability unknown to the vendor or public before a fix is available.[7] The present candidate uses “zero-day” only as a bounded metaphor for a **previously unmodeled governance anomaly**. It does not claim immunity from zero-day vulnerabilities, exploit detection, patching, or cyber incident response.

## Core research question

Does a governance practice for identifying, containing, characterizing, falsifying, and converting newly observed, previously unmodeled failure modes into provenance-preserving testable controls provide defensible incremental value, or does it merely rename existing incident response, vulnerability management, resilience engineering, assurance, CAPA, anomaly management, AI risk management, change control, monitoring, and regression practices?

The candidate definition under test is:

> **Zero-Day Governance is a governance practice for identifying, containing, characterizing, and converting newly observed, previously unmodeled failure modes into explicit, provenance-preserving, testable controls before they silently become persistent systemic behavior.**

The implementation does not assume that this definition is novel or necessary. It explicitly tests redundancy, insufficient evidence, overreaction, speed bias, false-zero-day status, provenance failure, unknown collapse, and regression overfitting.

## Prior-art comparison

| Existing framework | Prior-art coverage observed | Implication for candidate novelty |
|---|---|---|
| CISA incident/vulnerability response playbooks | Identify, coordinate, remediate, recover, and track successful mitigations; lessons learned and shared procedures.[1] | Core capture-to-control lifecycle is not new in cybersecurity. |
| NIST incident response | Preparation, incident response, recovery, and program improvement are integrated into cybersecurity risk management; Rev. 3 is a 2025 CSF 2.0 profile.[2] [4] | A lifecycle alone cannot establish a distinct concept. |
| NASA software assurance and IV&V | Objective evidence, process/product assessment, findings, metrics, rigorous testing, full lifecycle assurance, safety/security, and independent verification.[3] | Provenance, assurance, regression, and independent review already have mature analogues. |
| NIST AI RMF | Govern, Map, Measure, and Manage are continuous lifecycle functions with monitoring, accountability, incident identification, information sharing, and contingency processes.[5] | AI governance already covers much of the proposed cross-domain structure. |
| CMU/SEI CERT-RMM | Incident Management and Control identifies and analyzes events, detects incidents, and determines organizational response.[6] | Event-to-response resilience management directly overlaps capture, characterization, containment, and response. |
| Proposed candidate | Cross-domain anomaly record with explicit unknown-state, provenance freeze, competing explanations, containment, falsification, control, and regression references. | At most a possible synthesis or extension; distinctness is not established. |

The initial exact-phrase search found recent commercial or social uses of “zero-day governance,” mostly connected to cybersecurity or AI-agent vulnerability contexts, but no authoritative source establishing a stable cross-domain definition. This is a **terminology-collision finding**, not proof of novelty.

## Candidate lifecycle

The synthetic lifecycle is:

```text
CAPTURE
  → PROVENANCE_FROZEN
  → CONTAINED
  → CHARACTERIZED
  → FALSIFICATION_READY
  → CONTROL_PROPOSED
  → REGRESSION_CONVERTED
```

Each later stage requires the relevant earlier stage. A captured event requires source references and an observation summary. Containment cannot be accepted before provenance freeze. Characterization requires competing explanations. Control and regression stages require explicit control and regression-case references. No stage emits a canonical or deployment effect.

The contract also preserves the distinctions:

```text
UNKNOWN != TRUE
UNKNOWN != FALSE
HOLD != FAIL
NOT_ESTABLISHED != FALSE
NEEDS_CONFIRMATION != DENY
```

`ADMISSIBLE_FOR_REVIEW` means only that event metadata satisfies this synthetic contract. It does not confirm a mechanism, establish a root cause, validate a governance policy, or establish novelty.

## Day-0 Capture hypothesis

The prototype records `time_to_capture_hours` and supports four policy interpretations: `DESCRIPTIVE`, `PROJECT_SLO`, `RESEARCH_METRIC`, and `REJECTED`. A 24-hour threshold is not built into the definition. A case captured in 48 hours against a 24-hour project target remains reviewable while recording that the target was not met. This tests **speed bias** rather than treating speed as proof of quality.

The metrics are:

| Metric | Meaning in this prototype |
|---|---|
| `time_to_capture_hours` | Elapsed time from first observation to capture metadata. |
| `day0_24h_descriptive` | Descriptive indicator only; not a universal standard. |
| `day0_target_hours` | Optional project-specific target or research parameter. |
| `day0_target_met` | Whether the declared target was met; not whether the investigation was correct. |

Time-to-capture is therefore a candidate operational metric, not a universally valid 24-hour SLO. It must be evaluated against false closure, characterization quality, containment quality, and regression generality.

## Experiment results

The 23 unit tests and 12 synthetic cases passed. The cases included a valid unknown-state capture, full lifecycle review, 48-hour speed-bias case, confirmed-without-mechanism unknown collapse, false zero-day prior-art collision, missing provenance, governance overreaction, regression overfitting, existing-framework sufficiency, cross-framework synthesis, targeted existing-framework extension, and an unsupported distinctness claim.

| Case family | Result | Interpretation |
|---|---|---|
| Valid capture/full lifecycle | `ADMISSIBLE_FOR_REVIEW` | Mechanism metadata review only; unknown state remains preserved. |
| 48-hour capture versus 24-hour target | `ADMISSIBLE_FOR_REVIEW` with metric `day0_target_met=0` | Speed is recorded, not equated with quality or truth. |
| Confirmed status without mechanism | `INDETERMINATE` | A label cannot substitute for evidence. |
| Prior-art reference | `HOLD` | A previously documented failure is not silently relabeled zero-day. |
| Missing provenance | `HOLD` | Reconstruction is required before later lifecycle use. |
| Governance-effect request | `HOLD` | The research artifact cannot promote or change governance. |
| Missing regression case | `HOLD` | A one-instance fix cannot be called regression conversion. |
| Existing framework covers all fields | `REDUNDANT_TERMINOLOGY` | Strong negative result against distinctness. |
| Cross-framework synthesis | `USEFUL_SYNTHESIS_ONLY` | Candidate synthesis without evidence of distinct capability. |
| Single-framework targeted gap | `EXISTING_FRAMEWORK_EXTENSION` | Potential integration, not a new governance layer. |
| Distinctness claim without comparison | `INSUFFICIENT_EVIDENCE` | Novelty cannot be asserted from one review. |

The observed recommendation for this checkpoint is `USEFUL_SYNTHESIS_ONLY`, while the formal novelty conclusion remains `NOT_ESTABLISHED`. This classification is provisional and describes the synthetic comparison result, not a canonical project decision.

## Falsifiers and overengineering controls

The module tests the following falsifiers:

1. **Existing-framework sufficiency:** a complete NIST-like mapping produces `REDUNDANT_TERMINOLOGY`.
2. **Speed bias:** a missed 24-hour target is recorded without treating delay as automatic failure or rushing root-cause analysis.
3. **Governance overreaction:** a new event cannot request `PROMOTE`, canonical, or deployment effects.
4. **False zero-day:** prior-art references force `HOLD` for review.
5. **Provenance failure:** missing source references force `HOLD`.
6. **Regression overfitting:** a regression stage without a declared case reference is held.
7. **Unknown collapse:** confirmed status without mechanism evidence is `INDETERMINATE`, and unknown is serialized as neither true nor false.
8. **Novelty failure:** unsupported distinctness claims return `INSUFFICIENT_EVIDENCE`.

These negative controls are mechanism checks for the prototype. They do not prove that the candidate concept is useful in real organizations or that existing frameworks are insufficient in all domains.

## Reproduction

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_zero_day_experiment.py --output fixtures/zero_day_result.json
```

The runtime uses only the Python standard library. It does not call a model, external agent, private data source, live tool, deployment, canonical state, or main.

## Candidate classification and boundaries

```text
RECOMMENDED_CLASSIFICATION = USEFUL_SYNTHESIS_ONLY
NOVELTY_CONCLUSION = NOT_ESTABLISHED
ZERO_DAY_GOVERNANCE = CANDIDATE_RESEARCH_CONCEPT
ZERO_DAY_EXPLOIT_PREVENTION = OUT_OF_SCOPE
UNKNOWN_STATE_PRESERVED = TRUE
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
```

## References

[1]: https://www.cisa.gov/resources-tools/resources/federal-government-cybersecurity-incident-and-vulnerability-response-playbooks "CISA — Federal Government Cybersecurity Incident and Vulnerability Response Playbooks"
[2]: https://csrc.nist.gov/projects/incident-response/preparation-resources "NIST — Incident Response Preparation Resources"
[3]: https://sma.nasa.gov/sma-disciplines/software-assurance-and-software-safety "NASA — Software Assurance and Software Safety"
[4]: https://csrc.nist.gov/pubs/sp/800/61/r3/final "NIST SP 800-61 Rev. 3 — Incident Response Recommendations and Considerations"
[5]: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ "NIST AI RMF Core"
[6]: https://www.sei.cmu.edu/library/incident-management-and-control-imc-cert-rmm-process-area/ "CMU/SEI — Incident Management and Control (IMC) CERT-RMM Process Area"
[7]: https://www.sans.org/security-resources/glossary-of-terms/zero-day-exploit "SANS — Zero-Day Exploit"
