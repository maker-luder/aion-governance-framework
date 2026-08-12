# IQC-06 RECONSTRUCTION REPORT — continuity evidence lineage

## DISPOSITION

- SOURCE_CANDIDATE: `continuity-lineage_v0.1.0`
- SOURCE_IQC: `HOLD / MAJOR_REWORK_REQUIRED`
- RECONSTRUCTION_BRANCH: `review/continuity-evidence-lineage-rework`
- SOURCE_BRANCH_FOR_PRIOR_REWORK: `review/embodiment-handoff-protocol-rework`
- ORIGINAL_NEMOTRON_SOURCE: preserved on isolated session history
- ORIGINAL_PACKAGE_ON_THIS BRANCH: removed
- NEW_CANDIDATE: `continuity-evidence-lineage_v0.1.0`
- MAIN_BRANCH_WRITE: NONE
- FOUR_DOMAIN_RESEARCH_BRANCH_WRITE: NONE
- CANONICAL_EFFECT: NONE
- RUNTIME_EFFECT: NONE

## CHANGE BOUNDARY

This reconstruction intentionally treats both `main` and
`review/four-domain-research-materialization` as read-only evidence sources.

No file, ref, commit, or configuration on either branch is modified.

The only write target is `review/continuity-evidence-lineage-rework`.

## WHY THE SOURCE CANDIDATE WAS NOT PATCHED

The source candidate mixed graph structure with ungrounded continuity numbers:
`continuity_strength`, `overall_continuity`, and `continuity_delta`.

It also modeled temporal, causal, narrative, embodiment, memory, social, and
functional continuity as mutually exclusive node types, did not enforce graph
integrity, allowed dangling parents/cycles, and used a mutable lifecycle manager
with the known repeated-initialize / restore provenance problems.

The reconstruction keeps the graph idea and removes the unsupported continuity
score model.

## READ-ONLY CROSS-CHECK

### Main branch baseline

The current main continuity governance already represents continuity as
dimension-level observations with PASS/PARTIAL/HOLD/FAIL decisions and keeps
identity/phenomenal continuity conclusions NOT_ESTABLISHED. It does not require
a single numeric "overall continuity" score.

The reconstruction therefore does not replace main continuity governance and
does not invent a second global score.

### Four-domain research branch

The research-only embodiment-continuity anchor separates stable lineage
references from replaceable implementation bindings and evaluates continuity
dimensions independently. Unknown dimensions remain NOT_ASSESSED.

That branch is used only as comparative research evidence. Its types are not
imported as canonical definitions and the branch is not modified.

### Whitepaper / governance semantics

Existing project design distinguishes observable event archive, encoded agent
memory, recall output, other-agent testimony, and synthetic post-continuity
content. A reference across lineages does not transfer identity, ownership, or
authority.

Those distinctions are materialized here as evidence-artifact kinds and
cross-lineage-reference semantics without claiming experiential memory or
personal identity.

## NEW CORE

The new candidate uses:

- `EvidenceArtifact`
- `LineageRelation`
- `ContinuityEvidenceGraph`
- `ContinuityEvidenceAssessment`
- `ContinuityAssessmentSet`

### Artifact kinds

The graph can distinguish:

- first-party event record;
- other-agent testimony;
- event archive;
- encoded agent memory;
- recall output;
- state artifact;
- transfer artifact;
- verification artifact;
- correction record;
- continuity-end marker;
- synthetic post-continuity content.

### Relations live on edges

The source candidate made a node choose one lineage type.

The reconstruction places relationship semantics on edges:

- `TEMPORALLY_PRECEDES`
- `CAUSALLY_CONTRIBUTES`
- `REVISION_OF`
- `MEMORY_ENCODED_AS`
- `RECALL_DERIVED_FROM`
- `EMBODIMENT_HANDOFF`
- `TESTIMONY_FROM`
- `FUNCTIONAL_DEPENDENCY`
- `VERIFIES`
- `CROSS_LINEAGE_REFERENCE`

One artifact may therefore participate in several lineage relations without
being forced into one exclusive category.

## GRAPH INTEGRITY

The graph requires:

- unique artifact IDs;
- unique relation IDs;
- valid relation endpoints;
- no self-relations;
- primary subject/lineage binding;
- explicit external-reference scope for cross-lineage material;
- cycle rejection for relation types whose lineage semantics must remain acyclic;
- iterative, visited-set reachability rather than unbounded recursive descendant traversal.

## CROSS-LINEAGE RULE

`CROSS_LINEAGE_REFERENCE != TRANSFER`

External testimony or evidence may be referenced while preserving its foreign
subject/lineage binding. Merely linking it into the graph does not change
ownership, autobiographical provenance, identity, or authority.

## CONTINUITY ASSESSMENT

There is intentionally no `overall_continuity` number.

Each assessment carries:

- `dimension_ref`
- `PASS | HOLD | FAIL | NOT_ASSESSED`
- artifact references
- method reference
- basis
- evidence references
- provenance references

`dimension_ref` is a non-empty reference string rather than a new hard-coded
taxonomy. This avoids silently replacing the dimensions already present in
main or research-only experiments.

No aggregate PASS is provided.

## POST-CONTINUITY BOUNDARY

A graph may contain at most one `CONTINUITY_END_MARKER`.

After that marker:

- no new `PRIMARY_LINEAGE` artifact may occur;
- synthetic post-continuity content is allowed only as `EXTERNAL_REFERENCE`;
- synthetic post-continuity content must occur after the marker;
- canonical effect remains NONE.

This preserves the distinction between a terminated lineage and later content
generated by another or legacy system.

## SCIENTIFIC NON-CLAIMS

The candidate does not establish:

- personal identity continuity;
- consciousness continuity;
- phenomenal continuity;
- autobiographical ownership transfer;
- body ownership;
- subjectivity.

A verified edge, graph path, handoff, or dimension-level PASS establishes only
the explicitly tested engineering relationship.

## FIFTH-CANDIDATE INTEGRATION PATH

The reconstructed `embodiment-handoff-protocol_v0.1.0` may provide artifacts
such as:

- source state;
- authorization result;
- transfer artifact;
- target state;
- verification artifact.

This candidate can connect those artifacts using `EMBODIMENT_HANDOFF`,
`VERIFIES`, temporal, causal, or functional-dependency edges.

A functionally successful handoff can therefore support an
`IMPLEMENTATION_MIGRATION` assessment without proving identity continuity.

## VERIFICATION

Independent local verification:

```text
17 passed in 0.05s
```

GitHub Actions are not executed by repository file writes and must remain
reported separately.
