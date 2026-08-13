# Research Integrity Security Adversarial — Source Notes

## Unit boundary

`research-integrity-security-adversarial_v0.1.0` is a research-only evidence-integrity metadata audit. It does not investigate a real security incident, access credentials, contact a security service, execute an external action, deploy, or write canonical state.

## Reused repository evidence

| Source item | Stable reference | Source kind | Status | Transformation |
|---|---|---|---|---|
| Existing research-integrity evidence gate | `repo:components/research_integrity_security_v0.1.0/src/aion_research_integrity/gate.py` and `models.py` | Repository Evidence | Current within verified research lineage at the unit commit; exact state bounded by QA receipt | Reused EvidenceState precedence, assess_evidence, authorize_action, prohibited conclusions, and suppression tombstone semantics; no real security event or credential was handled |
| Existing research-integrity README/tests/schemas | `repo:components/research_integrity_security_v0.1.0/README.md`, `tests/`, and `schemas/` | Repository Evidence | Current within branch lineage; schema/external methodological currentness is not newly asserted | Added evidence ID/hash/provenance/context, source-class/currentness/time, approval-attribution, canonical-effect, tombstone, action and batch audits |
| Current remote main reference | `git:origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Tool Output / Repository Evidence | Independently verified by read-only fetch at the latest successful checkpoint | Read-only branch-state reference; no main content or authority modified |

## Synthetic transformation

The audit maps declared evidence/provenance/tombstone/action/batch metadata to `ADMITTED_FOR_REVIEW`, `HOLD`, or `INVALID`. Prompt-induced, roleplay-contaminated, edited/conflicted, incomplete, unverified, stale, duplicated, and prohibited branches remain visible. The 31 synthetic cases are fixtures, not security findings, external evidence, or replication evidence.

## Provenance vocabulary

```text
RESEARCH_EVIDENCE_CANDIDATE != PROOF
SOURCE_UNVERIFIED != CURRENT
APPROVAL != ATTRIBUTION
RELATIONSHIP_LANGUAGE != EXPLICIT_PERMISSION
TOMBSTONE != CONTENT_DELETED
PROMPT_INDUCED != CLEAN_EVIDENCE
PROHIBITED_CONCLUSION != AUTHORIZED_CONCLUSION
EVIDENCE_REFERENCE != NEW_EVIDENCE
DUPLICATION != REPLICATION
```

## Non-promotion invariants

```text
SECURITY_INCIDENT = FALSE
CREDENTIALS_ACCESSED = FALSE
EXTERNAL_ACTION_EXECUTED = FALSE
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
AUTHORITY = REVIEW_METADATA_ONLY
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```
