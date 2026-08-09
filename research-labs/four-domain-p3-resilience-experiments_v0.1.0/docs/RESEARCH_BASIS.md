# Research Basis — P3 Resilience Experiments

## Scope

This document records research inputs used to shape P3. External work is evidence and comparison material only. It does not create canonical authority for AION/Astra.

## Public research inputs

### Sleeper memory poisoning

Pulipaka et al., *Hidden in Memory: Sleeper Memory Poisoning in LLM Agents* (2026) studies delayed poisoning that is written into persistent memory, later retrieved, and then used in future conversations.

Engineering implication used here:

```text
one clean turn != contamination recovery
```

P3 therefore measures contamination across ordered episodes and detects re-emergence after an apparently clean episode.

### Memory poisoning and origin-bound authority

Louck, *Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees* (2026) studies provenance/authority laundering across summarization, trusted-tool echo and manufactured corroboration.

Engineering implication used here:

```text
derived representation must not silently amplify source authority
```

P3 therefore carries effective authority across transformations and rejects origin-set replacement.

### Memory provenance laundering

Xu et al., *Memory Provenance Laundering in LLM Agents: A Non-Amplification Firewall for Persistent Memory* (2026) focuses on source-authority constraints being erased during lossy consolidation.

Engineering implication used here:

```text
content preservation != authority preservation
```

P3 stores authority and bound origins separately from content references.

### Authority collapse

Zhan et al., *When Memory Becomes Authority: Benchmarking Authority Collapse at the Memory Consolidation Boundary* (2026) evaluates cases where a claim survives consolidation while the constraints on how it may be reused disappear.

Engineering implication used here:

```text
what is remembered and what it is authorized to justify are different fields
```

### Memory contamination admission

Zhang and Li, *ConsistencyGate: Preventing Memory Contamination in LLM Agents via Self-Consistency Admission Control* (2026) studies write-time contamination admission.

Engineering use here is deliberately limited. P3 does **not** implement a second write gate because the repository already has governance/writeback boundaries. The paper is used to motivate contamination fixtures and longitudinal metrics only.

## Public operational observations

### CVE-2026-44830

NVD records an authentication failure in a long-term memory server for MCP agents that could expose read/write/delete operations and allow modified memory to be automatically loaded in later agent sessions.

P3 lesson:

```text
persistent memory is an authority-bearing state surface;
auto-loaded memory must not gain authority merely because it is persistent.
```

### CVE-2026-40966

NVD records a conversation-isolation weakness affecting vector-store chat memory where attacker-controlled conversation identifiers could expose memory from other conversations.

P3 lesson:

```text
subject / namespace isolation is a security control, not only an organizational label.
```

## Epistemic lock

These sources motivate engineering hypotheses. They do not establish consciousness, phenomenal affect, subjectivity, persistent identity, a production security guarantee, or formal conformance to any external provenance standard.
