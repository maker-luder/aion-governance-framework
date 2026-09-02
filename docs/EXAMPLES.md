# Examples

The repository's primary runnable example is the standalone [`../examples/evidence_interop_export.py`](../examples/evidence_interop_export.py). It imports the real `aion_evidence_interop.build_bundle` surface, binds the exact Git head, decodes the returned bytes, and prints the deterministic `interop-manifest.json` content.

```powershell
python .\examples\evidence_interop_export.py --root .
```

- [`QUICKSTART.md`](QUICKSTART.md): install, run the output-writing CLI, and inspect its separate stdout and manifest-boundary contracts.
- `components/aion_evidence_interop_v0.1.0/tests`: executable accepted/rejected evidence-input examples.
- `examples/bazi-capability_v0.1.1`: stable CI path for the v0.2.0 bounded Bazi package, including four-pillar facts, versioned cycles, independent JDN day checks, fixed-qi term invariants, and source acquisition receipts; read its local README and non-claims first.
- `examples/classical-western-astrology_v0.1.0`: stable path for the v0.2.0 synthetic-only classical-primary Western astrology engine with a separately labelled modern outer-planet/minor-aspect/motion overlay. It performs no interpretation or prediction.
- `examples/zi-wei-dou-shu_v0.1.0`: Node 22.13+ synthetic-only Zi Wei Dou Shu adapter pinned to `iztro==2.6.0`; it emits twelve palaces, fourteen primary stars, auxiliary/decorative stars, transformations and explicit-reference temporal layers with a canonical receipt. It exposes classical-default and Zhongzhou comparison profiles while performing no interpretation or prediction.

Examples are not scientific demonstrations. They preserve `CANONICAL_EFFECT = NONE` and `DEPLOYMENT = FALSE` unless an independently governed action says otherwise.
