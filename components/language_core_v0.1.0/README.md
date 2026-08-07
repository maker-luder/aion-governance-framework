# Astra Language Core Research Lab Candidate v0.1.0

Offline-first research infrastructure for registering, comparing, and auditing
candidate language-model bases beneath AION／Astra. This component is a research
subsystem; it is not AION, Astra identity, AION Runtime, a model download tool,
or a weight-modification pipeline.

## Layering

- **AION／Astra** is the owner-governed research project and agent architecture.
- **Astra Language Core Research Lab** manages experimental model candidates.
- **Qwen, Llama, and Breeze** are examples of upstream model families.
- **Ollama** is a local runtime interface, not a model family.
- **HF, GGUF, and LoRA adapters** are distinct distribution/storage layers.
- **LoRA** is a detachable low-rank update; it is not ablation.
- **Ablation** is a controlled weakening/removal experiment and is not performed here.

The original base node is permanently read-only. Experimental nodes remain
`EXPERIMENTAL / QA_HOLD / canonical_effect=NONE` until explicit human approval.
No experiment is automatically connected to production memory, tools, canonical
documents, or deployment.

The two reported 4B side-effect observations and the single paired Traditional/
Simplified Chinese observation are preliminary internal observations only. They
do not establish causality or a general rule about any upstream family or all 4B models.

Configuration examples use JSON-compatible YAML, which is valid YAML 1.2 and can
be parsed without adding a runtime dependency. Local paths belong in ignored
`local*.yaml` files.

## Safe verification

```text
python -m pytest
python -m pytest --cov --cov-branch
python -m mypy src
python -m ruff check src tests
python -m astra_language_core.cli --help
python -m astra_language_core.cli validate-dataset --path data/astra_language_core/prompts/zh_tw_zh_cn_pairs.jsonl
```

Status: `IMPLEMENTED_CANDIDATE / QA_HOLD`  
Canonical effect: `NONE`

