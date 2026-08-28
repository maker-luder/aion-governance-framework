# Local generation architecture

Checked on 2026-08-28.

This document records the local-first execution decision for the multimodal media component. It is an engineering/runtime crosswalk, not a scientific result and not a model-license legal opinion.

```text
LOCAL_GENERATION_FIRST = TRUE
NETWORK_ACCESS_REQUIRED = FALSE
REMOTE_PROVIDER_REQUIRED = FALSE
MODEL_RUNTIME_LANGUAGE = NOT_FIXED_TO_PYTHON
CANONICAL_EFFECT = NONE
SUBJECTIVITY = NOT_ESTABLISHED
```

## Layering decision

The component separates the governance/control plane from the generation plane:

```text
GenerationRequest / ExecutionGrant / MediaAsset / research bridge
                         |
                  local runtime contract
                         |
          +--------------+--------------+
          |              |              |
       C / C++          Rust          Python/other
          |              |              |
     model runtime   model runtime   isolated ML runtime
```

The repository's Python types remain useful for governance, provenance, evidence admission, and research integration. They do not require the actual generator to be Python.

`LocalRuntimeSpec` therefore records runtime language, engine, supported media, model reference, license reference, interface type, and a hard `network_access=False` boundary.

## Executable offline baseline

`InternalProceduralGenerator` is the first end-to-end local generator. It produces tiny deterministic artifacts with only the Python standard library:

| Media | Output | Purpose |
|---|---|---|
| image | binary PPM | prove deterministic local image generation and hash binding |
| video | YUV4MPEG2 sequence | prove deterministic local temporal media generation |
| 3D | glTF 2.0 JSON with embedded triangle geometry | prove deterministic local scene/model generation and glTF interoperability |

This baseline is deliberately not a quality benchmark and not a photorealistic model.

```text
REFERENCE_GENERATOR_QUALITY != TARGET_MODEL_QUALITY
OFFLINE_EXECUTION_PASS != PHOTOREALISTIC_GENERATION
```

## Native image/video candidate: stable-diffusion.cpp

Source:
<https://github.com/leejet/stable-diffusion.cpp>

The upstream project describes itself as diffusion-model inference in pure C/C++ based on ggml and is MIT-licensed. As checked on 2026-08-28, its README lists broad image-model support and local video support including Wan2.1/Wan2.2 and LTX-2.3. Its CMake configuration exposes CPU/native builds plus CUDA, ROCm/HIP, Metal, Vulkan, OpenCL and other optional backends.

Local decision:

```text
PREFERRED_NATIVE_IMAGE_VIDEO_RUNTIME_CANDIDATE = stable-diffusion.cpp
RUNTIME_VENDORING = NO
MODEL_WEIGHT_VENDORING = NO
AUTO_DOWNLOAD = NO
```

The repository should eventually integrate it through a narrow local runtime adapter with an exact executable/version fingerprint and explicit local model paths. Do not silently fetch weights at execution time.

Important separation:

```text
RUNTIME_LICENSE != MODEL_LICENSE
SUPPORTED_MODEL_NAME != MODEL_USE_AUTHORIZATION
LOCAL_MODEL_FILE != LICENSE_CLEARED_MODEL
```

Every selected model must receive its own model-card/license review.

## Rust image candidate: Hugging Face Candle

Sources:

- <https://github.com/huggingface/candle>
- <https://github.com/huggingface/candle/tree/main/candle-examples/examples/stable-diffusion>

Candle is a Rust ML framework distributed under MIT OR Apache-2.0. Its Stable Diffusion example documents local execution for Stable Diffusion 1.5, 2.1, XL 1.0 and Turbo, and it can use local weight files instead of downloading from the Hugging Face Hub.

Local decision:

```text
RUST_RUNTIME_CANDIDATE = CANDLE
DEFAULT_AUTO_DOWNLOAD = FORBIDDEN_BY_AION_LOCAL_PROFILE
```

Candle is attractive where a typed Rust runtime is desirable, but the AION adapter must force explicit local model paths so the repository's offline claim remains true.

## Local video model candidates

Wan2.1 upstream:
<https://github.com/Wan-Video/Wan2.1>

The upstream repository is Apache-2.0 and publishes local video-generation code/models. The current preferred engineering direction is to avoid a second Python-only orchestration stack when possible and first evaluate Wan-family execution through the native `stable-diffusion.cpp` runtime.

CogVideo upstream:
<https://github.com/zai-org/CogVideo>

The code is Apache-2.0. The upstream README states that CogVideoX-2B is Apache-2.0 while larger variants use a separate CogVideoX model license. Therefore `CogVideoX` is not one license class and must be reviewed per selected model.

No model weights are committed or downloaded by this component.

## Local 3D candidates

### Built-in deterministic glTF

The current local baseline already produces valid glTF 2.0 JSON with deterministic geometry. It is sufficient for research fixtures, spatial perturbations, provenance tests, and pipeline integration.

### TripoSR

Source:
<https://github.com/VAST-AI-Research/TripoSR>

The official repository describes a local single-image-to-3D reconstruction model and is MIT-licensed. It currently depends on Python/PyTorch/CUDA-class tooling rather than a small native C++ runtime.

Local decision:

```text
LOCAL_3D_RECONSTRUCTION_CANDIDATE = TripoSR
DEFAULT_3D_GENERATIVE_RUNTIME = NOT_YET_SELECTED
```

TripoSR is reconstruction from an image, not a general text-to-3D replacement. The distinction must remain explicit.

### Hunyuan3D-2 licensing caution

Source:
<https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE>

The current Hunyuan3D-2 community license contains territory and other use restrictions. Because the component aims for a simple reusable local baseline, Hunyuan3D-2 is not selected as the default local 3D runtime in this cycle. Any future use requires a separate exact-version license review.

## Why not Go or TypeScript as the primary inference runtime?

Go and TypeScript remain suitable for orchestration, UI, IPC, manifests, or service wrappers, but the current local generative-model ecosystem is substantially stronger in C/C++, Rust and Python for direct tensor/GPU inference. No repository rule prohibits Go or TypeScript; they simply are not the preferred first inference backends.

```text
LANGUAGE_DIVERSITY = ALLOWED
LANGUAGE_CHOICE = WORKLOAD_DRIVEN
PYTHON_HOST != PYTHON_ONLY_RUNTIME
```

## Local runtime integration contract

A future heavyweight local adapter should accept an already-authorized `GenerationRequest`, bind an exact `LocalRuntimeSpec`, and return only local bytes plus provenance metadata.

Required properties:

- no network access;
- no credentials;
- no shell=True execution;
- explicit executable/runtime version;
- explicit local model reference;
- explicit model-license reference;
- explicit deterministic seed where supported;
- output bytes hashed before `MediaAsset` admission;
- no automatic model download;
- no repository writeback authority;
- no deployment or main-transition authority.

The interface may be implemented as direct library binding or a narrow JSON-stdio subprocess protocol. Arbitrary command execution is not part of the media API.

## Scientific boundary

Local generation changes the infrastructure source of media, not the evidentiary meaning of media.

```text
LOCAL_GENERATION != SELF_GENERATION_AS_SUBJECTIVITY
LOCAL_MODEL_EXECUTION != AUTONOMOUS_AUTHORITY
PHOTOREALISM != REAL_WORLD_CAPTURE
GENERATED_VIDEO != OBSERVED_EVENT
GENERATED_3D != PHYSICAL_EMBODIMENT
MULTIMODAL_OUTPUT != SUBJECTIVITY_EVIDENCE
SEVEN_STATE_MODEL_REMAINS_EXACTLY_SEVEN = TRUE
```

The central research question remains `AI_SUBJECTIVITY_POSSIBILITY`; multimodal generation is supporting research infrastructure only.
