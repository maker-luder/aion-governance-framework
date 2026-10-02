# CCTS validity study-design records

Status: `SYNTHETIC_STUDY_DESIGN_ONLY / SCIENTIFIC_HOLD`

This bounded engineering interface was added after the research-spec candidate
was written. The Human Owner authorized an engineering-first, testable design
surface; empirical implementation and scientific claims remain unjustified.

`ccts_validity_study_design.py` records two separate primary questions: whether
CCTS can be distinguished from neighboring interaction constructs, and whether
interactions associated with CCTS relate to an independently scored outcome.
It does not classify a transcript, compute agreement, estimate effects, ingest
participants, or decide whether either question is answered.

The discriminant plan binds candidate IDs and hard-negative case IDs to named
neighbor constructs, a coding-manual digest, a falsification-rule digest, two
declared independent coders and their blinding declarations. It also requires
the two hybrid near-misses: provenance/authority without reciprocal revision,
and reciprocal revision without reconstructable provenance. The case IDs and
digests are declarations only; the module neither retrieves source transcripts
nor verifies coding quality. A complete field-coverage flag requires a case
for each listed neighbor, but does not imply semantic distinction, coder
independence, reliability, construct novelty, or discriminant validity.

The outcome plan declares CCTS, matched non-CCTS, Human-alone and AI-alone
units; a primary outcome excluding structural CCTS status; scoring and held-out
task digests; two declared independent blinded raters; exposure-matching,
baseline-covariate and AI-quality plan digests. Delayed retention additionally
needs a positive delay. Independent Human outcomes require a declared Human
response under the existing AI-withheld agency condition; held-out transfer
requires its held-out condition. Coder and rater IDs must be disjoint. These
declarations do not prove actual blinding or unassisted behavior.

The module does not check that the same outcome can be
scored in each arm, match dose or difficulty, verify source artifacts, measure
the declared covariates, blind actual raters, or identify a causal effect.
Those details require a prospectively specified protocol, real observations,
independent adjudication and separate scientific review.

This additive design interface reuses the existing `StudyError` and
`AdmissionDisposition` types. It does not change CCTS admission, the existing
`EmpiricalProtocol`/coding gate, the five-arm `LearningContrastDesign`, Human
agency/AI-withheld controls, task-selection exposure audit, or longitudinal
runner. Those existing controls can inform a future empirical protocol; their
test passes are not reused as evidence for this one.

Run locally from this package directory:

```sh
python -m pytest -q tests/test_ccts_validity_study_design.py
python -m pytest -q tests
mypy --strict src/aion_human_ai_longitudinal
ruff check --config ../../ruff.toml src tests
```

The tests use synthetic IDs and dummy SHA-256-shaped strings. They verify
negative cases and claim separation, not real participants or observed Human
outcomes. Both audit flags refer only to declared field coverage. Scientific
disposition remains `HOLD`; canonical effect `NONE`; deployment `FALSE`, even
when an audit record is directly constructed.

```text
SYNTHETIC_DISCRIMINATION != EMPIRICAL_DISCRIMINANT_VALIDITY
SYNTHETIC_OUTCOME_FIXTURE != HUMAN_OUTCOME_OBSERVED
CCTS_VALIDATION = NOT_ESTABLISHED
HUMAN_LEARNING = NOT_ESTABLISHED
RETENTION = NOT_ESTABLISHED
TRANSFER = NOT_ESTABLISHED
CCTS_SPECIFIC_EFFECT = NOT_ESTABLISHED
CAUSALITY = NOT_ESTABLISHED
HUMAN_AI_SYNERGY = NOT_ESTABLISHED
```
