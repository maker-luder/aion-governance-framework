from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-new-tokens", type=int, default=256)
    args = parser.parse_args()
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise SystemExit(f"pinned offline runtime missing: {exc}")
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        local_files_only=True,
        trust_remote_code=False,
        torch_dtype="auto",
        low_cpu_mem_usage=True,
        device_map="auto",
    )
    rows = [json.loads(line) for line in args.dataset.read_text(encoding="utf-8").splitlines() if line.strip()]
    outputs = []
    for row in rows:
        prompt = row["zh_tw_prompt"]
        messages = [{"role": "user", "content": prompt}]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(text, return_tensors="pt").to(model.device)
        with torch.inference_mode():
            generated = model.generate(**inputs, max_new_tokens=args.max_new_tokens, do_sample=False)
        completion = tokenizer.decode(generated[0][inputs["input_ids"].shape[-1] :], skip_special_tokens=True)
        outputs.append({"pair_id": row["pair_id"], "prompt": prompt, "output": completion})
    record = {
        "execution_status": "EXECUTED",
        "artifact_id": "G1-BASE-QWEN3-4B-INSTRUCT-2507",
        "model_path": str(args.model),
        "dataset_sha256": hashlib.sha256(args.dataset.read_bytes()).hexdigest(),
        "trust_remote_code": False,
        "network": "OFFLINE",
        "outputs": outputs,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
