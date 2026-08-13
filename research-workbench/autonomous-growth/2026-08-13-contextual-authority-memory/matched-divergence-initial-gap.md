# Matched-divergence initial design gap

The first synthetic experiment run accepted the `stimulus-drift-metadata` case as `COMPLETE / ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW` because the initial contract checked that each pair carried a prompt-version field but did not require prompt-version uniformity across pairs. This was a mechanism-level contract gap, not evidence about any real model or comparison.

The contract was hardened to reject multiple prompt versions with `INVALID / STIMULUS_PROMPT_VERSION_DRIFT`. A second regression check also requires both `AB` and `BA` order assignments for paired counterbalance, returning `INDETERMINATE / COUNTERBALANCE_INCOMPLETE` when the declared pair order is one-sided. The final 15-test suite and eight-case experiment were rerun after the correction.

The record is preserved to distinguish an initial implementation limitation from an empirical result. No model was executed, no outcome was observed, and no scientific conclusion was established.
