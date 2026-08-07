# Stop Condition Policy

Success means all blocking Gate 0, Gate 1 and Gate 2 criteria pass and candidate packages verify. Blocking findings stop delivery. Non-blocking items are recorded without opening another engineering round. Deferred items remain out of scope.

After `PASS_PENDING_OWNER_REVIEW`, the task closes. It does not promote, deploy or start the next phase.
