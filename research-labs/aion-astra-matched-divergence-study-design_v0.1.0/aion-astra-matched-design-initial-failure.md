# Initial failures — AION/Astra matched-divergence study design v0.1.0

The first run produced `20 passed, 2 failed`.

The first failure exposed a head-semantics gap: a `reporting_head` equal to `tested_source_head` was accepted as complete, so the design did not enforce a visible distinction between execution source state and reporting state. The contract will explicitly hold this equality as `REPORTING_HEAD_MISLABELED_AS_TESTED_HEAD`.

The second failure exposed a completeness gap: an empty `source_evidence_refs` tuple was not treated as missing because the generic missing-value helper checked `None` and empty strings but not empty tuples. The contract will treat an empty evidence-reference collection as incomplete.

These are mechanism-level contract findings. They are not evidence of AION/Astra divergence, model behavior, source validity, scientific effect, subjectivity, identity continuity, or consciousness. No model executed and no result was observed.
