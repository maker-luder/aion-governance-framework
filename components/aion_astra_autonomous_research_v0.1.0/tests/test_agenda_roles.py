from __future__ import annotations

from fractions import Fraction

import pytest

from aion_astra_autonomous_research import AgendaScore, PeerRole, build_agenda, rotating_roles


def test_agenda_score_uses_exact_rational_arithmetic() -> None:
    score = AgendaScore(9, 8, 7, 3, 2)
    assert score.exact == Fraction(84, 1)
    assert score.to_record()["score_exact"] == "84/1"


@pytest.mark.parametrize("field", ["epistemic_value", "falsifiability", "expected_information_gain", "cost", "risk"])
def test_zero_score_denominator_or_factor_is_rejected(field: str) -> None:
    values = dict(epistemic_value=1, falsifiability=1, expected_information_gain=1, cost=1, risk=1)
    values[field] = 0
    with pytest.raises(ValueError, match="positive"):
        AgendaScore(**values)


def test_agenda_deduplicates_and_orders_reproducibly() -> None:
    first = build_agenda(("  Question A  ", "question a", "Question B"))
    second = build_agenda(("Question A", "Question B"))
    assert [item.question for item in first] == [item.question for item in second]
    assert [item.question_id for item in first] == [item.question_id for item in second]


def test_empty_explicit_agenda_stops_cleanly() -> None:
    assert build_agenda(("", "   ")) == ()


def test_roles_rotate_without_permanent_supporter_or_critic() -> None:
    round_one = rotating_roles(1)
    round_two = rotating_roles(2)
    assert round_one.aion_role is PeerRole.PROPOSER
    assert round_one.astra_role is PeerRole.FALSIFIER
    assert round_two.aion_role is PeerRole.FALSIFIER
    assert round_two.astra_role is PeerRole.PROPOSER
    assert round_one.aion_provider != round_one.astra_provider
    assert not round_one.shared_identity


def test_invalid_round_is_rejected() -> None:
    with pytest.raises(ValueError, match="positive"):
        rotating_roles(0)
