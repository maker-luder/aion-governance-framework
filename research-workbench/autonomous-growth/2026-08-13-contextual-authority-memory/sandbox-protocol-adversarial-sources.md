# External-Agent Sandbox Protocol Adversarial — Source Notes

## Unit boundary

`external-agent-sandbox-protocol-adversarial_v0.1.0` is a research-only policy/candidate metadata audit. It does not start an external agent, transmit a capsule, access credentials/private memory, create a sandbox repository, schedule a worker, or grant repository authority.

## Reused repository evidence

| Source item | Stable reference | Source kind | Status | Transformation |
|---|---|---|---|---|
| Existing sandbox policy and preflight | `repo:research-labs/external-agent-sandbox-protocol_v0.1.0/src/aion_external_agent_sandbox/core.py` | Repository Evidence | Current within verified research lineage at the unit commit; exact state is bounded by QA receipt | Reused policy fields, base preflight reasons, candidate quarantine/retain/reject states, and claim-lock boundary; no external run was repeated or counted as new evidence |
| Existing protocol policy JSON and README | `repo:research-labs/external-agent-sandbox-protocol_v0.1.0/protocol/sandbox_policy_v0.1.0.json` and `README.md` | Repository Evidence | Current within branch lineage; pilot details remain historical repository records | Added placeholder model, provider/model role, candidate ID/set, self-reported pass, adoption, deletion, and noninterference adversarial checks |
| Current remote main reference | `git:origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Tool Output / Repository Evidence | Independently verified by read-only fetch at the latest successful checkpoint | Read-only branch-state reference; no main content or authority modified |

## Synthetic transformation

The audit maps policy/candidate metadata to `ADMITTED_FOR_REVIEW`, `HOLD`, or `INVALID`. `ADMITTED_FOR_REVIEW` does not authorize an external-agent run. Candidate retention is not adoption, and a self-reported pass without verification references remains held. The 19 synthetic cases are fixtures, not external evidence and not replication evidence.

## Provenance vocabulary

```text
PREFLIGHT_READY != EXTERNAL_AGENT_EXECUTED
AGENT_OUTPUT != VERIFIED_EVIDENCE
AGENT_SELF_REPORTED_PASS != VERIFIED_PASS
SANDBOX_RESULT != AION_RESULT
RETAINED_RESULT != ADOPTED_RESULT
MULTIPLE_AGENT_AGREEMENT != INDEPENDENT_TRUTH
DUPLICATION != REPLICATION
```

## Non-promotion invariants

```text
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
