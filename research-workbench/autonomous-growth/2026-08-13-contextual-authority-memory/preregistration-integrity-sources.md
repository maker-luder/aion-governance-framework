# Preregistered intervention integrity source notes

## 1. Center for Open Science — Preregistration Challenge

URL: https://www.cos.io/initiatives/prereg-more-information

The COS resource requires reporting results of all preregistered analyses, clearly differentiating additional exploratory analyses from confirmatory analyses, and linking the preregistered project. This supports an integrity contract that records plan version, analysis class, deviations, and complete outcome reporting rather than silently relabeling exploratory work as confirmatory.

## 2. Existing COS preregistration source

URL: https://www.cos.io/initiatives/prereg

The prior source note for this autonomous cycle records that a pre-analysis plan is intended to keep confirmatory analysis decisions independent of observed results, while allowing explicitly identified deviations and exploratory work.

## Design consequence

The next bounded unit should be `preregistered-intervention-integrity_v0.1.0`. It will be a design and audit contract only: no human participants, real intervention, external model, or live study. It will validate immutable plan identity, temporal ordering, outcome/analysis declarations, deviation disclosure, confirmatory-versus-exploratory labels, and all-outcome reporting. It will return `HOLD` or `INDETERMINATE` for plan drift or incomplete reporting, never a scientific conclusion.

## References

[1]: https://www.cos.io/initiatives/prereg-more-information "Center for Open Science — More About the Preregistration Challenge"
[2]: https://www.cos.io/initiatives/prereg "Center for Open Science — Preregistration"
