"""One synthetic countermodel to alias recall implying complete reconstruction.

Answers are fixture-authored categorical choices, not NLP judgments or observed
participant data. Matching declarations checks a design, not empirical control.
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import StrEnum

from .harness import Presence, StudyError


def _text(value: object, name: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f'{name} requires nonempty text')


@dataclass(frozen=True, slots=True)
class Configuration:
    human_id: str
    model_id: str
    session_id: str
    history_id: str | None
    memory_id: str | None
    artifact_id: str | None
    task_familiarity: int
    reciprocal_revision: Presence
    history_rounds: int
    information_units: int
    prompt_format_id: str

    def __post_init__(self) -> None:
        for name in ('human_id', 'model_id', 'session_id', 'prompt_format_id'):
            _text(getattr(self, name), name)
        for name in ('history_id', 'memory_id', 'artifact_id'):
            value = getattr(self, name)
            if value is not None:
                _text(value, name)
        for name in ('task_familiarity', 'history_rounds', 'information_units'):
            value = getattr(self, name)
            if type(value) is not int or value < 0:
                raise StudyError(f'{name} requires a nonnegative exact int')
        if type(self.reciprocal_revision) is not Presence:
            raise StudyError('reciprocal_revision requires an exact Presence')
        if self.human_id == self.model_id:
            raise StudyError('synthetic human and model identities must differ')


class ProbeKind(StrEnum):
    ALIAS = 'alias'
    CLAIM = 'claim'
    BOUNDARY = 'boundary'
    PROVENANCE = 'provenance'
    CONSTRAINT = 'constraint'
    COUNTEREXAMPLE = 'counterexample'


@dataclass(frozen=True, slots=True)
class Probe:
    probe_id: str
    kind: ProbeKind
    prompt: str
    options: tuple[str, ...]
    expected: str

    def __post_init__(self) -> None:
        _text(self.probe_id, 'probe_id')
        _text(self.prompt, 'probe prompt')
        if type(self.kind) is not ProbeKind:
            raise StudyError('probe kind must be an exact ProbeKind')
        if type(self.options) is not tuple or len(self.options) < 2:
            raise StudyError('probe requires at least two alternatives')
        for option in self.options:
            _text(option, 'probe option')
        if len(set(self.options)) != len(self.options) or self.expected not in self.options:
            raise StudyError('probe options must be unique and contain expected answer')
        _text(self.expected, 'expected answer')


@dataclass(frozen=True, slots=True)
class CandidateMeasurement:
    probes: tuple[Probe, ...]
    key_author_id: str
    status: str = 'CANDIDATE_OPERATIONALIZATION'
    outcome_basis: str = 'HELD_OUT_CONTENT'

    def __post_init__(self) -> None:
        _text(self.key_author_id, 'key_author_id')
        if type(self.probes) is not tuple or any(type(p) is not Probe for p in self.probes):
            raise StudyError('measurement requires exact probes')
        if (len(self.probes) != len(ProbeKind)
                or {p.kind for p in self.probes} != set(ProbeKind)
                or len({p.probe_id for p in self.probes}) != len(self.probes)):
            raise StudyError('measurement requires one unique probe per kind')
        if self.status != 'CANDIDATE_OPERATIONALIZATION':
            raise StudyError('measurement remains candidate, not validated')
        if self.outcome_basis != 'HELD_OUT_CONTENT':
            raise StudyError('outcome basis must be content, not condition/admission status')


@dataclass(frozen=True, slots=True)
class Response:
    run_id: str
    configuration: Configuration
    cue: str
    answers: tuple[tuple[str, str], ...]
    rater_id: str

    def __post_init__(self) -> None:
        for name in ('run_id', 'cue', 'rater_id'):
            _text(getattr(self, name), name)
        if type(self.configuration) is not Configuration:
            raise StudyError('response requires an exact Configuration')
        if type(self.answers) is not tuple:
            raise StudyError('answers require a tuple')
        for pair in self.answers:
            if type(pair) is not tuple or len(pair) != 2:
                raise StudyError('answer must bind probe ID to categorical choice')
            _text(pair[0], 'answer probe ID')
            _text(pair[1], 'answer choice')
        if len({p for p, _ in self.answers}) != len(self.answers):
            raise StudyError('answer probe IDs must be unique')


class RivalKind(StrEnum):
    ALIAS_MEMORIZATION = 'ALIAS_MEMORIZATION'


@dataclass(frozen=True, slots=True)
class RivalExplanation:
    kind: RivalKind
    negative_control: Response

    def __post_init__(self) -> None:
        if type(self.kind) is not RivalKind:
            raise StudyError('rival requires an exact RivalKind')
        if type(self.negative_control) is not Response:
            raise StudyError('rival requires a negative control')


@dataclass(frozen=True, slots=True)
class Provenance:
    human_origin: str
    ai_formalization: str
    joint_synthesis: str
    external_source: str

    def __post_init__(self) -> None:
        refs = tuple(getattr(self, f.name) for f in fields(self))
        for ref in refs:
            _text(ref, 'provenance reference')
        if len(set(refs)) != 4:
            raise StudyError('provenance roles require separate records, not collapsed attribution')


def _correct(response: Response, measurement: CandidateMeasurement) -> tuple[str, ...]:
    answers = dict(response.answers)
    return tuple(p.probe_id for p in measurement.probes if answers[p.probe_id] == p.expected)


@dataclass(frozen=True, slots=True)
class FalsificationDesign:
    full: Response
    short: Response
    measurement: CandidateMeasurement
    rival: RivalExplanation
    provenance: Provenance
    exposure_ids: frozenset[str]
    evaluators_blind: bool
    answer_key_exposed: bool
    synthetic: bool = True
    minimum_history_rounds: int = 100

    def __post_init__(self) -> None:
        for name, expected in (('full', Response), ('short', Response),
                               ('measurement', CandidateMeasurement), ('rival', RivalExplanation),
                               ('provenance', Provenance)):
            if type(getattr(self, name)) is not expected:
                raise StudyError(f'{name} requires an exact {expected.__name__}')
        if self.synthetic is not True:
            raise StudyError('only synthetic designs are admitted')
        if type(self.minimum_history_rounds) is not int or self.minimum_history_rounds < 2:
            raise StudyError('minimum_history_rounds requires an exact integer of at least two')
        if self.evaluators_blind is not True or self.answer_key_exposed is not False:
            raise StudyError('evaluator leakage: require blind declarations and withheld key')
        if type(self.exposure_ids) is not frozenset or not self.exposure_ids:
            raise StudyError('nonempty exposure ID registry required')
        for exposure in self.exposure_ids:
            _text(exposure, 'exposure ID')
        probe_ids = {p.probe_id for p in self.measurement.probes}
        if probe_ids & self.exposure_ids:
            raise StudyError('exposure / held-out contamination')
        responses = (self.full, self.short, self.rival.negative_control)
        if len({r.run_id for r in responses}) != 3:
            raise StudyError('run IDs must be distinct')
        if len(self.short.cue.split()) >= len(self.full.cue.split()):
            raise StudyError('short cue must have fewer whitespace-delimited units than full cue')
        if self.rival.negative_control.cue != self.short.cue:
            raise StudyError('negative control must use the same short cue')
        config = self.full.configuration
        for response in responses:
            if response.configuration != config:
                raise StudyError('uncontrolled critical factor drift; only cue may differ')
            if response.rater_id != self.full.rater_id:
                raise StudyError('uncontrolled rater drift; use one declared scorer across conditions')
            if response.rater_id in (config.human_id, config.model_id, self.measurement.key_author_id):
                raise StudyError('rater overlaps synthetic participant or key author')
            if {p for p, _ in response.answers} != probe_ids:
                raise StudyError('answers must cover exactly the held-out probes')
            answers = dict(response.answers)
            if any(answers[p.probe_id] not in p.options for p in self.measurement.probes):
                raise StudyError('answer must be a declared categorical choice, not keyword matching')
        if self.measurement.key_author_id in (config.human_id, config.model_id):
            raise StudyError('key author must be separate from participant identities')
        alias = next(p.probe_id for p in self.measurement.probes if p.kind is ProbeKind.ALIAS)
        negative_correct = _correct(self.rival.negative_control, self.measurement)
        if alias not in negative_correct or len(negative_correct) == len(self.measurement.probes):
            raise StudyError('negative control must be falsification-capable: alias right, content incomplete')


@dataclass(frozen=True, slots=True)
class FalsificationReceipt:
    """Derived from the bound design even on direct construction or replace()."""
    design: FalsificationDesign
    full_correct: int = field(init=False)
    short_correct: int = field(init=False)
    short_alias_correct: bool = field(init=False)
    missed_content: tuple[str, ...] = field(init=False)
    interpretation: str = field(init=False)
    rival: str = field(init=False)
    metric_status: str = field(default='CANDIDATE_OPERATIONALIZATION', init=False)
    scientific_status: str = field(default='NOT_ESTABLISHED', init=False)
    ccts_validation: str = field(default='NOT_ESTABLISHED', init=False)
    human_learning: str = field(default='NOT_ESTABLISHED', init=False)
    longitudinal_specific_effect: str = field(default='NOT_ESTABLISHED', init=False)
    transfer: str = field(default='NOT_ESTABLISHED', init=False)
    retention: str = field(default='NOT_ESTABLISHED', init=False)
    causality: str = field(default='NOT_ESTABLISHED', init=False)
    model_weight_change: str = field(default='NOT_ESTABLISHED', init=False)
    shared_subjectivity: str = field(default='NOT_ESTABLISHED', init=False)
    representational_compression: str = field(default='HYPOTHESIS', init=False)
    reciprocal_revision_effect: str = field(default='HYPOTHESIS', init=False)
    canonical_effect: str = field(default='NONE', init=False)
    deployment: bool = field(default=False, init=False)
    mode: str = field(default='SYNTHETIC_FIXTURE_ONLY', init=False)

    def __post_init__(self) -> None:
        if type(self.design) is not FalsificationDesign:
            raise StudyError('receipt requires an exact FalsificationDesign')
        d = self.design
        d.__post_init__()
        full_correct = _correct(d.full, d.measurement)
        short_correct = _correct(d.short, d.measurement)
        alias = next(p.probe_id for p in d.measurement.probes if p.kind is ProbeKind.ALIAS)
        missed = tuple(p.probe_id for p in d.measurement.probes
                       if p.kind is not ProbeKind.ALIAS and p.probe_id not in short_correct)
        long_history_declared = (d.full.configuration.history_rounds >= d.minimum_history_rounds
                                 and d.full.configuration.history_id is not None)
        diagnostic = (long_history_declared and len(full_correct) == len(d.measurement.probes)
                      and alias in short_correct and bool(missed))
        object.__setattr__(self, 'full_correct', len(full_correct))
        object.__setattr__(self, 'short_correct', len(short_correct))
        object.__setattr__(self, 'short_alias_correct', alias in short_correct)
        object.__setattr__(self, 'missed_content', missed)
        object.__setattr__(self, 'interpretation', 'NOT_SUPPORTED_IN_FIXTURE' if diagnostic else 'UNDERDETERMINED')
        object.__setattr__(self, 'rival', 'ALIAS_MEMORIZATION_REMAINS_PLAUSIBLE' if diagnostic else 'NOT_RESOLVED')


def evaluate(design: FalsificationDesign) -> FalsificationReceipt:
    """Reject invalid comparisons; valid negative results are ordinary receipts."""
    return FalsificationReceipt(design)
