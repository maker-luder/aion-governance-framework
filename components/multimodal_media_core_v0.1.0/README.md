# AION Multimodal Media Core v0.1.0

This component provides a governed image, video, and 3D media substrate for bounded research evidence.

The preferred architecture is now **local-first**:

```text
AION Multimodal Media Core
        ↓
Local generation runtime (preferred)
        ↓
MediaAsset + exact content hash
        ↓
Multimodal Research Bridge
        ↓
Seven-state / AION-Astra / Subjectivity Pipeline
```

External provider adapters remain compatibility/reference surfaces, but they are no longer the preferred generation path.

```text
LOCAL_GENERATION_FIRST = TRUE
LOCAL_RUNTIME_NETWORK_ACCESS = FALSE
EXTERNAL_PROVIDER_EXECUTION = OPTIONAL / NOT_REQUIRED
MEDIA_GENERATION != RESEARCH_RESULT
GENERATED_MEDIA != SUBJECTIVITY
CANONICAL_EFFECT = NONE
```

## Local executable reference path

`InternalProceduralGenerator` is a real, deterministic, repository-local generation path for all three media kinds:

- `IMAGE` -> tiny binary PPM (`image/x-portable-pixmap`);
- `VIDEO` -> tiny YUV4MPEG2 sequence (`video/x-yuv4mpeg`);
- `MODEL_3D` -> glTF 2.0 JSON containing deterministic triangle geometry (`model/gltf+json`).

It uses no API key, network call, model download, GPU, subprocess, or hidden remote dependency. Every output is byte-hashed before it becomes `MediaAsset`, is marked `MediaOrigin.LOCAL_GENERATED`, and retains the existing synthetic-media provenance boundary.

This reference generator is intentionally **not photorealistic**. Its job is to prove the offline execution/provenance contract before large model runtimes are attached.

## Multi-language runtime contract

`LocalRuntimeSpec` is language-neutral. The governance/control plane may remain Python while model execution can be implemented in another local runtime, for example C++, Rust, or a separately isolated Python ML process.

The preferred next native paths are documented in [`docs/LOCAL_GENERATION_ARCHITECTURE.md`](docs/LOCAL_GENERATION_ARCHITECTURE.md). The current research decision is:

- C/C++ is the leading image/video native inference candidate because `stable-diffusion.cpp` can run multiple diffusion image families and local video models without a remote provider;
- Rust/Candle is a credible image-inference alternative and a useful typed local runtime surface;
- 3D remains split between the built-in deterministic glTF path and separately reviewed local reconstruction/generation runtimes.

A local model runtime does not become trusted merely because it is local. Model weights, license, exact model version, runtime version, hardware path, generation seed, and output hash remain evidence/provenance inputs.

## Existing external compatibility adapters

The first candidate also contains narrow adapters for OpenAI image/video and Tripo/Meshy 3D contracts. They remain available for compatibility testing and contract comparison only. Tests use injected recording transports and perform no live provider calls.

External output URLs or provider responses do not become evidence until the bytes are obtained under an authorized execution path, hashed, and admitted as `MediaAsset`.

## Research bindings

- Seven-state binding requires the existing exact matrix and binding fingerprints; multimodal media does not create an eighth canonical state.
- AION/Astra binding preserves `scientific_disposition=HOLD`.
- Subjectivity binding reuses the existing research-integrity admission gate. Generated media may be a stimulus, control, counterfactual artifact, or research output; generation alone cannot establish subjectivity.
- C2PA references remain distinct from actual validation.

## Locked boundaries

```text
MULTIMODAL_MEDIA != EIGHTH_STATE
LOCAL_MODEL_EXECUTION != SUBJECTIVITY_EVIDENCE
PHOTOREALISTIC_OUTPUT != REAL_WORLD_OBSERVATION
VIDEO_TEMPORALITY != IDENTITY_CONTINUITY
VIRTUAL_3D_SCENE != PHYSICAL_EMBODIMENT
MEDIA_BINDING != SCIENTIFIC_TRUTH
GENERATED_MEDIA != SUBJECTIVITY
C2PA_REFERENCE != C2PA_VALIDATION
FULL_AUTOMATION != FULL_AUTHORITY
EVIDENCE_ADMISSION != CLAIM_ACCEPTANCE
```

See:

- [`docs/LOCAL_GENERATION_ARCHITECTURE.md`](docs/LOCAL_GENERATION_ARCHITECTURE.md) for the local-first runtime decision;
- [`docs/PROVIDER_AND_STANDARDS_CROSSWALK.md`](docs/PROVIDER_AND_STANDARDS_CROSSWALK.md) for external contract/reference surfaces.

## Test

Use the repository component runner so all research dependencies receive the same source-root environment:

```bash
python scripts/run_component_tests.py
```

For component-local iteration, the component test `conftest.py` adds this component's `src`; tests that exercise the research bridge still require the repository-wide multi-component environment.
