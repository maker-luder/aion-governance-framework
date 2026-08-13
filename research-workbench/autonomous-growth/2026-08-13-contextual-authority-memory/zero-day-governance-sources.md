# Zero-Day Governance research notes — 2026-08-13

## Research status

`ZERO_DAY_GOVERNANCE = CANDIDATE_RESEARCH_CONCEPT`

`NOVELTY_CONCLUSION = NOT_ESTABLISHED`

`ZERO_DAY_GOVERNANCE != ZERO_DAY_EXPLOIT_PREVENTION`

These notes are a prior-art review, not project authority and not a canonical terminology change. The focused question is whether a cross-domain lifecycle for previously unmodeled governance failures adds defensible structure beyond existing incident response, vulnerability management, assurance, resilience, CAPA, anomaly management, and regression practices.

## Source 1 — CISA Federal Government Cybersecurity Incident and Vulnerability Response Playbooks

Source: <https://www.cisa.gov/resources-tools/resources/federal-government-cybersecurity-incident-and-vulnerability-response-playbooks>

Date: page accessed 2026-08-13; page publication date not shown in the extracted body.

Authority: U.S. Cybersecurity and Infrastructure Security Agency; official federal operational publication for FCEB information systems.

Claim: CISA presents two playbooks, one for incident response and one for vulnerability response. The page describes shared procedures to identify, coordinate, remediate, recover, and track successful mitigations, and says the playbooks evolve practices using lessons learned and industry practice.

Scope: cybersecurity incidents and vulnerabilities affecting FCEB systems, data, and networks.

Transformation: this is strong prior art for CAPTURE/CHARACTERIZATION/CONTAINMENT-or-REMEDIATION/RECOVERY/REGRESSION-TRACKING. It weakens a claim that the proposed lifecycle is novel in cybersecurity. It does not by itself cover non-cyber governance anomalies such as authority precedence, provenance drift, memory contamination, evidence conflict, or research/canonical leakage.

## Source 2 — NIST Incident Response project, Preparation Resources

Source: <https://csrc.nist.gov/projects/incident-response/preparation-resources>

Date: created 2024-02-29; updated 2025-11-20, as shown on the page.

Authority: National Institute of Standards and Technology, Computer Security Resource Center.

Claim: NIST organizes incident-response resources across general and sector-specific programs, program assessment and improvement, and training and exercises; the project also links preparation and life-cycle resources and identifies incident response, threats, vulnerability management, cybersecurity framework, and forensics as related topics.

Scope: cybersecurity incident response program preparation and improvement, not a general governance theory.

Transformation: this is prior art for preparedness, lifecycle governance, assessment/improvement, exercises, and evidence/forensics context. A Zero-Day Governance concept cannot claim these elements as new. A possible residual value would have to be a domain-neutral event schema and explicit unknown-state/closure controls spanning governance anomalies, but that residual is a hypothesis only.

## Initial terminology finding

The initial public search returned cybersecurity "zero-day" usage and many established response/assurance frameworks, but no authoritative source establishing "Zero-Day Governance" as a settled cross-domain term. Absence in this search is not proof of nonexistence. The exact-term question remains `INSUFFICIENT_EVIDENCE` until broader databases and official terminology sources are checked.

## Source 3 — NASA Software Assurance and Software Safety

Source: <https://sma.nasa.gov/sma-disciplines/software-assurance-and-software-safety>

Date: page site last updated 2026-08-06.

Authority: NASA Office of Safety and Mission Assurance.

Claim: NASA describes software assurance and safety as activities that assess adherence and adequacy of processes, produce objective evidence and conclusions, determine software quality, ensure safety/security, and apply rigorous analysis and testing throughout the lifecycle. It describes IV&V, risk/issue/finding reporting, metrics, lifecycle assurance, and standards from conception through operations, maintenance, and retirement.

Scope: NASA software assurance, software safety, and independent verification/validation for mission and safety-critical systems.

Transformation: this is prior art for provenance-bearing assurance, independent evaluation, findings, metrics, lifecycle controls, regression/test evidence, and safe retirement. It strongly weakens any novelty claim based only on `CHARACTERIZATION → TESTABLE CONTROL → REGRESSION`. A residual hypothesis could be a domain-neutral anomaly schema that links non-cyber governance anomalies to assurance artifacts, but it must prove reduced complexity rather than add another vocabulary layer.

## Source 4 — NIST SP 800-61 Rev. 3

Source: <https://csrc.nist.gov/pubs/sp/800/61/r3/final>

Date: published April 2025; supersedes SP 800-61 Rev. 2.

Authority: NIST Computer Security Resource Center.

Claim: NIST Rev. 3 integrates incident-response recommendations throughout cybersecurity risk management using the CSF 2.0 Community Profile, with the stated aim of preparing for incidents, reducing incident number/impact, and improving detection, response, and recovery efficiency/effectiveness.

Scope: cybersecurity incident response and cybersecurity risk management.

Transformation: the proposed lifecycle is not novel within cybersecurity incident response. It is more defensible as a cross-domain synthesis only if it preserves unknown/indeterminate states and provenance across non-cyber governance failures without claiming to replace NIST incident response.

## Source 5 — NIST AI Risk Management Framework Core

Source: <https://airc.nist.gov/airmf-resources/airmf/5-sec-core/>

Date: AI RMF 1.0 (2023) excerpt; page accessed 2026-08-13; page states a revised version is in progress.

Authority: NIST AI Resource Center.

Claim: AI RMF Core organizes risk-management activities into Govern, Map, Measure, and Manage. Governance is cross-cutting and continuous across the AI lifecycle; the Core includes documented policies, roles/accountability, ongoing monitoring and periodic review, incident identification and information sharing, third-party contingency processes, and risk management based on organizational tolerance.

Scope: AI system risk management across design, development, deployment, evaluation, acquisition, monitoring, and retirement.

Transformation: AI RMF already covers much of proposed governance lifecycle structure, including ongoing monitoring, incidents, uncertainty/risk mapping, measurement, management, accountability, and documentation. A Zero-Day Governance prototype therefore needs explicit sufficiency tests: if the same event can be represented by existing Govern/Map/Measure/Manage and incident-response records, the proposed concept is an extension or synthesis rather than a distinct capability.

## Source 6 — CMU/SEI CERT-RMM Incident Management and Control

Source: <https://www.sei.cmu.edu/library/incident-management-and-control-imc-cert-rmm-process-area/>

Date: book chapter published February 14, 2016.

Authority: Carnegie Mellon University Software Engineering Institute; CERT Resilience Management Model process area.

Claim: the process area establishes processes to identify and analyze events, detect incidents, and determine an appropriate organizational response. It is explicitly a resilience/process-improvement practice.

Scope: operational resilience and incident management/control within CERT-RMM.

Transformation: this directly overlaps `CAPTURE → CHARACTERIZATION → CONTAINMENT/CONTROL → RESPONSE` and weakens the distinct-concept hypothesis. It supports a possible reusable event/unknown-state schema only if that schema links heterogeneous governance anomalies to existing incident/resilience controls without duplicating their lifecycle.

## Source 7 — SANS Zero-Day Exploit glossary

Source: <https://www.sans.org/security-resources/glossary-of-terms/zero-day-exploit>

Date: page accessed 2026-08-13; page does not show a publication date in the extracted content.

Authority: SANS Institute security terminology resource; used here for the cybersecurity collision boundary, not as a universal governance authority.

Claim: a zero-day exploit is a cyberattack exploiting a software, hardware, or firmware vulnerability unknown to the vendor or public, before developers have had prior knowledge or time to fix it. The page describes discovery, weaponization, deployment, exploitation, detection, and mitigation within cybersecurity.

Scope: cybersecurity vulnerabilities and exploits.

Transformation: this establishes why `ZERO_DAY_GOVERNANCE != ZERO_DAY_EXPLOIT_PREVENTION`. The proposed research concept uses “zero-day” metaphorically for previously unmodeled governance failure modes and must not claim immunity from zero-day vulnerabilities, cybersecurity prevention, or exploit detection.

## Terminology collision update

An exact-phrase search returned a small number of recent commercial/social uses of “zero-day governance,” mostly in cybersecurity or AI-agent vulnerability contexts, but no authoritative source establishing a stable cross-domain definition. This is evidence of terminology collision risk, not evidence of novelty. The exact-term classification remains `NOT_ESTABLISHED` and requires scope-limited interpretation.
