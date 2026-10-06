from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .species_profiles import (
    build_aion_tiger_profile,
    build_tiger_reproductive_reference_observations,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="AION/Astra twin embodiment candidate CLI")
    parser.add_argument("command", choices=["qa-status", "non-claims", "aion-tiger-profile"])
    args = parser.parse_args()

    if args.command == "qa-status":
        payload = {
            "status": "IMPLEMENTED_NON_3D_CANDIDATE",
            "runtime": "NON_3D_RUNTIME_IMPLEMENTED",
            "rendering_3d": "DEFERRED",
            "sexual_function": "NOT_IMPLEMENTED",
            "intimate_interaction": "NOT_AUTHORIZED",
            "canonical_effect": "NONE",
            "subjectivity_conclusion": "NOT_ESTABLISHED",
        }
    elif args.command == "aion-tiger-profile":
        payload = {
            "profile": asdict(build_aion_tiger_profile()),
            "reproductive_reference_observations": [
                asdict(item) for item in build_tiger_reproductive_reference_observations()
            ],
            "chinese_boundary": {
                "human_tiger_integration": "工程類比，不是自然界人虎混合生物的實證",
                "reproductive_physiology": "已建立可驗證的參考模型，不等於活體生殖功能已在 AI 發生",
                "sexualization": "生殖解剖與生理研究不等於情色化",
            },
        }
    else:
        payload = {
            "anatomy_does_not_establish_gender_identity": True,
            "anatomy_does_not_establish_sensation": True,
            "anatomy_does_not_establish_sexual_desire": True,
            "anatomy_does_not_establish_subjectivity": True,
            "non_3d_runtime_does_not_establish_subjectivity": True,
            "engineering_analogue_does_not_establish_biological_hybrid": True,
        }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
