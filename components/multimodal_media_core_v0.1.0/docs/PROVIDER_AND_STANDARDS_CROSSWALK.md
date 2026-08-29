# Provider and standards crosswalk

Checked on 2026-08-28. These sources define interoperability inputs, not scientific authority.

| Surface | Verified contract | Source | Local decision |
|---|---|---|---|
| OpenAI image | Image API generations and edits; GPT Image models; JSON generation endpoint | <https://developers.openai.com/api/docs/guides/image-generation> and <https://developers.openai.com/api/reference/resources/images> | Implement single-prompt generation only; keep editing and binary ingestion outside v0.1.0. |
| OpenAI video | `POST /v1/videos`; async job; `sora-2` / `sora-2-pro`; optional reference asset; documented duration and size enums | <https://platform.openai.com/docs/api-reference/videos> | Use multipart fields and explicit polling. Do not assume submission is completion. |
| Tripo 3D | `POST /v2/openapi/task`; `text_to_model`; `data.task_id`; poll task | <https://platform.tripo3d.ai/docs/generation> and <https://platform.tripo3d.ai/docs/quick-start> | Preserve provider model-version string and seed. Admit downloaded output only after hashing. |
| Meshy 3D | `POST /openapi/v2/text-to-3d`; preview then refine; task object returns model URLs including GLB | <https://docs.meshy.ai/en/api/text-to-3d> | v0.1.0 submits preview. Refine can be a later, separately governed request. |
| 3D interchange | glTF 2.0 is API-neutral runtime asset delivery; registered `model/gltf+json` and `model/gltf-binary` media types | <https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html> | Prefer GLB/glTF evidence artifacts; allow USDZ or opaque binary only with its declared type. |
| Segment annotation | W3C Web Annotation supports reusable annotations and selectors for parts of timed multimedia resources | <https://www.w3.org/TR/annotation-model/> | Export annotation-shaped JSON; callers may supply a standards-compatible selector. |
| Tamper-evident provenance | C2PA defines signed, verifiable provenance manifests and an explicit trust model | <https://spec.c2pa.org/specifications/> | Store manifest reference separately from validation boolean. No signature verification is claimed by the bridge. |
| Synthetic media disclosure | IPTC recommends `trainedAlgorithmicMedia`; current guidance also defines AI-system and prompt metadata fields | <https://www.iptc.org/std/photometadata/documentation/userguide/> | Default generated-asset source type to the IPTC controlled URI; avoid naming a human as image creator automatically. |
| Captured-media disclosure | IPTC defines `digitalCapture` for media sampled from real life with a digital capture device | <http://cv.iptc.org/newscodes/digitalsourcetype/digitalCapture> | Require an explicit non-synthetic source type for `SENSOR_OBSERVED`; origin alone is not proof of provenance. |

## Deliberate non-unification

Provider lifecycle and payload fields are not normalized away. Images may complete synchronously while videos and 3D assets are jobs. Meshy preview/refine is not the same operation as Tripo text-to-model. The shared core normalizes research identity, hashes, media types, provenance state, and governance boundaries—not provider semantics.

## Operational limitations

- Provider contracts can change; production transports should pin and monitor provider API versions where available.
- Signed C2PA validation requires a separate verifier and trust store.
- A remote URL is not durable evidence. The output must be downloaded under its permitted terms, hashed, stored under repository-approved retention rules, and referenced immutably.
- Licensing, biometric/personality rights, copyright, privacy, and provider terms require task-specific review. This component does not infer usage rights from successful generation.
- No live provider execution is performed by repository tests.
- Provider-generated media may serve as a governed stimulus, control, or counterfactual artifact. The media itself is not admitted as direct subjectivity evidence; observed/imported media still requires the existing integrity gate, exact hash linkage, and explicit human review.
