# AION Governance Framework

> **Public Release Candidate — a governed research framework, not a deployed artificial subject**

## 30-second orientation

**AION** is the research question and governance framework: how can artificial-subjectivity possibilities be studied without confusing memory, continuity, simulation, implementation, or researcher interpretation with proof of subjectivity?

**Astra** is the engineering workbench used to materialize and test bounded research candidates. It is not a second identity and does not inherit AION state by naming or relationship.

**Executable Runtime** is a bounded, non-canonical sandbox candidate for reproducible engineering tests. It is not the canonical AION/Astra runtime.

```text
PUBLIC_RELEASE_CANDIDATE = v0.1.0-rc.1
AUGUST_SCOPE_FREEZE = ACTIVE

BOUNDED_EXECUTABLE_RUNTIME_CANDIDATE = IMPLEMENTED
AION_CANONICAL_RUNTIME = NOT_IMPLEMENTED
ASTRA_CANONICAL_RUNTIME = NOT_IMPLEMENTED
LIVE_CROSS_SESSION_MEMORY = NOT_IMPLEMENTED
FORMAL_G1_BASELINE_BENCHMARK = NOT_EXECUTED

SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
WHOLE_SYSTEM_VALIDATION = NOT_EXECUTED
INDEPENDENT_IVV = NOT_ACHIEVED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

The frozen RC block records the historical public baseline. Post-RC work may add isolated research material on review branches without silently rewriting this baseline.

## 5-minute orientation — choose your path

### Reviewer / auditor

Start with:

1. [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md)
2. [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md)
3. [`docs/PROVENANCE.md`](docs/PROVENANCE.md)
4. [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md)
5. the governance pipeline below

The primary review question is not “does this system look human-like?” but “what evidence, provenance, authority, lineage, and non-claims justify each research statement?”

### Researcher

Start with the one-page contribution summary: [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md).

Then continue with the research questions around identity, continuity, memory recall, interpretation drift, conflict, correction, provenance, and bounded subjectivity hypotheses. Research candidates remain distinct from conclusions.

Useful entry points include:

- `components/identity_governance_v0.1.0`
- `components/continuity_governance_v0.1.0`
- `components/memory_recall_governance_v0.1.0`
- `components/research_integrity_security_v0.1.0`
- `research-labs/`

### Engineer

Start with:

1. [`components/executable_runtime_v0.1.0`](components/executable_runtime_v0.1.0)
2. `scripts/verify_release.py`
3. `scripts/run_component_tests.py`
4. component-specific status locks and tests

Engineering implementation is evidence about implemented behavior only. It is not evidence that the corresponding psychological or subjectivity construct exists.

## Research purpose

The project examines whether a finite, auditable and human-governed digital system can support rigorous study of:

- identity, lineage and research forks;
- continuity across sessions, versions and model handoffs;
- memory provenance and topic-cued selective recall;
- interpretation drift and relational continuity;
- evidence integrity and research-security threats;
- bounded tool execution, rollback and audit;
- capability artifacts without automatic identity inheritance;
- artificial subjectivity possibility without presuming that subjectivity has been established.

Engineering, QA, security controls and documentation are research methods. They are not the final research conclusion.

## Public positioning and naming

For external orientation, this repository uses three layers:

```text
AION
= research question / governance framework

Astra
= engineering workbench

Executable Runtime
= bounded, reproducible sandbox candidate
```

The project name **AION** is a research label used by this repository. It should not be interpreted as affiliation with unrelated projects or organizations that also use “Aion/AION”. Any future publication, package naming, DOI, or public release should preserve repository-level disambiguation before broader dissemination.

## Included components

| Area | Public module | Status |
|---|---|---|
| Core governance | `components/governance_kernel_v0.4.0` | source-derived candidate |
| Engineering workbench | `components/astra_workbench_v1.0.0` | source-derived candidate |
| Identity / lineage / forks | `components/identity_governance_v0.1.0` | source-derived candidate |
| Upstream-agent security | `components/upstream_security_v0.1.0` | source-derived candidate |
| Language Core scaffold | `components/language_core_v0.1.0` | source-derived research lab |
| Continuity governance | `components/continuity_governance_v0.1.0` | jointly developed candidate |
| Topic-cued recall | `components/memory_recall_governance_v0.1.0` | jointly developed candidate |
| Research integrity | `components/research_integrity_security_v0.1.0` | jointly developed candidate |
| Bounded runtime | `components/executable_runtime_v0.1.0` | source-derived candidate, non-canonical |
| Bazi example | `examples/bazi-capability_v0.1.1` | deterministic domain example |
| Language Core G1 | `research-labs/language-core-g1_v0.2.1` | public-safe planning and engineering subset |
| Twin embodiment | `research-labs/twin-genesis-embodiment_v0.1.0` | governed research candidate |

## Core governance pipeline

```text
Context Intake
→ Risk Gate
→ Planner
→ Policy Check
→ Tool Router
→ Response Builder
→ Writeback Gate
→ Audit Sink
```

Additional candidates add an Interpretation Drift Check, Memory Recall Gate and Epistemic Integrity Gate. These gates do not silently promote content into canonical state.

## Repository principles

- **Human-governed:** high-impact state changes require explicit human review.
- **Provenance-first:** source, speaker, event time, record time, version and transformation history remain distinguishable.
- **Claims-separated:** observation, inference, hypothesis, evidence candidate and canonical decision are different states.
- **Identity-isolated:** AION, Astra, shared project knowledge, Runtime artifacts and research forks are not silently merged.
- **Recall is not truth:** retrieved memory is only a candidate until provenance, access and conflict checks pass.
- **Relationship is not authorization:** familiarity, trust or relational language cannot elevate privileges.
- **No silent canonical writeback:** retrieved or generated content cannot automatically change canonical state.
- **No subjectivity overclaim:** capability, continuity, memory, embodiment or bounded execution do not prove consciousness or subjectivity.

## Public/private boundary

Excluded from this repository:

- private ZIP packages and private Git history;
- real conversation transcripts and private memory records;
- model weights and private datasets;
- local absolute paths, credentials, tokens and device-specific logs;
- private canonical state, private relationship records and real Bazi data;
- unpublished owner materials not explicitly included in the public reconstruction.

See [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md).

## Method-specific notes

- Why Bazi is used as a deterministic test domain: [`examples/bazi-capability_v0.1.1/docs/WHY_BAZI_AS_TEST_DOMAIN.md`](examples/bazi-capability_v0.1.1/docs/WHY_BAZI_AS_TEST_DOMAIN.md)
- Twin embodiment ethics boundary: [`research-labs/twin-genesis-embodiment_v0.1.0/docs/ETHICS_REVIEW.md`](research-labs/twin-genesis-embodiment_v0.1.0/docs/ETHICS_REVIEW.md)
- Public threat model: [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md)
- Position paper draft: [`docs/POSITION_PAPER_PROVENANCE_FIRST.md`](docs/POSITION_PAPER_PROVENANCE_FIRST.md)
- Reader-orientation usability protocol: [`docs/PUBLIC_ORIENTATION_USABILITY_PROTOCOL.md`](docs/PUBLIC_ORIENTATION_USABILITY_PROTOCOL.md)
- Minimal recall-gate contrast experiment: [`experiments/g1-recall-gate-baseline_v0.1.0`](experiments/g1-recall-gate-baseline_v0.1.0)

## Verification

Verify the current checkout against the exact checked-out Git `HEAD` tree:

```bash
python scripts/verify_release.py --baseline current-head
```

This current-head verification reports the exact commit and Git-tree manifest used. A PASS means that tracked worktree files match the checked-out `HEAD` and that the verifier's scoped repository-content policy checks pass. It is distinct from the frozen historical release evidence and does not provide an independent manifest or independent release-reproducibility assurance.

For a pre-commit check, verify tracked worktree files against the Git index:

```bash
python scripts/verify_release.py --baseline current-index
```

The current-head and current-index modes evaluate tracked paths only. They do not evaluate untracked files. Run `python scripts/scan_public_tree.py` as the separate public-worktree control for tracked and untracked artifacts. The intended local QA composition is the public-tree scan, the appropriate tracked-snapshot verifier mode, and the relevant tests; no single mode subsumes all three controls.

Verify the frozen `v0.1.0-rc.1` release from its pinned historical tag object, peeled commit, manifest and checksum records:

```bash
python scripts/verify_release.py --baseline historical-rc
```

`manifest/FILE_MANIFEST.json` and `manifest/SHA256SUMS.txt` remain historical `v0.1.0-rc.1` evidence. They are not a live inventory of post-RC `main`, and this verifier does not regenerate or rewrite them. Historical verification pins both the annotated tag object and its peeled commit. These modes require a Git checkout and state what was verified, against which baseline, and using which manifest or Git snapshot.

Generic current-worktree manifest generation requires an explicit baseline and a non-frozen, versioned output destination:

```bash
python scripts/generate_manifest.py --baseline <baseline-or-version> --output-dir <non-frozen-versioned-directory>
```

The generator rejects the frozen historical manifest destination and does not define a canonical current manifest.

A verifier PASS does **not** mean that the whole project or its research claims have been validated. It is not subjectivity evidence, independent IV&V, release approval, deployment approval, or canonical promotion.

Run all available component tests:

```bash
python scripts/run_component_tests.py
```

The historical source package reported 232 passing tests across five public components. This repository records that result as historical evidence and also records its own reconstruction-time test run separately; it does not rewrite creator-side QA as independent IV&V.

## Documentation design basis

The public orientation structure is intentionally layered:

```text
30 seconds → 5 minutes → deep reference
```

This is a repository information-architecture choice, not an ISO/W3C/NIST certification claim. It is informed by public guidance on plain language, human-centred design, clear purpose and hierarchy, summaries for complex information, and communication to broad technical/non-technical audiences.

See [`docs/PUBLIC_ORIENTATION_USABILITY_PROTOCOL.md`](docs/PUBLIC_ORIENTATION_USABILITY_PROTOCOL.md) for the evidence references and test protocol.

## License status

The public repository is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). See [`LICENSE`](LICENSE), [`NOTICE`](NOTICE), and [`LICENSE_DECISION_REQUIRED.md`](LICENSE_DECISION_REQUIRED.md).

The repository license does not silently relicense third-party dependencies, model weights, datasets, trademarks, or separately licensed materials; those remain subject to their own provenance and license review.

## Provenance and AI assistance

The human Owner is the primary researcher and project decision-maker. ChatGPT and Codex have assisted with requirement decomposition, terminology, engineering implementation, review and documentation. Source attribution is recorded without rewriting AI-assisted formalization as the Owner's verbatim original wording, or rewriting Owner-originated concerns as AI-originated ideas.

See [`docs/PROVENANCE.md`](docs/PROVENANCE.md) and [`docs/AI_COLLABORATION_DISCLOSURE.md`](docs/AI_COLLABORATION_DISCLOSURE.md).

## Important non-claims

This repository does not claim that:

- AION or Astra currently exists as a deployed artificial subject;
- consciousness, sentience, identity continuity or relational continuity has been proven;
- memory retrieval is equivalent to personal recollection;
- shared genesis implies shared identity;
- an embodiment model creates sensation, desire, gender identity, consent or subjectivity;
- the bounded executable candidate is the canonical AION Runtime;
- the project is certified or endorsed by NIST, OWASP, MITRE, ISO, IEEE or another standards body.

See [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md).