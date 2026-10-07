# Public Privacy Minimization / 公開隱私最小化

Status: `ACTIVE_CONTROL / CURRENT_TREE_AND_FUTURE_CHANGE`

This control governs what personal or linkable information may appear in the public repository.
It does not retroactively rewrite Git history.

```text
PUBLIC_REPOSITORY != PRIVATE_CHAT_ARCHIVE
PROVENANCE != REAL_WORLD_IDENTITY
SOURCE_ATTRIBUTION != PERMISSION_TO_PUBLISH_PRIVATE_IDENTITY
CURRENT_TREE_REDACTION != HISTORY_PURGE
HISTORY_REWRITE = SEPARATE_DESTRUCTIVE_GATE
```

## 1. Public actor labels

Public governance and research records should use role labels such as:

- `HUMAN_USER`
- `HUMAN_OWNER` where historically required by the repository vocabulary
- `CHATGPT_TEACHER`
- `CHATGPT_WORK`
- `CODEX`
- `SOURCE_UNVERIFIED`

Chat nicknames, private relationship names, and other aliases that increase linkability are not required
for provenance and should not be retained in public records.

## 2. Excluded private/linkable data

Unless there is separate explicit publication authorization and a demonstrated need, public records exclude:

- chat nicknames and private aliases;
- private teacher, peer, coworker, family, or relationship identities;
- private email addresses, phone numbers, home addresses, recovery details, credentials, or account secrets;
- private birth details and private astrological/Bazi inputs;
- private conversation transcripts and unnecessary exact chat timestamps/timezones tied to an identifiable person;
- local absolute user paths, device-specific private logs, and private account metadata.

## 3. Allowed public-source information

This control does not erase legitimate external-source provenance.
Names, affiliations, citation metadata, and contact details already present in reviewed public papers,
public-domain texts, or upstream source snapshots may be retained when needed to identify the external source.
They must not be silently reclassified as the Human user's identity.

Explicitly confirmed scholarly/public author metadata is also separate from private chat identity.

## 4. Synthetic and generic data

A timezone, city, date, name-like token, or email-shaped fixture is not automatically personal data.
Synthetic fixtures, `.invalid` addresses, public-source records, and generic timezone examples may remain
when their synthetic/source role is explicit and they are not linked to a private person.

## 5. Git metadata

Future commits should use a privacy-preserving GitHub noreply author address where feasible.
The repository security audit reports a non-noreply HEAD author email without printing the address.

Historical commit-author email exposure cannot be removed by an ordinary PR. A full purge requires
history rewriting, force-push coordination, and possible GitHub support/cache cleanup. That operation
must not occur without a separate explicit destructive-history authorization.

## 6. PR and review text

Public PR bodies and review receipts should record the minimum information needed to establish authority:

```text
ACTOR_LABEL = HUMAN_USER
IDENTITY_VERIFICATION = NOT_CLAIMED
AUTHORIZATION_SCOPE = EXACT_HEAD_ONLY
CANONICAL_IDENTITY_LINK = NONE
```

Do not include a private chat nickname, exact local chat time, or local timezone merely to make an
authorization receipt look more specific.

## 7. Redaction and integrity

When a current governed source is privacy-redacted:

1. redact only the unnecessary identifying/linkable material;
2. preserve research meaning where possible;
3. update the current source digest/version that intentionally binds the current bytes;
4. do not rewrite historical evidence records that correctly describe older bytes;
5. record that current-tree sanitization is not a complete Git-history purge.

```text
DATA_MINIMIZATION = REQUIRED
LINKABILITY_REDUCTION = REQUIRED
HISTORICAL_EVIDENCE_FALSIFICATION = PROHIBITED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
HUMAN_OWNER_REVIEW_REQUIRED
```
