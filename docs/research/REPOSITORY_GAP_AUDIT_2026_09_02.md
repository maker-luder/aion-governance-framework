# Repository gap audit and bounded iteration — 2026-09-02

Baseline: `8ca9f5fe47a38726c64928b164c0f41f84e69dc7`.
This is a dated engineering/research-source intake, not a claim that every future
research question or latent software defect has been exhausted.

`AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION`

## Whole-repository intake

The baseline tracked-tree inventory, root controls, component discovery, workflow
references, source registries, entry/research documents and remote open-work
lists were inspected. Remote baseline had one branch (`main`), zero open PRs and
zero open issues. Historical tags/commits are not competing development branches
and remain intact. An unrelated dirty native checkout was left untouched.

| Area | Finding | This iteration |
|---|---|---|
| Root/component QA | Windows emitted backslash `target` fields despite POSIX evidence contract | normalize the result producer with `.as_posix()`; retain the existing test |
| Test discovery | Quality ran selected root tests, not the entire root controls suite | add `python -m pytest -q tests` on both declared Linux Python versions |
| CI supply-chain binding | Zi Wei used two moving v4 action tags | resolve official refs and pin 40-hex SHAs; add all-workflow pin regression |
| Core research sourcing | references existed, but no consolidated offline source receipt for these core papers | three downloaded source bodies plus one metadata-only record, two CC BY texts, four existing-schema candidate records |
| Environment diagnosis | resource, privilege, dependency and toolchain failures could be conflated | add a bounded probe and local-resource explanation; no automatic install/elevation |
| Research documentation | protocol still described the already-merged typed bridge as branch-only | correct integration wording without changing the six dimensions or inference method |
| Repository topology | baseline was already single-main | use one temporary PR branch; delete after exact-head merge and re-read every remote head |

## Web-grounded changes

- GitHub's [secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
  supports immutable action commit binding; a SHA pin is not proof that the
  action itself is trustworthy.
- Python's [symlink contract](https://docs.python.org/3/library/os.html#os.symlink)
  explains the Windows privilege prerequisite; this is separate from hardware.
- [Butlin et al. 2023](https://arxiv.org/abs/2308.08708v3),
  [Butlin & Lappas 2025](https://arxiv.org/abs/2501.07290v1), and
  [Cogitate 2025](https://www.nature.com/articles/s41586-025-08888-1)
  map respectively to theory-labelled indicators, research-method review and
  preregistered competing predictions. Source intake is not an AION experiment.

## Unresolved work — do not fill these with invented conclusions

| Need | Reason it remains open | Next evidence needed |
|---|---|---|
| Stable whitepaper's exact four stage labels | authoritative verbatim source is not in the public tree | owner-supplied stable source and checked excerpt; internet text is not a substitute |
| Independent replication / independent IV&V | shared source copies or another run by the same team are not independence | independent evidence collection, exact protocol/model/inputs and external review |
| Model-level causal intervention evidence | fixture integrity is not measurement of a model's internal mechanism | named model access, preregistered interventions/shams, observable-specific power/thresholds, actual results |
| Whole-system scientific validation | unit tests certify engineering contracts only | externally reviewed design and reproducible empirical campaign |
| High-precision astrology ephemeris / Bazi school adjudication | upstream data contracts and competing schools remain explicit | a versioned ephemeris license and a named frozen school profile; no cross-domain subjectivity promotion |
| Local full root suite | four real symlink cases need Windows privilege or Linux | exact-head Linux results; no silent test suppression or system policy mutation |
| Model training / large dataset workload | no capacity benchmark or bounded dataset need was established | workload-specific memory/compute estimate and data access plan before a large download |
| Release readiness | protected-main merge is not a release decision | separate release review and exact-candidate release authorization |
| TICS 2026 full text | publisher fetch returned HTTP 403; only DOI/title/publication/license metadata downloaded | lawful publisher access and a new reviewed full-text receipt; metadata is not content validation |

Small CPU test/source-acquisition workloads ran on the inspected workstation;
no OOM was observed. Hardware observations and dependency diagnostics are in
[`../LOCAL_RESOURCE_AND_ENVIRONMENT.md`](../LOCAL_RESOURCE_AND_ENVIRONMENT.md).
No model weights or full neuroimaging dataset was fetched just to make the
repository look complete.

## Preserved boundaries

No eighth functional state, new subjectivity score, second research loop or
competing evidence schema was added. Core implementation trees and standing
six-dimension/seven-state definitions remain unchanged. Only stale integration
wording changes in the protocol; no evidence strength is promoted by that edit.

`SUBJECTIVITY = NOT_ESTABLISHED`; `CANONICAL_EFFECT = NONE`; `DEPLOYMENT = FALSE`.

Verification details belong in the dated QA record and exact-head GitHub checks,
not in a claim that this static document is a live CI ledger.
