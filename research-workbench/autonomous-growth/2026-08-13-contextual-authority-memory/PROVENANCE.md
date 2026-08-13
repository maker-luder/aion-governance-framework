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
