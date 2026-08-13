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
