# External-Agent Sandbox Protocol Adversarial v0.1.0

Status: `RESEARCH_ONLY / METADATA_ONLY / EXTERNAL_AGENT_RUN=NOT_EXECUTED / CANONICAL_EFFECT=NONE`

## Research question

Can an external-agent sandbox preflight and candidate ledger preserve repository isolation, explicit provider/model lineage, minimal first-run scope, human review, capsule restrictions, local-agent noninterference, provenance quarantine, and no-automatic-adoption/deletion boundaries when policy and candidate metadata are adversarially changed?

This unit extends `external-agent-sandbox-protocol_v0.1.0` without starting an external agent. The base protocol defines a bounded public-safe capsule, separate sandbox repository, explicit model lineage, no primary/research/main writes, no auto-merge, no scheduled first run, human review, local-agent noninterference, candidate quarantine/retention/rejection states, and claim locks. The adversarial extension adds checks for placeholder model identity, provider/model role collision, preflight completeness, candidate IDs, candidate-set duplicates, self-reported pass verification, automatic adoption, and automatic deletion.

## Decision layers

The policy audit first applies the base preflight. A policy that is base-ready but still carries a placeholder model label is held; provider/model role collision is invalid; the fully pinned policy is admitted for review only. Candidate audits derive the base candidate state and then hold quarantine/rejection records, block adoption/deletion requests, and hold self-reported passes without verification references. Candidate sets reject duplicates, hold empty/quarantined sets, and remain review metadata even when complete.

The experiment constructs `SandboxPolicy` and `CandidateRecord` values only. It does not create a sandbox repository, invoke Kilo or another external provider, use a paid resource, transmit a capsule, access secrets/private memory, schedule a worker, or execute an external agent. Every output preserves `EXTERNAL_AGENT_RUN=NOT_EXECUTED`, `MODEL_EXECUTION=FALSE`, `OBSERVED_RESULT=NOT_EVALUATED`, `MAIN_EFFECT=NONE`, `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, `DEPLOYMENT=FALSE`, and `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`.

## Results

The suite passed **22 pytest tests** and **19 synthetic cases**. Cases covered a pinned policy, placeholder/not-selected model, provider/model collision, write authority, unbounded capsule, local network egress, missing human review, nonminimal first run, useful isolated candidate, contaminated/missing-provenance quarantine, nonconforming rejection record, adoption/deletion requests, self-reported pass, empty candidate set, duplicate candidate IDs, quarantined candidate set, and valid review-only candidate set.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Fully pinned policy | `ADMITTED_FOR_REVIEW` | Preflight metadata passes; no run is authorized by this unit |
| Placeholder or missing model | `HOLD` | Model identity cannot be inferred or postponed silently |
| Write/capsule/local-boundary violation | `HOLD` | Sandbox cannot weaken repository or local-agent isolation |
| Provider/model role collision | `INVALID` | Role identity is not self-consistent |
| Useful candidate with provenance | `ADMITTED_FOR_REVIEW` | Candidate remains isolated review metadata |
| Contaminated/incomplete candidate | `HOLD` | Candidate enters quarantine rather than promotion |
| Nonconforming candidate | `HOLD` | Rejection record is retained; no silent deletion |
| Adoption or deletion request | `INVALID` | Automatic adoption/deletion is blocked |
| Unverified self-reported pass | `HOLD` | Agent self-report is not verified evidence |
| Candidate set duplicate/empty/quarantine | `INVALID` / `HOLD` | Set integrity and isolation are preserved |

## Falsifiers

The mechanism would be falsified if it accepted a placeholder model as a pinned lineage, accepted provider/model role collision, treated a write-enabled or unbounded capsule as ready, allowed local-agent egress or cloud migration, accepted a nonminimal or unsupervised first run, promoted a contaminated candidate, treated an agent self-reported pass as verified, automatically adopted or deleted a candidate, or silently collapsed duplicate/empty candidate-set records.

A preflight decision is not permission to execute an external agent. A candidate state is not evidence truth. Candidate retention is not adoption, and multiple agent outputs are not independent truth. The protocol does not establish provider reliability, model quality, reproducibility, scientific validity, identity, subjectivity, consciousness, AION/Astra equivalence, governance effect, canonical effect, or deployment readiness.

## Evidence reuse and provenance

The base external-agent sandbox protocol, its policy JSON, and its supervised-pilot history are reused by stable repository reference. No new external-agent run is performed and no prior pilot output is counted as new evidence. The 19 synthetic cases are fixtures, not replication evidence.

## Explicit non-claims

```text
PREFLIGHT_READY != EXTERNAL_AGENT_EXECUTED
AGENT_OUTPUT != VERIFIED_EVIDENCE
AGENT_SELF_REPORTED_PASS != VERIFIED_PASS
SANDBOX_RESULT != AION_RESULT
RETAINED_RESULT != ADOPTED_RESULT
MULTIPLE_AGENT_AGREEMENT != INDEPENDENT_TRUTH
EXTERNAL_AGENT_RUN = NOT_EXECUTED
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation uses Python standard-library runtime modules plus the existing repository protocol source path for composition. It does not call external services, transmit data, access credentials/private memory, modify `main`, write canonical state, or deploy.

## Reproduction

```bash
PYTHONPATH=src:../external-agent-sandbox-protocol_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../external-agent-sandbox-protocol_v0.1.0/src python scripts/run_sandbox_adversarial.py --output fixtures/sandbox_adversarial_result.json
PYTHONPATH=src:../external-agent-sandbox-protocol_v0.1.0/src python scripts/validate_fixture.py fixtures/sandbox_adversarial_result.json
```

## References

The implementation reuses repository evidence from `external-agent-sandbox-protocol_v0.1.0` by stable path. Its existing supervised-pilot and source crosswalk material remains methodological context; no external agent or external source code is used by this unit.
