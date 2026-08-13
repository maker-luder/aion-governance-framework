# Matched-divergence protocol source notes

## 1. NIST Engineering Statistics Handbook — Randomized block designs

URL: https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm

NIST describes blocking as controlling important nuisance factors while allowing the factor of interest to vary, and states the general rule: “Block what you can, randomize what you cannot.” The source distinguishes nuisance factors from the primary factor and recommends accounting for blocked factors in the analysis.

For a matched-divergence protocol, the contract therefore treats stimulus identity, prompt version, context, exposure budget, order, runtime/environment, and evaluator blinding as protocol factors. It does not estimate their effects; it only checks that the declared matching/blocking/randomization metadata is present and internally consistent.

## Design consequence

The next bounded unit should be `matched-divergence-protocol-integrity_v0.1.0`. It will audit a paired protocol without executing either model/system: paired stimulus digests, exposure parity, context parity, order/counterbalance declarations, outcome-blinding status, predeclared comparison rule, and no-leakage attestations. Missing or contradictory controls will return `HOLD`/`INVALID`; a complete protocol will be `ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW`, never a result.

## References

[1]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm "NIST — Randomized block designs"
