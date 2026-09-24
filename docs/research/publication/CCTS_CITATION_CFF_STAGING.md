# Proposed CCTS CITATION.cff content — NOT ROOT METADATA

This is a human-readable staging template only. It is intentionally not named `CITATION.cff` at the repository root because required Human-controlled metadata remains unresolved.

```yaml
cff-version: 1.2.0
message: "If you use the CCTS scholarly release, please cite the archived release identified by its DOI."
title: "Co-Constructed Thinking Space (CCTS): A Provenance-Bounded Framework for Human–AI Reciprocal Epistemic Collaboration"
type: software
version: "0.1.0"

authors:
  - name: "<PUBLIC_AUTHOR_NAME_REQUIRES_HUMAN_CONFIRMATION>"

repository-code: "https://github.com/maker-luder/aion-governance-framework"

abstract: >-
  Co-Constructed Thinking Space (CCTS) is a repository-defined,
  provenance-bounded interaction-and-artifact framework for studying
  reciprocal Human–AI epistemic collaboration. It requires explicit problem
  representation, substantive bidirectional revision or challenge,
  source-role provenance, claim boundaries, authority separation and
  rejected-branch preservation. CCTS is presented as a conceptual and
  methodological construct, not as a validated psychological mechanism or
  evidence of AI subjectivity.

keywords:
  - Human-AI collaboration
  - Human-AI interaction
  - epistemic collaboration
  - co-construction
  - provenance
  - reciprocal revision
  - distributed cognition
  - research integrity

# date-released: "<SET_ONLY_WHEN_RELEASE_DATE_EXISTS>"
# doi: "<BACKFILL_AFTER_DOI_IS_MINTED>"
# license: "<FINAL_LICENSE_REQUIRES_RELEASE-SCOPE_DECISION>"
```

## Validation boundary

The template above is **not release-valid yet** because it contains unresolved placeholders.

```text
TEMPLATE_EXISTS != ROOT_CITATION_UPDATED
PLACEHOLDER_METADATA != RELEASE_METADATA
```

Before copying any form of this template to root `CITATION.cff`:
1. Human public author name must be explicitly confirmed.
2. Release scope and license must be confirmed.
3. Exact release commit must be frozen.
4. The root historical citation transition must be reviewed.
5. The Human Owner must explicitly authorize the root metadata change.
