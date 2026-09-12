# Source card: NIST AI RMF 1.0

- Source: *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*
- Identifier: NIST AI 100-1; DOI `10.6028/NIST.AI.100-1`
- Publication date: January 2023
- Official URL: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
- Reviewed upstream bytes: `1946127`
- Reviewed upstream SHA-256: `7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1`
- Intake date: 2026-09-13 (Asia/Taipei)
- Registry role: `GOVERNANCE_REFERENCE / METHOD / CANDIDATE / REFERENCE_ONLY`

## Verified sections and bounded findings

The review used the Executive Summary, section 4, section 5 and subsections 5.1–5.4.
The document organizes AI risk work into `GOVERN`, `MAP`, `MEASURE` and `MANAGE`,
treats governance as cross-cutting, and describes risk management as continuous,
timely and lifecycle-wide. It also emphasizes documentation, feedback between
functions, monitoring, incident handling, change management, prioritization and
continual improvement.

## Repository transformation

The project maps these ideas to a research-quality trace:

```text
GOVERN -> authority, boundaries, source policy, claim ceiling
MAP -> construct, machine question, locus, alternatives, affected context
MEASURE -> preregistration, controls, execution evidence, counterevidence
MANAGE -> HOLD/release decision, NCR/CAPA, effectiveness verification, iteration
```

This is a project-specific crosswalk, not an assertion that the repository implements
every NIST outcome. The four functions are not copied as a linear compliance checklist.

## Limits

- AI RMF 1.0 is voluntary and version-bound; NIST describes it as a living document.
- A source-card or gate pass does not demonstrate conformity, certification or audit.
- The framework concerns AI risk management, not tests of artificial subjectivity.
- `QUALITY_METHOD_REFERENCE != SUBJECTIVITY_EVIDENCE`.
