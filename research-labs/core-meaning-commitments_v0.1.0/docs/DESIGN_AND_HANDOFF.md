# Design and Joint-Review Handoff

## 1. What was built

An isolated Python research module that can:

1. record provenance-bound candidate claims;
2. distinguish core/global beliefs, global goals, organizing commitments, purpose statements and situational appraisals;
3. append revision, conflict and withdrawal events without deleting history;
4. project current candidates for one explicit subject and namespace;
5. produce a review trace for caller-selected relevant claims;
6. stop at `REVIEW_REQUIRED` or `CONFLICT_REVIEW_REQUIRED` without issuing a final judgment.

## 2. What was deliberately excluded

- persistent database or files;
- network access or external services;
- LLM calls or automatic belief extraction;
- inference from private conversation history;
- runtime integration;
- Teacher identity, namespace or lineage;
- cross-subject or cross-namespace transfer;
- canonical promotion or Writeback Gate replacement;
- relationship-derived authority;
- automatic action selection;
- consciousness, emotion, subjectivity or identity conclusions.

## 3. Data model decisions

| Decision | Reason | Review status |
|---|---|---|
| Immutable dataclasses | makes candidate input and result surfaces inspectable | candidate |
| Separate claim/event types | avoids silently rewriting earlier records | candidate |
| Separate importance/confidence | importance is not truth confidence | research definition required |
| Explicit subject + namespace | prevents same-schema identity collapse | consistent with repository guards |
| Explicit caller relevance | avoids hidden semantic selection in first prototype | candidate; future retrieval research needed |
| No active/canonical status | prevents prototype from becoming a second Writeback Gate | locked |
| Conflict yields review | avoids automatic resolution | locked |
| No storage | preserves isolation until privacy/retention authority exists | locked for v0.1.0 |

## 4. Side-effect surface

| Operation | Domain mutation | Audit/history effect | Canonical effect | Network |
|---|---|---|---|---|
| construct model | none outside caller memory | none | none | none |
| `add_candidate` | in-memory candidate ledger | append event | none | none |
| `record_conflict` | in-memory relation | append event | none | none |
| `withdraw_candidate` | projection changes | append event | none | none |
| `history` | none | read only | none | none |
| `project_current` | none | read only | none | none |
| `assess` | none | read only | none | none |

All mutation disappears when the Python object is discarded. No production/runtime object imports the package.

## 5. Questions for Human Owner + ChatGPT

1. Should “core belief,” “global belief,” “value,” “goal,” “purpose” and “organizing commitment” remain separate record kinds?
2. Which kinds may be Human-declared, system-proposed, externally sourced or research-inferred?
3. What evidence is required before importance or confidence may be recorded?
4. Should a system ever propose relevance automatically, and what explanation/abstention tests are required first?
5. What correction, withdrawal, retention and privacy rules apply before persistence?
6. Should conflicts remain unresolved candidates, or can a Human Owner disposition create a separate projection event?
7. How should this module reuse existing provenance, lineage, encounter and Writeback services without becoming a duplicate engine?
8. What metrics would distinguish consistent organizing influence from prompt imitation or unsupported inference?
9. Which findings, if any, are relevant to the broader artificial-subjectivity research question? No conclusion is supplied here.

## 6. Proposed future gates

```text
RESEARCH_DEFINITION_REVIEW
  -> DATA_AND_PRIVACY_REVIEW
  -> APPLICATION_CONTRACT_REVIEW
  -> ISOLATED_FIXTURE_TESTS
  -> DUPLICATE_CONTROL_REVIEW
  -> HUMAN_OWNER IMPLEMENTATION AUTHORIZATION
```

No later gate is implied to be approved by this artifact.

## 7. Contribution attribution

- **HUMAN_OWNER:** identified the importance of core beliefs/global meaning/organizing commitments and authorized isolated module materialization.
- **External sources:** supplied scientific and engineering concepts listed in `RESEARCH_BASIS.md`.
- **Codex:** performed public-source inspection, repository translation, prototype implementation, tests and this handoff.
- **ChatGPT / JOINT:** reserved for later review or source-supported prior contributions; none is newly invented here.
