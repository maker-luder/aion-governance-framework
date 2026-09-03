# Cross-cycle claim rechecking and revision / 跨輪次命題重查與修正

Status: bounded engineering candidate; exact-head delivery and test evidence are external.
This document does not assert that the candidate is merged, deployed, or running.

## Purpose and origin

The Human Owner described a recurring learning practice: notice a discrepancy,
revisit the reasons for an earlier statement, consult evidence, and revise the
affected inference rather than discard an entire field of study. This is an
attributed first-person report and a source of research questions, not a
psychological measurement or proof of a particular cognitive mechanism.

The current bounded implementation permission concerns engineering this proposal.
It does not supply a fresh exact-head main-transition receipt or change repository
freeze controls. No original private dialogue or personal chart is included.

**AI_SUBJECTIVITY_POSSIBILITY remains the central question.** A useful revision
mechanism does not require a prior conclusion either for or against subjectivity.

## What was already present; what this candidate adds

The existing `SQLiteMemoryStore` persists memory, checks identity/access/provenance,
and excludes conflicted, inactive or superseded memory during recall. Those flag
operations alone neither track dependent claims nor retain a revision rationale.

`aion_memory_recall.revision.ClaimRevisionService` is an opt-in service over the
**same SQLite database and memory records**. It adds three local tables for
immutable version references, typed evidence links and a chained event history.
These are component-internal persistence tables, not a replacement canonical
schema, eighth functional state, second research loop or subjectivity score.

The service:

1. Enrolls an existing approved, active memory as a stable claim ID/version.
2. Separates `OBSERVATION`, `ANALOGY` and `INFERENCE`, recording assumptions and
   exact premise-version IDs. These labels describe the caller's classification.
3. Accepts an explicit `SUPPORTS`, `CONTRADICTS` or `IRRELEVANT` evidence relation.
4. Atomically marks the target challenged and transitive dependents on hold.
5. Exposes pending reviews in a bounded, read-only view. A thin adapter creates
   the existing `AgendaEntry`/`AgendaKind.CONTRADICTION` records with provenance.
6. Records an explicit caller review: retain, revise or withdraw. Retaining and
   revising produce a new immutable memory version; withdrawing preserves the old
   content. Dependent claims stay on hold until separately reviewed.
7. Rejects stale review receipts when new events have arrived. Records remain
   reproducible across process restarts and deterministic fixture replay.

The agenda adapter **does not execute or resolve the review**. Existing campaign
probes study synthetic mechanisms; they are not general-purpose adjudicators of
arbitrary claims. No new background queue, timer, external lookup or model call
is installed. The caller explicitly invokes each operation.

## Status is not truth

| Local status | Meaning |
|---|---|
| `RECORDED` | Eligible for the existing recall gate, not proven true |
| `CHALLENGED` | Typed counterevidence has been registered; exclude from recall |
| `DEPENDENCY_HOLD` | A premise is challenged/inactive; exclude until rechecked |
| `SUPERSEDED` | Preserve this version, use its explicitly reviewed successor if eligible |
| `WITHDRAWN` | Preserve historical content but exclude it from recall |

Positive evidence does not automatically clear negative evidence. A review must
address all registered counterevidence in the target's transitive premise lineage.
Evidence targeting an inactive old version is not silently redirected to a new one.
Successor assumptions and dependencies must be explicitly supplied (empty tuples
mean the reviewer explicitly proposes no such premises); review reason is required.
The service checks the structure, **not the adequacy or truth of that reason**.

Repeated delivery of an identical evidence ID is a no-op. A changed payload under
that ID is rejected. Distinct source labels and content digests are reported
separately; neither is promoted to a count of independent supporting observations.

## Bounded contrast design

Research hypothesis: with explicitly typed counterevidence, dependency-aware
revision prevents recall of affected downstream claims compared with the existing
flag-only behavior, without suppressing unrelated premises.

Five **constructed** claims are used: an observation, an analogy, an overclaim
of unique determination, one dependent inference and an unrelated observation.
A constructed same-input/different-output pair challenges only the overclaim.
It is a software fixture, not an observed biological or astrological case.

| Condition | Intervention | Measurement |
|---|---|---|
| Historical base | Existing direct conflict flag only | Downstream stale recall and unaffected recall |
| Matched ablation | Candidate code, no revision enrollment/propagation | Same measurements |
| Revision enabled | Typed contradiction + dependency propagation | Same measurements + pending agenda |
| Restart | Reopen the same temporary SQLite file | Exact snapshot and queue equality |
| Replay | Fresh database, identical ordered input | Exact output and event-head equality |

Acceptance thresholds for this **finite fixture**: revised stale-dependent recall
count = 0; unaffected false-hold count = 0; both pending claim versions appear
within the selected limit; replay/restart equality = true; original content remains
available for history; dependent claim remains held after the overclaim is withdrawn.
The flag-only condition is expected to retain the dependent claim, demonstrating
the concrete missing link rather than fabricating an already-successful baseline.

Additional tests cover approval denial, identity/namespace/access separation,
dependency cycles, duplicate evidence, stale review, omitted counterevidence,
event limits and transaction rollback, two-connection writes, legacy setter bypass,
versioned re-review and explicit rebasing of dependent claims.

No statistical significance or population-level estimate is claimed for these
deterministic tests. Competing explanations include explicit bookkeeping alone,
caller-supplied correct labels, and curated fixture selection. A correct negative
control, removal of propagation, and adversarial invalid inputs test the mechanism;
they do not establish spontaneous or human-like reflection.

## Reproduction

From a source checkout with the repository QA dependencies installed:

```powershell
python scripts/probe_claim_revision.py --mode legacy
python scripts/probe_claim_revision.py --mode revision
python -m pytest -q components/memory_recall_governance_v0.1.0/tests
```

For the complete cross-component suites, use the repository-native
`discover_source_roots()` / `run_component_tests()` mechanism described in
[`../../scripts/run_component_tests.py`](../../scripts/run_component_tests.py).
The CLI script injects those native source roots itself. It creates only a
temporary synthetic database, prints JSON and optionally writes the selected
`--output` file. It does not open a user's existing database.

The autonomous-research adapter imports memory-recall only when called. Both
components must be available for that optional integration; neither adds an
undeclared mandatory third-party dependency. The memory component remains usable
as a standalone installed package.

## Boundaries, threats and residual work

- All mutation methods require the caller's explicit local writeback approval.
  This Boolean is not a login mechanism, Human Owner presence attestation, or
  GitHub merge approval. Callers supply authenticated identity/scopes separately.
- Active namespace bounds: 256 retained claim versions, 1,024 evidence links,
  2,048 events, 16 direct premises per version. Exhaustion rejects the transaction.
  No silent history eviction is implemented. Archive/export policy is future work.
- A derived claim cannot expose a premise to broader access scopes. Full event
  export requires access to every enrolled record in the namespace. A propagation
  involving inaccessible descendants rejects atomically; use the permitted
  namespace controller rather than weakening scope checks.
- Managed versions reject legacy direct flag setters. Unenrolled memories keep
  existing behavior. No existing live/private database is automatically migrated.
- Normal store/service database sessions now explicitly close their handles:
  SQLite's transaction context alone does not close them. Windows cleanup tests
  exposed this existing resource-lifetime issue; this is not inadequate hardware.
- Hash-chain verification detects changed event payloads relative to the supplied
  head; it is not signed attestation, full database consistency verification, or
  protection against a database owner rewriting both data and hashes.
- Content digest, provenance verification, evidence relation and reviewer judgment
  are supplied by the caller. The service does not fetch, authenticate or evaluate
  external source content. No semantic contradiction detector is claimed.
- Reviewing can still be wrong; source independence is not established by URLs,
  labels, consensus or repetition. No AGM-postulate compliance is claimed.
- A future semantic/model-backed study needs an independently annotated dataset,
  false-positive/false-negative measurements, scope/assumption matching, adversarial
  source cases and separate review of model, data and runtime permissions.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
IDENTITY_CONTINUITY = NOT_ESTABLISHED
SEMANTIC_CONTRADICTION_DETECTION = NOT_IMPLEMENTED
AUTOMATIC_REVIEW = FALSE
AUTONOMOUS_REPOSITORY_WRITEBACK = NO
ENGINEERING_REVISION != SUBJECTIVE_REFLECTION
PROVENANCE != CORRECTNESS
CONSENSUS != TRUTH
```

## Subsequent local hardening

The [bounded hardening addendum](CLAIM_REVISION_HARDENING_2026_09_03.md) records
stricter graph/data validation, V2 canonical events, explicit source lineage,
transaction/concurrency tests and compatibility limits. Historical V1 event hashes
remain unchanged. This addendum does not confer remote integration authority.

## Primary-source reading and counterarguments

Access checked 2026-09-03. The entries below are short original summaries based
on publisher/PubMed abstracts, **not retained publication full texts**. No source
license is replaced by the repository license. Full formal algorithms and proofs
were not audited in this cycle.

1. **Doyle (1979), A truth maintenance system.** Recording reasons for beliefs and
   their dependencies can support revision when assumptions conflict with new
   findings. This is a closer engineering precedent for the current limited
   implementation than claiming a human cognitive mechanism.
   [Publisher abstract](https://www.sciencedirect.com/science/article/pii/0004370279900080),
   DOI: `10.1016/0004-3702(79)90008-0`.
2. **Alchourrón, Gärdenfors & Makinson (1985), On the logic of theory change.**
   Formal contraction/revision operations and their properties provide a research
   reference. This candidate does not implement or verify the AGM postulates.
   [Publisher abstract](https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/on-the-logic-of-theory-change-partial-meet-contraction-and-revision-functions/7ED837BAD5FB6D9A7C77906D73527F9C),
   DOI: `10.2307/2274239`.
3. **Botvinick et al. (2001), Conflict monitoring and cognitive control.**
   Computational models investigate links between conflict monitoring and control.
   This motivates a functional analogy, not an inference about the Owner's brain
   or an attribution of human metacognition to this software.
   [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/11488380/),
   DOI: `10.1037/0033-295x.108.3.624`.
4. **Ward & Ward (2006), Cognitive conflict without explicit conflict monitoring
   in a dynamical agent.** A modeled agent displayed conflict resolution without
   a distinct explicit monitor. Similar behavior therefore need not identify one
   particular underlying mechanism. This is a substantive competing explanation,
   not evidence against every possible form of artificial subjectivity.
   [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/17027226/),
   DOI: `10.1016/j.neunet.2006.08.003`.
