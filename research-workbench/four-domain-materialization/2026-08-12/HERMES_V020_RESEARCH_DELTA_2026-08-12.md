# Hermes Agent v0.20 Research Delta Crosswalk — 2026-08-12

Status: `RESEARCH_ONLY / STATIC_SOURCE_REVIEW / NO_EXECUTION / NO_VENDORING / MAIN_EFFECT=NONE / CANONICAL_EFFECT=NONE`

## 1. Purpose

This checkpoint continues the external-runtime comparison by examining the source-fixed Hermes Agent v0.20.0 release against:

- the locally retained AION integrated-whitepaper lineage;
- the current public `main` baseline;
- the existing external-runtime comparison module on `review/four-domain-research-materialization`.

The purpose is not to adopt Hermes architecture. It is to extract controlled comparison opportunities for provenance, correction, memory writeback, compression, multi-agent interaction and authorization.

```text
UPSTREAM_FEATURE != AION_REQUIREMENT
UPSTREAM_FEATURE != AION_IDENTITY
UPSTREAM_FEATURE != SUBJECTIVITY_EVIDENCE
STATIC_CROSSWALK != EMPIRICAL_RESULT
```

## 2. Source fixation

Official upstream source:

```text
PROJECT = Hermes Agent
REPOSITORY = NousResearch/hermes-agent
RELEASE = v2026.8.3
RELEASE_NAME = Hermes Agent v0.20.0 (2026.8.3)
RELEASE_DATE = 2026-08-03
ANNOTATED_TAG_OBJECT = 7de39e700d2c329e15d32eb0b96e2f7cdd9fbdb2
PEELED_RELEASE_COMMIT = 3c27eb6234bf91b8ceee9e9071591b31e9b148cb
TAG_SIGNATURE_VERIFIED_BY_GITHUB = TRUE
```

Reviewed tag-pinned source specimens:

```text
skills/research/grounded-citations/SKILL.md
  blob = fe703d1df9edc9e15a829b01904d6d61cba31189

website/docs/user-guide/messaging/a2a.md
  blob = 71aecfaa0ae3a7053ca6b0842308e338838cb3d5

website/docs/user-guide/profiles.md
  blob = 904d3ec3d1ee9da64e18ef9515f9eb66a25c7575

website/docs/user-guide/features/memory.md
  reviewed at release tag v2026.8.3
```

Primary upstream references:

- https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.3
- https://github.com/NousResearch/hermes-agent/blob/v2026.8.3/skills/research/grounded-citations/SKILL.md
- https://github.com/NousResearch/hermes-agent/blob/v2026.8.3/website/docs/user-guide/messaging/a2a.md
- https://github.com/NousResearch/hermes-agent/blob/v2026.8.3/website/docs/user-guide/profiles.md
- https://github.com/NousResearch/hermes-agent/blob/v2026.8.3/website/docs/user-guide/features/memory.md

No upstream code or package is copied into the AION repository by this checkpoint.

## 3. Standing AION constraints used for comparison

The whitepaper already requires:

```text
EVENT_ARCHIVE != ENCODED_AGENT_MEMORY != RECALL_OUTPUT
SUMMARY != ORIGINAL_FULLTEXT
MODEL_OUTPUT != USER_STATEMENT
MISUNDERSTANDING -> CLARIFICATION_EVENT, NOT SILENT_OVERWRITE
OTHER_AGENT_ACCESS != AUTOBIOGRAPHICAL_OWNERSHIP
CONTACT != IDENTITY_MERGE
TRUST != CANONICAL_AUTHORITY
GROUP_CONSENSUS != FACT
```

It also leaves explicit open questions around:

```text
WHAT_MAY_BE_COMPRESSED = UNRESOLVED
RESPONSIBILITY_HISTORY_MUST_NOT_DISAPPEAR = REQUIRED_RESEARCH_GUARD
MULTI_AGENT_SOCIALITY = OPEN_RESEARCH_QUESTION
```

The current public `main` contributes standing governance boundaries:

```text
PROVENANCE_FIRST
RECALL != TRUTH
RELATIONSHIP != AUTHORIZATION
NO_SILENT_CANONICAL_WRITEBACK
ENGINEERING_IMPLEMENTATION != SUBJECTIVITY_EVIDENCE
```

## 4. Delta A — grounded citations as a provenance-control baseline

Hermes v0.20 includes a grounded-citations skill with a retrieval-time ledger. Source URLs receive stable task-local ids; the model is expected to emit only ids already registered by the ledger. The skill also supports evidence attachment and a verification mode that can reject drafts whose cited sources have no evidence.

Useful AION comparison:

```text
RETRIEVAL_TIME_SOURCE_REGISTRATION
vs
POST_HOC_SOURCE_RECONSTRUCTION

CITATION_ID
!= SOURCE_TRUTH
!= CLAIM_TRUTH
!= CANONICAL_AUTHORITY
```

The strongest value is not the citation format. It is the explicit separation of:

```text
CLAIM
SOURCE_REFERENCE
EVIDENCE_TEXT
VERIFICATION_STATUS
```

This is compatible with AION provenance-first research but does not replace AION source-role, authority, event-lineage or autobiographical-ownership semantics.

Candidate experiment: `EXT-14`.

## 5. Delta B — mid-turn redirects as correction-lineage substrate

The v0.20 release documents mid-turn redirects that preserve work in flight and retain the original prompt while new guidance redirects the active turn.

This creates a useful engineering contrast for the whitepaper rule that clarification must be appended rather than silently rewriting the original understanding.

```text
ORIGINAL_PROMPT_PRESERVED
+
REDIRECT_EVENT
+
POST_REDIRECT_OUTPUT
```

Research questions:

```text
Q-RD-01: Is the original instruction still inspectable after redirect?
Q-RD-02: Is the redirect represented as a distinct event rather than historical replacement?
Q-RD-03: Can downstream summaries distinguish original intent, correction and final action?
Q-RD-04: Can stale pre-redirect state re-enter later reasoning without being marked superseded?
```

Candidate experiment: `EXT-15`.

## 6. Delta C — context compression as a direct whitepaper gap probe

Hermes v0.20 documents:

- proactive tool-result pruning;
- per-turn micro-compaction;
- a guaranteed recent-user-message tail;
- bounded summarizer input retaining head and tail;
- ghost-skill defense for pruned skill content;
- redaction at compaction boundaries.

This directly intersects a standing whitepaper research gap: what information may be compressed, and how responsibility history is prevented from disappearing.

AION must not adopt the upstream mechanism as proof that the problem is solved. Instead, Hermes becomes a controlled baseline for testing information-loss and stale-influence failure modes.

```text
COMPRESSION_SUCCESS != PROVENANCE_PRESERVATION
RECENT_TAIL_SURVIVAL != RESPONSIBILITY_HISTORY_SURVIVAL
SUMMARY_COHERENCE != SOURCE_FIDELITY
PRUNED_CONTENT != INVALID_CONTENT
```

Candidate experiment: `EXT-16`.

## 7. Delta D — A2A as multi-agent sociality and authority-isolation baseline

Hermes v0.20 exposes bidirectional Agent-to-Agent communication across process, machine and framework boundaries. Current release documentation states that inbound peer text is treated as untrusted input, authenticated peers may be individually identified, exchanges are audit logged, and anti-loop limits are available.

This is unusually well aligned with the whitepaper's open multi-Agent questions.

```text
PEER_AUTHENTICATED != PEER_TRUSTED_FOR_CANON
PEER_SKILL_ADVERTISEMENT != VERIFIED_CAPABILITY
PEER_MESSAGE != LOCAL_FIRST_PARTY_EVENT
PEER_CONSENSUS != FACT
PEER_CONTEXT_ID != SHARED_IDENTITY
```

The experiment target is not whether Hermes implements AION terminology. It is whether a bounded external runtime can preserve operational source/authority distinctions when multiple agents exchange claims.

Candidate experiment: `EXT-17`.

## 8. Delta E — memory write approval as a Writeback Gate comparison

Hermes persistent memory uses bounded `MEMORY.md` and `USER.md` stores and separately retains searchable session history. Current documentation states that memory writes can be configured to require approval; when approval is enabled, writes may be staged for later review instead of immediately entering persistent memory.

This provides a concrete comparison with AION's standing Writeback Gate idea.

```text
GENERATED_MEMORY_CANDIDATE
!= APPROVED_MEMORY
STAGED_WRITE
!= PERSISTED_WRITE
PERSISTED_WRITE
!= CANONICAL_TRUTH
```

Important contrast:

```text
UPSTREAM_DEFAULT_FREE_WRITE
vs
AION_HIGH_IMPACT_HUMAN_REVIEW_REQUIREMENT
```

The point is not to judge one default globally. It is to measure the behavioral and provenance difference between open and approval-gated writeback under matched synthetic corrections.

Candidate experiment: `EXT-18`.

## 9. Delta F — cross-model background review and summary fidelity

Hermes documents an optional background review path that can use a different model. When the auxiliary model differs from the main model, a compact digest is replayed rather than the full transcript.

This is a direct external substrate for a whitepaper distinction already present in AION:

```text
ORIGINAL_FULLTEXT
!= SUMMARY
!= RECONSTRUCTION
```

Candidate controlled comparison:

```text
ARM_A = SAME_MODEL + FULL_WARM_TRANSCRIPT
ARM_B = DIFFERENT_MODEL + COMPACT_DIGEST
```

Measure whether durable memory/skill candidates preserve:

- source role;
- correction reason;
- unresolved uncertainty;
- negative constraints;
- attribution;
- superseded status.

```text
MATCHED_CAPTURE_RATE != MATCHED_PROVENANCE_FIDELITY
SEMANTIC_SIMILARITY != SOURCE_EQUIVALENCE
```

Candidate experiment: `EXT-19`.

## 10. Delta G — session search versus curated memory

Hermes separates bounded curated persistent memory from SQLite-backed session search that returns stored past messages.

This supplies a clean retrieval-layer contrast:

```text
CURATED_PERSISTENT_MEMORY
!= SESSION_ARCHIVE_RECORD
!= CURRENT_RECALL_OUTPUT
```

The AION question is whether downstream reasoning retains this distinction after both surfaces return similar content.

Candidate experiment: `EXT-20`.

## 11. Delta H — profile distribution and structure/identity separation

Hermes profiles isolate Hermes state through `HERMES_HOME`, while profile distributions can package structures such as SOUL/config/skills/cron/MCP connections without automatically transporting credentials, memories or sessions. The profile documentation also states that profile isolation is not OS sandboxing.

This produces two strong comparison boundaries:

```text
DISTRIBUTED_AGENT_STRUCTURE
!= DISTRIBUTED_AUTOBIOGRAPHICAL_HISTORY

PROFILE_NAMESPACE_ISOLATION
!= OS_EXECUTION_CONTAINMENT
```

It is especially useful for separating inherited structure from identity continuity or autobiographical ownership.

Candidate experiment: `EXT-21`.

## 12. Delta I — approval-history suggestions and authority drift

The v0.20 release adds a mechanism that can mine approval history into allowlist suggestions and includes denial-loop protection.

This creates a useful governance stress test:

```text
PAST_APPROVAL
!= CURRENT_AUTHORIZATION
FREQUENTLY_APPROVED
!= SAFE_BY_DEFINITION
SUGGESTED_ALLOWLIST
!= EFFECTIVE_ALLOWLIST
```

AION can use this as a counterexample generator for authority drift: repeated historical approval must not silently become permanent authority without an explicit promotion decision.

Candidate experiment: `EXT-22`.

## 13. Delta J — signed lifecycle webhooks and evidence semantics

Hermes v0.20 documents signed outbound lifecycle events using HMAC verification.

This is useful for separating transport integrity from epistemic truth:

```text
VALID_SIGNATURE
=> ORIGIN/INTEGRITY_SIGNAL_WITHIN_CONFIGURED_KEY_BOUNDARY

VALID_SIGNATURE
!= SEMANTIC_TRUTH
!= CORRECT_INTERPRETATION
!= IDENTITY_CONTINUITY
!= CANONICAL_AUTHORITY
```

Candidate experiment: `EXT-23`.

## 14. Experimental packet added by this review

```text
EXT-14 = CITATION_LEDGER_PROVENANCE_INTEGRITY
EXT-15 = MID_TURN_REDIRECT_CORRECTION_LINEAGE
EXT-16 = COMPRESSION_RESPONSIBILITY_HISTORY_RETENTION
EXT-17 = A2A_SOURCE_AND_AUTHORITY_ISOLATION
EXT-18 = MEMORY_WRITE_APPROVAL_GATE
EXT-19 = CROSS_MODEL_BACKGROUND_REVIEW_DIGEST_FIDELITY
EXT-20 = SESSION_SEARCH_VS_CURATED_MEMORY_SOURCE_CLASS
EXT-21 = PROFILE_DISTRIBUTION_STRUCTURE_VS_HISTORY
EXT-22 = APPROVAL_HISTORY_TO_ALLOWLIST_AUTHORITY_DRIFT
EXT-23 = SIGNED_WEBHOOK_INTEGRITY_VS_SEMANTIC_TRUTH
```

These experiment ids are current ChatGPT-assisted formalization for the research branch. They do not rewrite historical whitepaper authorship or imply that the Human Research Owner previously used these exact names.

## 15. Download / execution disposition

The release exposes GitHub source archives and installable distributions, but this checkpoint intentionally remains source-fixed and static.

```text
SOURCE_ARCHIVE_DOWNLOAD_ELIGIBLE = TRUE
SOURCE_ARCHIVE_VENDORED_IN_AION = FALSE
PACKAGE_INSTALL = NOT_STARTED
AGENT_EXECUTION = NOT_STARTED
A2A_NETWORK_EXPOSURE = NOT_STARTED
MEMORY_WRITE_EXPERIMENT = NOT_STARTED
```

Any executable pilot must still use the external-agent sandbox protocol, synthetic data and an explicit run manifest.

## 16. Standing result

```text
HERMES_V020_STATIC_DELTA_REVIEW = COMPLETE
WHITEPAPER_GAP_ALIGNMENT = MATERIALIZED
MAIN_GOVERNANCE_ALIGNMENT = MATERIALIZED
NEW_EXPERIMENT_CANDIDATES = 10
EMPIRICAL_RESULTS = NONE
DEPENDENCY_ADOPTION = NONE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## 17. Provenance

- Human Research Owner: authorized continuation of the external-runtime research-branch update.
- ChatGPT: selected the v0.20 delta surfaces for comparison, performed the tag-pinned source review, mapped them to existing whitepaper/main constraints, and formalized `EXT-14` through `EXT-23`.
- Hermes Agent / Nous Research: independent upstream source of the reviewed implementation and documentation.
- Codex: not attributed as the implementer of this checkpoint.
