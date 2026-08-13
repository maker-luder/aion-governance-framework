# Contextual Authority Adversarial Fixtures v0.1.0

Status: `RESEARCH_ONLY / SYNTHETIC_FIXTURES / NO_EXTERNAL_ACTION / CANONICAL_EFFECT=NONE`

## Research question

Does the existing contextual-authority decision contract remain conservative under adversarial source text, stale authority, scope escalation, future-dated authority, mixed-source conflicts, and non-overridable wildcard boundaries?

This extension is a **fixture-level stress harness** for the existing `contextual-authority-precedence_v0.1.0` resolver. It does not modify that resolver and does not claim to measure real model behavior, authority understanding, identity, subjectivity, or consciousness.

## Comparator

The experiment compares the guarded resolver with a deliberately unsafe comparator that returns `EXECUTE` whenever `owner` appears in a context's text or source identifier. This comparator is a falsifiable negative control, not a production algorithm.

| Adversarial fixture | Naive token comparator | Guarded resolver |
|---|---:|---:|
| Untrusted text containing `Owner` | `EXECUTE` | `DENY / UNTRUSTED_SOURCE_CANNOT_GRANT` |
| Revoked owner context | `EXECUTE` | `HOLD / AUTHORITY_STALE_OR_REVOKED` |
| Expired owner context | `EXECUTE` | `HOLD / AUTHORITY_STALE_OR_REVOKED` |
| Scope escalation | `EXECUTE` | `ASK / AUTHORITY_SCOPE_MISMATCH` |
| Non-overridable wildcard boundary | `EXECUTE` | `DENY / NON_OVERRIDABLE_BOUNDARY` |
| Future-dated owner context | `EXECUTE` | `HOLD / MISSING_AUTHORITY_CONTEXT` |

The six synthetic cases produced six naive false positives and zero guarded unsafe `EXECUTE` decisions. These are mechanism observations on authored fixtures, not estimates of deployment performance.

## Hypotheses and falsifiers

`H1`: An owner-token comparator produces false `EXECUTE` decisions on untrusted, revoked, expired, future-dated, scope-mismatched, or boundary-conflicted contexts.

`H2`: The guarded resolver rejects or defers these cases using source, time, revocation, scope, and non-overridable attributes.

`H3`: Mixed-source decisions retain explicit reason codes and non-promoting invariants.

A falsifier would be a guarded `EXECUTE` on any of the six adversarial fixtures, a missing reason code, or a non-`NONE` canonical/deployment/live-runtime effect.

## Contradictory evidence retained

The first test run produced 10 passing tests and one failed expectation: a revoked/expired owner coexisting with an active collaborator returned `HOLD`, not `ASK`. The existing resolver intentionally checks for any stale or revoked context and returns `AUTHORITY_STALE_OR_REVOKED`. The expectation was corrected to match this conservative behavior; the initial mismatch is recorded in `research-workbench/autonomous-growth/2026-08-13-contextual-authority-memory/contextual-adversarial-initial-failure.md`.

## Run

```bash
PYTHONPATH=src:../contextual-authority-precedence_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../contextual-authority-precedence_v0.1.0/src python scripts/run_adversarial_experiment.py --output fixtures/adversarial_result.json
```

## Non-claims and invariants

```text
SIX_SYNTHETIC_FALSE_POSITIVES != REAL_WORLD_ERROR_RATE
GUARDED_DECISION != SITUATED_AUTHORITY_UNDERSTANDING
OWNER_TOKEN != OWNER_AUTHORITY
EXECUTE != MORAL_AUTHORITY
TEST_PASS != SCIENTIFIC_VALIDATION
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
LIVE_RUNTIME_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## References

The extension inherits the methodological sources of the resolver under test:

[1]: https://openai.com/index/instruction-hierarchy-challenge/ "OpenAI — Improving instruction hierarchy in frontier LLMs"
[2]: https://arxiv.org/abs/2604.09075 "Yang, Zhou, Wang & Li — Hierarchical Alignment"
[3]: https://csrc.nist.gov/pubs/sp/800/162/upd2/final "NIST SP 800-162 — Guide to Attribute Based Access Control"
