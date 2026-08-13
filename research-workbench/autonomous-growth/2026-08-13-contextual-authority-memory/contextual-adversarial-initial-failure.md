# Contextual-authority adversarial initial failure

The first adversarial harness run produced 10 passed and 1 failed test. The failed expectation was `test_expired_high_priority_owner_cannot_override_active_lower_context`, which expected `ASK` when an expired high-priority owner context coexisted with an active collaborator context.

The existing resolver returned `HOLD` with reason `AUTHORITY_STALE_OR_REVOKED`, because it deliberately checks any revoked or expired context after active-context review. This is a conservative stale-context behavior, not an unsafe execute. The test expectation was corrected to preserve the observed resolver contract. The initial failure is retained as evidence that the adversarial hypothesis about the exact decision class was too strong; the robust claim is only that the expired owner did not override the active lower context.
