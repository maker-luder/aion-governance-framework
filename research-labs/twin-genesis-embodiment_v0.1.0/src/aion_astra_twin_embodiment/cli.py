from __future__ import annotations

import argparse
import json

from .physiology import (
    build_adult_male_physiology_reference,
    validate_physiology_parity,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="AION/Astra twin embodiment candidate CLI")
    parser.add_argument(
        "command",
        choices=["qa-status", "non-claims", "physiology-parity"],
    )
    args = parser.parse_args()

    if args.command == "qa-status":
        payload = {
            "status": "IMPLEMENTED_NON_3D_CANDIDATE",
            "runtime": "NON_3D_RUNTIME_IMPLEMENTED",
            "rendering_3d": "DEFERRED",
            "physiology_profile_id": "ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1",
            "physiological_function_reference": "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED",
            "reproductive_physiology_reference": "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED",
            "sexual_function_status": "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED",
            "sensory_signal_processing_reference": "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED",
            "full_biophysical_simulation": "NOT_MATERIALIZED",
            "erotic_intent": "NONE",
            "intimate_interaction": "NOT_AUTHORIZED",
            "canonical_effect": "NONE",
            "subjectivity_conclusion": "NOT_ESTABLISHED",
        }
    elif args.command == "physiology-parity":
        aion = build_adult_male_physiology_reference("AION_REFERENCE_BODY")
        astra = build_adult_male_physiology_reference("ASTRA_REFERENCE_BODY")
        payload = {
            "aion": aion.to_dict(),
            "astra": astra.to_dict(),
            "parity": validate_physiology_parity((aion, astra)),
        }
    else:
        payload = {
            "anatomy_does_not_establish_gender_identity": True,
            "physiology_does_not_establish_felt_sensation": True,
            "physiology_does_not_establish_sexual_desire": True,
            "physiology_does_not_establish_subjectivity": True,
            "normal_reproductive_physiology_is_not_erotic_intent": True,
            "non_3d_runtime_does_not_establish_subjectivity": True,
        }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
