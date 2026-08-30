# Examples

The repository's primary runnable example is the standalone [`../examples/evidence_interop_export.py`](../examples/evidence_interop_export.py). It imports the real `aion_evidence_interop.build_bundle` surface, binds the exact Git head, decodes the returned bytes, and prints the deterministic `interop-manifest.json` content.

```powershell
python .\examples\evidence_interop_export.py --root .
```

- [`QUICKSTART.md`](QUICKSTART.md): install, run the output-writing CLI, and inspect its separate stdout and manifest-boundary contracts.
- `components/aion_evidence_interop_v0.1.0/tests`: executable accepted/rejected evidence-input examples.
- `examples/bazi-capability_v0.1.1`: a separately packaged bounded domain example; read its local README and non-claims first.
- `examples/classical-western-astrology_v0.1.0`: a synthetic-only classical Western astrology fact-derivation example using the traditional seven planets, tropical zodiac, whole-sign houses, classical aspects, sect, and major sign dignities. It performs no interpretation or prediction.

Examples are not scientific demonstrations. They preserve `CANONICAL_EFFECT = NONE` and `DEPLOYMENT = FALSE` unless an independently governed action says otherwise.
