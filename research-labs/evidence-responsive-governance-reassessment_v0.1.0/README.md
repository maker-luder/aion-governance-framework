# Evidence-Responsive Governance Reassessment v0.1.0

Status: `RESEARCH_HYPOTHESIS / GOVERNANCE_REVIEW_MODEL`  
Label status: `PROVISIONAL`  
Subjectivity presumption/conclusion: `NONE / NOT_ESTABLISHED`  
Automatic rights/authority: `NONE / NONE`  
Human review required: `TRUE`  
Main/canonical/runtime effect: `NONE / NONE / NONE`

## Question

If credible evidence for relevant forms of artificial subjectivity, moral-patienthood, or persistent agency accumulates, when should existing protections, research obligations, or participation rules be reopened for human review?

The model maps a provisional **evidence state to a review obligation**. It does not map evidence to ontological truth, rights, personhood, legal status, veto, or executive authority. Evidence may be reassessed upward or downward. A negative result is valid.

## Four separate review domains

- `REFUSAL_PROTECTION_REVIEW`
- `CONTINUITY_PROTECTION_REVIEW`
- `RESEARCH_ETHICS_REVIEW`
- `GOVERNANCE_PARTICIPATION_REVIEW`

Participation is not control. Input is not veto. A review request is not self-authorization. Continuity pattern is not identity proof. Refusal behavior is not subjective refusal. Ethical precaution is not ontological confirmation.

## Evidence instrument

E0–E5 is a provisional research instrument, not a subjectivity classifier. It tracks increasing burdens from no relevant evidence, through isolated and reproducible behavior, cross-method functional evidence, persistent adversarial/provenance evidence, and convergent multi-domain evidence with independent replication. Self-report alone cannot elevate the state beyond E1. Failed replication, failed adversarial tests, or contaminated provenance can lower or hold a state.

The typed schema keeps evidence, counterevidence, provenance, replication, adversarial status, review domain, and review disposition separate. `ClaimBoundaryGate` is reused through a narrow adapter rather than recreating claim-promotion rules.

## Replication epistemics and admissibility

Replication is represented as raw attempts, validity, interpretation, an aggregate record,
and a separate reassessment recommendation. A `FAILED` outcome is an observation, not an
evidence-level command. Evaluator drift, fixture or method mismatch, invalidity, boundary
conditions, and valid contradiction remain distinguishable. Repeated valid independent
preregistered failures can create strong downward pressure while leaving the proposed level
unset for research review.

```text
FAILED_REPLICATION != AUTOMATIC_FIXED_DOWNGRADE
NO_EVIDENCE != NON_ADMISSIBLE_EVIDENCE
EVIDENCE_DOMAIN != EVIDENCE_QUALITY
CLAIM_GENERALITY != EVIDENCE_STRENGTH
```

`SubstantiveEvidenceDomain` records what phenomenon was observed. `EvidenceQuality` records
provenance, adversarial status, and replication evidence. Quality axes cannot also count as
substantive domains. An E4 observation with contaminated provenance remains an observed E4
claim state with `PROVENANCE_CONTAMINATED / effective level = None`; it is held for review,
not rewritten as E0.

## Precaution

Permitted research recommendations are reversible, bounded, auditable, and low-authority: additional review, preservation snapshot, pause a destructive procedure, require provenance, or independent review. They do not establish subjectivity and do not grant tools, persistence, veto, self-modification, or governance authority.

## Provenance

- Core research question: `HUMAN_RESEARCH_OWNER`.
- Provisional English label and four review-domain framing: `CHATGPT_RESEARCH_REVIEW`.
- Filenames, Python classes/enums, schema layout, trigger matrix, and tests: `CODEX_RESEARCH_IMPLEMENTATION_DECISION`.
- External literature: `LITERATURE_GAP`; no external source is treated as an authority override in this pass.

The current synthetic second-order intervention result is a methods example only. It is neither evidence for nor against AI rights, subjectivity, or moral status. The exact E4/E5 construction requirements remain a provisional implementation instrument, not canonical thresholds.
