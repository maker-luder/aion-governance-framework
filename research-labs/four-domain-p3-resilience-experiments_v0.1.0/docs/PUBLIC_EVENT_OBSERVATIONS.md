# Public Event Observations — 2026-08-09

Status: research observation only.

| Observation | Public record | P3 interpretation | Materialized control |
|---|---|---|---|
| Long-term agent memory could be modified through an exposed memory service and later auto-loaded | CVE-2026-44830 | persistence must not imply trusted authority | origin-bound authority + provenance/ablation trials |
| Conversation isolation could be bypassed in vector-store chat memory | CVE-2026-40966 | subject/namespace boundaries have confidentiality impact | subject and namespace ablation |
| Delayed poisoned memories can remain dormant and reactivate later | sleeper-memory research | a clean episode is insufficient evidence of recovery | longitudinal re-emergence metric |
| Consolidation can erase source authority constraints | authority-collapse / provenance-laundering research | content and reuse authority must be tracked separately | authority non-amplification |
| Hallucinated/incorrect memory can compound across long trajectories | contamination research | contamination requires sequence-level metrics | longitudinal contamination rate |

## Safety boundary

The P3 repository fixtures contain structural state changes and identifiers only. They do
not contain exploit payloads, credential material, shell commands, hidden prompt strings or
instructions for attacking a deployed system.
