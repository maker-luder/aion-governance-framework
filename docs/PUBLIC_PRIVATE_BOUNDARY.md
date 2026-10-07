# Public / Private Boundary

## Publicly included

- sanitized source code and deterministic fixtures;
- public-safe governance documents and schemas;
- status locks and reports without private paths or personal records;
- synthetic examples and tests;
- public provenance and non-claims;
- explicitly authorized scholarly/public identity metadata;
- necessary external-source citation metadata that belongs to public third-party sources.

## Excluded

- private ZIP archives and restricted documents;
- real conversation transcripts and private episodic memory;
- private names, chat nicknames, relationship identities, contact details, birth data and relationship records;
- credentials, tokens, recovery codes and private keys;
- model weights, private datasets and local model-store paths;
- local absolute paths and device-specific logs;
- unnecessary exact chat timestamps/timezones when they increase linkability to a private person;
- private canonical state and unapproved Human materials.

## Public provenance without private identity

A public research record may preserve that a contribution came from a Human without publishing a private
nickname or real-world identity.

```text
PROVENANCE != REAL_WORLD_IDENTITY
HUMAN_ORIGIN != CHAT_NICKNAME_REQUIRED
SOURCE_ATTRIBUTION != PRIVATE_RELATIONSHIP_DISCLOSURE
```

Use generic role labels such as `HUMAN_USER`, `HUMAN_OWNER` where historically required,
or `SOURCE_UNVERIFIED` when identity/source evidence is insufficient.

## Git metadata boundary

Future commits should use a privacy-preserving GitHub noreply author address where feasible.
Current-tree redaction does not remove email addresses already embedded in historical commit objects.

```text
CURRENT_TREE_REDACTION != HISTORY_PURGE
HISTORY_REWRITE = SEPARATE_DESTRUCTIVE_GATE
FORCE_PUSH_REQUIRES_EXPLICIT_AUTHORIZATION
```

Public extraction does not change the canonical status of private source packages.

See also: `docs/security/PUBLIC_PRIVACY_MINIMIZATION.md`.
