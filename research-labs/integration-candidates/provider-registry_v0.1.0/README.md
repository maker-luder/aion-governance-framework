# AION Provider Registry Candidate v0.1.0

This offline candidate defines provider metadata, capability declarations and deterministic policy selection. It does not invoke a provider, perform network access, load credentials, download models or implement serving.

The design is informed by the separation between tokenizer/model/runtime/serving layers documented by [Hugging Face Transformers](https://huggingface.co/docs/transformers/en/main_classes/tokenizer) and [vLLM online serving](https://docs.vllm.ai/en/stable/serving/online_serving/). Those sources are comparison references, not dependencies or conformance targets.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
```
