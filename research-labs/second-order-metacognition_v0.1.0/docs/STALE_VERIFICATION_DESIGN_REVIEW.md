# Stale Verification Design Review

Status: `KEEP_DEFERRED`

Staleness requires a stable binding between the old evidence target and the current request. The current target identifies one first-order prediction and one trial. It does not encode a safe cross-trial identity relation, validity interval, supersession rule, or proof that the underlying target remained unchanged.

Required before implementation:

1. a typed target identity and version;
2. evidence validity interval and observation time;
3. an explicit same-target predicate across requests;
4. supersession and contradiction handling;
5. fail-closed behavior for absent or contaminated provenance.

Until those elements exist, evidence valid for a prior trial does not bind to a current request. `VERIFICATION_STALE` remains deferred rather than silently reusing evidence.
