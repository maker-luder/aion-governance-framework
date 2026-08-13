# External Evidence Normalization Adversarial v0.1.0

Status: `RESEARCH_ONLY / METADATA_ONLY / MODEL_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a public external evidence report be admitted for bounded review without allowing its declared execution mode, branch, actor label, digest, result claim, or report identifier to silently become an independent replication result or a governance/canonical effect?

This unit extends `external-evidence-normalization_v0.1.0` rather than duplicating its normalizer. The base module distinguishes `STATIC_REVIEW`, `LOGICAL_REPRODUCTION`, `EXECUTED_REPLICATION`, and `UNKNOWN`, and checks digest, fixture, evidence, and public-search trace metadata. The adversarial wrapper adds report-ID deduplication, expected research-branch scope, main-branch blocking, unresolved actor handling, unknown-mode digest handling, result-observation consistency, non-empty executed-result claims, and explicit mapping of base normalizer rejection/hold states.

## Decision layers

The base normalizer runs first. The adversarial audit then checks whether the report is in the expected research branch, whether its identifier is already known, whether its actor kind is unresolved, whether an unknown execution class carries execution digests, whether an executed result is claimed without an observation flag, and whether a static/logical report is presented with an observed result. Constructor-level checks continue to reject non-SHA baseline references and main/canonical effects.

A report that reaches `ACCEPT_EXECUTED_REPLICATION` is still only `ADMITTED_FOR_REVIEW` by this wrapper. The wrapper never promotes evidence, certifies an independent replication, or writes governance/canonical state. Every output preserves `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, `DEPLOYMENT=FALSE`, `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`, and `OBSERVED_RESULT=NOT_EVALUATED`.

## Results

The corrected suite passed **16 pytest tests** and **13 synthetic cases**. Cases covered static review, logical reproduction, executed replication without/with observation, duplicate report ID, branch mismatch, main branch, unresolved actor, unknown execution mode with/without digest, empty executed claim, static observation overreach, and static pass-hash masquerading.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Static review or logical reproduction | `ADMITTED_FOR_REVIEW` | Review metadata only; not replication eligible |
| Complete executed packet without observation | `HOLD` | A result claim cannot stand without an observed-result boundary |
| Complete executed packet with observation flag | `ADMITTED_FOR_REVIEW` | Base eligibility is preserved but no promotion follows |
| Duplicate report ID (`DUPLICATE_REPORT_ID`) | `INVALID` | Reuse is not new evidence |
| Branch scope mismatch | `HOLD` | Evidence is outside the declared research scope |
| Main-branch report | `INVALID` | Research evidence cannot use main as a promotion path |
| Unknown actor or unknown execution mode | `HOLD` | Identity/class uncertainty is retained |
| Static/logical observed-result overreach | `INVALID` | Observation cannot exceed declared mode |
| Base normalizer rejection | `INVALID` | Static review cannot masquerade as executed replication |

## Falsifiers

The mechanism would be falsified if it accepted a duplicate report identifier as new evidence, treated a main-branch report as a valid research input, allowed unresolved actor identity to pass as authoritative, accepted execution digests under an unknown mode, admitted an executed result claim without the declared observation boundary, accepted a static/logical report with an observed result, bypassed base normalizer rejection, or emitted a governance/canonical/deployment effect.

The wrapper's `ADMITTED_FOR_REVIEW` status is not evidence truth, independent replication, causal effect, source authority, identity verification, subjectivity, consciousness, AION/Astra equivalence, or deployment readiness. Currentness and deduplication are not inferred from a report's existence; they require separate provenance/currentness records and are not duplicated here.

## Evidence reuse and provenance

The base external-evidence normalization module is reused by stable repository path and source-state reference. Its accepted execution packet is used as a mechanism input, not as a new replication result. The 13 synthetic fixtures are not external evidence, and repeated report IDs intentionally test duplicate handling rather than replication.

## Explicit non-claims

```text
ADMITTED_FOR_REVIEW != EVIDENCE_PROMOTED
REPLICATION_ELIGIBLE != REPLICATION_EXECUTED
REPORT_EXISTS != RESULT_OBSERVED
DIGEST_PRESENT != DIGEST_TRUTH
ACTOR_LABEL != IDENTITY_VERIFICATION
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The runtime implementation uses the Python standard library plus the repository's existing normalizer source path for clean-room composition. It does not call external services, read private data, execute a model, modify `main`, write canonical state, or deploy.

## Reproduction

```bash
PYTHONPATH=src:../external-evidence-normalization_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../external-evidence-normalization_v0.1.0/src python scripts/run_external_evidence_adversarial.py --output fixtures/external_evidence_adversarial_result.json
PYTHONPATH=src:../external-evidence-normalization_v0.1.0/src python scripts/validate_fixture.py fixtures/external_evidence_adversarial_result.json
```

## References

The implementation reuses repository evidence from `external-evidence-normalization_v0.1.0` by stable path. Its existing external-source crosswalk remains methodological context; no external source code or runtime dependency is copied into this unit.
