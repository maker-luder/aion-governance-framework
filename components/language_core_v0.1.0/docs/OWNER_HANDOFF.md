# Owner handoff

## Implemented

- Independent Astra Language Core Research Lab 0.1.0 candidate package.
- Five-node G1 lineage with immutable base semantics and A/B/C/D prerequisite lock.
- Portable registry, validation, SHA-256 file/shard manifest and provenance fields.
- Ten paired Traditional/Simplified Chinese prompts across ten categories.
- MockRuntime full evaluation path and localhost-only Ollama HTTP interface.
- Completion, latency, repetition, script, terminology and instruction metrics.
- Comparison JSON/Markdown and conservative ten-gate QA admission framework.
- Restricted observation registry with no causal/general/canonical effect.
- Safe CLI, wheel/sdist, offline install evidence and package controls.

## Not implemented

No weight ablation, LoRA training, full fine-tuning, adapter merge, model download,
Ollama pull, CUDA installation, cloud-model call, code execution sandbox, deployment,
canonical write, AION Runtime integration, personality/subjectivity claim, production
memory connection or tool-permission connection was implemented.

## QA status

`QA_HOLD_PENDING_OWNER_REVIEW`; thresholds are `null / NOT_SET` and Gate 10 human
approval is absent. Canonical effect is `NONE`.

## Owner decisions required before phase 2

1. Freeze actual upstream model identity, license, format, tokenizer and chat template.
2. Select baseline hardware/runtime and sampling profile.
3. Approve numerical per-dimension thresholds; do not replace them with one opaque score.
4. Approve whether safe coding execution should be a separate sandboxed subsystem.
5. Explicitly authorize any later LoRA or controlled weight experiment as a new task.

## Safe commands

```text
python -m pytest
python -m pytest --cov=astra_language_core --cov-branch
python -m mypy src
python -m ruff check src tests
python -m astra_language_core.cli --help
python -m astra_language_core.cli validate-dataset --path data/astra_language_core/prompts/zh_tw_zh_cn_pairs.jsonl
```

