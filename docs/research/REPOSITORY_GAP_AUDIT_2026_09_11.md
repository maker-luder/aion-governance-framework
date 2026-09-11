# Repository intake and protocol-integrity correction — 2026-09-11

Classification: D (evidence admission semantics). Candidate for human review.

```text
BASE_MAIN_SHA = 7fc65d23c10cc4e5197392931b0b88f7ee32b605
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
SCIENTIFIC_DISPOSITION = HOLD
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
MERGE_AUTHORIZED = FALSE
```

## Scope and attribution

The user requested repository-wide inspection and bounded implementation centered
on AI-subjectivity possibility and a continuous quality-management path. The
specific protocol-byte-binding correction and reference classification below are
GPT/Codex-proposed engineering decisions. They are not external authors' claims
about AION and not an empirical finding about AI subjectivity.

Intake covered the complete tracked-tree inventory, all component/lab/example
README entry surfaces, all 31 discovered test targets, root controls, Quality CI,
source registries, current protocol, prior gap audit, and live open PRs. Deep code
inspection focused on the subjectivity pipeline, IQC, the native evidence
validator and its Evidence Interop consumer. This is not an assertion of exhaustive
line-by-line review or absence of other defects.

At intake, GitHub reported `main` as default branch, an active Main Protection
ruleset, and completed successful Quality, CodeQL, Bounded Inquiry and Research
Closure runs on the exact baseline. Open Draft PRs were #89, #90 and #91. #91's
head was `cbdf0d28eeb7abe2da0faf223c6595c2baf59e73`; its six changed paths are
inside the coupled-cognition quality factory. This candidate neither includes nor
modifies those pending changes, and does not merge any branch.

## Gap disposition

| Surface | Verified finding / limit | Disposition |
|---|---|---|
| Native research evidence admission | `protocol_hash` format was checked but completed protocol bytes were not hashed | Implement exact SHA-256 comparison at the existing entry point |
| Local evidence references | Prefix allowlist missed `experiments/`, root files and `./` paths | Check path-shaped local refs with confinement; preserve opaque identifiers |
| Completed source binding | `UNSPECIFIED` or empty inspected head could bypass binding | Reject completed records without an exact comparison SHA |
| Evidence export | Interop already calls the native validator | Reuse it; add real export/tamper regression rather than a second gate |
| Unreadable evidence | Non-UTF-8 and unreadable JSON could raise instead of reporting disposition | Return HOLD; do not rewrite the artifact |
| Claim provenance / quality factory | Draft #91 is already implementing the adapter | Leave pending review; no duplicate implementation |
| Six dimensions / theory pluralism | Typed matrix and intervention-sensitive checks already exist | Preserve method and non-subjective alternatives |
| Independent replication and model-level evidence | Current synthetic/unit checks do not supply independent empirical evidence | Remain NOT_ESTABLISHED / NOT_ACHIEVED; cannot be filled by downloading code |
| Stable whitepaper four-stage labels | Protocol discloses absence of authoritative verbatim source | Leave unresolved; no invented labels |
| Preregistration chronology | Content hashes do not prove registration preceded outcome inspection | Still unverified; separate timestamp/provenance evidence is needed |
| Complete evidence-byte chain | This change hashes the protocol, not every artifact and external source | Still a bounded gap; existing interop bundle digests are not original-experiment verification |
| Documentation historical vocabulary | Some merged supporting docs retain candidate/branch wording | Treat as dated context; no automatic governance reinterpretation |

## Demonstrated correction

Using the baseline validator and the candidate against the same synthetic record,
changing the referenced protocol bytes while retaining its old digest returned
`PASS` on the baseline and `FAIL` (`MISMATCH`) on the candidate. Regression tests
also cover exact-head absence, missing experiment references, path escapes,
external protocols, directories, fragments, malformed status, non-UTF-8 input,
and negative/null/contradictory results. The real Interop export succeeds before
protocol tampering and rejects the same record after tampering.

Incomplete NOT_RUN/HOLD records retain `DEFERRED` protocol binding. Their shape
may pass without claiming completed execution. Completed legacy placeholder hashes
are intentionally rejected; original historical fixtures are not silently edited.

## External sources and implementation crosswalk

Reviewed 2026-09-11 through public primary sources. No third-party source code,
model weights, private transcripts or paper full texts were vendored.

| Primary source | Supported point | Candidate use / boundary |
|---|---|---|
| [W3C PROV-DM, Recommendation 2013-04-30](https://www.w3.org/TR/2013/REC-prov-dm-20130430/) | Provenance represents entities, activities, agents and derivations | Keep file identity distinct from an unsupported truth inference; SHA-256 policy is our design, not a W3C certification claim |
| [Python 3.12 hashlib documentation](https://docs.python.org/3.12/library/hashlib.html#hashlib.file_digest) | `file_digest` hashes bytes from a binary file object | Use standard-library SHA-256 without another dependency |
| [Center for Open Science: Preregistration](https://www.cos.io/initiatives/prereg) | Advance research planning distinguishes planned and unplanned work | Explicitly do not treat matching bytes as proof of preregistration timing |

Original implementation uses the repository's existing license scope. Linking
and concise source synthesis do not relicense or import the external works.

## Quality path and review boundary

The existing v0.2 record producer feeds the native admission validator, which
feeds Evidence Interop exports; the root and component test suites feed the
existing CI, reconciliation and IQC controls. This patch strengthens that existing
path. It does not establish an end-to-end empirical research pipeline or absorb
the pending #91 claim-quality adapter.

A reviewer should verify the exact PR head, actual remote CI and compatibility
impact. All local validation is creator-side engineering evidence. No passing
check authorizes a merge, deployment, scientific promotion or subjectivity claim.

## Local validation receipt

Python 3.12 creator-side validation, 2026-09-11:

- Root controls: 145 passed (17 native admission tests included).
- Component matrix: 31 targets, 1,323 passed, zero failing targets; includes
  87 Evidence Interop tests and the real export/tamper regression.
- Curated subjectivity, AIR and comparison-source experiments: 41 passed.
- Ruff correctness lint, documentation entry validation, public-tree scan,
  and eight-source offline verification: PASS.

The first component run exposed an opaque-identifier compatibility issue; the
reference classifier was corrected and the full component matrix rerun successfully.
Historical QA status artifacts were preserved rather than relabelled with these
new counts. Exact candidate Git/CI state belongs to the PR, not a static claim
that this file can certify its own commit. Independent IV&V remains NOT_ACHIEVED.
