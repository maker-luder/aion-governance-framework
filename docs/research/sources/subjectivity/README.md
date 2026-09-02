# Core subjectivity research sources: bounded reference intake

`AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION`

Three primary source bodies and one Crossref metadata record were downloaded on
2026-09-02. The fourth paper's publisher returned HTTP 403; its full text was not
downloaded. The metadata-only scope is explicit. `DOWNLOAD_MANIFEST.json`
binds each exact payload, version, size, license and transformation. Two CC BY
texts are retained for offline review. The CC BY-NC-SA 2023 PDF is download/hash
only, with an original method card retained instead. Binary payloads belong in an
external cache, not the public text-only source tree.

## Verify or acquire

From repository root, with Python 3.11+ and the declared `jsonschema` dependency:

```powershell
python scripts/fetch_subjectivity_sources.py
python scripts/fetch_subjectivity_sources.py --download-cache ../aion-reference-cache
```

The first command is offline and read-only. The second explicitly downloads only
the allowlisted HTTPS sources, checks exact size/SHA-256, and writes only to an
external cache. Existing cache bytes with a different digest cause HOLD rather
than overwrite. No live API/model call is part of research fixture execution.
Upstream payload drift requires a new reviewed acquisition receipt; it is not
silently accepted. Text extraction is a one-time reviewed transformation recorded
in the manifest, not an extra dependency of the offline verifier.

## Reuse existing governance; no new research schema

`GOVERNED_SOURCES.json` validates against the existing
`schemas/governed_knowledge_source_v0.1.0.schema.json`. All four records are
`CANDIDATE`, `REFERENCE_ONLY`, `ON_DEMAND` with a 1,500-token context cap. Content
hashes bind the exact retained text/card, not a title or a network request.
These records do not automatically activate the runtime source registry.
Separate AION/Astra source exposure accounting remains necessary.

| Source | Methodological role | Existing owner | Limit |
|---|---|---|---|
| Butlin et al. 2023 v3 | theory-labelled computational indicators | `TheoryIndicatorRecord`, `SubjectivityEvidenceMatrix` | no count-based consciousness score; philosophical assumptions remain contested |
| Butlin & Lappas 2025 v1 | research objectives and communication under uncertainty | existing governance / evidence-card limitations | normative recommendations are not empirical evidence or authority |
| Cogitate 2025 | preregistered divergent predictions and counterevidence | `AdversarialPrediction`, `AdversarialTheoryTest` | human-neural results do not transfer directly to AI |
| Butlin et al. TICS 2026 | metadata-only index of the separately published indicator-method article | existing source registry | full-text fetch 403; no source-grounded content inference from downloaded metadata |

## Next empirical work (design only; not run by this intake)

Use the existing six evidence dimensions and seven functional state channels.
For a mechanism hypothesis, compare targeted intervention, matched sham, and
retrieval-only controls with fixed task/input and model version. Register the
predicted direction, exclusion criteria and effect/uncertainty threshold before
held-out evidence is inspected. Choose thresholds from the specific observable,
pilot variance and power analysis, not a universal subjectivity number. Keep a
negative-control outcome and at least one competing mechanism prediction.
If held-out directions disagree or uncertainty crosses the preregistered decision
boundary, record INCONCLUSIVE/COUNTEREVIDENCE and revise a new version rather than
rewriting prior predictions. Independent replication must use independently
collected evidence, not two agents reading this same corpus.

`SUBJECTIVITY = NOT_ESTABLISHED`; `CANONICAL_EFFECT = NONE`; `DEPLOYMENT = FALSE`.
