# Grok gap-closure register

```text
AUTHORITY = NONE
BASELINE = main@f3789b7f4c08f39093886e4b07c036add363ab73
WORKSPACE = grok/experimental-sandbox
PR = #84
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
DERIVED_REPORT = TRUE
```

This file is a derived campaign notebook. It is not a governance authority,
evidence schema, or scientific conclusion register.

Dated source reused and re-checked against current main:
`docs/research/REPOSITORY_GAP_AUDIT_2026_09_02.md` (audit baseline was older than `f3789b7`).

## Classification counts (this campaign pass)

See entries below. CLOSE_NOW items are implemented only in this sandbox.

## Gaps from the 2026-09-02 audit, re-checked on main@f3789b7

| ID | Classification | Evidence | Problem | Result |
|---|---|---|---|---|
| GA-01 POSIX target fields | ALREADY_CLOSED | `.github/workflows/quality.yml`; root tests | Windows backslash `target` fields | Quality now runs `python -m pytest -q tests` on Linux 3.11/3.12 |
| GA-02 root test discovery | ALREADY_CLOSED | `.github/workflows/quality.yml` | Quality used a subset | Current workflow runs the complete control suite |
| GA-03 action pin | ALREADY_CLOSED | `.github/workflows/quality.yml` | moving v4 tags | checkout/setup-python are 40-hex pinned |
| GA-04 core paper intake | ALREADY_CLOSED / BLOCKED_EXTERNAL_EVIDENCE | `docs/research/sources/subjectivity/` | consolidated receipts | some sources retained; TICS full text remains 403 |
| GA-05 environment probe | ALREADY_CLOSED | `docs/LOCAL_RESOURCE_AND_ENVIRONMENT.md` | conflated failures | probe exists; no auto-install |
| GA-06 protocol integration wording | ALREADY_CLOSED | current protocol docs on main | stale branch-only wording | current main already merged later research |
| GA-07 whitepaper four-stage labels | OWNER_DECISION_REQUIRED | audit unresolved table | authoritative wording not in tree | internet text is not a substitute |
| GA-08 independent IV&V | BLOCKED_INDEPENDENT_VALIDATION | HOLD `BOUNDARY-IVV-01` | same-team rerun != independent | remains open |
| GA-09 model-level causal evidence | SCIENTIFIC_EXPERIMENT_REQUIRED | audit unresolved table | fixture != model mechanism | remains open |
| GA-10 whole-system scientific validation | SCIENTIFIC_EXPERIMENT_REQUIRED | audit unresolved table | unit tests != scientific validation | remains open |
| GA-11 ephemeris / school adjudication | OWNER_DECISION_REQUIRED | `examples/*/DEFERRED_ITEMS.md` | competing schools / license | comparison domains only |
| GA-12 TICS 2026 full text | BLOCKED_EXTERNAL_EVIDENCE | audit unresolved table | HTTP 403 | metadata != content |
| GA-13 release readiness | OWNER_DECISION_REQUIRED | `PUBLIC_RELEASE_POLICY.md` | merge != release | Human Owner gate |
| GA-14 C0 HOLDs | OWNER_DECISION_REQUIRED | `docs/history/c0/C0_REMAINING_HOLD_REGISTER_2026-08-08.md` | deferred capabilities | `DEFERRED != DEFECT` |

## Gaps found by EX-001 / this campaign

### GC-001 Gutenberg repository hash drift

- classification: CLOSE_NOW (closed in this campaign)
- evidence paths: `examples/classical-western-astrology_v0.1.0/sources/SOURCE_FETCH_MANIFEST.json`; EX-001 RESULT
- problem: checked-in Ptolemy/Sepharial texts no longer matched recorded `repository_sha256` (download hash was copied into the repository field after LF normalization)
- why it matters: provenance integrity of vendored witnesses
- reuse: existing fetch-manifest fields (`sha256` vs `repository_sha256` + `repository_normalization`) already used by Lilly/Bazi entries
- minimal repair: set `repository_sha256`/`repository_bytes` to current checked-in bytes; keep original download `sha256`/`bytes`; add the existing normalization token
- tests: `python -m pytest -q experiments/comparison-domain-source-ledger_v0.1.0/tests`
- result: after repair, EX-001 `C3B_ALL_CHECKED_IN_HASHES_MATCH = SUPPORTED`, coverage `24/24`
- remaining limitation: external URL current content still NOT_VERIFIED; legal license effectiveness NOT_ESTABLISHED
- promotion implication: sandbox-only until Human Owner / Codex review of PR #84

### GC-002 EX-001 not invoked by Quality

- classification: CLOSE_NOW
- evidence: `.github/workflows/quality.yml` runs `g1-recall-gate-baseline` but not the new ledger experiment
- reuse: existing Quality experiment step pattern
- minimal repair: add the EX-001 pytest invocation after the Recall Gate step
- remaining limitation: Quality push trigger still omits `grok/**`; pull_request still runs it
- promotion implication: sandbox workflow change only

## Scientific stop-lines kept

```text
ENGINEERING_PASS != SCIENTIFIC_VALIDATION
REPRODUCIBLE_FIXTURE != MODEL_LEVEL_CAUSAL_EVIDENCE
SAME_TEAM_RERUN != INDEPENDENT_IVV
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
