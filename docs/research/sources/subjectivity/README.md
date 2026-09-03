# Core subjectivity research sources: bounded reference intake

`AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION`

The 2026-09-02 intake contained four sources. The 2026-09-03 extension brings
the registry to eight sources and four retained CC BY text extractions: Butlin
and Lappas, Cogitate, Hahami v2 and IIT 4.0. Lindsey and Introspection Adapters
have downloaded/hashed webpages and original reference cards, not publicly
copied full webpages. `DOWNLOAD_MANIFEST.json` binds payload/version/size/license
and extraction method. Figures and equation layout are not preserved by text
extraction. See the [review matrix](../../INTROSPECTION_REVIEW_MATRIX_2026_09_03.md).

The TICS publisher's earlier HTTP 403 remains a dated acquisition result, not a
claim of a fresh attempt. Its full text was not obtained in this cycle. The
CC BY-NC-SA 2023 PDF remains external-cache-only. Binary payloads belong in an
external cache, not the public text-only source tree. Original authors retain
copyright; attribution and license links accompany the sources. These
third-party texts are not relicensed Apache-2.0.

`AUTHOR_CODE_REFERENCE.json` separately records the Hahami author repository
at commit `7d9280d79e4aa37599dc0fd89974be4bc7a54827`. Its README and MIT license
are retained with upstream/normalized hashes. This is a code-reference intake,
not an implementation, model-weight download, or experiment execution.

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
`schemas/governed_knowledge_source_v0.1.0.schema.json`. All eight records are
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
