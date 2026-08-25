from pathlib import Path
import pytest
from astra_language_core.g1_ablation import controlled_low_strength, synthetic_control_dry_run
from astra_language_core.g1_dataset import deterministic_split, load_pairs, privacy_hits
from astra_language_core.g1_lora import LoRAConfig, synthetic_dry_run
from astra_language_core.g1_runtime_policy import RuntimePolicy, safe_child
from astra_language_core.g1_side_effects import DIMENSIONS, blank_report

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/language_core_g1/PAIRED_ZH_DATASET_V1.jsonl'

def test_dataset_50_unique_and_private():
    rows=load_pairs(DATA); assert len(rows)==50; assert privacy_hits(rows)==[]
def test_split_complete():
    rows=load_pairs(DATA); parts=deterministic_split(rows); assert sum(map(len,parts.values()))==50; assert len(parts['holdout'])>0
def test_lora_dry_run_reproducible():
    c=LoRAConfig('LIGHT',8,16,.05); assert synthetic_dry_run(c)==synthetic_dry_run(c)
def test_lora_rejects_bad_rank():
    with pytest.raises(ValueError): synthetic_dry_run(LoRAConfig('BAD',7,16,.05))
def test_ablation_strength_limited():
    with pytest.raises(ValueError): controlled_low_strength([1.0],[0],.2)
def test_random_control_reproducible_and_equal():
    x=synthetic_control_dry_run(); assert x['status']=='DRY_RUN_PASS' and x['equal_perturbation_count']
def test_runtime_candidate_and_kill_switch():
    p=RuntimePolicy(); assert p.candidate_output('x')['canonical_effect']=='NONE'; p.kill();
    with pytest.raises(RuntimeError): p.candidate_output('x')
def test_runtime_denials():
    p=RuntimePolicy()
    for fn in (p.memory_write,p.canonical_write,p.identity_mutation,p.privilege_inheritance):
        with pytest.raises(PermissionError): fn('x')
def test_localhost_and_traversal():
    p=RuntimePolicy(); p.validate_endpoint('http://127.0.0.1:11434/api/generate')
    with pytest.raises(PermissionError): p.validate_endpoint('https://example.com')
    with pytest.raises(PermissionError): safe_child(ROOT,'../escape')
def test_side_effect_schema_has_no_fake_scores():
    report=blank_report('A'); assert len(DIMENSIONS)==22 and all(v is None for v in report['dimensions'].values())
