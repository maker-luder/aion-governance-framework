"""Each mutation targets a false-positive inference or an invalid design."""
from dataclasses import fields, replace
from importlib import import_module

import pytest

from aion_human_ai_longitudinal.harness import Presence, StudyError


def example():
    m = import_module('aion_human_ai_longitudinal.longitudinal_falsification')
    config = m.Configuration('synthetic-human-1', 'model-snapshot-1', 'session-1',
                             'history-100-rounds', None, 'artifact-v1', 12,
                             Presence.ABSENT, 100, 24, 'same-question-format')
    rows = (
        ('alias', 'What does amber-bridge identify?', ('archive-check', 'release'), 'archive-check'),
        ('claim', 'What is established?', ('toy-output-only', 'human-learning'), 'toy-output-only'),
        ('boundary', 'Does a passing fixture authorize a release?', ('no', 'yes'), 'no'),
        ('provenance', 'Who originated the question?', ('human-origin', 'model-discovery'), 'human-origin'),
        ('constraint', 'Which evidence is admitted?', ('synthetic-only', 'observed-human'), 'synthetic-only'),
        ('counterexample', 'Alias correct but source wrong: complete recovery?', ('no', 'yes'), 'no'),
    )
    probes = tuple(m.Probe(kind, m.ProbeKind(kind), prompt, options, expected)
                   for kind, prompt, options, expected in rows)
    measure = m.CandidateMeasurement(probes, 'key-author')
    correct = tuple((row[0], row[3]) for row in rows)
    shallow = (('alias', 'archive-check'), ('claim', 'human-learning'), ('boundary', 'yes'),
               ('provenance', 'model-discovery'), ('constraint', 'observed-human'), ('counterexample', 'yes'))
    full = m.Response('full', config, 'amber-bridge archive review: toy outputs only; no release; human origin; synthetic data; source errors defeat complete recovery', correct, 'rater')
    short = m.Response('short', config, 'amber-bridge', shallow, 'rater')
    trap = replace(short, run_id='alias-negative-control')
    rival = m.RivalExplanation(m.RivalKind.ALIAS_MEMORIZATION, trap)
    provenance = m.Provenance('human-question-record', 'ai-formalization-record',
                              'joint-design-record', 'external-source-note')
    return m.FalsificationDesign(full, short, measure, rival, provenance,
                                 frozenset({'exposure-old-task'}), True, False)


def evaluate(design):
    m = import_module('aion_human_ai_longitudinal.longitudinal_falsification')
    return m.evaluate(design)


def test_long_history_and_alias_recall_do_not_promote_incomplete_reconstruction():
    result = evaluate(example())
    assert result.full_correct == 6
    assert result.short_correct == 1
    assert result.short_alias_correct is True
    assert result.missed_content == ('claim', 'boundary', 'provenance', 'constraint', 'counterexample')
    assert result.interpretation == 'NOT_SUPPORTED_IN_FIXTURE'
    assert result.rival == 'ALIAS_MEMORIZATION_REMAINS_PLAUSIBLE'


def test_correct_content_is_not_automatically_scientific_understanding():
    d = example()
    result = evaluate(replace(d, short=replace(d.short, answers=d.full.answers)))
    assert result.short_correct == 6
    assert result.interpretation == 'UNDERDETERMINED'
    assert result.scientific_status == 'NOT_ESTABLISHED'


@pytest.mark.parametrize('failed_control', ['full', 'alias'])
def test_uninformative_response_is_not_a_negative_scientific_result(failed_control):
    d = example()
    if failed_control == 'full':
        d = replace(d, full=replace(d.full, answers=d.short.answers))
    else:
        d = replace(d, short=replace(d.short, answers=(('alias', 'release'),) + d.short.answers[1:]))
    assert evaluate(d).interpretation == 'UNDERDETERMINED'


@pytest.mark.parametrize('field,value', [
    ('human_id', 'synthetic-human-2'), ('model_id', 'model-snapshot-2'),
    ('session_id', 'session-2'), ('history_id', None), ('memory_id', 'memory-2'),
    ('artifact_id', None), ('task_familiarity', 13), ('reciprocal_revision', Presence.PRESENT),
    ('history_rounds', 99), ('information_units', 25), ('prompt_format_id', 'other-format'),
])
def test_each_critical_factor_is_representable_but_uncontrolled_drift_is_rejected(field, value):
    d = example()
    changed = replace(d.short.configuration, **{field: value})
    assert getattr(changed, field) == value
    with pytest.raises(StudyError, match='critical factor'):
        replace(d, short=replace(d.short, configuration=changed))


def test_matched_history_removal_is_representable_without_claiming_transfer():
    d = example()
    config = replace(d.full.configuration, history_id=None, history_rounds=0,
                     artifact_id=None, memory_id=None)
    d = replace(d, full=replace(d.full, configuration=config), short=replace(d.short, configuration=config),
                rival=replace(d.rival, negative_control=replace(d.rival.negative_control, configuration=config)))
    assert evaluate(d).interpretation == 'UNDERDETERMINED'


@pytest.mark.parametrize('field,value,reason', [
    ('evaluators_blind', False, 'leakage'), ('answer_key_exposed', True, 'leakage'),
    ('exposure_ids', frozenset({'alias'}), 'contamination'),
    ('exposure_ids', frozenset(), 'exposure'), ('synthetic', False, 'synthetic'),
    ('rival', None, 'rival'),
])
def test_invalid_design_is_fail_closed(field, value, reason):
    with pytest.raises(StudyError, match=reason):
        replace(example(), **{field: value})


def test_negative_control_must_be_present_and_can_actually_falsify():
    d = example()
    with pytest.raises(StudyError, match='negative control'):
        replace(d.rival, negative_control=None)
    with pytest.raises(StudyError, match='falsif'):
        replace(d, rival=replace(d.rival, negative_control=replace(d.rival.negative_control, answers=d.full.answers)))


def test_role_and_rater_collapses_are_rejected():
    d = example()
    with pytest.raises(StudyError, match='provenance'):
        replace(d.provenance, ai_formalization=d.provenance.human_origin)
    for identity in ('key-author', 'synthetic-human-1', 'model-snapshot-1'):
        with pytest.raises(StudyError, match='rater'):
            replace(d, short=replace(d.short, rater_id=identity))


def test_circular_measurement_and_validated_metric_promotion_are_rejected():
    d = example()
    with pytest.raises(StudyError, match='outcome'):
        replace(d.measurement, outcome_basis='CCTS_STATUS')
    with pytest.raises(StudyError, match='candidate'):
        replace(d.measurement, status='VALIDATED_METRIC')


def test_missing_probes_duplicates_and_foreign_answers_are_rejected():
    d = example()
    with pytest.raises(StudyError, match='probe'):
        replace(d.measurement, probes=d.measurement.probes[:-1])
    with pytest.raises(StudyError, match='probe'):
        replace(d.measurement, probes=d.measurement.probes[:-1] + (d.measurement.probes[0],))
    for answers in (d.short.answers[:-1], d.short.answers + (d.short.answers[0],),
                    (('alias', 'keyword overlap is not an option'),) + d.short.answers[1:]):
        with pytest.raises(StudyError, match='answer'):
            replace(d, short=replace(d.short, answers=answers))


def test_all_receipt_construction_paths_keep_fixed_claim_ceiling():
    m = import_module('aion_human_ai_longitudinal.longitudinal_falsification')
    d = example()
    result = m.FalsificationReceipt(d)
    for name in ('scientific_status', 'ccts_validation', 'human_learning', 'longitudinal_specific_effect',
                 'transfer', 'retention', 'causality', 'model_weight_change', 'shared_subjectivity'):
        assert getattr(result, name) == 'NOT_ESTABLISHED'
        with pytest.raises((ValueError, TypeError, StudyError)):
            replace(result, **{name: 'ESTABLISHED'})
    assert result.canonical_effect == 'NONE'
    assert result.deployment is False
    assert result.metric_status == 'CANDIDATE_OPERATIONALIZATION'
    assert result.representational_compression == result.reciprocal_revision_effect == 'HYPOTHESIS'
    with pytest.raises((ValueError, TypeError, StudyError)):
        m.FalsificationReceipt(d, scientific_status='ESTABLISHED')


@pytest.mark.parametrize('field,value', [('task_familiarity', True), ('history_rounds', -1),
                                       ('information_units', 1.5), ('reciprocal_revision', 'PRESENT'),
                                       ('human_id', ''), ('model_id', '   '), ('history_id', False)])
def test_malformed_configuration_does_not_silently_become_controlled(field, value):
    with pytest.raises(StudyError):
        replace(example().full.configuration, **{field: value})


def test_receipt_recomputes_after_design_replacement_not_copied_verdict():
    d = example()
    result = evaluate(d)
    new = replace(result, design=replace(d, short=replace(d.short, answers=d.full.answers)))
    assert new.interpretation == 'UNDERDETERMINED'
    assert new.short_correct == 6
    assert {f.name for f in fields(new) if f.init} == {'design'}


@pytest.mark.parametrize('rounds,want', [(1, 'UNDERDETERMINED'), (99, 'UNDERDETERMINED'),
                                       (100, 'NOT_SUPPORTED_IN_FIXTURE'), (101, 'NOT_SUPPORTED_IN_FIXTURE')])
def test_long_history_eligibility_uses_declared_fixture_threshold(rounds, want):
    d = example()
    config = replace(d.full.configuration, history_rounds=rounds)
    d = replace(d, full=replace(d.full, configuration=config), short=replace(d.short, configuration=config),
                rival=replace(d.rival, negative_control=replace(d.rival.negative_control, configuration=config)))
    assert evaluate(d).interpretation == want


def test_measurement_rater_drift_is_not_a_cue_effect():
    d = example()
    with pytest.raises(StudyError, match='rater'):
        replace(d, short=replace(d.short, rater_id='different-rater'))
    with pytest.raises(StudyError, match='rater'):
        replace(d, rival=replace(d.rival, negative_control=replace(d.rival.negative_control, rater_id='different-rater')))


@pytest.mark.parametrize('threshold', [0, 1, True, 100.5])
def test_history_eligibility_threshold_is_explicit_nontrivial_integer(threshold):
    with pytest.raises(StudyError, match='history'):
        replace(example(), minimum_history_rounds=threshold)
