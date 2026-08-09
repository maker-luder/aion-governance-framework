# POL-UPSTREAM-SUPPLIER-TRUST-001 — External / Internal Crosswalk

- `STATUS = POLICY_CALIBRATION_CANDIDATE`
- `CROSSWALK_SYNTHESIZED_BY = CHATGPT`
- `CERTIFICATION_CLAIM = FALSE`
- `FULL_CONFORMITY_CLAIM = FALSE`
- `INDEPENDENT_IVV = NOT_ACHIEVED`
- `CANONICAL_EFFECT = NONE`

本 crosswalk 用公開標準與既有 AION / Astra QMS 校準 `POL-UPSTREAM-SUPPLIER-TRUST-001`。Mapping 表示 methodological influence / compatibility，不等於外部機構認證、背書或完整符合性。

## Public calibration

| External source | Calibration use | AION / Astra mapping | Claim boundary |
|---|---|---|---|
| NIST SP 1326 (2026), *Cybersecurity Supply Chain Risk Management: Due Diligence Assessment Quick-Start Guide* | Supplier due diligence、provenance、resilience、foundational cybersecurity practices、supply-chain visibility | supplier admission/reassessment；provenance；resilience；dependency criticality/exposure | No NIST certification/conformance claim |
| NIST SP 800-161 Rev.1 Update 1 | C-SCRM across acquisition, development, integration, deployment and use | scope separation；dependency/exposure；incident/CAPA；reassessment | Project-specific mapping only |
| NIST AI RMF 1.0 / Playbook | `GOVERN → MAP → MEASURE → MANAGE` | roles/policy；scope/exposure；evidence/security/privacy；disposition/reassessment | No AI RMF certification claim |
| ISO/IEC 25040 / 25041 project calibration | evaluation planning；evaluator-role transparency | criteria before evaluation；internal review != independent IV&V | No SQuaRE conformity claim |
| ISO/IEC 25010 project calibration | quality broader than test pass | documentary/governance/provenance/privacy review in addition to automated tests | No full product-quality certification |
| NASA SWE-034 project calibration | general software acceptance criteria and acceptance planning | criteria are defined and frozen before evaluation; evidence remains distinct from the Owner decision | Method calibration only |
| NASA SWE-193 project calibration | acceptance tests for loaded/uplinked data, rules and code that affect software/system behavior, including nominal/off-nominal scenarios | applicable only if such loaded/uplinked behavior-affecting artifacts enter the evaluated scope | Not generic acceptance-testing authority |
| NASA SWE-052 / SWE-053 / SWE-080 project calibration | bidirectional traceability；requirements-change management；tracking and evaluation of software-product changes | anti-hindsight；impact-based revalidation | Method calibration only |
| W3C PROV / existing project provenance model | Entity / Activity / Agent lineage | claim/source/transformation/reviewer/authority separation | AION-specific roles remain project extensions |

## NIST AI RMF mapping

```text
GOVERN
→ policy / roles / Owner authority / conflict disclosure

MAP
→ supplier / model / artifact / configuration / project exposure

MEASURE
→ evidence class / evidence strength / security / provenance /
  privacy / methodological confound

MANAGE
→ CONDITIONAL / ENHANCED_REVIEW / SCOPE_RESTRICTED /
  QUARANTINED / DENIED + reassessment
```

## Internal architecture crosswalk

```text
SUPPLIER TRUST POLICY
→ admission / disposition / scope constraints

POL-UPSTREAM-AGENT-INCIDENT-001
→ runtime / tool / network / credential containment

IDENTITY / LINEAGE WRITEBACK GATE
→ canonical authority
```

`NO_DUPLICATE_CANONICAL_GATE = TRUE`

The existing upstream-security component remains responsible for task budgets, trajectory monitoring, filesystem/network boundaries, credential denial, reduced-safeguard combination gates, incident isolation, immutable evidence, NCR/RCA/CAPA and Owner recovery.

## Public references

- NIST SP 1326: https://csrc.nist.gov/pubs/sp/1326/final
- NIST SP 800-161 Rev.1 Update 1: https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final
- NIST AI RMF Playbook: https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook
- Existing AION/Astra crosswalks in this repository remain the authoritative project records for the ISO/NASA/W3C mappings reused here.

## Non-claims

This crosswalk does not establish certification, legal compliance, independent IV&V, deployment readiness, vendor innocence/guilt, subjectivity or consciousness.
