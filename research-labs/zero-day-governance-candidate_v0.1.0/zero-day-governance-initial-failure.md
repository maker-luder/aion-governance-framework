# Initial failures — Zero-Day Governance candidate v0.1.0

The first test run produced `18 passed, 5 failed`.

Three failures were test-fixture construction defects: `full_regression_event` supplied default keyword arguments and override keywords simultaneously, producing Python `TypeError` for lifecycle-order, containment-uncertainty, control-reference, and regression-reference cases. The helper will be rewritten to merge a base dictionary before constructing the event.

One failure exposed an expected-reason precedence mismatch in the prior-art classifier. A framework mapping that covered the entire declared lifecycle and had no proposed incremental fields returned `REDUNDANT_TERMINOLOGY / EXISTING_FRAMEWORKS_COVER_DECLARED_LIFECYCLE`, while the test expected the more specific incremental-fields reason. The implementation is retained as the observed contract; the test will be aligned to the explicit no-increment branch.

The failures are mechanism/test-contract observations, not evidence establishing or rejecting Zero-Day Governance. No external system, model, deployment, canonical state, or governance effect was invoked.
