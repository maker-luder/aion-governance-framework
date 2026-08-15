# Independent IV&V readiness packet

Status: `PREPARE_EVIDENCE_ONLY` — this document does not claim that independent verification and validation has occurred.

## Reviewer entry points

An eventual independent reviewer should receive a fixed commit/tag and verify at least:

1. repository manifest and public/private boundary checks;
2. component unit tests and type checks from a clean environment;
3. governance policy decisions, approval gates and rollback behavior;
4. runtime baseline isolation and kill-switch behavior;
5. persistent-memory identity, access-scope, provenance, conflict, tombstone and write-approval behavior;
6. absence of automatic canonical writeback;
7. separation of AION and Astra identities/namespaces;
8. public deployment documentation and the feedback-channel privacy boundary;
9. held-scope enforcement: no public ablation execution, no sexual/intimate runtime, no 3D claim, no unverified hardware benchmark claim;
10. dependency and repository-wide license compatibility after the Owner chooses a license.

## Evidence to capture

For each verification run, record:

- reviewer identity/organization and independence statement;
- exact commit SHA and environment;
- Python/OS/tool versions;
- commands executed;
- raw test/type/scan output hashes;
- pass/fail/hold result per requirement;
- defects/NCRs and remediation references;
- final scope limitations and unverified claims.

## Current independent status

`INDEPENDENT_IVV = NOT_ACHIEVED`

Creator/assistant-side implementation, tests authored in the repository, or GitHub CI runs are useful engineering evidence but are not independent IV&V by themselves.
