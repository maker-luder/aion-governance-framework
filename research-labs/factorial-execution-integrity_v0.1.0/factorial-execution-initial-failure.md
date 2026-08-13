# Initial Failure Record — Factorial Execution Integrity

The first test run reported one failure in `test_execution_id_collision_is_invalid`. The test intended to create a duplicate `execution_id`, but its fixture used the new `run:1` followed by `complete_executions()[1:]`, which omitted the original `run:1`. The model therefore correctly observed no ID collision and returned `COMPLETE`; the failure was in the synthetic test construction, not in the execution-integrity contract.

The fixture was corrected to include both the original `run:1` and the duplicate `run:1`. The test is retained as a negative control and rerun after correction. This is a mechanism/test-construction audit item, not a scientific result.
