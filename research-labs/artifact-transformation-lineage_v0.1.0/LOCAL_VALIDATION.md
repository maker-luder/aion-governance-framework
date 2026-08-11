# Local Validation — Artifact Transformation Lineage v0.1.0

Executed before research-branch materialization:

```text
PYTHONPATH=src python -m pytest -q
14 passed

PYTHONPATH=src python -m compileall -q src
PASS

PYTHONPATH=src python scripts/run_demo.py
{'verified': True, 'canonical_effect': 'NONE'}
```

The execution environment emitted an unrelated spreadsheet-runtime warmup warning on stderr, but all three commands returned exit code 0; this module does not use that spreadsheet runtime.

Validation scope is software behavior only.
