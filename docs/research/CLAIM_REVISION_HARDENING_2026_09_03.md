# Claim revision: bounded local hardening (2026-09-03)

This addendum supersedes only the engineering details below in
[the initial candidate design](CLAIM_REVISION_2026_09_03.md). It does not promote
the candidate, confer authority or change scientific conclusions. The persistent
owner remains `SQLiteMemoryStore`; `ClaimRevisionService` and its internal
`revision_integrity` helper share that database. The agenda adapter reuses the
existing `AgendaEntry`/`CONTRADICTION` format. No second research loop, canonical
schema, eighth functional state or subjectivity score is introduced.

## Graph and review contract

Dependencies name **exact memory versions**, not the latest logical claim.
Direct parents and their transitive ancestors are tracked as a bounded DAG.
Sorted iterative Kahn traversal rejects missing nodes, self/long cycles, repeated
logical-claim ancestors and excess longest-path depth. Sorting does not erase the
meaning of an ordered event sequence. Propagation includes historical retired
nodes as traversal bridges, preserves their retired status and leaves unrelated
siblings untouched. Already challenged nodes stay challenged.

Repairing A1 by creating A2 does not release B1 or C1 that used A1/B1. An explicit
review must create B2 with dependency A2; C1 remains pending until a separate
review creates C2 against B2. RETAIN creates a successor with unchanged wording;
REVISE creates a successor with new wording/reason and explicitly supplied
assumptions/dependencies. WITHDRAW preserves history without creating a successor.
None of these decisions establishes truth or rejects an entire domain.

Writes use the existing SQLite `BEGIN IMMEDIATE` transaction and explicit local
approval flag. Graph/status/evidence/event consistency is checked before and after
each mutation; exceptions roll back and connections close in `finally`. The
namespace event head is the conservative compare-and-set epoch: any intervening
event makes a review stale, even if it concerns a different claim. Versioned memory
IDs, linear predecessor checks and unique constraints prevent silent successors
forking. SQLite lock failures also propagate rather than silently retrying/overwriting.

Pending requests and agenda entries are **derived reads**, not separately inserted
rows. Failure while constructing an agenda leaves the previous complete database
transaction committed, not a partially created agenda. No background worker,
network access, shell execution, repository writer or model is invoked.

## Evidence is not a vote

An exact evidence ID/payload delivery is idempotent; a changed payload on that ID
is rejected. Different IDs with identical content digests are retained with a
duplicate-group annotation, not collapsed into one retrieval and not counted as
independent corroboration. SHA-256 values are caller supplied: content bytes are
not fetched or verified against an external source by this library.

`EvidenceLink` keeps its original required fields and appends optional
`derived_from`, `publisher`, `retrieval_agent`, `retrieval_event_id`. Source IDs
and declared parents form another **provenance DAG**, not a new research ontology.
Contradictory declared parent lists and cycles reject the whole write. Missing
parent descriptions remain terminal declared labels, not certified originals.
Absent/empty lineage means unknown, not proven independence. Same-paper retrieval
by AION and Astra is still the same underlying declared source. No URL heuristic
infers independence and no language model adjudicates the bounded relation enum.

```text
CONTENT_DEDUP_IMPLEMENTED = YES (digest grouping; no source-byte verification)
LOGICAL_DEDUP_IMPLEMENTED = NO
SOURCE_LINEAGE_TRACKING = YES (caller-declared)
AUTOMATIC_SOURCE_INDEPENDENCE_JUDGMENT = NO
CONTRADICTION_RELATION = CALLER_DECLARED / STRUCTURED
REVISION_AGENDA_ITEM != AUTOMATIC_EXECUTION
```

Requests include claim/version, direct parents, transitive evidence references,
explicit counterevidence IDs, affected upstream memory IDs and exact event head.
The adapter exposes these as existing agenda source references. Consuming such an
item remains subject to the existing research budgets and governance.

## Canonical replay and corruption checks

New events carry `canonicalization=CLAIM_REVISION_V2`:

| Input | Rule |
|---|---|
| JSON object keys | Lexicographically sorted, compact UTF-8 JSON, no NaN/infinity |
| Human text | Content/replacement content, rationale, reason, assumptions, publisher: NFC and LF |
| IDs and locators | IDs require NFC, 1..200 nonblank characters, no control/format/surrogate characters; never silently rewrite IDs or URIs |
| Timestamps | Explicit caller-supplied aware ISO time, normalized to UTC with microseconds |
| Null/missing | Distinct generally; appended optional evidence fields receive documented defaults before comparison |
| Boolean/integer | JSON types remain distinct; no bool-as-int for versions/budgets |
| Lists/tuples | Preserve order; assumptions remain ordered |
| Sets/floats/bytes | Rejected by the event canonicalizer; reference sets are sorted by callers before encoding |
| Dependencies/evidence refs | Distinct IDs, sorted before event serialization |
| Source parents | Distinct tuple normalized to sorted parent IDs |
| SQLite snapshots | Versions by claim/version, evidence by ID, events by sequence |
| Event ordering | Significant: reversing two different write operations is not promised to yield the same head |

Original stored wording and old V1 event payloads/hashes are not rewritten. V1
event projection retains V1 propagation semantics; new V2 events use the hardened
policy. Opening a real fd8f096-created disposable history, preserving all old
events, appending V2 and reopening is covered by a test. Old records that violate
new explicit bounds or identifiers are rejected, not silently repaired.

Reads/writes validate schema columns, graph, flags, lineage, bounded sizes and
hash chain. A second event-effect cross-check detects orphan/missing versions,
evidence deletion, unsupported kinds, inconsistent status/dependencies and event
suffix deletion that leaves inconsistent rows. This is bounded structural
validation, not full semantic reconstruction or arbitrary malicious database
repair. A database owner who rewrites **both** rows and the entire history can
still construct a consistent alternative history. There is no external trusted
head, signature or authentication service. The supplied identity/access request
is a caller scope, not proof of caller identity.

DETERMINISTIC_REPLAY means deterministic relative to declared canonicalized
inputs. Hash equality establishes neither tamper resistance nor semantic validity.

## Resource ceilings

| Resource | Maximum per identity/namespace |
|---|---:|
| Claim versions | 256 |
| Evidence records | 1,024 |
| Events | 2,048 |
| Dependency depth (edges; isolated root = 0) | 64 |
| Parents per version | 16 |
| Total dependency edges | 1,024 |
| Affected versions per operation, including root/retired bridges | 256 |
| Pending review requests returned | 64 (default 8) |
| Agenda input requests / output entries | 64 / 20 (default output 3) |
| Source-lineage nodes / parents per source | 2,048 / 8 |
| Event payload / total event payload bytes | 196,608 / 8,388,608 |

Source edges are bounded by evidence count times eight and source depth by 64.
Content/provenance/rationale/reason limits and JSON field limits reject oversized
input before mutation. SQL length checks precede loading oversized managed
version/evidence/event text. Generic unmanaged memory APIs are not turned into a
new storage quota system. All namespace limits include historical records; at
capacity the service rejects writes, with no automatic archive/pruning routine.
These caps bound work, not a benchmark/latency service-level guarantee. Tests use
real graph boundary values and reduced runtime quotas for inexpensive atomicity
checks; they do not claim machine-exhaustion testing.

## Compatibility, migration and rollback limits

The baseline at `4b77b2be69c7721da4e93465b7feb0c3a2aec265` creates the disposable
baseline DB fixtures using its **actual Git version** of `store.py`. Tests cover
empty/populated records, original provenance/flags, mixed identities and repeated
opening. Opt-in service construction transactionally creates the existing three
candidate tables/triggers using `IF NOT EXISTS`; there are no new columns in this
hardening cycle. Failed schema validation rolls back newly created schema objects.
Opening twice adds no events. No personal/production DB is accessed or migrated.

Legacy direct flag setters remain supported for unmanaged memory and reject
managed current/quarantined/retired memory. The old baseline can read a tested
candidate fixture, but **old baseline writes on a managed DB are unsupported**:
they can bypass the Python guard and make status/flag state inconsistent, which
candidate validation rejects. No general backward-writable database promise is
made. Source-file rollback is not a production database downgrade/migration.

The external delivery contains exact archives, both diffs, full file manifests,
command outputs, a default-dry-run exact-byte source rollback tool and disposable
rollback evidence. Unknown files/changes and Git checkouts are rejected by that
tool. No remote mutation or approval receipt is created.

## Epistemic and governance invariants

```text
PREVIOUS_ACCEPTANCE != TRUTH
REPEATED_REUSE != VALIDATION
RETRIEVAL_COUNT != INDEPENDENT_EVIDENCE_COUNT
EVIDENCE_DUPLICATION != CORROBORATION
PROVENANCE != CORRECTNESS
CLAIM_REVISION != SEMANTIC_TRUTH
CONFLICT_FLAG != PROVEN_CONTRADICTION
REVIEW_RESULT != SCIENTIFIC_TRUTH
PEER_CONSENSUS != SCIENTIFIC_TRUTH
PREMISE_REVISED != DEPENDENT_CLAIM_REVALIDATED
UPSTREAM_REPAIRED != DOWNSTREAM_AUTOMATICALLY_VALID
RETAIN != CANONICAL_TRUTH
WITHDRAW != GLOBAL_DOMAIN_REJECTION
REPLAY_HASH_MATCH != TAMPER_PROOF
HASH_INTEGRITY != SEMANTIC_VALIDITY
LOCAL_TEST_PASS != REMOTE_CI_PASS
BASELINE_REPRODUCED_FAILURE != PASS
ENGINEERING_METACOGNITION_ANALOGUE != HUMAN_METACOGNITION
ENGINEERING_BELIEF_REVISION != SUBJECTIVE_REFLECTION
ENGINEERING_BEHAVIOR != SUBJECTIVITY_EVIDENCE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
FULL_AUTOMATION != FULL_AUTHORITY
AUTONOMOUS_RESEARCH != CANONICAL_AUTHORITY
NORMATIVE_STATE != AUTHORITY
DEPENDENCY_ON_A_V1 != DEPENDENCY_ON_A_V2
TRANSACTION_FAILURE => NO_PARTIAL_REVISION_STATE
STALE_WRITE != VALID_WRITE
RESOURCE_LIMIT_EXCEEDED => REJECTED_TRANSACTION
LEGACY_MEMORY_API != REVISION_GOVERNANCE_BYPASS
UPSTREAM_REVISION != TRANSITIVE_AUTO_REHABILITATION
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
TRACEABLE_REVISION != HUMAN_REFLECTION
BETTER_EPISTEMIC_HYGIENE != PROOF_OF_SUBJECTIVITY
```

## Verification map and limitations

- `test_claim_revision.py`: existing approval/stale review/access/lifecycle suite.
- `test_revision_hardening.py`: graph shapes/bounds; SQL/event-stage fault injection
  with whole-database comparisons; barrier concurrency; explicit source lineage;
  canonicalization/process replay; baseline/V1 fixtures; schema rollback;
  legacy API matrix; event/row corruption; GC-on/off immediate file deletion.
- `test_revision_agenda.py`: upstream provenance, bounded deterministic output,
  external-execution sentinels and post-commit adapter failure without DB mutation.
- Native component discovery and root/control suites must both be rerun on the
  exact candidate. Baseline-reproduced Windows symlink failures remain FAIL.
- This is SELF-REVIEW, not independent review, IV&V or second-researcher replication.
  Linux exact-head CI and any remote integration are separate future gates.
