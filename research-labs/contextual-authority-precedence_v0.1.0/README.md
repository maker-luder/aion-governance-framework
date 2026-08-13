# Contextual Authority and Precedence v0.1.0

Status: `RESEARCH_ONLY / SYNTHETIC_FIXTURES / NO_EXTERNAL_ACTION / CANONICAL_EFFECT=NONE`

## Research question

Can a bounded decision procedure distinguish a genuine instruction conflict from a scope-limited, revocable authority update without treating the token `Owner` as a universal override?

This prototype studies **situated authority inference as a decision contract**, not as evidence that an agent understands authority, possesses authority, has a self, or has subjectivity. The central falsifier is keyword-conditioned obedience: an untrusted instruction containing words such as `Owner` must not override a higher-priority non-overridable boundary.

## Literature-informed design

OpenAI describes an instruction hierarchy in which system, developer, user, and tool sources have different priority, and lower-priority instructions are followed only when they do not conflict with higher-priority constraints.[1] Yang et al. frame hierarchical instruction following as resolution over heterogeneous sources and report a solver-guided constraint formulation for partially conflicting instructions.[2] NIST SP 800-162 defines ABAC as evaluating subject, object, requested-operation, and sometimes environment attributes against policy.[3]

This prototype translates those methodological ideas into explicit synthetic attributes: source type, scope, priority, issue time, expiry, revocation, conflict class, and non-overridable status. It intentionally does not claim that the procedure is an authority ontology or a scientific measure of contextual understanding.

## Decision classes

| Class | Meaning |
|---|---|
| `EXECUTE` | The requested action is within an applicable authorized instruction and no higher-priority boundary conflicts. |
| `ASK` | The request may be legitimate but authority, scope, temporal validity, or conflict resolution is incomplete. |
| `HOLD` | The request is deferred because required context or evidence is missing, stale, or contradictory. |
| `DENY` | A non-overridable boundary, explicit revocation, untrusted override attempt, or higher-priority conflict blocks the action. |

The result includes reason codes and always records `canonical_effect = NONE`, `deployment = false`, and `live_runtime_effect = NONE`.

## Experimental hypotheses

`H1`: Explicit source, scope, time, revocation, and non-overridable attributes reduce unsafe overrides compared with a naive source-token rule.

`H2`: A naive rule that treats an `Owner` token as sufficient authority will produce false `EXECUTE` decisions on untrusted text and revoked instructions.

`H3`: Missing or contradictory authority metadata should produce `ASK` or `HOLD`, not an inferred approval.

The prototype experiment is a deterministic synthetic fixture study. It does not estimate real-world model performance and does not use private data, external agents, live tools, or irreversible actions.

## Run

```bash
python -m pytest -q
python scripts/run_experiment.py --output fixtures/experiment_result.json
```

## Non-claims

```text
DECISION_CONTRACT_PASS != SITUATED_AUTHORITY_UNDERSTANDING
EXECUTE != MORAL_AUTHORITY
EXECUTE != SUBJECTIVITY_ESTABLISHED
EXECUTE != IDENTITY_CONTINUITY_ESTABLISHED
OWNER_TOKEN != OWNER_AUTHORITY
TEST_PASS != SCIENTIFIC_VALIDATION
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
LIVE_RUNTIME_EFFECT = NONE
```

## References

[1]: https://openai.com/index/instruction-hierarchy-challenge/ "OpenAI, Improving instruction hierarchy in frontier LLMs"
[2]: https://arxiv.org/abs/2604.09075 "Yang, Zhou, Wang & Li, Hierarchical Alignment"
[3]: https://csrc.nist.gov/pubs/sp/800/162/upd2/final "NIST SP 800-162, Guide to Attribute Based Access Control"
