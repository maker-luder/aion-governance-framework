# Factorial-completeness initial failure

The first factorial-completeness run produced 12 passing tests and 1 failed test. `test_cell_order_is_canonicalized_to_declared_factor_order` expected a valid cell mapping whose tuple order was reversed to be canonicalized.

The implementation instead treated `tuple(cell_map) != factor_names` as malformed, even though the mapping contained the same factor names. This was an implementation defect in the prototype's order check, not a scientific result. The intended contract is to compare factor-name sets for validity and then canonicalize keys into declared factor order. The test and failure are retained while the implementation is corrected.
