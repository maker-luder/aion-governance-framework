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
