# QA gates

Release from QA HOLD requires all of the following:

- source classification reviewed;
- task budget present;
- workspace boundary configured;
- network default deny confirmed;
- credential access denied;
- trajectory stop flags tested;
- immutable evidence path configured;
- rollback and incident sequence tested;
- Identity/Lineage Writeback Gate passes;
- human owner approval reference exists.

Missing values fail closed to `QA_HOLD`.
