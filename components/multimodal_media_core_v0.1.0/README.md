# AION Multimodal Media Core v0.1.0

This component provides a governed, provider-neutral path for image, video, and 3D media to become bounded research evidence.

```text
AION Multimodal Media Core
        ↓
Image Provider Adapter / Video Provider Adapter / 3D Provider Adapter
        ↓
Multimodal Research Bridge
        ↓
Seven-state / AION-Astra / Subjectivity Pipeline
```

The core separates four concerns:

1. `GenerationRequest` is a canonical, credential-free research request.
2. Provider adapters translate that request into documented provider API shapes through an injected transport.
3. `MediaAsset` admits only completed, content-hashed media with explicit generated/observed/imported origin, media type, and provenance status.
4. `MultimodalResearchBridge` creates a W3C Web Annotation-shaped evidence view and binds exact seven-state matrix, AION/Astra chain, and bounded subject references.

No adapter contains an API key. `credential_env` names the runtime secret slot; the injected transport owns credential resolution. Tests use a recording transport and never make provider calls.

## Supported adapter profiles

| Adapter | Submission contract | Execution form |
|---|---|---|
| `OpenAIImageAdapter` | `POST /v1/images/generations` | synchronous JSON result |
| `OpenAIVideoAdapter` | `POST /v1/videos`, then `GET /v1/videos/{id}` | asynchronous multipart job |
| `Tripo3DAdapter` | `POST /v2/openapi/task` with `type=text_to_model` | asynchronous JSON task |
| `Meshy3DAdapter` | `POST /openapi/v2/text-to-3d` with `mode=preview` | asynchronous two-stage-compatible task |

Adapter request construction is intentionally narrow. Provider response bytes and time-limited URLs do not become evidence until a caller downloads the output, verifies it, computes `content_sha256`, and creates a `MediaAsset`.

## Research bindings

- Seven-state binding requires both the exact matrix fingerprint and its underlying binding fingerprint, plus `matrix_integrity_pass=True`.
- AION/Astra binding requires the exact `final_chain_hash` and preserves `scientific_disposition=HOLD`.
- Subjectivity binding reuses the existing research-integrity admission gate and emits the existing `SUBJECTIVITY_EVIDENCE` stage type only after exact hash binding plus explicit human review. Provider-generated media remains a stimulus/output and cannot directly become subjectivity evidence. The bridge record remains `NOT_ESTABLISHED` for subjectivity and phenomenal experience.
- C2PA is represented as a validation result and manifest reference. A mere URL or provider claim is never promoted into `c2pa_validated=True`.

## Locked boundaries

```text
MEDIA_GENERATION != RESEARCH_RESULT
MEDIA_BINDING != SCIENTIFIC_TRUTH
GENERATED_MEDIA != SUBJECTIVITY
PROVIDER_OUTPUT != CANONICAL_EFFECT
C2PA_REFERENCE != C2PA_VALIDATION
FULL_AUTOMATION != FULL_AUTHORITY
PROVIDER_AVAILABILITY != EVIDENCE_VALIDITY
EVIDENCE_ADMISSION != CLAIM_ACCEPTANCE
```

See [`docs/PROVIDER_AND_STANDARDS_CROSSWALK.md`](docs/PROVIDER_AND_STANDARDS_CROSSWALK.md) for the externally checked contract sources and limitations.

## Test

```bash
PYTHONPATH=src:../../research-labs/subjectivity-pipeline_v0.1.0/src \
  python -m pytest -q -o addopts=
```
