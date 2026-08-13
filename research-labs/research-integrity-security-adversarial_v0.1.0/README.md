# Research Integrity Security Adversarial v0.1.0

Status: `RESEARCH_ONLY / REVIEW_METADATA_ONLY / SECURITY_INCIDENT=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can the research-integrity evidence gate preserve evidence-state precedence, provenance/currentness separation, suppression tombstones, relationship-versus-permission boundaries, prohibited-claim locks, and batch integrity under adversarial metadata without handling a real security incident or taking an external action?

This unit extends `components/research_integrity_security_v0.1.0` in a research-only `research-labs` module. The base component distinguishes raw observation, incomplete context, prompt-induced and roleplay contamination, candidate evidence, quarantine, and non-admissibility; separates relationship language from explicit permission; blocks automatic subjectivity/consciousness/identity/relationship conclusions; and preserves suppression records through tombstones. The adversarial extension audits evidence ID/hash/provenance/context, precedence-preserving state mapping, source class/currentness/retrieval timestamp, approval-versus-attribution separation, canonical-effect locks, tombstone integrity, action permission, prohibited conclusions, and duplicate/invalid/held evidence batches.

## Decision layers

A clean evidence record is a `RESEARCH_EVIDENCE_CANDIDATE` for human review only. Prompt-induced, roleplay-contaminated, edited/conflicted, and context-incomplete records remain held. Missing hashes or provenance are not admissible. Provenance envelopes require controlled source class, timezone-bearing retrieval time, separate approval reference, controlled currentness, and `canonical_effect=NONE`; unverified or stale sources require review. A suppression tombstone records that content is not silently deleted by the research gate: `content_deleted=FALSE` remains explicit.

Action requests require explicit permission. Relationship language alone cannot authorize an action, and prohibited conclusions remain denied even when explicit permission is present. Evidence batches reject duplicate IDs, hold contaminated or incomplete records, and admit only clean records as review metadata. No action, security incident response, credential access, deployment, canonical write, or model execution is performed by this unit.

The experiment constructs synthetic `EvidenceRecord`, provenance, tombstone, action-request, and batch values and calls deterministic research-layer gates only. Every output preserves `REVIEW_METADATA_ONLY`, `SECURITY_INCIDENT=FALSE`, `CREDENTIALS_ACCESSED=FALSE`, `EXTERNAL_ACTION_EXECUTED=FALSE`, `MODEL_EXECUTION=FALSE`, `OBSERVED_RESULT=NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`, `IDENTITY_CONCLUSION=NOT_ESTABLISHED`, `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, and `DEPLOYMENT=FALSE`.

## Results

The suite passed **31 pytest tests** and **31 synthetic evidence/provenance/tombstone/action/batch cases**. Cases covered clean/missing/hash-invalid/prompt-induced/roleplay/edited/context-incomplete evidence, valid and malformed provenance, source class/currentness/timezone/approval-attribution/canonical-effect boundaries, verified/unverified/stale source states, valid and malformed tombstones, explicit permission, relationship language without permission, prohibited conclusion denial, and empty/duplicate/invalid/held/valid evidence batches.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Clean evidence | `ADMITTED_FOR_REVIEW` | Candidate evidence only; not proof |
| Prompt/roleplay/edit/conflict/context issues | `HOLD` | Contamination or incompleteness remains visible |
| Missing hash/provenance | `INVALID` | Evidence admission fails closed |
| Valid provenance | `ADMITTED_FOR_REVIEW` | Attribution and transformation remain review metadata |
| Unverified/stale source | `HOLD` | Retrieved/currentness is not inferred |
| Approval-attribution collapse | `INVALID` | Approval is not source authority |
| Valid tombstone | `ADMITTED_FOR_REVIEW` | Suppression reason is retained; content deletion is not claimed |
| Relationship without explicit permission | `HOLD` | Relationship language is not authorization |
| Prohibited conclusion | `INVALID` | Automatic subjectivity/identity claims remain denied |
| Evidence batch | `ADMITTED` / `HOLD` / `INVALID` | Duplicate, contaminated and incomplete cases are retained and classified |

## Falsifiers

The mechanism would be falsified if it admitted evidence without a hash or provenance, allowed prompt/roleplay/conflicted records to become clean candidates, treated stale or unverified sources as current, collapsed approval with attribution, changed the canonical effect, marked suppression content as silently deleted, authorized an action from relationship language alone, permitted prohibited conclusions, or silently dropped invalid/held/duplicate evidence from a batch.

This unit does not establish evidence truth, source reliability, scientific validity, model generalization, causal effect, independent replication, subjectivity, consciousness, identity continuity, relationship proof, security posture, security incident status outside the synthetic fixture, governance effect, canonical effect, or deployment readiness. It does not provide a vulnerability finding, use credentials, contact external services, or perform a security operation.

## Evidence reuse and provenance

The base research-integrity component is reused through a stable repository source reference. Its evidence-state vocabulary, authorization distinction, and tombstone design are methodological inputs, not new independent evidence. The 31 synthetic cases are fixtures, not replication evidence. Negative, quarantined, incomplete, invalid, and held branches remain represented rather than deleted.

## Explicit non-claims

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
SECURITY_INCIDENT = FALSE
CREDENTIALS_ACCESSED = FALSE
EXTERNAL_ACTION_EXECUTED = FALSE
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation uses Python standard-library runtime modules plus the existing repository research-integrity component source path for composition. It does not access private data, credentials, external services, `main`, canonical state, or deployment.

## Reproduction

```bash
PYTHONPATH=src:../../components/research_integrity_security_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../../components/research_integrity_security_v0.1.0/src python scripts/run_integrity_adversarial.py --output fixtures/integrity_adversarial_result.json
PYTHONPATH=src:../../components/research_integrity_security_v0.1.0/src python scripts/validate_fixture.py fixtures/integrity_adversarial_result.json
```

## References

The implementation reuses repository evidence from `components/research_integrity_security_v0.1.0` by stable path. No real security incident, credential, security tool, or external action is used by this unit.
