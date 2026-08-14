# CSOMI Selective Promotion Inventory v0.1.0

## Purpose and boundary

This document defines a **candidate-only selective promotion inventory**. It is reconstructed from the read-only CSOMI research source and is not a merge, cherry-pick, or release instruction.

| Boundary | Value |
|---|---|
| Candidate branch | `promotion/csomi-selective-canonical-20260814` |
| Candidate base | `main@e079fb7dfe7a04be7dcb94b8a059951a003caa94` |
| Read-only research source | `research/cross-substrate-other-minds-inference-20260814@87405c1877c6f016c303971da13923a1ab690aae` |
| Transfer mode | Reconstructed generic infrastructure; no direct branch copy or cherry-pick |
| Canonical effect | `PENDING_OWNER_PROMOTION` |
| Deployment | `FALSE` |
| Topics applied | `FALSE` |
| Main merge | `PROHIBITED` |
| Subjectivity conclusion | `NOT_ESTABLISHED` |
| Review state | `READY_FOR_CHATGPT_PROMOTION_REVIEW` |
| Owner approval | `PENDING` |

The provenance roles are deliberately separated. **Human Owner** supplies task authorization and final authority; **ChatGPT** supplies architecture review and selective-promotion design; **Manus** implements and validates the candidate; and **Owner approval** remains pending. These roles do not assign external scientific authorship or authority to ChatGPT or Manus.

## Candidate inventory

| ID | Decision | Candidate promotion unit | Canonical treatment | Why |
|---|---|---|---|---|
| PROM-001 | **INCLUDE** | Semantic-separation guard | Reconstruct a generic schema/checker invariant for `RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION`. | This is a reusable category boundary and contains no CSOMI claim or subjectivity conclusion. |
| PROM-002 | **INCLUDE** | Test/CI non-evidence guard | Reconstruct a generic machine-checkable rule that test or CI success cannot serve as subjectivity evidence. | This prevents repository validation from being misrepresented as scientific evidence and does not alter CI execution. |
| PROM-003 | **INCLUDE** | Source-access provenance grading | Reconstruct generic access-grade enums and require explicit access evidence. | A source being primary does not imply that its full text was directly verified. This unit contains no literature row or scientific claim. |
| PROM-004 | **INCLUDE** | Claim/evidence/alternative/disanalogy/falsifier consistency | Reconstruct generic record-level requirements for alternatives, transfer/disanalogy status and falsifier disposition. | The structure is useful as canonical evidence hygiene, while all CSOMI-specific fixtures, claims and matrices remain excluded. |
| PROM-005 | **OWNER_REVIEW** | Canonical path/version/main integration | Do not implement integration in this candidate. | Path placement, versioning, maintainership and any main integration require Owner review. |
| PROM-006 | **OWNER_REVIEW** | Scientific-conclusion or public-positioning policy | Preserve all conclusions as `NOT_ESTABLISHED`; do not implement a positioning change. | Any subjectivity, consciousness or identity-continuity policy is an authority and evidence decision. |
| PROM-007 | **OWNER_REVIEW** | Canonical promotion/release/deployment/Topics | Keep all effects disabled. | Promotion, release, deployment, Topics and main merge are outside this candidate. |

## Research artifacts explicitly excluded

The candidate does not bring over the literature dossier, `PRIMARY_SOURCE_FINDINGS`, `CSOMI_FINAL_HANDOFF`, research-specific workflow, synthetic positive/negative controls, reviewer-facing vertical slice, unexecuted experiment or preregistration, individual literature scientific dispositions, CSOMI research claim rows, CSOMI research matrices as canonical data, runtime or model changes, deployment/release/Topics operations, or any subjectivity, consciousness or identity-continuity conclusion.

The candidate therefore promotes **generic infrastructure semantics only**, not the research content that motivated or demonstrated them. A schema or test that is valid only for CSOMI research remains on the read-only research branch and is not copied merely to make this candidate appear complete.

## Promotion review gate

The candidate is **READY_FOR_CHATGPT_PROMOTION_REVIEW** because the inventory is explicit, the included units are reconstructed generically, and the candidate can be reviewed without changing `main`. It remains **OWNER_DECISION_REQUIRED** for any canonical promotion, main merge, public positioning, release, deployment, Topics, experiment, model change or runtime integration.

> `CANONICAL_EFFECT=PENDING_OWNER_PROMOTION` is a candidate-state marker, not an executed promotion.
