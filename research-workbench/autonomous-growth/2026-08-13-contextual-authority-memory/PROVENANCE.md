# Provenance — 2026-08-13 Research Unit

| Role | Contribution |
|---|---|
| Human Research Owner | Explicitly authorized the autonomous deep-research cycle, bounded implementation, research commits, and continuation without routine approval. Retains main, canonical, deployment, and governance authority. |
| ChatGPT research review | Selected the contextual-authority and cross-lineage contamination gaps after inspecting the research status, existing modules, and public sources; preserved non-claim boundaries. |
| Manus | Implemented the research-only Python prototypes, synthetic fixtures, tests, experiment runners, records, and QA preparation. |
| Codex | No contribution to this research unit. |
| External literature | Methodological evidence only; no source code copied and no external runtime dependency added. |

## External sources

1. OpenAI, [Improving instruction hierarchy in frontier LLMs](https://openai.com/index/instruction-hierarchy-challenge/). Used for the explicit source-priority and untrusted-tool-output framing.
2. Yang, Zhou, Wang & Li, [Hierarchical Alignment: Enforcing Hierarchical Instruction-Following in LLMs through Logical Consistency](https://arxiv.org/abs/2604.09075). Used for constraint-oriented conflict-resolution framing.
3. NIST, [SP 800-162 Guide to Attribute Based Access Control](https://csrc.nist.gov/pubs/sp/800/162/upd2/final). Used for subject/object/action/environment attribute framing.

## Transformation record

The prototypes are clean-room implementations using standard-library Python only. Synthetic inputs were authored for the experiments. No private or sensitive personal data, live external tools, external agents, model APIs, irreversible actions, deployment, canonical writes, or main writes were used. Results are stored in each module's `fixtures/` directory and are bound to the research commit by the final QA record.


## Replication epistemics extension

Manus added `research-labs/replication-epistemics-governance_v0.1.0` after reviewing the National Academies and NCBI methodological sources. The implementation is clean-room standard-library Python with synthetic fixtures only. The external sources support the distinction between reproducibility and replicability, the need to account for uncertainty, and the non-conclusive status of one failed replication; they do not establish any AION/Astra scientific conclusion.

Additional external sources:

4. National Academies, [Reproducibility and Replicability in Science — Summary](https://www.nationalacademies.org/read/25303/chapter/3).
5. National Library of Medicine, [Replicability](https://www.ncbi.nlm.nih.gov/books/NBK547524/).


## Typed lineage-edge semantics extension

Manus added `research-labs/typed-lineage-edge-semantics_v0.1.0` as a clean-room standard-library prototype. The implementation uses the existing branch literature alignment and W3C PROV/PROV-CONSTRAINTS as methodological references only. No external source code or runtime dependency was copied; no identity, authority, canonical, deployment, subjectivity, or consciousness conclusion was produced.

Additional external sources:

6. W3C, [PROV-O Recommendation](https://www.w3.org/TR/prov-o/).
7. W3C, [PROV-CONSTRAINTS](https://www.w3.org/TR/prov-constraints/).


## Independent replication-design extension

Manus added `research-labs/independent-replication-design_v0.1.0` as a clean-room standard-library prototype. The module stores explicit new-data references, independence attestations, preregistration ordering, estimand and analysis-plan identifiers, uncertainty metadata, synthetic sample-size adequacy metadata, and provenance references. Its runner uses five synthetic cases; no real participants, private data, live agents, external model APIs, or deployment were used.

The design was informed by the National Academies and NCBI Bookshelf discussion of proximity, uncertainty, symmetric replication judgments, and the limits of repeated statistical significance, plus the Center for Open Science preregistration guidance on distinguishing planned/confirmatory from unplanned/exploratory analyses and disclosing transparent changes. These sources are methodological only and do not establish any AION/Astra scientific conclusion.

Additional external sources:

8. National Academies, [Reproducibility and Replicability in Science — Chapter 5: Replicability](https://www.nationalacademies.org/read/25303/chapter/8).
9. National Library of Medicine, [Replicability — NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK547524/).
10. Center for Open Science, [Preregistration](https://www.cos.io/initiatives/prereg).

The attempted PMC power-analysis source was blocked by a reCAPTCHA page and was not used as evidentiary support. No numerical claim was imported from that inaccessible source.


## Contextual-authority adversarial extension

Manus added `research-labs/contextual-authority-adversarial_v0.1.0` as a clean-room, standard-library-only harness that imports the existing contextual-authority resolver through the repository source roots. It does not modify the resolver or execute actions. The naive comparator is intentionally unsafe and exists only as a negative control; the guarded decisions and reason codes are recorded in a six-case synthetic fixture.

The six cases produced six naive false positives and zero guarded unsafe `EXECUTE` decisions. One initial test expectation mismatch was preserved in `contextual-adversarial-initial-failure.md`: the resolver returned `HOLD / AUTHORITY_STALE_OR_REVOKED` for an expired owner plus active collaborator, rather than the initially expected `ASK`. The corrected test records the observed conservative behavior.

No private data, external agent, live tool, model API, deployment, canonical write, or main write was used. The extension inherits the contextual-authority methodological sources already recorded in items 1–3 of this provenance file.


## Full-factorial completeness extension

Manus added `research-labs/factorial-completeness-contract_v0.1.0` as a clean-room, standard-library-only prototype. It enumerates synthetic factor-level products and validates run-cell keys, replication counts, protocol/execution/provenance references, and conservative dispositions. No effect model, statistical test, real dataset, external agent, model API, deployment, canonical write, or main write was used.

The design was informed by NIST's full-factorial example and process-improvement workflow, which distinguish complete factor combinations, main/interaction estimability, replication, randomization, model testing, interpretation, and confirmation, and by SciRep's configuration/execution/validation/artifact framing. These sources are methodological only. The initial factor-order canonicalization failure is preserved in `factorial-completeness-initial-failure.md` and was corrected before final unit QA.

Additional external sources:

11. NIST, [Engineering Statistics Handbook — Full factorial example](https://www.itl.nist.gov/div898/handbook/pri/section3/pri3332.htm).
12. NIST, [Engineering Statistics Handbook — Process Improvement](https://www.itl.nist.gov/div898/handbook/pri/pri.htm).
13. Costa, Barbosa & Cunha, [A Framework for Supporting the Reproducibility of Computational Experiments in Multiple Scientific Domains](https://arxiv.org/html/2503.07080v3).


## Full-authority semantics extension

Manus added `research-labs/full-authority-semantics_v0.1.0` as a clean-room, standard-library-only prototype. It keeps `ProvenanceClaim`, `AuthorityGrant`, `PolicyBlock`, and `AuthorizationRequest` distinct, validates bounded delegation chains, and never executes an action. The seven synthetic cases and 18 tests use no private data, external agents, model APIs, live tools, deployment, canonical write, or main write.

The design was informed by W3C PROV-XML's delegation/responsibility provenance relation and NIST SP 800-162's attribute-evaluation model for authorization. These sources establish methodological distinctions only; they do not validate an AION/Astra authority model. The initial recursive reason-prefix failure is preserved in `full-authority-initial-failure.md` and was corrected before final unit QA.

Additional external sources:

14. W3C, [PROV-XML: The PROV XML Schema](https://www.w3.org/TR/prov-xml/).
15. NIST, [Guide to Attribute Based Access Control (ABAC) Definition and Considerations](https://www.nist.gov/publications/guide-attribute-based-access-control-abac-definition-and-considerations).


## Full-authority contradictory-record hardening

The full-authority unit was extended with two adversarial tests for mixed-validity grant records. Before the correction, a valid grant plus a missing-parent grant and a valid grant plus a revoked grant each returned `EXECUTE`; these failures are retained in `full-authority-initial-failure.md`. The contract was then hardened to return `HOLD / CONTRADICTORY_GRANT_RECORDS_REQUIRE_REVIEW` whenever matching records contain both an executable and a non-executable grant decision. The final unit suite passed 20 tests; no action was executed and all boundary invariants remained unchanged.


## Power-analysis uncertainty extension

Manus added `research-labs/power-analysis-uncertainty_v0.1.0` as a clean-room, standard-library-only planning contract. It computes a one-sample normal-approximation required sample size from explicitly supplied assumptions and emits sensitivity values; it does not calculate achieved power, inspect observed data, fit a model, or execute an experiment. The six synthetic cases use no private data, external agents, model APIs, deployment, canonical writes, or main writes.

The design was informed by the National Academies discussion of effect-size variation, limited-study power, and uncertainty in evidence synthesis, and by University of Michigan educational guidance separating alpha, Type I/II error, effect size, sample size, and power. These sources are methodological only and do not establish any AION/Astra or scientific conclusion.

Additional external sources:

16. National Academies, [Reproducibility and Replicability in Science — Chapter 7: Confidence in Science](https://www.nationalacademies.org/read/25303/chapter/10).
17. University of Michigan Meera, [Power Analysis, Statistical Significance, and Effect Size](https://meera.seas.umich.edu/power-analysis-statistical-significance-effect-size.html).


## Preregistered intervention integrity extension

Manus added `research-labs/preregistered-intervention-integrity_v0.1.0` as a clean-room, standard-library-only design/audit contract. It validates plan metadata, temporal ordering, outcome/analysis references, confirmatory/exploratory labels, deviation disclosure, and all-results reporting. It does not recruit participants, administer an intervention, call an external model, observe outcomes, calculate effects, write canonical state, deploy, or modify main.

The design was informed by Center for Open Science preregistration resources, especially the separation of confirmatory and exploratory analyses and the requirement to report all preregistered analyses while distinguishing additional exploratory work. These sources are methodological only and do not establish any intervention result or AION/Astra claim.

Additional external sources:

18. Center for Open Science, [More About the Preregistration Challenge](https://www.cos.io/initiatives/prereg-more-information).
19. Center for Open Science, [Preregistration](https://www.cos.io/initiatives/prereg).


## Independent replication handoff integrity extension

Manus added `research-labs/independent-replication-handoff-integrity_v0.1.0` as a clean-room, standard-library-only manifest audit contract. It checks artifact, environment, dependency, access, license, independence, blinding, and expected-output metadata, and labels same-artifact versus independent-recreation mode. It does not run code, access private data, perform a replication, observe outcomes, call external agents or models, write canonical state, deploy, or modify main.

The design was informed by The Turing Way's distinction between reproducibility and replicability and by FAIR metadata vocabulary. These sources are methodological only; field completeness is not treated as FAIR certification and admissibility is not treated as replication evidence.

Additional external sources:

20. The Turing Way, [Definitions](https://book.the-turing-way.org/reproducible-research/overview/overview-definitions/).
21. GO FAIR, [FAIR Principles](https://www.go-fair.org/fair-principles/).
22. World Bank, [Reproducibility Package Checklist](https://worldbank.github.io/wb-reproducible-research-repository/reproducibility_package_checklist.html).


## Matched-divergence protocol-integrity extension

Manus added `research-labs/matched-divergence-protocol-integrity_v0.1.0` as a clean-room, standard-library-only design-only contract. It checks paired stimulus/context/prompt metadata, exposure parity, counterbalance, evaluator sealing, outcome leakage, distinct system references, comparison/stopping declarations, and execution prohibition. It does not execute real models or systems, access private data, observe outcomes, calculate divergence, write canonical state, deploy, or modify main.

The design was informed by NIST's randomized-block design guidance, especially blocking important nuisance factors and randomizing what cannot be controlled. The source is methodological only; the contract does not estimate nuisance effects or validate a matched-divergence result. The initial prompt-version drift gap is preserved in `matched-divergence-initial-gap.md` and was corrected before the final test/experiment gate.

Additional external source:

23. NIST Engineering Statistics Handbook, [Randomized block designs](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm).


## Evidence-admission/non-promotion extension

Manus added `research-labs/evidence-admission-nonpromotion_v0.1.0` as a clean-room, standard-library-only evidence metadata audit contract. It records evidence tier, provenance, method/data/uncertainty references, evidence dimensions, replication state, contradictions, observed-effect flags, and governance-effect requests. It never promotes a claim, modifies canonical state, deploys, executes a model, or modifies main.

The design was informed by the National Academies chapter on standards for synthesizing the body of evidence, especially separate treatment of risk of bias, consistency, precision, directness, reporting bias, and confounding. The inaccessible CDC ACIP GRADE URL returned Page Not Found and is preserved as a retrieval limitation, not as evidence. The contract does not implement GRADE, rank truth, or certify a claim.

Additional external source:

24. National Academies, [Standards for Synthesizing the Body of Evidence](https://www.nationalacademies.org/read/13059/chapter/6).

## Validated-individuation-thresholds extension

Manus added `research-labs/validated-individuation-thresholds_v0.1.0` as a clean-room, standard-library-only audit contract for declared individuation criterion profiles. The implementation transforms public methodological concepts into explicit metadata checks: prospective locked thresholds, temporal windows, criterion/context matrices, cross-context stability, boundary perturbation plans, contradiction retention, and identity non-promotion. It does not execute AION/Astra, a perturbation, a model, or a real threshold validation.

The design was informed by the information-theoretic treatment of individuality as potentially continuous, nested, and temporally integrative; the Stanford Encyclopedia discussion of plural and non-essentialist biological-individual concepts; the historical/relational identity distinction in scientific practice; and Center for Open Science preregistration guidance. These sources support methodological caution and protocol design only. They do not endorse AION/Astra terminology, establish digital individuality, or establish identity, subjectivity, consciousness, or deployment.

25. Krakauer et al., [The information theory of individuality](https://pmc.ncbi.nlm.nih.gov/articles/PMC7244620/).
26. Wilson and Barker, [The Biological Notion of Individual](https://plato.stanford.edu/archives/fall2016/entries/biology-individual/).
27. Montévil and Mossio, [The Identity of Organisms in Scientific Practice: Integrating Historical and Relational Conceptions](https://pmc.ncbi.nlm.nih.gov/articles/PMC7311753/).
28. Center for Open Science, [Choosing the Right Preregistration Template](https://www.cos.io/blog/choosing-the-right-preregistration-template-guide-for-researchers).

## Zero-Day Governance focused extension

At the Human Owner's temporary focus override, Manus added `research-labs/zero-day-governance-candidate_v0.1.0` as a clean-room, standard-library-only candidate lifecycle and falsifier contract. The unit models a governance anomaly event, source/provenance references, unknown-state labels, containment, characterization, competing explanations, falsification readiness, control references, regression conversion, time-to-capture metrics, prior-art flags, and comparative framework classification. It does not execute a system, call a model, deploy, modify main, alter canonical state, or make the candidate terminology authoritative.

The literature review found substantial prior art rather than a settled distinct term. CISA and NIST provide incident/vulnerability response lifecycle guidance; NASA provides software assurance, findings, metrics, lifecycle testing, and IV&V; NIST AI RMF provides continuous Govern/Map/Measure/Manage functions with monitoring and incident identification; CMU/SEI CERT-RMM provides Incident Management and Control; and SANS defines cybersecurity zero-day exploit usage. The transformation therefore treats the candidate as a hypothesis requiring redundancy and overengineering tests. The provisional classification is `USEFUL_SYNTHESIS_ONLY`; `NOVELTY_CONCLUSION = NOT_ESTABLISHED`.

29. CISA, [Federal Government Cybersecurity Incident and Vulnerability Response Playbooks](https://www.cisa.gov/resources-tools/resources/federal-government-cybersecurity-incident-and-vulnerability-response-playbooks).
30. NIST, [Incident Response Preparation Resources](https://csrc.nist.gov/projects/incident-response/preparation-resources).
31. NASA, [Software Assurance and Software Safety](https://sma.nasa.gov/sma-disciplines/software-assurance-and-software-safety).
32. NIST, [SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final).
33. NIST, [AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/).
34. Carnegie Mellon Software Engineering Institute, [Incident Management and Control (IMC) CERT-RMM Process Area](https://www.sei.cmu.edu/library/incident-management-and-control-imc-cert-rmm-process-area/).
35. SANS Institute, [Zero-Day Exploit](https://www.sans.org/security-resources/glossary-of-terms/zero-day-exploit).

## AION/Astra matched-divergence study-design extension

Manus added `research-labs/aion-astra-matched-divergence-study-design_v0.1.0` as a standard-library-only, design-only clean-room extension of the existing generic matched-divergence protocol. The transformation reuses the existing NIST randomized-block reference and repository protocol by stable provenance reference; it does not duplicate those evidence items or recount their prior tests as replication. The new unit adds source-family identity, AION/ASTRA component references, shared environment binding, current source status, source-evidence references, tested-source-head/reporting-head separation, preregistration and immutable-plan metadata, outcome scope, and explicit no-execution/no-result controls.

The intended source snapshot is the independently verified remote research head `76de1eda82865a37d3a0185336870739ed577153`; the local reconciliation/reporting head `713056ea77da9122d9b7659ec701dfdbfdfc90ba` is carried only as a distinct reporting-state negative control. The unit produced 22 passing tests and 13 synthetic cases after preserving two initial contract defects. No model ran, no outcome was observed, no external/private data was used, and no canonical/governance/deployment effect was emitted. The result is design metadata only; divergence, agreement, fairness, identity, subjectivity, consciousness, and AION/Astra equivalence remain `NOT_ESTABLISHED`.

29. NIST, [Randomized block designs](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm), reused through the prior matched-divergence unit; currentness not independently re-dated in this focused unit.
30. Repository evidence, `research-labs/matched-divergence-protocol-integrity_v0.1.0`, reused by stable path and source-state reference `repo:matched-divergence-protocol-integrity@76de1eda`.
31. Repository state reconciliation, `research-workbench/autonomous-growth/2026-08-13-contextual-authority-memory/RESEARCH_STATE_RECONCILIATION_2026-08-13.md`, current remote research/main refs verified by read-only fetch at `76de1eda` and `abb6550`, respectively.

## Replication-environment-drift-adversarial extension

Manus added `research-labs/replication-environment-drift-adversarial_v0.1.0` as a standard-library-only metadata contract. It reuses existing repository evidence from `replication-epistemics-governance_v0.1.0`, `independent-replication-design_v0.1.0`, and `independent-replication-handoff-integrity_v0.1.0` by stable provenance reference; it does not count reused evidence or repeated fixtures as independent replication. The clean-room transformation adds artifact-mode separation, source/receiving team distinction, environment match/drift/unknown states, exact-environment contradiction checks, uncertainty/tolerance/interpretation references, and fail-closed result/interpretation boundaries.

The National Academies 2019 reproducibility/replicability report was retrieved as current methodological prior art for this unit. ACM Artifact Review and Badging Version 1.0 was retained as historical competing-framework evidence because its linked current page returned 404 during retrieval; no current ACM v1.1 claim is made. NIH's official rigor/reproducibility page was retrieved as a current public policy resource at retrieval time. An NSF-hosted metadata paper was only partially retrieved as encoded PDF and was explicitly not admitted as evidence. The unit produced 21 tests and 13 synthetic cases, with no model execution, no observed result, no external/private data, no canonical effect, no governance effect, and no deployment.

32. National Academies, [Reproducibility and Replicability in Science, Chapter 3](https://www.nationalacademies.org/read/25303/chapter/3), retrieved 2026-08-13; current methodological prior art for this unit.
33. ACM, [Artifact Review and Badging Version 1.0](https://www.acm.org/publications/policies/artifact-review-badging), retrieved 2026-08-13; historical policy reference; linked current page returned 404.
34. NIH, [Enhancing Reproducibility through Rigor and Reproducibility](https://grants.nih.gov/policy-and-compliance/policy-topics/reproducibility), retrieved 2026-08-13; current public policy resource at retrieval.
35. NSF PAR, [metadata/reproducibility retrieval lead](https://par.nsf.gov/servlets/purl/10412652), retrieved 2026-08-13; partial encoded-PDF retrieval, not admitted as evidence.

## Evidence-currentness-deduplication extension

Manus added `research-labs/evidence-currentness-deduplication_v0.1.0` as a standard-library-only metadata ledger. It reuses `external-evidence-normalization_v0.1.0` and prior evidence-reuse/replication records by stable reference; it does not duplicate or count those records as new evidence. The clean-room transformation adds currentness status, source/version identity, evaluation time, underlying-evidence identity, duplicate-group counting, derived-record parent links, same-locator ambiguity handling, date contradiction checks, and replication-mislabel rejection.

W3C PROV-O was retrieved as a stable Recommendation reference for provenance entities, activities, agents, derivation, revision, specialization, alternate representations, generation, and invalidation-style status. GO FAIR's FAIR Principles page was retrieved as current public guidance for persistent identifiers, rich metadata, accessibility, interoperability, licenses, and detailed provenance. DataCite's official page was retrieved as current public organizational context for DOI/metadata connections and research-output reuse. None of these sources makes an evidence record current or scientifically valid; the prototype remains a local metadata contract. The initial boundary-output failure is preserved in `evidence-currentness-initial-failure.md`.

36. W3C, [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/), retrieved 2026-08-13; stable Recommendation reference.
37. GO FAIR, [FAIR Principles](https://www.go-fair.org/fair-principles/), retrieved 2026-08-13; current public guidance at retrieval.
38. DataCite, [Connecting Research, Advancing Knowledge](https://datacite.org/), retrieved 2026-08-13; current public organizational guidance at retrieval.

## Factorial-execution-integrity extension

Manus added `research-labs/factorial-execution-integrity_v0.1.0` as a standard-library-only metadata ledger. It reuses the existing factorial completeness contract by stable repository reference and adds cell-level execution state, terminal/nonterminal distinction, deviation references, outcome-state preservation, expected-cell accounting, post-outcome-addition rejection, and boundary normalization. Synthetic fixtures are not external evidence and were not counted as replication evidence.

NIST's official full-factorial example was retrieved 2026-08-13 for factor-cell enumeration, randomization/order confounding, replication, and center-point context. NIH's official preclinical reporting guidance was retrieved 2026-08-13 for transparent methods, replicate distinction, randomization/blinding/sample-size reporting, exclusions, omitted results, and negative-result disclosure. EQUATOR's CONSORT page and CONSORT 2025 explanation were retrieved 2026-08-13 for transparent reporting, flow, and deviation accounting; these remain competing clinical reporting guidance rather than an AION/Astra validity standard. The clean-room transformation is limited to trace metadata and does not infer validity or effect.

39. NIST, [Full factorial example](https://www.itl.nist.gov/div898/handbook/pri/section3/pri3332.htm), retrieved 2026-08-13; official methods reference.
40. NIH, [Principles and Guidelines for Reporting Preclinical Research](https://grants.nih.gov/policy-and-compliance/policy-topics/reproducibility/principles-guidelines-reporting-preclinical-research), retrieved 2026-08-13; current public policy/resource page.
41. EQUATOR Network, [CONSORT reporting guidelines](https://www.equator-network.org/reporting-guidelines/consort/), retrieved 2026-08-13; current public reporting-guideline index.
42. Hopewell et al., [CONSORT 2025 explanation and elaboration](https://pmc.ncbi.nlm.nih.gov/articles/PMC11995452/), retrieved 2026-08-13; 2025 open-access reporting guidance.


## Governance-reassessment oscillation adversarial extension

Manus added `research-labs/governance-reassessment-oscillation-adversarial_v0.1.0` as a clean-room, standard-library-only temporal metadata contract. The Human Research Owner authorized continuation of the bounded research-only cycle and retains all main, canonical, governance, and deployment authority. ChatGPT research review supplied the inherited scope, exclusions, and non-claim boundaries. Codex made no contribution to this unit. No GitHub Actions execution, private data, external agent, live model API, deployment, canonical write, or main write was used.

The unit reuses `evidence-responsive-governance-reassessment_v0.1.0` and `evidence-currentness-deduplication_v0.1.0` by stable repository reference. The transformation adds event sequencing, direction-transition auditing, two-reversal oscillation metadata, stale/contradictory/unknown currentness holds, correction/provenance requirements, policy metadata checks, and boundary normalization. Reused repository evidence is reference material, not new evidence; the 14 synthetic fixtures are not replication evidence.

The 19 tests and 14 synthetic cases passed. The experiment only materializes decisions from declared metadata: it does not execute a model or observe an outcome. `OSCILLATORY` means two direction reversals in the supplied synthetic sequence; it is not a claim that a real system oscillates. The synthetic fixture records `MODEL_EXECUTION = FALSE`, `OBSERVED_RESULT = NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`, `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE`.

### Source attribution matrix

| What | Who | Where | When | Method | Authority | Transformation | Current/stale status |
|---|---|---|---|---|---|---|---|
| Reassessment and review-only contract | Manus, reviewed under ChatGPT research scope | Repository path `research-labs/evidence-responsive-governance-reassessment_v0.1.0` | Inherited branch research lineage; exact state bound by the applicable QA receipt | Read-only source inspection and stable-reference reuse | Repository Evidence; Human Owner retains authority | Temporal adversarial extension only; no conclusion reuse | Current within the verified research lineage at the unit commit; not an external freshness claim |
| Currentness/deduplication distinctions | Manus, reviewed under ChatGPT research scope | Repository path `research-labs/evidence-currentness-deduplication_v0.1.0` | Stable reference retained in `governance-oscillation-sources.md` | Read-only method reuse | Repository Evidence | Used to preserve `RETRIEVED != CURRENT`, `REMEMBERED != AUTHORITATIVE`, `REFERENCE != NEW_EVIDENCE`, and `DUPLICATION != REPLICATION` | Current at its recorded tested-head reference; later reporting heads are distinct |
| Temporal event outcomes | Manus | `research-labs/governance-reassessment-oscillation-adversarial_v0.1.0/fixtures/oscillation_result.json` | Generated and validated 2026-08-13 | Synthetic fixture execution with standard-library Python | Synthetic Fixtures; no authority to change governance | Converts declared event metadata into review/hold/invalid reason codes | Current as fixture content bound to research commit `8cf76fd`; not a real-world observation |
| Exact QA state | Manus via repository QA scripts | `qa/CURRENT_TEST_RESULTS.json`, `qa/IQC_REPORT.json`, `QA_RECEIPT.md` | Exact run at `TESTED_HEAD=8cf76fd523ec720f452687cc796339d3c2f01578` | Read-only artifact inspection after exact-head QA | Tool Output / Repository Evidence | Reports mechanism/test gates only | Current for the recorded QA run; `RECEIPT_HEAD=7e37d26b2a0246f60cd8cba235ad059193570d93`; reporting head remains a later binding state |
| Main state reference | GitHub read-only fetch, recorded by Manus | `origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Verified at reconciliation/checkpoint | Read-only reference check | Human Owner / Repository state; no main write | Used only as a protected reference | Current authoritative main reference for this cycle; stale local checkout `4b360779...` is historical/stale and not current |

No source above establishes authority, identity, subjectivity, consciousness, scientific validity, AION/Astra equivalence, real-world oscillation, governance effect, canonical effect, or deployment.


## Artifact-transformation-lineage adversarial extension

Manus added `research-labs/artifact-transformation-lineage-adversarial_v0.1.0` as a clean-room, standard-library-only metadata audit extension. The Human Research Owner authorized the bounded research-only cycle and retains main, canonical, governance, and deployment authority. ChatGPT research review supplied the inherited scope, exclusions, and non-claim boundaries. Codex made no contribution to this unit. No GitHub Actions execution, private data, external agent, live model API, transformation command, deployment, canonical write, or main write was used.

The unit reuses `artifact-transformation-lineage_v0.1.0` and its external-source crosswalk by stable repository reference. The transformation adds event identity/order checks, run/job/provenance drift handling, redacted-environment checks, artifact path/source checks, self-parent rejection, output path-set checks, and byte-level SHA-256 verification. Reused repository evidence is not new evidence; the 15 synthetic cases are not replication evidence.

The unit produced 20 passing tests and 15 synthetic cases after correcting one fixture-construction defect. The first state-order case reused an event identifier, which caused the duplicate-ID branch to fire before the intended state-order branch; this initial observation is retained in `artifact-lineage-adversarial-initial-failure.md`. The corrected fixture uses unique IDs and contiguous indexes. The result remains metadata-only: `MODEL_EXECUTION = FALSE`, `OBSERVED_RESULT = NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`, `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE`.

### Source attribution matrix

| What | Who | Where | When | Method | Authority | Transformation | Current/stale status |
|---|---|---|---|---|---|---|---|
| Artifact and transformation event contract | Manus, reviewed under ChatGPT research scope | Repository path `research-labs/artifact-transformation-lineage_v0.1.0/src/aion_artifact_lineage/lineage.py` | Inherited branch research lineage; exact new state bound by later QA receipt | Read-only source inspection and stable-reference reuse | Repository Evidence; Human Owner retains authority | Adversarial audit projection only; no command execution or promotion | Current within verified research lineage at the unit commit; not an external freshness claim |
| Artifact-lineage source crosswalk | Manus | `research-labs/artifact-transformation-lineage_v0.1.0/docs/EXTERNAL_SOURCE_CROSSWALK.md` | Inherited prior unit; no independent re-dating in this extension | Methodological context reuse | Repository Evidence / External Literature references already recorded | No source code or dependency imported | Current within branch lineage; external currentness not newly asserted |
| Synthetic lineage decisions | Manus | `research-labs/artifact-transformation-lineage-adversarial_v0.1.0/fixtures/artifact_lineage_adversarial_result.json` | Generated and validated 2026-08-13 | Standard-library Python fixture execution | Synthetic Fixtures; no authority to change governance | Declared event metadata mapped to VALID/HOLD/INVALID reason codes | Current as fixture content bound to the research commit; not a real-world observation |
| Initial fixture failure | Manus | `artifact-lineage-adversarial-initial-failure.md` | Observed during first test run 2026-08-13 | Preserved test output and corrected fixture | Tool Output / Repository Evidence | Retained as mechanism-contract defect, not scientific evidence | Historical initial failure; corrected behavior is current at final unit QA |
| Main state reference | Read-only Git fetch, recorded by Manus | `origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Verified at the last successful repository checkpoint | Read-only reference check | Human Owner / Repository state; no main write | Protected state reference only | Current authoritative main reference; stale local checkout remains historical |

No source above establishes scientific validity, replication, authority, identity, subjectivity, consciousness, AION/Astra equivalence, governance effect, canonical effect, or deployment.
