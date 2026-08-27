# Current Programmatic Interfaces

This repository has no repository-wide stable Python API. The interfaces below are explicitly classified to avoid promoting internal implementation details to stable contracts.

| Interface | Status | Purpose | Inputs / outputs and boundaries |
|---|---|---|---|
| `aion_evidence_interop.build_bundle(root, record_path, *, expected_head)` | `SUPPORTED_PUBLIC` | Build deterministic inspection-only interoperability views from an existing evidence record. | Inputs: repository `Path`, repository-local record `Path`, exact 40-hex head. Returns `dict[str, bytes]`: artifact paths mapped to UTF-8 JSON/JSONL bytes. It does not write by itself; `write_bundle` is the explicit writer. No network/model execution; canonical effect `NONE`. |
| `aion_evidence_interop.validate_source_record(root, record_path, *, expected_head)` | `SUPPORTED_PUBLIC` | Validate source evidence before export. | Returns `tuple[dict[str, Any], SourceValidation]`: parsed record plus validation metadata. Validation only; incompatible records fail closed. |
| `aion-evidence-interop` / `python -m aion_evidence_interop.cli` | `SUPPORTED_PUBLIC` | CLI export path described in [`QUICKSTART.md`](QUICKSTART.md). | JSON status on stdout; explicit output path; inspection-only. |
| `aion_astra_inquiry.AutonomousInquiryCampaign` and `aion-astra-inquiry` | `EXPERIMENTAL` | Run a bounded repository inquiry campaign. | Writes reports only outside repository root; network stays off unless `--external-web` is explicitly supplied; no canonical or deployment authority. |
| Component-local `__init__.py` exports outside these two surfaces | `INTERNAL` or `EXPERIMENTAL` | Research and governed-runtime implementation. | Consult component-local README/tests; importability does not create a stability promise. |

## Minimal export example

[`../examples/evidence_interop_export.py`](../examples/evidence_interop_export.py) is a directly executable example using the exact interface above. The essential call is:

```python
bundle = build_bundle(
    root,
    record_path,
    expected_head=exact_head,
)
manifest = bundle["interop-manifest.json"].decode("utf-8")
```

`SUPPORTED_PUBLIC` means a currently documented compatibility surface, not a release-stability guarantee. `PUBLIC_API != STABILITY_GUARANTEE`.
