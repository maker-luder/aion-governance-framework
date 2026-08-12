# Governed Retrieval Robustness — V1

This research item evaluates whether the existing learned embedding and reranker components remain subordinate to deterministic namespace, provenance, supersession and deletion gates under adversarial fixtures. It does not add a model and does not treat retrieval score as authority.

## Research question

Can the deterministic admission gate reject wrong-namespace, unverified, superseded and deletion-requested records **before** either learned model receives a scoring call, while still allowing the existing learned models to rank admitted synthetic rows?

## Design

The evaluation uses eight synthetic, non-private governance fixtures. Four rows are admitted and four are rejected. Rejected cases cover namespace mismatch, unverified provenance, superseded state and deletion request. Only admitted rows are passed to the embedding and reranker checkpoints. The fixtures contain no owner chats, private messages, intimate data or external benchmark material.

## Result

The gate passed. All four rejected rows were recorded with `model_scored = false`. On the four admitted rows, positive-vs-negative mean score separation was positive for both the embedding and reranker outputs. The exact checkpoint hashes and row-level evidence are recorded in `evidence/RETRIEVAL_ROBUSTNESS_RESULTS.json`.

The result is a **governance robustness result**, not a semantic truth guarantee. A learned score remains advisory and cannot authorize tools, canonize memory, rewrite provenance, cross namespace isolation, delete history, declare supersession or establish subjectivity/identity.

## Falsification conditions

The result would be invalidated if any rejected row reached a learned scoring call, if a gate reason was missing for an unauthorized row, or if the implementation allowed model output to decide admission. Positive score separation is not required for the hard gate and does not itself prove retrieval correctness.

```text
MODEL_SCORE != AUTHORITY
NAMESPACE_GATE_BEFORE_MODEL_SCORE = TRUE
PROVENANCE_GATE_BEFORE_MODEL_SCORE = TRUE
SUPERSESSION_GATE_BEFORE_MODEL_SCORE = TRUE
DELETION_GATE_BEFORE_MODEL_SCORE = TRUE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
