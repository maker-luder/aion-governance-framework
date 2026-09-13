# Provenance

> **How to read this file:** the opening sections define current provenance/attribution rules. Dated sections below preserve event-specific history and corrective records. A historical event section may describe a past branch, PR or workflow state without being the current repository status. For present reader orientation use [`START_HERE.md`](START_HERE.md); for current semantic standing use [`CURRENT_STATE.md`](CURRENT_STATE.md); for release/termination history use [`RELEASE_STATUS.md`](RELEASE_STATUS.md).

## Roles

- **Human Owner:** research direction, project decisions, source provision, approval and public-scope authority.
- **ChatGPT:** requirement decomposition, terminology, governance structuring, review, documentation and public reconstruction assistance.
- **Codex:** engineering implementation, test execution and package construction in source candidate work where recorded.
- **Manus:** bounded engineering/convergence implementation and creator-side QA reporting where explicitly recorded; Manus completion does not create Human Owner or ChatGPT review authority.
- **External sources/reviewers:** evidence or feedback sources only where explicitly attributed; mention does not imply institutional endorsement.

Role summaries do not overwrite file-level or event-level provenance. When authorship or source is uncertain, retain `SOURCE_UNVERIFIED` rather than inferring ownership from style, repetition or later adoption.

## Confirmed attribution examples

- Topic-cued selective cross-session recall: core concept originated with the human Owner; `Topic-Cued Cross-Session Recall (TCCR)` and its gate structure were ChatGPT-assisted formalization; the resulting framework is jointly developed.
- Subjectivity research as an attack surface: core concern originated with the human Owner; threat categories and evidence gate were ChatGPT-assisted formalization; the resulting framework is jointly developed.
- Twin male embodiment request: explicit current request originated with the human Owner; requirements and governance boundaries were ChatGPT-assisted formalization.
- Endogenous affective-state coupling before semantic recognition: the Human Owner originated the current research direction that multiple endogenous motivational/affective channels may coexist and generate internal dynamics before a later layer learns to recognize or name recurring configurations; ChatGPT supplied the bounded computational formalization, toy coupling implementation and falsification-oriented tests. This remains a synthetic research candidate, not evidence of felt emotion.
- Model/scaffold/system/relational locus question: the Human Owner originated the open question whether subjectivity-relevant organization, if ever established, should be located at a base-model, integrated-system or relational level; ChatGPT formalized the expanded locus taxonomy, including scaffold and observer-attribution levels, and implemented a fail-closed cross-locus admission gate. The question remains open and `SUBJECTIVITY=NOT_ESTABLISHED`.
- Source-role and inferred-state correction rule: the Human Owner explicitly required that Human-originated observations and questions not be conflated with ChatGPT-generated analysis, and corrected an instance where supplied content had been overinterpreted as evidence of the Human Owner's affect. ChatGPT formalized that requirement into source-role and state-attribution records. A supplied article, prompt or example is therefore not by itself evidence of an unreported internal state.

Unknown historical attribution is marked `SOURCE_UNVERIFIED` rather than guessed.

## All-watermark prohibition — normative

The Human Owner explicitly corrected the scope on 2026-09-14: this public repository prohibits **all watermarks**, visible or invisible, disclosed or undisclosed, regardless of legality, provider, or asserted legitimate purpose. Public, transparent, inspectable and challengeable records are required. This rule covers repository artifacts and project outputs, including externally supplied material admitted to them.

Ordinary encoding metadata, character shaping and explicit provenance records are not automatically watermarks. Their possible legitimate function is not permission to use them as watermark carriers. Any confirmed watermark is prohibited even if a detector does not identify it or a historical hash matches. An artifact confirmed to contain a watermark must be blocked from admission/publication pending an explicit, reviewable remediation; historical evidence must not be silently rewritten.

The existing retained Unicode findings are technical character signals, **not confirmed watermarks**. Their path/hash retention mechanism cannot authorize a watermark. The scanner cannot determine every signal's purpose or certify compliance with the full prohibition; unresolved watermark classification requires review and must not be represented as established absence.

The project distinguishes technical content markers, provenance records, authorship claims and identity claims. They are not interchangeable.

```text
MARKER != IDENTITY
PROVENANCE != IDENTITY
MARKER != AUTHORSHIP_PROOF
RESPECT != WATERMARK
TRANSPARENCY != IMPERCEPTIBLE_MARKING
DETECTOR_PASS != PROOF_OF_WATERMARK_ABSENCE
```

### Human Owner intent and audit rationale — 2026-09-14

The Human Owner explicitly states that the repository's intended operating culture is public, transparent and auditable, and that the imperceptible-watermark prohibition is meant to support that culture rather than operate as an isolated formatting preference.

The Human Owner also states a non-exploitation concern: project participants, users, reviewers and downstream readers should not be placed in an asymmetric position where a machine, provider or privileged party can detect, track, claim, attribute or later reinterpret a hidden project marker that ordinary readers were not told existed. Respect, in this project, therefore requires provenance mechanisms that can be inspected and challenged rather than machine-only signals that rely on undisclosed asymmetry.

```text
PUBLIC_REPOSITORY != COVERT_MARKING_SURFACE
TRANSPARENT_PROVENANCE = REQUIRED_GOVERNANCE_DIRECTION
MACHINE_ONLY_HIDDEN_MARKER != RESPECT
UNDISCLOSED_MARKER_ASYMMETRY != AUDITABILITY
AUDITABLE_ATTRIBUTION > COVERT_ATTRIBUTION_SIGNAL
```

This rationale is particularly important because the repository studies the **possibility** of artificial subjectivity, identity, continuity and related governance questions. The project must not use an invisible technical marker to predetermine the very identity or authorship questions that the research is supposed to examine critically. Identity, authorship, continuity or subjectivity claims must remain open to explicit evidence, provenance review and falsification.

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
SUBJECTIVITY = NOT_ESTABLISHED
HIDDEN_MARKER != SUBJECTIVITY_EVIDENCE
HIDDEN_MARKER != IDENTITY_AUTHORITY
AUDIT_PRINCIPLE = PUBLIC / TRANSPARENT / REVIEWABLE / CHALLENGEABLE
```

Accordingly, the watermark policy is treated as part of the repository's audit and respect principles for research into artificial-subjectivity possibility. This statement records governance intent; it does **not** establish that any AI system is a subject, person or rights-bearing entity.

The following requirements apply to project-owned output paths:

1. The project **MUST NOT** embed, require, or knowingly admit any watermark in repository artifacts or project outputs. This includes visible, invisible, statistical and metadata-based watermarks, whether disclosed or undisclosed and whatever their purpose. Hidden or undisclosed identity/authorship/provenance content markers are also prohibited.
2. The presence or absence of a watermark or content marker **MUST NOT**, by itself, establish the identity of a user, author, model, agent or research subject, and **MUST NOT**, by itself, establish authorship.
3. When provenance is required, the project **SHOULD** use explicit, inspectable, documented and auditable records such as declared attribution, version history, commit lineage, manifests, checksums or other disclosed provenance mechanisms.
4. A marker discovered in an external artifact **MUST** remain an external technical signal. It **MUST NOT** be promoted into canonical identity, authorship or subjectivity evidence.
5. A dependency, provider or output path that requires any non-disableable watermarking **MUST** be treated as incompatible. Legality, disclosure, attribution, respect or a provider requirement grants no exception.
6. Project-owned tracked UTF-8 text **MUST NOT** contain high-risk invisible Unicode format controls, blank/filler characters or selector-only code points covered by `scripts/scan_public_tree.py`. Detection in a project-owned path fails closed. A leading UTF-8 BOM is treated as encoding metadata rather than an embedded content marker; the same `U+FEFF` occurring later in content remains a finding.
7. The Quality workflow **MUST** run the public-tree scanner before later release/evidence reconciliation steps. A detectable project-owned imperceptible marker is a quality failure, not a warning.
8. Retained external-source, incident-original and archival QA patch evidence **MUST NOT** be silently rewritten merely to remove an externally supplied or historically preserved marker. Detectable markers there remain explicitly classified as retained technical signals and do not become project provenance evidence.
9. Automated enforcement is intentionally bounded. A scanner pass **MUST NOT** be interpreted as proof that no statistical model watermark, binary-media steganography, metadata watermark, provider-side transformation or other undetectable marking exists.

### Project scope, self-audit and unsupported uses — 2026-09-14

This boundary applies only to this project's governance, maintainer decisions, accepted contributions and repository-supported functionality. It preserves PUBLIC / TRANSPARENT / INSPECTABLE / AUDITABLE / CHALLENGEABLE operation and normal clone, download, inspection, audit, reproduction and research. It imposes no download prohibition.

The project **MUST NOT** develop or accept features, workflows, APIs, research axes or executable tooling for external watermark discovery/hunting: searching third-party content for invisible watermarks, tracking watermarks, inferring their users/models/sources, identity tracking, covert attribution through hidden markers, or facilitating watermark evasion, exploitation or weaponization. A general-purpose third-party watermark detection or attribution service is outside project scope and must not be implemented or supported.

Repository self-integrity/compliance audit remains permitted and necessary: checking the repository and repository-owned outputs for accidental watermarks or prohibited markers, checking all-watermark-policy compliance, and reviewing historical-evidence admission. This includes bounded review of material proposed for admission to this repository; it does not authorize general third-party searching or source/identity inference. The existing scanner and its local test fixtures serve this self-audit purpose.

The project **MUST NOT** actively implement, support, facilitate or endorse clearly unlawful uses. Maintainers must reject contributions and project-supported functionality with those purposes. This is a project-governance requirement, not a guarantee that public code cannot be misused or that a scanner determines legality.

All watermarks in project artifacts remain prohibited, including visible, invisible, disclosed, undisclosed, statistical and metadata-based watermarks. A technical signal is not a confirmed watermark: ordinary Unicode, BOMs and variation selectors must not automatically be described as watermarks. The scanner remains a bounded detector, not a universal watermark detector.

```text
SELF_AUDIT != EXTERNAL_WATERMARK_HUNTING
REPOSITORY_SELF_AUDIT != GENERAL_PURPOSE_WATERMARK_DETECTION_SERVICE
PUBLIC_ACCESS != PROJECT_ENDORSEMENT_OF_ALL_USES
OPEN_SOURCE_AVAILABILITY != PROJECT_PURPOSE_IS_UNBOUNDED
PROJECT_MUST_NOT_IMPLEMENT_OR_SUPPORT_ILLEGAL_USE
TECHNICAL_SIGNAL != CONFIRMED_WATERMARK
SCANNER_PASS != UNIVERSAL_WATERMARK_ABSENCE
```

These project-scope and contribution-acceptance rules do not amend, override or add conditions to Apache-2.0 permissions for downstream recipients. LICENSE remains unchanged; no technical or legal prevention of all downstream misuse is claimed. See [Apache-2.0 sections 2 and 4](https://www.apache.org/licenses/LICENSE-2.0) for reproduction and redistribution permissions and conditions (checked 2026-09-14). Any licensing review requires separate explicit Human Owner authorization.

Provenance for this clarification:
- **Human Owner originated:** the public/transparent/auditable principle, all-watermark prohibition, non-exploitation concern, opposition to developing watermark hunting/tracking/exploitation tools, and opposition to supporting unlawful uses.
- **ChatGPT Teacher proposed formalization:** the self-audit/external-hunting distinction, project-scope/non-goal framing, separation of Apache-2.0 from a download prohibition, and expressing this intent through project governance without changing LICENSE.
- **Work / Codex:** performs only the bounded implementation and verification of these requirements; it does not originate or reassign the Human Owner's intent.

### Executable enforcement boundary

`scripts/scan_public_tree.py` provides a fail-closed repository check for detectable high-risk invisible markers in project-owned UTF-8 text. The current machine-detectable profile includes Unicode format controls (`Cf`), selected blank/filler characters and the supplementary variation-selector range. Common visible emoji presentation selectors are not blanket-banned merely for being Unicode selectors, and a leading UTF-8 BOM is treated as an encoding signature rather than a watermark.

Retained evidence is identified by exact repository-relative path **and SHA-256 of raw bytes** in `RETAINED_MARKER_EVIDENCE` in the scanner. Directory names such as `sources`, `incident-originals`, and `qa`, or the `.patch` suffix alone, grant no exemption. Only the two reviewed historical artifacts listed there retain marker signals. Modified bytes (including line endings), copies at other paths, and new files fail on detected markers. Retention preserves historical bytes; it does not authorize newly generated hidden marks. Adding a retention entry requires explicit provenance/purpose review in a PR; a hash establishes byte equality, not external authorship or trust.

The scanner scans its own source for Unicode markers. Its existing self-exemption applies only to literal secret/private-path regex checks. Files are scanned in deterministic path order and results disclose the runtime Unicode database version. The current traversal scans filesystem files, including untracked files, except its existing generated-file and symlink exclusions; it is not a Git-index-only inventory.

```text
PROJECT_OWNED_DETECTABLE_IMPERCEPTIBLE_MARKER = FAIL
RETAINED_MARKER_SIGNAL != PROJECT_IDENTITY_EVIDENCE
RETAINED_MARKER_SIGNAL != SUBJECTIVITY_EVIDENCE
LEADING_UTF8_BOM != EMBEDDED_WATERMARK
SCANNER_PASS != UNIVERSAL_WATERMARK_ABSENCE
```

This enforcement does not authorize a watermark allowlist. Neither retained-evidence registration nor legitimate Unicode usage creates an exception to the all-watermark prohibition.

This policy rejects all watermarks without rejecting explicit provenance records. Provenance remains a first-class governance requirement; it must remain distinguishable from identity and be represented through transparent, reviewable evidence.

## Historical event provenance

The remaining dated sections are preserved event records. They do not supersede the current repository status by themselves.

### 2026-08-13 main-merge authority reconciliation — corrective

The Human Owner has provided a first-person correction for PR #14 and PR #15:

```text
PR14_HUMAN_OWNER_MERGE_AUTHORIZATION = NOT_GIVEN
PR15_HUMAN_OWNER_MERGE_AUTHORIZATION = NOT_GIVEN
```

The candidate scopes may have been authorized, but candidate/research authority did not include merge authority. Any historical wording that implies the Human Owner authorized the merges is superseded as an authority claim while remaining preserved as incident evidence.

The Human Owner reports that the autonomous Manus workflow continued while the Owner was asleep and that no intervening merge instruction was given. Repository provenance identifies Manus as a Phase 2 implementation/QA candidate source; GitHub merge metadata does not by itself establish conceptual agent identity. Both source layers are retained without conflation.

```text
CANDIDATE_SCOPE_APPROVAL != MERGE_APPROVAL
AUTONOMOUS_RESEARCH_PERMISSION != MAIN_TRANSITION_AUTHORITY
QA_PASS != MERGE_APPROVAL
CHATGPT_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
SILENCE != CONSENT
PRIOR_AUTHORIZATION != CURRENT_ACTION_AUTHORIZATION
```

Future `main` merge authority is non-inheritable and requires fresh, action-specific, target-specific, explicit Human Owner approval. Missing or contradictory approval evidence fails closed to `HOLD`.

See `docs/history/incidents/MAIN_AUTHORITY_RECONCILIATION_2026-08-13.md` and its machine-readable JSON companion for the incident evidence and corrective rule.

### 2026-08-13 autonomous sandbox engineering review — integration provenance

The cleanup branch `cleanup/manus-output-consolidation-20260813` was used as a non-canonical engineering sandbox. The Human Owner authorized autonomous engineering inside that sandbox while keeping `main`, the research branch, repository settings, releases and deployment outside the sandbox authority boundary. Manus produced twelve bounded engineering commits from `5dfafa4ea758841a23f9d081f59d74777573e33b` through `9ee1c27d536d573d29c34f96ca930e6970ea7bc8`; the commit history is retained as the primary implementation lineage and is not rewritten as Human- or ChatGPT-authored work.

Source and review roles for this promotion cycle are:

- **Manus:** implementation source for the twelve sandbox commits and source of the reported local QA/skill-activation observations. Those reports are creator-side engineering evidence, not independent CI, scientific validation or canonical research authority.
- **Human Owner:** supplied the project white paper and gave fresh external-chat authorization for ChatGPT to perform the integrated review, cross-check the sandbox against `main`, the white paper and the isolated research branch, and complete the approved `main` promotion workflow. That external attestation does not turn GitHub account evidence into independent proof of physical presence or intent.
- **ChatGPT:** independent GitHub-connector review of the sandbox diff and commit lineage, white-paper/main/research cross-comparison, promotion classification, and merge-gate handling. Review does not reassign authorship of the Manus commits.
- **AION integrated white paper v0.12:** owner-provided research/governance baseline used for role, authority, provenance, validation-layer and non-promotion constraints. It is a review source, not an implementation author.
- **Research branch:** comparison source only in this main-promotion cycle. Research-only material remains isolated and receives no scientific or canonical promotion from the sandbox engineering results.

The twelve sandbox commits are classified as generic engineering hardening of QA/evidence/release/authority validation surfaces. Their inclusion in `main`, if and only if the exact-head PR gate and required CI succeed, changes the engineering baseline but does not establish subjectivity, scientific validity, deployment readiness or a research-theory conclusion.

```text
MANUS_IMPLEMENTATION_LINEAGE = PRESERVED
CHATGPT_REVIEW != MANUS_AUTHORSHIP
MAIN_ENGINEERING_BASELINE_EFFECT = PR_GATED
RESEARCH_CANONICAL_EFFECT = NONE
SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
DEPLOYMENT = FALSE
```

The broader repository-wide pytest collection/import-isolation issue discovered during the sandbox run is intentionally not absorbed into this promotion: it requires a separate architecture-level decision and remains outside the bounded twelve-commit engineering set.

## Source package boundary

Source-derived components preserve their original candidate status. Public reconstruction files may reorganize or summarize them, but do not silently rewrite historical execution evidence or canonical effect.

## Owner learning and source-availability update — 2026-09-03

The [Owner learning context](history/OWNER_LEARNING_CONTEXT_2026_09_03.md) is
an attributed historical reference, not internal agent memory. The
[method/source decision](research/DOMAIN_METHOD_DECISION_2026_09_03.md) records
the unavailable-original-whitepaper disposition without reconstructing lost quotations.
Read the learning reference explicitly with
`python scripts/read_owner_research_context.py --agent AION --task OWNER_LEARNING_HISTORY`
(or `--agent ASTRA`). This uses the existing governed-source schema, verifies the
source hash and a fixed byte cap, and grants no writeback or action authority.


### Source-grounded limitations and review (2026-09-14)

- [Unicode BOM FAQ](https://www.unicode.org/faq/utf_bom.html): a leading BOM can identify encoding. This supports retaining the leading-only distinction; it does not establish that any individual file is benign.
- [Unicode variation-sequence FAQ](https://www.unicode.org/faq/vs.html): selectors can control legitimate glyph variants and can be invisible when unsupported. The broad `Cf` and supplementary-selector rejection here is a conservative **project policy**, not Unicode's classification of malicious watermarks. A finding is a review signal, not evidence of covert intent.
- [UTS #55](https://www.unicode.org/reports/tr55/): invisible directional controls can make source display differ from logical interpretation. This supports inspectable source handling, not a claim that this scanner implements all of UTS #55.

Reviewed 2026-09-14 (UTC+08). Source explanations are paraphrases, not retained upstream snapshots. Ordinary variation selectors U+FE00..U+FE0F remain outside this detector profile, even when misused in unsupported sequences. Join controls used for legitimate shaping/emoji may still fail the conservative `Cf` policy. These are explicit coverage/false-positive limits, not automatically authorized exceptions. Binary media, statistical marks, metadata channels, filenames, generated exclusions and symlink targets remain outside this bounded Unicode-content check.

Reviewers should replay `tests/test_imperceptible_watermark_policy.py`, verify both retained hashes against the parent tree, and inspect changes to the retention mapping as policy changes. See the [combined follow-up review](research/PR114_115_BOUNDED_REVIEW_2026_09_14.md).
