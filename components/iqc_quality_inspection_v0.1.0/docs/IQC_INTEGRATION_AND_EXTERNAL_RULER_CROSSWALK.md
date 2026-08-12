# IQC Integration and External Ruler Crosswalk

**Status:** `ENGINEERING_CANDIDATE / INSPECTION_ONLY / HUMAN_OWNER_REVIEW_REQUIRED`

## Purpose

AION already has an internal quality vocabulary: IQC, IPQC, QC, QA, status locks, manifests, SHA-256, rollback, NCR and CAPA. The missing piece is an executable inspection surface that reads the existing evidence and detects stale counts, failed targets, open governance boundaries, missing external-ruler documentation and absent corrective-action records. This component fills that narrow gap without replacing the existing Quality or Runtime Strong QA workflows.

The inspector is an **IQC evidence-consistency gate**, not an ISO certification engine, NASA acceptance authority, independent IV&V system, deployment gate or scientific-claim evaluator.

## Integration contract

| Existing AION artifact | IQC check | Result meaning |
|---|---|---|
| Git HEAD / tree / working tree | `IQC-SRC-001` | Requires the inspected target head to match actual Git HEAD and rejects staged or non-QA source drift; governed generated QA artifacts remain explicitly bounded. |
| `qa/CURRENT_TEST_RESULTS.json` | `IQC-TEST-001` | Counts targets and passed tests, detects non-zero component return codes, and compares the observed total with `qa/CURRENT_RELEASE_STATUS_LOCK.json`. |
| `qa/CURRENT_RELEASE_STATUS_LOCK.json` | `IQC-GOV-001` | Requires `canonical_effect = NONE`, `deployment = false`, and `independent_ivv = NOT_ACHIEVED`. |
| `qa/CURRENT_RELEASE_STATUS_LOCK.json` | `IQC-REL-001` | Requires the existing public scan status to be recorded as `PASS`. |
| `docs/C0_EXTERNAL_STANDARDS_CROSSWALK_2026-08-08.md` | `IQC-EVAL-001` | Confirms that the repository has an external calibration record and explicitly denies certification claims. |
| `qa/NCR_CAPA_REGISTER.md` | `IQC-CAPA-001` | Confirms that the repository has a visible NCR/corrective-action record surface. |
| `qa/CURRENT_EVIDENCE_TRACEABILITY.json` | `IQC-TRACE-001` | Checks that the current C0 evidence index has structurally traceable criteria, preserves future/out-of-tree evidence states, and does not evaluate Owner acceptance. |
| `qa/CURRENT_QA_RECONCILIATION.json` | `IQC-RECON-001` | Compares current test results, status-lock counts, current target head, failed-target list, and the QA-only reconciliation envelope. |
| Every test-bearing target | `IQC-PKG-001` | Requires the target's README and pyproject metadata so the matrix does not depend only on incidental PYTHONPATH behavior. |

The inspector never rewrites any of these inputs. A missing or stale artifact yields `HOLD`; a tested open boundary or non-zero target return code yields `FAIL`. `scripts/reconcile_current_qa.py` and the evidence generators are separate build-time artifact producers; their QA-only mutations occur before IQC, while IQC itself remains non-mutating.

## External calibration

The module uses only high-level, publicly visible principles already mapped by AION's local crosswalk. ISO/IEC 25040:2024 is used as an evaluation-planning ruler: evaluation criteria, evidence and decision rules should be explicit rather than inferred from test success. ISO/IEC 25041:2012 is used for evaluator-role separation: creator-side execution, repository IQC inspection, Human Owner review and independent IV&V are distinct roles. ISO/IEC 25010:2023 is used as a reminder that product quality is broader than functional test pass. ISO/IEC 25045:2010 is relevant to the separate recoverability workstream and is not silently claimed by this component.

NASA Software Engineering Handbook references are used as public calibration only. SWE-034 supports explicit, traceable acceptance criteria; SWE-052, SWE-053 and SWE-080 support bidirectional traceability, change management and change evaluation; SWE-087 through SWE-094 support inspection/checklist and measurement discipline; SWE-118 supports a distinguishable test-report artifact. The IQC report does not claim NASA process compliance or NASA acceptance.

ISO/IEC TS 25058:2024 provides public guidance for evaluating AI systems using an AI system quality model. AION may use that concept to organize future AI-quality dimensions, but this v0.1.0 component intentionally checks repository evidence consistency only. It does not implement an AI model quality score, safety certification, fairness judgment, consciousness classifier or capability promotion mechanism.

## Current integration boundary

The current strict mode includes target-head-bound branch-aware coverage, structural C0 traceability, QA reconciliation, and package metadata checks. These checks remain evidence-consistency controls. They do not evaluate whether an Owner has accepted a criterion, do not create a recoverability acceptance result, do not establish change-impact sufficiency, and do not convert an existing `PASS` into an acceptance or deployment decision. Future checks must use new IDs and return `HOLD` when their evidence is absent.

## Non-claims

The IQC verdict does not establish subjectivity, consciousness, identity continuity, moral status, legal status, authority, deployment readiness, canonical state or independent IV&V. `PASS` means only that the inspected repository artifacts satisfy this narrow internal consistency policy at the inspected target head.

## References

[1]: https://www.iso.org/standard/82570.html "ISO/IEC TS 25058:2024 — AI system quality evaluation guidance"
[2]: https://www.iso.org/obp/ui/#iso:std:iso-iec:25041:ed-1:v1:en "ISO/IEC 25041 public browsing entry"
[3]: https://swehb.nasa.gov/display/7150/Book+B.+7150+Requirements+Guidance "NASA Software Engineering Handbook Book B"
[4]: https://github.com/maker-luder/aion-governance-framework/blob/main/docs/C0_EXTERNAL_STANDARDS_CROSSWALK_2026-08-08.md "AION external standards crosswalk"
[5]: https://github.com/maker-luder/aion-governance-framework/blob/main/docs/QUALITY_ASSURANCE.md "AION quality assurance policy"
