# Local Validation — v0.1.0

Executed before research-branch materialization:

```text
PYTHONPATH=src python -m pytest -q
11 passed in 0.05s

PYTHONPATH=src python -m compileall -q src
PASS

PYTHONPATH=src python scripts/run_demo.py
{'dataset_name': 'demo', 'left_implementation': 'upper', 'right_implementation': 'identity', 'left_pass_rate': 1.0, 'right_pass_rate': 0.0, 'canonical_effect': 'NONE', 'interpretation': 'COMPARATIVE_RESEARCH_EVIDENCE_ONLY'}
```

Validation scope is software behavior only.

```text
TEST_PASS != SEMANTIC_VALIDITY
TEST_PASS != CAUSAL_VALIDITY
TEST_PASS != SUBJECTIVITY
```
