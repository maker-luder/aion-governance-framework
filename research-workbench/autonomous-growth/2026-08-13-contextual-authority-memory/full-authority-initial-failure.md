# Full-authority semantics initial failure

The first full-authority test run produced 17 passing tests and 1 failed test. The cycle fixture correctly returned `DENY`, but the reason was `PARENT_PARENT_DELEGATION_CYCLE` rather than the expected direct reason `DELEGATION_CYCLE`.

The underlying mechanism detected the delegation cycle correctly. The mismatch was caused by recursive parent-reason prefixing, which made reason codes less stable and duplicated the `PARENT_` prefix. This is an implementation/reporting defect, not evidence about authority or delegation in the world. The correction will preserve the direct cycle reason while retaining parent context for non-cycle failures.
