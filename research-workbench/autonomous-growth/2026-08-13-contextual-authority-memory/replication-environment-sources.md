# Independent Replication / Environment Drift — Source Notes

Date: 2026-08-13

## Selection rationale

The next broad-cycle gap is **independent replication readiness under environment, artifact, and interpretation drift**. Existing repository units already cover generic replication epistemics, design validity, handoff completeness, and matched-divergence protocol integrity. The new question is narrower: can a research-only contract distinguish computational reproducibility, independent replication, artifact audit, environment drift, and scientific interpretation without counting reused evidence as a new replication or promoting a result?

## Source record A — National Academies

**What:** The National Academies distinguishes reproducibility as consistent results using the same input data, computational steps, methods, code, and analysis conditions, while replicability uses new data to address the same scientific question. It also emphasizes complete reporting of data, methods, computational environment, dependencies, uncertainty, and limits; and warns that successful replication does not guarantee correctness while a failed replication does not conclusively refute an original claim.

**Who / authority:** National Academies of Sciences, Engineering, and Medicine; authoritative consensus report commissioned through NSF context.

**Where:** <https://www.nationalacademies.org/read/25303/chapter/3>

**When / status:** 2019 publication; retrieved during this cycle and treated as current methodological prior art, not as current repository state.

**Method:** Public full-text extraction; relevant definitions/recommendations were recorded, not reinterpreted as empirical rates for AION/Astra.

**Transformation:** Candidate schema should separate artifact replay from new-data replication, record environment/dependency drift, record uncertainty and interpretation status, and prevent `replication_result` from being collapsed into truth or governance effect.

## Source record B — ACM Artifact Review and Badging

**What:** ACM's artifact review policy defines reviewable artifact properties such as documented, consistent, complete, and exercisable. It distinguishes repeatability, reproducibility, and replicability by team, setup, measurement system, location, and use of author-supplied versus independently developed artifacts. It also separates artifact evaluation/availability/result validation badges and states that results need only agree within an acceptable tolerance for the experiment type.

**Who / authority:** Association for Computing Machinery publication policy; the retrieved page is explicitly labeled Version 1.0 and links to a current version, so this record is `HISTORICAL_POLICY_REFERENCE / CURRENT_VERSION_NOT_YET_RETRIEVED` and must not be treated as the current ACM policy without rechecking.

**Where:** <https://www.acm.org/publications/policies/artifact-review-badging>; linked current-page check: <https://www.acm.org/publications/policies/artifact-review-badging-current> (404 at retrieval).

**When / status:** Version 1.0 revised 2020-08-24; retrieved 2026-08-13; historical policy text. The page's linked `artifact-review-badging-current` URL returned a rendered ACM 404 page during this cycle, so current ACM v1.1 terminology was not admitted as evidence.

**Method:** Public full-text extraction; terminology and badge distinctions were extracted as competing framework evidence.

**Transformation:** Candidate schema should keep artifact-audit status separate from result validation, distinguish author-artifact replay from independent recreation, and require an explicit acceptable-tolerance/interpretation reference before any consistency label.

## Source record C — NIH rigor and reproducibility

**What:** NIH describes rigor as robust and unbiased experimental design, methodology, analysis, interpretation, and reporting, and frames reproducibility as a cornerstone of scientific advancement. It points reviewers to details that may be overlooked, including sample-size calculation, authentication plans, reviewer guidance, and reporting principles.

**Who / authority:** National Institutes of Health official policy/resource page.

**Where:** <https://grants.nih.gov/policy-and-compliance/policy-topics/reproducibility>

**When / status:** Page retrieved 2026-08-13; current public policy resource at retrieval time.

**Method:** Public full-text extraction; used for general rigor/transparency requirements only.

**Transformation:** Candidate schema should retain design/analysis/reporting completeness and uncertainty as separate metadata dimensions; it should not convert an NIH-style rigor field into a certification or AION/Astra conclusion.

## Source record D — NSF-hosted metadata paper

**What:** Search results identified a paper on mainstreaming metadata into research workflows, with the relevant distinction that replication requires complete metadata for creating new data. The direct NSF PDF extraction returned encoded PDF content rather than readable text in this retrieval, so no substantive claim from the paper is used below.

**Who / authority:** External research paper hosted by NSF PAR; authority and exact bibliographic details require a successful text/PDF read before use.

**Where:** <https://par.nsf.gov/servlets/purl/10412652>

**When / status:** Retrieved 2026-08-13 but `PARTIAL / TEXT_EXTRACTION_FAILED`; retained as a retrieval lead, not as evidence for the prototype.

**Transformation:** None until the source is successfully read and bibliographic identity verified. This preserves `RETRIEVED != CURRENT` and `PARTIAL_RETRIEVAL != ADMITTED_EVIDENCE`.

## Evidence reuse boundary

Existing repository units `replication-epistemics-governance_v0.1.0`, `independent-replication-design_v0.1.0`, and `independent-replication-handoff-integrity_v0.1.0` are stable prior evidence. The next unit must not duplicate their evidence count or claim that a repeated fixture is independent replication. It may add a new environment-drift/interpretation contract with explicit source references and new synthetic falsifiers.

## Attribution boundary

```text
HUMAN_OWNER = task authorization and current repository-state authority
EXTERNAL_LITERATURE = National Academies, ACM, NIH, NSF-hosted retrieval lead
REPOSITORY_EVIDENCE = existing replication units and current branch state
MANUS = clean-room transformation and synthetic implementation
SYNTHETIC_FIXTURES = mechanism-only negative controls
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Candidate next gap — evidence currentness, staleness, and duplicate-vs-replication ledger

The next candidate unit is not another replication result check. It would audit whether an evidence record is current, stale, historical, retrieved-only, or unverified; whether two records share the same underlying evidence; and whether reuse is incorrectly labeled replication. It would remain a metadata-only contract and would not assess subjectivity or scientific truth.

## Source record E — W3C PROV-O

**What:** PROV-O provides an OWL2 representation of the PROV Data Model for representing and interchanging provenance across systems and contexts. It models entities, activities, agents, derivation, attribution, generation, invalidation, revision, specialization, alternate representations, and provenance chains. W3C describes PROV-O as a Recommendation and a stable reference, while noting that later documents may supersede a document and that the technical-reports index should be consulted for the latest revision.

**Who / authority:** W3C Provenance Working Group; W3C Recommendation.

**Where:** <https://www.w3.org/TR/prov-o/>

**When / status:** 2013 Recommendation retrieved 2026-08-13; stable historical normative reference, with current W3C status to be checked through the technical-reports index when needed.

**Method:** Public full-text extraction; only provenance concepts relevant to generation/invalidation/revision/specialization and provenance chain identity are used.

**Transformation:** Candidate currentness contract may use source identity, generated/invalidated time, revision/specialization links, and provenance chains to distinguish same underlying evidence, new derived records, and genuinely new evidence. It must not claim full PROV-O conformance from a small standard-library schema.

## Source record F — FAIR Principles

**What:** FAIR guidance emphasizes globally unique and persistent identifiers, rich metadata, explicit identifier linkage, accessibility of metadata, interoperability, detailed provenance, clear licenses, and reuse. It states that metadata should remain accessible even when data are no longer available.

**Who / authority:** GO FAIR official FAIR Principles resource; explanatory guidance for the FAIR Guiding Principles.

**Where:** <https://www.go-fair.org/fair-principles/>

**When / status:** Retrieved 2026-08-13; current public guidance at retrieval time, not a repository authority.

**Method:** Public full-text extraction.

**Transformation:** Candidate ledger should require stable evidence identifiers, source/record identity separation, explicit status fields, license/access metadata, and provenance links; FAIR-aligned metadata is not equivalent to evidence validity or scientific confirmation.

## Source record G — DataCite

**What:** DataCite describes its infrastructure as connecting research outputs/resources through DOI and metadata records and enabling discovery and reuse, with emphasis on reliability, transparency, trust, and interoperability.

**Who / authority:** DataCite official public organization resource.

**Where:** <https://datacite.org/>

**When / status:** Retrieved 2026-08-13; current public organizational guidance at retrieval time.

**Method:** Public full-text extraction from the official homepage; no DataCite API or DOI record was queried.

**Transformation:** Candidate ledger may treat persistent identifiers and metadata records as identity/provenance anchors, but must not infer that a DOI or metadata record makes evidence current, independent, or true.

## Candidate-unit boundary

```text
RETRIEVED != CURRENT
REMEMBERED != AUTHORITATIVE
REFERENCE != NEW_EVIDENCE
DUPLICATION != REPLICATION
PROVENANCE_METADATA != SCIENTIFIC_VALIDITY
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Candidate next gap — factorial execution completeness and attrition integrity

A second candidate after evidence-currentness is a **factorial execution completeness/attrition ledger**. The existing `factorial-completeness-contract_v0.1.0` verifies planned Cartesian cells and design metadata but explicitly does not execute or audit an execution trace. The new unit would remain synthetic and metadata-only: it would distinguish planned cells, attempted cells, completed cells, failed/aborted cells, excluded cells, and unreported cells; require predeclared deviation reasons; preserve negative/null/failed cells; and reject post-outcome factor/cell addition or silent attrition.

## Source record H — NIST full factorial design

**What:** NIST's full-factorial example enumerates factor-level combinations, shows replication/randomization considerations, and warns that unrandomized run order can confound a factor with an environmental condition. The example distinguishes the standard factorial cell list from randomized execution order and center-point additions.

**Who / authority:** National Institute of Standards and Technology Engineering Statistics Handbook; official methods reference.

**Where:** <https://www.itl.nist.gov/div898/handbook/pri/section3/pri3332.htm>

**When / status:** Retrieved 2026-08-13; official public methods reference at retrieval.

**Transformation:** A candidate execution ledger should preserve planned cell identity, execution order/randomization metadata, added center points, and cell-level completion/attrition. It must not infer factor effects from the synthetic ledger.

## Source record I — NIH Principles and Guidelines for Reporting Preclinical Research

**What:** NIH-endorsed reporting principles call for transparent methods, reporting how often experiments were performed, whether results were substantiated under a range of conditions, distinguishing independent biological data points from technical replicates, reporting randomization/blinding/sample-size decisions, and disclosing exclusions and omitted results including results that do not support the main findings.

**Who / authority:** National Institutes of Health official policy/resource page, based on a joint workshop with Nature/Science and journal editors.

**Where:** <https://grants.nih.gov/policy-and-compliance/policy-topics/reproducibility/principles-guidelines-reporting-preclinical-research>

**When / status:** Retrieved 2026-08-13; current public resource at retrieval.

**Transformation:** Candidate schema should preserve cell-level attempts, replicate type, deviations/exclusions, omitted results, and conditions. It must not convert completeness into validity or treat a reported run count as an observed scientific result.

## Source record J — CONSORT/EQUATOR reporting guidance

**What:** EQUATOR lists CONSORT 2025 as an updated reporting guideline for randomized trials, including a 30-item checklist and flow documentation. The CONSORT 2025 explanation emphasizes complete, accurate, and transparent reporting of design, conduct, analysis, results, protocol deviations, and participant flow; its general logic supports explicit accounting for exclusions and changes rather than silent omission. This is a competing reporting framework, not a factorial-execution standard for AION/Astra.

**Who / authority:** EQUATOR Network reporting-guideline repository and CONSORT 2025 authors; clinical-trial reporting guidance.

**Where:** <https://www.equator-network.org/reporting-guidelines/consort/> and <https://pmc.ncbi.nlm.nih.gov/articles/PMC11995452/>

**When / status:** CONSORT 2025 materials retrieved 2026-08-13; current public reporting guidance at retrieval.

**Transformation:** Candidate ledger should include flow-like accounting for planned/attempted/completed/excluded/unreported cells and preserve deviation reasons. It must not borrow clinical claims or treat the guidance as a proof of scientific reliability.

## Candidate-unit boundary

```text
PLANNED_CELL != EXECUTED_CELL
EXECUTED_CELL != VALID_RESULT
EXCLUDED_CELL != DELETED_EVIDENCE
FAILED_CELL != NEGATIVE_SCIENTIFIC_RESULT
REPORTING_COMPLETENESS != SCIENTIFIC_VALIDITY
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
