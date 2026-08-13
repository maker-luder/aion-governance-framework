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
