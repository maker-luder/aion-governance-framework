# R3 HOLD / Quarantine Archive Manifest — 2026-08-18

> These files are inert historical diff snapshots. They are not executable source, not active MCP/runtime code, not deployment configuration, and not publication artifacts.

## Publication candidate

```text
SOURCE_BRANCH = publication/aion-astra-publication-v0.1-20260817
SOURCE_HEAD = 540d190e8b60e92e3b6af94ad8f96d06091c73b3
ARCHIVE_PATH = docs/research-consolidation/quarantine/2026-08-18/publication-aion-astra-v0.1-20260817.patch
PATCH_SHA256 = f5198ca3d57da0d8ed4235d8349af50752c3bc864200601aa59882710739c6cc
PATCH_BYTES = 55706
PROVENANCE_STATUS = PUBLICATION_CANDIDATE / HOLD_ARTIFACT
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
ACTIVE_PATH_MATERIALIZATION = NO
```

The snapshot preserves the branch-only delta without placing `vercel.json`, site runtime, or publication files in active executable paths. It does not authorize public deployment, publication, release, or canonical promotion.

## Provenance-uncertain MCP candidate

```text
SOURCE_BRANCH = feat/mcp-readonly-interface-20260817
SOURCE_HEAD = d5125c91da3cfa170f0651c0d2d44939fef2f070
ARCHIVE_PATH = docs/research-consolidation/quarantine/2026-08-18/feat-mcp-readonly-interface-20260817.patch
PATCH_SHA256 = 6781c41d6567eef1f22f0708be627c2435fc6e0109aa820c51cbeb989771d21f
PATCH_BYTES = 58320
PROVENANCE_STATUS = PROVENANCE_UNCERTAIN / QUARANTINED_RESEARCH_ARTIFACT
RUNTIME_ACTIVATION = NO
MEMORY_WRITE = NO
IDENTITY_AUTHORITY = NO
CANONICAL_EFFECT = NONE
PUBLIC_DEPLOYMENT = NO
ACTIVE_PATH_MATERIALIZATION = NO
```

The snapshot preserves the exact branch-only delta as non-executable evidence. It must not be imported into an active component path, exposed through MCP, treated as approved implementation, or used to establish runtime/identity authority.

## Preservation rule

Both source branches remain active transitional refs because PR #42 does not delete branches. The ledger may classify them as retirement candidates only after this durable preservation is verified and Human Owner confirms the exact deletion target list in a later phase.
