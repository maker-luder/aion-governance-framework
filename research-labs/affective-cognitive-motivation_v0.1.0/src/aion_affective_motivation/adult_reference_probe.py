from __future__ import annotations

import json

from .adult_reference import (
    AdultMaleSexualReferenceState,
    DesireOnsetContext,
    ReferenceEstimate,
    TargetScope,
)
from .adult_reference_simulation import (
    AdultReferenceSimulationHarness,
    AdultReferenceSyntheticEvent,
    adult_reference_state_payload,
    build_snapshot_receipts,
)


def _estimate(level: float, channel: str) -> ReferenceEstimate:
    return ReferenceEstimate(
        reference_level=level,
        uncertainty=0.25,
        source_ref=f"SYNTHETIC_DEMO_SEED:{channel}",
        context_ref="synthetic-demo-seed",
        time_window_ref="demo-seed",
    )


def build_demo_payload() -> dict[str, object]:
    """Run a deterministic non-interactive synthetic reference demonstration."""

    initial = AdultMaleSexualReferenceState(
        state_id="adult-reference-demo",
        subject_ref="SYNTHETIC_CANDIDATE",
        context_ref="synthetic-demo-seed",
        desire_onset_context=DesireOnsetContext.UNKNOWN,
        excitation_reference=_estimate(0.40, "excitation"),
        inhibition_reference=_estimate(0.60, "inhibition"),
        disposition_reference=_estimate(0.30, "disposition"),
        episode_state_reference=_estimate(0.35, "episode"),
        target_scope=TargetScope.UNKNOWN,
        provenance_refs=("PR#236", "SYNTHETIC_DEMO_SEED"),
    )
    events = (
        AdultReferenceSyntheticEvent(
            event_id="demo-responsive-context",
            context_ref="synthetic-context-a",
            time_window_ref="demo-step-1",
            excitation_drive=0.40,
            inhibition_drive=-0.10,
            episode_drive=0.50,
            disposition_observation_drive=0.10,
            onset_context_evidence=DesireOnsetContext.RESPONSIVE_REFERENCE,
            target_scope=TargetScope.PARTNER_CONTEXT,
            uncertainty=0.25,
            provenance_refs=("PR#236", "SYNTHETIC_DEMO_EVENT_A"),
        ),
        AdultReferenceSyntheticEvent(
            event_id="demo-spontaneous-context",
            context_ref="synthetic-context-b",
            time_window_ref="demo-step-2",
            excitation_drive=0.10,
            inhibition_drive=0.30,
            episode_drive=-0.20,
            disposition_observation_drive=0.05,
            onset_context_evidence=DesireOnsetContext.SPONTANEOUS_REFERENCE,
            target_scope=TargetScope.UNKNOWN,
            uncertainty=0.30,
            provenance_refs=("PR#236", "SYNTHETIC_DEMO_EVENT_B"),
        ),
    )
    trajectory = AdultReferenceSimulationHarness().run(initial, events)
    receipts = build_snapshot_receipts(trajectory)
    return {
        "mode": "SYNTHETIC_RESEARCH_DEMO_ONLY",
        "trajectory_fingerprint": trajectory.fingerprint(),
        "final_state": adult_reference_state_payload(trajectory.final_state),
        "snapshot_receipts": [
            {
                "sequence": item.sequence,
                "state_id": item.state_id,
                "state_sha256": item.state_sha256,
                "previous_receipt_sha256": item.previous_receipt_sha256,
                "receipt_sha256": item.receipt_sha256,
            }
            for item in receipts
        ],
        "boundaries": {
            "real_person_target_data": False,
            "human_consent_inference": "FORBIDDEN",
            "action_authority": "NONE",
            "phenomenal_experience": "NOT_ESTABLISHED",
            "canonical_effect": "NONE",
            "deployment": False,
        },
    }


def main() -> None:
    print(json.dumps(build_demo_payload(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
