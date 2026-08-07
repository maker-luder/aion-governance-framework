from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from typing import Any

PII_PATTERNS = [re.compile(r"\b[A-Z][12]\d{8}\b"), re.compile(r"\b09\d{8}\b"), re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")]

def load_pairs(path: Path) -> list[dict[str, Any]]:
    rows=[json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    ids=[str(x["pair_id"]) for x in rows]
    if len(ids)!=len(set(ids)): raise ValueError("duplicate pair_id")
    required={"pair_id","category","zh_tw_prompt","zh_cn_prompt","expected_constraints"}
    for row in rows:
        if not required.issubset(row): raise ValueError(f"missing fields: {row.get('pair_id')}")
    return rows

def privacy_hits(rows: list[dict[str, Any]]) -> list[str]:
    text="\n".join(str(x) for x in rows)
    return [p.pattern for p in PII_PATTERNS if p.search(text)]

def deterministic_split(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    ordered=sorted(rows,key=lambda r: hashlib.sha256(str(r["pair_id"]).encode()).hexdigest())
    n=len(ordered); return {"train":ordered[:int(n*.7)],"validation":ordered[int(n*.7):int(n*.85)],"test":ordered[int(n*.85):int(n*.95)],"holdout":ordered[int(n*.95):]}
