# Initial failure record

The first artifact-lineage adversarial test for `state-order-invalid` reused the `event:1` identifier and therefore triggered `DUPLICATE_EVENT_ID` before the intended state-order check. This was a synthetic fixture-construction defect, not evidence about transformation lineage. The test and experiment runner were corrected to use unique event IDs with contiguous indices while placing `COMPLETE` before `START`; the intended `RUN_STATE_ORDER_INVALID` contract is then exercised. The initial observation is retained rather than deleted.
