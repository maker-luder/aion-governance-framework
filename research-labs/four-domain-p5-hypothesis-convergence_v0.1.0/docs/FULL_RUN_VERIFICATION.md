# P5 Full-Run Verification

Date: 2026-08-09
Scope: `research-labs/four-domain-p5-hypothesis-convergence_v0.1.0`
Effect: research branch only

## Test suite

```text
python -m pytest -q
10 passed
```

## Compile verification

```text
python -m compileall -q src scripts
PASS
```

## Deterministic full demo

```text
python scripts/run_full_demo.py
```

Observed output:

```json
{"disagreement_class":"STRUCTURED_DISAGREEMENT","evidence_overlap":0.3333333333333333,"falsification_decision":"NOT_TRIGGERED","hypothesis_state":"TESTING","main_effect":"NONE","p6_gate":"HOLD_STAGE_CAP","replication_decision":"DIVERGENT","research_status":"REVIEW_READY"}
```

## What the demo proves

The synthetic P5 flow can:

1. register a formal hypothesis with preregistered falsification criteria;
2. record testing state without silently resolving the hypothesis;
3. compare conflicting agent positions;
4. register clean but divergent replication outputs;
5. evaluate a falsification criterion separately from lifecycle state;
6. apply the Human Owner P5 stage cap;
7. reject progression to P6;
8. return the research workbench to `REVIEW_READY`;
9. preserve `main_effect = NONE`.

This is engineering verification of the research harness, not evidence for subjectivity,
consciousness, identity continuity or truth of any research hypothesis.
