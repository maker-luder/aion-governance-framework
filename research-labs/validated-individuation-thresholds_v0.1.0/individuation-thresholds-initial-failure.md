# Initial failure — validated individuation thresholds v0.1.0

The first test run produced `15 passed, 1 failed`. The failing case was `test_missing_boundary_perturbation_metadata_is_indeterminate`.

Observed behavior:

```text
expected: INDETERMINATE / BOUNDARY_PERTURBATION_METADATA_MISSING
observed: HOLD / PROFILE_METADATA_INCOMPLETE
```

The implementation treated an empty `perturbations` tuple as generic profile metadata absence before reaching the dedicated boundary-perturbation branch. This was a contract-ordering defect, not a scientific result. The intended distinction is that a complete criterion profile with no declared perturbation metadata is uncertainty-limited (`INDETERMINATE`), while malformed perturbation entries remain `HOLD`. The correction removes `perturbations` from the generic required-field scan and retains its dedicated uncertainty decision.

The initial failure remains preserved for auditability. No system was executed and no threshold, identity, subjectivity, canonical, governance, or deployment conclusion was produced.
