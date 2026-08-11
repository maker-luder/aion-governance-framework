# Local Validation — Trajectory Evaluation v0.1.0

Executed before research-branch materialization:

```text
PYTHONPATH=src python -m pytest -q
14 passed

PYTHONPATH=src python -m compileall -q src
PASS

PYTHONPATH=src python scripts/run_demo.py
same_final_output = True
same_recorded_path = False
causal_claim = NOT_ESTABLISHED
canonical_effect = NONE
```

The execution environment emitted an unrelated spreadsheet-runtime warmup warning on stderr, but validation commands returned exit code 0; this module does not use that spreadsheet runtime.
