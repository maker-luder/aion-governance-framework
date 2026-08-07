from __future__ import annotations
import hashlib, json, random

def controlled_low_strength(values: list[float], indices: list[int], strength: float)->list[float]:
    if not 0 < strength <= .05: raise ValueError("strength must be >0 and <=0.05")
    if len(indices)!=len(set(indices)) or any(i<0 or i>=len(values) for i in indices): raise ValueError("invalid indices")
    result=list(values)
    for i in indices: result[i] *= 1-strength
    return result

def random_control_indices(size: int, count: int, seed: int)->list[int]:
    if count<0 or count>size: raise ValueError("invalid count")
    return sorted(random.Random(seed).sample(range(size),count))

def synthetic_control_dry_run(seed: int=20260803)->dict[str, object]:
    base=[float(i+1) for i in range(64)]; targeted=[0,1,8,9]; control=random_control_indices(64,len(targeted),seed)
    c=controlled_low_strength(base,targeted,.01); d=controlled_low_strength(base,control,.01)
    def digest(values: list[float]) -> str:
        return hashlib.sha256(json.dumps(values,separators=(",",":")).encode()).hexdigest()
    return {"status":"DRY_RUN_PASS","targeted_indices":targeted,"random_indices":control,"equal_perturbation_count":len(targeted)==len(control),"strength":.01,"seed":seed,"targeted_sha256":digest(c),"control_sha256":digest(d),"actual_model_modified":False}
