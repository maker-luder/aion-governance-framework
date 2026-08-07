from __future__ import annotations
import argparse, json
from pathlib import Path

def main()->None:
    p=argparse.ArgumentParser(); p.add_argument('--config',type=Path,required=True); p.add_argument('--dry-run',action='store_true'); args=p.parse_args()
    cfg=json.loads(args.config.read_text(encoding='utf-8'))
    base=Path(cfg['base_model_path']); out=Path(cfg['output_dir'])
    if not base.exists(): raise SystemExit('approved base path missing')
    if base.resolve() in out.resolve().parents or out.resolve()==base.resolve(): raise SystemExit('output must be a separate fork')
    if args.dry_run: print(json.dumps({'status':'CONFIG_DRY_RUN_PASS','real_training':False,'config':cfg['name']})); return
    try:
        import torch
        from datasets import load_dataset
        from peft import LoraConfig, get_peft_model
        from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
    except ImportError as exc: raise SystemExit(f'training dependency missing: {exc}')
    raise SystemExit('Real training requires the transferred reviewed dataset and stronger-hardware execution gate; remove this guard only in the approved runbook.')
if __name__=='__main__': main()
