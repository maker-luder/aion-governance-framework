# Incident response sequence

```text
STOP TASK
→ ISOLATE RUNTIME
→ REVOKE TOOLS AND NETWORK
→ PRESERVE IMMUTABLE LOGS AND HASHES
→ ARCHIVE AFFECTED CANDIDATE BRANCH
→ ROTATE POSSIBLY EXPOSED CREDENTIALS
→ COMPARE GIT AND FILE DIFFERENCES
→ OPEN NCR
→ ROOT CAUSE ANALYSIS
→ CAPA
→ OWNER RECOVERY DECISION
```

The involved agent must not erase logs, destroy evidence, self-approve recovery or decide its own final incident status.
