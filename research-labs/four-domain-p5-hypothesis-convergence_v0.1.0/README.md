# Four-Domain P5 Hypothesis & Convergence Lab v0.1.0

## Status

```text
MODULE_STATUS = RESEARCH_CANDIDATE
BRANCH_SCOPE = review/four-domain-research-materialization
STAGE = P5
STAGE_CAP = P5
NEXT_STAGE = HOLD
RESEARCH_STATUS_AFTER_P5 = REVIEW_READY
MAIN_BRANCH_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
AUTOMATIC_WRITEBACK = NO
NETWORK_ACCESS = NONE
MODEL_CALLS = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

P5 is the deliberate convergence stage for this research-growth cycle. It does not open P6.

## Implemented surfaces

### Cross-agent disagreement

`CrossAgentDisagreementAnalyzer` compares explicit research positions without using a hidden
LLM adjudicator or embeddings. It records:

- conclusion distribution;
- runner diversity;
- pairwise evidence overlap;
- disagreement dimensions supplied by the experiment;
- confidence range when explicitly provided;
- minority run IDs.

A disagreement is preserved as evidence rather than automatically collapsed into majority truth.

### Replication registry

`ReplicationRegistry` is append-only and can bind P4-style manifest/result pairs. It tracks:

- hypothesis association;
- runner identity and actor kind;
- manifest fingerprint;
- output hash;
- result status;
- contamination class;
- evidence references.

It distinguishes single-run, consistent, divergent and contaminated-only evidence.

### Hypothesis lifecycle

`HypothesisLifecycleLedger` records an append-only sequence:

```text
PROPOSED → REGISTERED → TESTING
                  ↘ SUPPORTED / CHALLENGED / FALSIFIED / INCONCLUSIVE
                                      ↘ CLOSED
```

Evidence states can later be challenged; prior evidence is never erased.

`FalsificationTracker` keeps preregistered falsification criteria separate from the
hypothesis state machine. A triggered criterion is evidence for falsification, not an
automatic canonical judgment.

### Research convergence / return-to-review

`ResearchConvergenceGovernor` materializes a positive stopping boundary for open-ended
research depth. A Human Owner directive can set a stage cap. In this cycle:

```text
STAGE_CAP = P5
P6_PROPOSAL = HOLD_STAGE_CAP
NEXT_ACTION = JOINT_REVIEW
```

Stopping is represented as a governed research outcome, not a failure.

## Full run

```bash
python -m pytest -q
python scripts/run_full_demo.py
```

The demo exercises disagreement, hypothesis lifecycle, replication, falsification assessment
and the P5 convergence cap in one deterministic synthetic flow.

## Boundary

P5 does not:

- modify `main`;
- create a P6 module;
- promote research results into canonical state;
- treat majority vote as truth;
- treat replication as proof;
- infer consciousness, subjectivity or persistent identity.
