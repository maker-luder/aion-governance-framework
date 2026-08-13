# Initial Failure Record — Evidence Currentness and Deduplication

The first 15-case experiment run passed all 21 unit tests and all case reason/status expectations, but the experiment-level invariant assertion failed on the `boundary-effect` case. The ledger input intentionally requested `canonical_effect = WRITE`; the decision copied that requested value into its output record even though the decision reason was `BOUNDARY_EFFECT_REQUESTED` and status was `INVALID`.

This was a mechanism boundary leak, not a scientific result. The model was corrected so every `LedgerDecision` normalizes `canonical_effect = NONE`, `governance_effect = NONE`, and `deployment = FALSE`, while preserving the invalid reason and hold disposition. The full 21-test and 15-case experiment was rerun successfully after the correction.

The record is retained because it demonstrates that a fail-closed reason alone is insufficient if output metadata still carries a requested effect. No canonical or governance effect occurred.
