# Task State Machine

States are the closed `TaskStatus` enumeration. `transition_task` accepts only the declared transition table and appends a hash-chained audit event.

Key invariants:

- approval precedes implementation;
- `BLOCKED` cannot self-resume;
- review packet ready is not submission;
- validation pass is not canonical;
- package creation is not deployment;
- rejected/cancelled/hold states only close;
- stop condition ends at `CLOSED`.
