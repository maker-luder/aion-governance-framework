## Change classification

- Change class: A / B / C / D / E
- Scope:
- User-visible effect:
- Research-semantic effect:
- Canonical effect: `NONE` unless independently authorized
- Deployment effect: `FALSE` unless independently authorized
- Tests:
- Docs updated:
- Breaking change:
- Authority-sensitive change:

## Boundary checklist

- [ ] This PR preserves current scientific non-claims.
- [ ] This PR does not weaken the Main Transition Authority Gate.
- [ ] This PR does not treat CI, contributor authorship, or AI review as merge authority.

## Main transition authority

A change targeting `main` requires a **fresh, exact-head, target-specific Human Owner approval receipt** under the repository's Main Transition Authority Gate. Prior approval, broad maintenance permission, CI success, or AI review does not authorize a different head.

After the candidate head is frozen and reviewed, generate a self-checked copy-ready block with `python scripts/generate_main_transition_authority_receipt.py --pr PR_NUMBER --head EXACT_40_HEX_HEAD`, or run the `Generate Main Transition Receipt` workflow. Generation is not approval; the Human Owner must verify and paste the block into the target PR body.
