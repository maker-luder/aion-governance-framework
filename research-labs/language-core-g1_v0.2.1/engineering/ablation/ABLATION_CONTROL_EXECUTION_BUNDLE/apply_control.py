from __future__ import annotations
import argparse, hashlib, json, random
from pathlib import Path

def main()->None:
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['targeted','random'],required=True);p.add_argument('--dry-run',action='store_true');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if not a.dry_run: raise SystemExit('actual model intervention is blocked pending reviewed method and compute gate')
    seed=20260803; values=[float(i+1) for i in range(64)]; target=[0,1,8,9]; idx=target if a.mode=='targeted' else sorted(random.Random(seed).sample(range(64),len(target)))
    result=list(values)
    for i in idx: result[i]*=.99
    out={'status':'DRY_RUN_PASS','mode':a.mode,'seed':seed,'strength':.01,'indices':idx,'actual_model_modified':False,'sha256':hashlib.sha256(json.dumps(result).encode()).hexdigest()}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
