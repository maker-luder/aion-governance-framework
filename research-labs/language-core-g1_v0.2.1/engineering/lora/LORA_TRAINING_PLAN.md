# LoRA Training Plan

Two branches are specified: G1-TW-LORA-LIGHT and G1-TW-LORA-STANDARD. Both must read the immutable G1-BASE and write checkpoints/adapters to separate fork directories. The current host performs configuration/synthetic dry runs only; it does not produce loss, checkpoint, adapter, training-time or GPU-use claims. Resume must verify base, dataset and config hashes before continuing.
