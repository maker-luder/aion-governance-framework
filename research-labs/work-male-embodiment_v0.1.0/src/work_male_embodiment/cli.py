from __future__ import annotations
import argparse, json
from .core import AssetEvidence, ExecutionSurface, GovernancePolicy, PhysiologyState, default_coverage_matrix

def qa_status() -> dict[str, object]:
    d=GovernancePolicy().evaluate(ExecutionSurface.OFFLINE_RESEARCH); s=PhysiologyState("qa"); a=AssetEvidence()
    return {"status":"IMPLEMENTED_SYNTHETIC_RESEARCH_CANDIDATE","coverage_rows":len(default_coverage_matrix()),
      "offline_synthetic_physiology_allowed":d.synthetic_physiology_allowed,
      "public_executable_exposure":d.public_executable_exposure,"actual_3d_mesh":a.actual_3d_mesh,
      "biological_reproduction":s.fertility,"body_sensation":s.body_sensation,"subjectivity":s.subjectivity,
      "consciousness":s.consciousness,"phenomenal_experience":s.phenomenal_experience,
      "canonical_effect":s.canonical_effect,"deployment":s.deployment}

def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("command",choices=["qa-status"]); a=p.parse_args()
    if a.command=="qa-status": print(json.dumps(qa_status(),indent=2,sort_keys=True))
if __name__=="__main__": main()
