# Contributing

Contributors may propose bounded changes; they do not self-authorize a transition into `main`.

```text
CONTRIBUTOR_CAN_PROPOSE_CHANGE = TRUE
CONTRIBUTOR_CAN_SELF_AUTHORIZE_MAIN = FALSE
CONTRIBUTION_PERMISSION != MERGE_AUTHORITY
LOW_RISK_CONTRIBUTION != AUTOMATIC_MAIN_MERGE
```

## Contributor fast path

1. Open a small issue or use the applicable feedback template.
2. Make a focused branch and identify the change class below.
3. Run focused tests and update relevant documentation.
4. Open a normal PR using the repository template.
5. A maintainer reviews the change; protected-main transition remains a separate fresh exact-head Human Owner decision.

## Change classes

| Class | Typical scope | Minimum evidence |
|---|---|---|
| A | Documentation and examples | Link/example check; user-visible effect noted. |
| B | Tests, tooling, non-semantic refactor | Focused tests and no semantic-effect statement. |
| C | Component behavior | Component tests, compatibility/review note, affected-boundary analysis. |
| D | Research semantics, schema, or evidence interpretation | Design/review evidence, schema/test evidence, explicit scientific-nonclaim review. |
| E | Governance or authority controls | Adversarial review, validator tests, and Human Owner review; no self-authorization. |

Do not place credentials, private conversations, personal data, or restricted research material in issues or PRs. See [`SECURITY.md`](SECURITY.md), [`docs/governance/MAIN_TRANSITION_AUTHORITY_GATE.md`](docs/governance/MAIN_TRANSITION_AUTHORITY_GATE.md), and [`BUILD_AND_VERIFY.md`](BUILD_AND_VERIFY.md).

A passing CI result is not merge authority, scientific validation, certification, or deployment authorization.
