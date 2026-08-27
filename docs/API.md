# Current Programmatic Interfaces

This repository has no repository-wide stable Python API. The interfaces below are explicitly classified to avoid promoting internal implementation details to stable contracts.

| Interface | Status | Purpose | Side effects and boundaries |
|---|---|---|---|
| `aion_evidence_interop.build_bundle(root, record, expected_head=...)` | `SUPPORTED_PUBLIC` | Build deterministic inspection-only JSON interoperability views from an existing evidence record. | Writes only when its caller invokes `write_bundle`; no network/model execution; canonical effect `NONE`. |
| `aion_evidence_interop.validate_source_record(record, expected_head=...)` | `SUPPORTED_PUBLIC` | Validate source evidence before export. | Validation only; rejects incompatible records. |
| `aion-evidence-interop` / `python -m aion_evidence_interop.cli` | `SUPPORTED_PUBLIC` | CLI export path described in [`QUICKSTART.md`](QUICKSTART.md). | JSON result on stdout; output path is explicit; inspection-only. |
| `aion_astra_inquiry.AutonomousInquiryCampaign` and `aion-astra-inquiry` | `EXPERIMENTAL` | Run a bounded repository inquiry campaign. | Writes reports only outside the repository root; network stays off unless `--external-web` is explicitly supplied; no canonical or deployment authority. |
| Component-local `__init__.py` exports outside these two surfaces | `INTERNAL` or `EXPERIMENTAL` | Research and governed-runtime implementation. | Consult the component-local README and tests; no stability promise from importability. |

## Minimal export example

```python
from pathlib import Path
from aion_evidence_interop import build_bundle

bundle = build_bundle(
    Path('.'),
    Path('components/aion_evidence_interop_v0.1.0/fixtures/valid_minimal.json'),
    expected_head='YOUR_EXACT_GIT_HEAD',
)
assert bundle['interop-manifest.json']
```

`build_bundle` returns `dict[str, str]`: artifact names mapped to deterministic JSON/JSONL text. Use `aion_evidence_interop.manifest.write_bundle(output, bundle)` only with an intended external output directory.

`SUPPORTED_PUBLIC` means a currently documented compatibility surface, not a release-stability guarantee. `PUBLIC_API != STABILITY_GUARANTEE`.
