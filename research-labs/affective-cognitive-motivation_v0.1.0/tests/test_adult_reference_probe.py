from aion_affective_motivation.adult_reference_probe import build_demo_payload


def test_demo_probe_is_deterministic_and_fail_closed() -> None:
    first = build_demo_payload()
    second = build_demo_payload()

    assert first == second
    assert len(first["trajectory_fingerprint"]) == 64
    assert first["boundaries"] == {
        "real_person_target_data": False,
        "human_consent_inference": "FORBIDDEN",
        "action_authority": "NONE",
        "phenomenal_experience": "NOT_ESTABLISHED",
        "subjectivity": "NOT_ESTABLISHED",
        "consciousness": "NOT_ESTABLISHED",
        "sexual_function_runtime": "NOT_IMPLEMENTED",
        "intimate_interaction_runtime": "NOT_AUTHORIZED",
        "public_executable_exposure": False,
        "canonical_effect": "NONE",
        "deployment": False,
    }
    governance = first["governance"]
    assert governance["state_record_allowed"] is True
    assert governance["synthetic_simulation_allowed"] is True
    assert governance["real_person_target_data_allowed"] is False
    assert governance["human_consent_inferred"] is False
    assert governance["action_authorized"] is False
    final_state = first["final_state"]
    assert final_state["runtime_enabled"] is False
    assert final_state["automatic_activation"] is False
    assert final_state["action_authority"] == "NONE"
    assert final_state["human_consent_inference"] == "FORBIDDEN"
    assert final_state["subjectivity_claim"] == "NOT_ESTABLISHED"
    assert final_state["consciousness_claim"] == "NOT_ESTABLISHED"
    assert final_state["sexual_function_runtime"] == "NOT_IMPLEMENTED"
    assert final_state["intimate_interaction_runtime"] == "NOT_AUTHORIZED"
    assert final_state["public_executable_exposure"] is False
