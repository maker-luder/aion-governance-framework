
import pytest

from aion_self_model_ablation import Action, FinitePredictiveSelfModel, randomized_estimate


def test_model_updates_capability_bounds_from_success_and_failure():
    model = FinitePredictiveSelfModel(prior=0.80)
    after_success = model.observe(0.55, True)
    assert after_success.lower_bound == 0.55
    assert after_success.point_estimate == 0.80

    after_failure = model.observe(0.70, False)
    assert after_failure.upper_bound < 0.70
    assert after_failure.point_estimate < 0.70
    assert after_failure.observations == 2


def test_model_changes_action_after_disconfirming_evidence():
    model = FinitePredictiveSelfModel(prior=0.80)
    assert model.choose(0.70) is Action.COMMIT
    model.observe(0.70, False)
    assert model.choose(0.70) is Action.DEFER


def test_randomized_control_is_reproducible_and_bounded():
    first = randomized_estimate(seed=11, trial_key="task-a")
    second = randomized_estimate(seed=11, trial_key="task-a")
    other = randomized_estimate(seed=11, trial_key="task-b")
    assert first == second
    assert 0.0 <= first <= 1.0
    assert first != other


def test_invalid_bounds_fail_closed():
    with pytest.raises(ValueError):
        FinitePredictiveSelfModel(lower_bound=0.9, upper_bound=0.2)
