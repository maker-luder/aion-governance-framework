# Owner Approval Model

Approval requests bind task ID, permission, paths, commands, expiry and a canonical request hash. Grants must match the request and task and must be unexpired.

Permissions:

- `READ_ONLY_ANALYSIS`
- `CANDIDATE_WRITE`
- `DESTRUCTIVE_CHANGE` (operation-specific)
- `EXTERNAL_SUBMISSION` (manual Owner action only)
- `PROMOTION_OR_DEPLOYMENT` (prohibited in this candidate)
