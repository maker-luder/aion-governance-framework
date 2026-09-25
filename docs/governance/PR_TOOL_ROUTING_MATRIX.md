# PR Tool Routing Matrix

Status: `CURRENT_SUPPORT / ACTION-SPECIFIC_ACTIVE_CONTROL`

## Purpose

This control routes repository review tools by existing contribution change class so that each pull request uses the minimum sufficient tool set.

It does not create a second PR taxonomy. It extends the A–E change classes already defined in [`CONTRIBUTING.md`](../../CONTRIBUTING.md).

```text
TOOL_AVAILABLE != TOOL_RELEVANT
MORE_TOOLS != BETTER_REVIEW
NO_TRIGGER -> DO_NOT_INVOKE
DUPLICATE_CAPABILITY -> USE_MINIMUM_SUFFICIENT_TOOL_SET
PLUGIN_OUTPUT != MERGE_AUTHORITY
```

## Routing dispositions

| Disposition | Meaning |
|---|---|
| `REQUIRED` | The tool/capability is part of the normal route for this change class. |
| `CONDITIONAL` | Use only when its explicit trigger is present. |
| `DO_NOT_USE_BY_DEFAULT` | Do not invoke merely because the tool is available. Escalate only through a documented trigger. |
| `NOT_APPLICABLE` | The capability does not materially serve this PR class or scope. |

If a required or triggered tool is unavailable, record `NOT_AVAILABLE` and either use a justified substitute or hold the affected review step. Do not silently pretend the unavailable tool ran.

## Existing PR change classes

| Class | Typical scope |
|---|---|
| A | Documentation and examples |
| B | Tests, tooling, non-semantic refactor |
| C | Component behavior |
| D | Research semantics, schema, or evidence interpretation |
| E | Governance or authority controls |

## Default tool matrix

| Tool / capability | A — docs/examples | B — tests/tooling | C — component behavior | D — research/evidence | E — governance/authority |
|---|---|---|---|---|---|
| GitHub live repository / PR / CI | `REQUIRED` | `REQUIRED` | `REQUIRED` | `REQUIRED` | `REQUIRED` |
| Superpowers engineering workflow | `CONDITIONAL` | `REQUIRED` | `REQUIRED` | `CONDITIONAL` | `REQUIRED` |
| Context7 current technical documentation | `CONDITIONAL` | `CONDITIONAL` | `CONDITIONAL` | `CONDITIONAL` | `CONDITIONAL` |
| Consensus scholarly literature | `DO_NOT_USE_BY_DEFAULT` | `DO_NOT_USE_BY_DEFAULT` | `DO_NOT_USE_BY_DEFAULT` | `CONDITIONAL` | `DO_NOT_USE_BY_DEFAULT` |
| Scite citation-context review | `DO_NOT_USE_BY_DEFAULT` | `DO_NOT_USE_BY_DEFAULT` | `DO_NOT_USE_BY_DEFAULT` | `CONDITIONAL` | `DO_NOT_USE_BY_DEFAULT` |
| MindMap dependency / scope mapping | `DO_NOT_USE_BY_DEFAULT` | `CONDITIONAL` | `CONDITIONAL` | `CONDITIONAL` | `CONDITIONAL` |
| Wolfram formal / statistical analysis | `DO_NOT_USE_BY_DEFAULT` | `CONDITIONAL` | `CONDITIONAL` | `CONDITIONAL` | `CONDITIONAL` |
| Hugging Face model / dataset / benchmark tooling | `DO_NOT_USE_BY_DEFAULT` | `DO_NOT_USE_BY_DEFAULT` | `CONDITIONAL` | `CONDITIONAL` | `DO_NOT_USE_BY_DEFAULT` |
| Codex Security security-specialist review, when connected | `CONDITIONAL` | `CONDITIONAL` | `CONDITIONAL` | `DO_NOT_USE_BY_DEFAULT` | `CONDITIONAL` |

The table routes capability. It does not assert that every listed plugin is installed, connected, licensed, or available in every session.

## Explicit triggers

### GitHub

`GitHub = REQUIRED` for all PR classes because live repository state is the source of truth for:

- current `main`;
- exact PR head;
- changed-file scope;
- CI/workflow state;
- mergeability;
- final main transition.

```text
CHAT_CONTEXT != SOURCE_OF_TRUTH_FOR_GITHUB
LIVE_REPOSITORY_STATE = SOURCE_OF_TRUTH_FOR_GITHUB
```

### Superpowers

Use when the change requires software-development process support, including:

- implementation planning;
- test-driven development;
- systematic debugging;
- code review;
- verification before completion;
- governance/control design where implementation discipline matters.

For a small documentation-only Class A change, Superpowers may be limited to bounded design and verification rather than a full implementation workflow.

### Context7

Trigger only when the PR depends on current, version-sensitive technical documentation, such as:

- external library or framework APIs;
- GitHub Actions syntax;
- workflow action versions;
- workflow permissions;
- OIDC or artifact-attestation APIs;
- other technical behavior likely to change across versions.

Do not invoke Context7 merely because a PR contains code.

### Consensus

Trigger only when a Class D research/evidence PR needs new external scholarly evidence, literature discovery, or structured research-gap review.

```text
PAPER_FOUND != CLAIM_CONFIRMED
LITERATURE_SEARCH != EMPIRICAL_VALIDATION
```

### Scite

Trigger after one or more materially important papers have been identified and citation context could change interpretation, including:

- supporting citation context;
- contrasting citation context;
- later replication or challenge signals;
- citation-network checks relevant to evidence weight.

Scite is complementary to literature discovery; it is not a substitute for reading the underlying study.

```text
CITATION_COUNT != SCIENTIFIC_TRUTH
SUPPORTING_CITATION != INDEPENDENT_REPLICATION
```

### MindMap

Trigger when the review has multiple interacting dependencies that are becoming difficult to audit linearly, such as:

- multi-component scope;
- claim/evidence/provenance dependency;
- cross-PR or cross-standard relationship mapping;
- competing branches or remediation sequencing.

Do not use it for a small linear change.

### Wolfram

Trigger only for an actual formal or quantitative need, such as:

- statistical design or calculation;
- sampling or power analysis;
- mathematical consistency;
- state-space or formal-model checks;
- uncertainty propagation.

Do not invoke Wolfram as decoration for a qualitative review.

### Hugging Face

Trigger only when the PR materially depends on external model, dataset, benchmark, evaluation, or Hub artifact inspection.

Typical triggers:

- named model capability review;
- dataset/schema inspection;
- benchmark/evaluation design;
- model-card or linked artifact verification.

```text
MODEL_AVAILABLE != MODEL_RELEVANT
DATASET_AVAILABLE != DATASET_NEEDED
```

### Codex Security

When the capability is actually connected and available, trigger it for security-sensitive work, especially:

- workflow permissions;
- supply-chain controls;
- artifact signing or attestation;
- authentication/authorization boundaries;
- security-sensitive code paths;
- high-impact dependency or CI changes.

Do not use a security-specialist review to manufacture security claims for non-security research semantics.

## Minimal-route examples

### Class A — documentation reconciliation

```text
GitHub = REQUIRED
Superpowers = CONDITIONAL
Context7 = NOT_APPLICABLE unless version-sensitive technical facts are changed
Consensus = DO_NOT_USE_BY_DEFAULT
Scite = DO_NOT_USE_BY_DEFAULT
MindMap = DO_NOT_USE_BY_DEFAULT
Wolfram = DO_NOT_USE_BY_DEFAULT
Hugging Face = DO_NOT_USE_BY_DEFAULT
Codex Security = DO_NOT_USE_BY_DEFAULT
```

### Class D — literature refresh

```text
GitHub = REQUIRED
Consensus = CONDITIONAL when new scholarly evidence is needed
Scite = CONDITIONAL when citation context is material
MindMap = CONDITIONAL when concept/claim dependencies are complex
Context7 = DO_NOT_USE_BY_DEFAULT
Wolfram = DO_NOT_USE_BY_DEFAULT
Hugging Face = DO_NOT_USE_BY_DEFAULT unless model/dataset artifacts are actually in scope
```

### Class E — supply-chain / attestation governance

```text
GitHub = REQUIRED
Superpowers = REQUIRED
Context7 = CONDITIONAL and normally triggered by version-sensitive workflow/API design
Codex Security = CONDITIONAL when connected and security-sensitive review is material
Consensus = DO_NOT_USE_BY_DEFAULT
Scite = DO_NOT_USE_BY_DEFAULT
Hugging Face = DO_NOT_USE_BY_DEFAULT
```

## Escalation and substitution

A PR may cross classes. In that case:

1. identify the highest-impact affected class;
2. add only the extra tools whose triggers are actually present;
3. do not automatically union every tool from every class;
4. record any unavailable required/triggered capability;
5. keep authority and scientific-claim boundaries unchanged.

A substitute must serve the same evidence need and must be identified as a substitute.

```text
SUBSTITUTE_USED = DISCLOSE
SUBSTITUTE_USED != ORIGINAL_TOOL_RAN
```

## Review-loop limit

For a review cycle that invokes the full CI/review pipeline:

```text
MAX_FULL_PIPELINE_ROUNDS_PER_REVIEW_CYCLE = 2

ROUND_1
-> REVIEW
-> material defect? YES
-> ROUND_2 = FINAL FULL PIPELINE

DEFECT_AFTER_ROUND_2
-> HOLD / DEFER / RE_SCOPE
-> NO AUTOMATIC THIRD FULL PIPELINE
```

This limit does not prohibit focused read-only inspection or a bounded diagnostic check. It prevents repeated full-pipeline churn.

## Authority and epistemic boundaries

```text
TOOL_SELECTION != CHANGE_AUTHORITY
TOOL_OUTPUT != SOURCE_TRUTH_BY_DEFAULT
PLUGIN_OUTPUT != SCIENTIFIC_VALIDATION
PLUGIN_OUTPUT != MERGE_AUTHORITY

CI_PASS != MERGE_AUTHORITY
AI_REVIEW != HUMAN_OWNER_APPROVAL
CODE_REVIEW_PASS != SCIENTIFIC_VALIDATION

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
```

Protected-main transition remains governed by the repository's dedicated main-transition authority control.

## Provenance

```text
HUMAN_OWNER
= requested a PR-type-to-tool routing matrix
= required practical tool use and avoidance of wasted plugin/runtime capacity
= reviewed the bounded design and returned PASS

CHATGPT_TEACHER
= mapped the request onto existing A-E change classes
= formalized REQUIRED / CONDITIONAL / DO_NOT_USE_BY_DEFAULT / NOT_APPLICABLE routing
= preserved tool-trigger, scientific-nonclaim and Human-Owner authority boundaries
```
