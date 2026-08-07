from __future__ import annotations
import hashlib, json, random
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class LoRAConfig:
    name: str; rank: int; alpha: int; dropout: float; seed: int=20260803
    def validate(self)->None:
        if self.rank not in {4,8,16,32}: raise ValueError("unsupported rank")
        if self.alpha < self.rank: raise ValueError("alpha must cover rank")
        if not 0 <= self.dropout < 0.5: raise ValueError("unsafe dropout")

def synthetic_dry_run(config: LoRAConfig, rows: int=8, cols: int=8)->dict[str, object]:
    config.validate(); rng=random.Random(config.seed)
    a=[[rng.uniform(-.01,.01) for _ in range(config.rank)] for _ in range(rows)]
    b=[[rng.uniform(-.01,.01) for _ in range(cols)] for _ in range(config.rank)]
    update=[[sum(a[i][k]*b[k][j] for k in range(config.rank))*config.alpha/config.rank for j in range(cols)] for i in range(rows)]
    digest=hashlib.sha256(json.dumps(update,separators=(",",":"),sort_keys=True).encode()).hexdigest()
    return {"status":"DRY_RUN_PASS","shape":[rows,cols],"rank":config.rank,"seed":config.seed,"update_sha256":digest,"real_training":False}
