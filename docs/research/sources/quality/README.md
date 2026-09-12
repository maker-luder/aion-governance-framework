# Research-quality source intake — 2026-09-13

This directory contains reviewed **derivative source cards**, not copied source
publications. The exact official PDFs were acquired once into a repository-external
cache, byte-counted and SHA-256-bound. The public repository retains only the cards,
the acquisition receipt and governed-source records.

The sources support the quality-management chain only. They do not provide evidence
for artificial subjectivity, consciousness, phenomenal experience, moral agency or
moral status.

```text
QUALITY_METHOD_REFERENCE != SUBJECTIVITY_EVIDENCE
OFFICIAL_GUIDANCE != PROJECT_CERTIFICATION
FDA_DEVICE_QSIT != AION_REGULATORY_APPLICABILITY
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Retained set

| Card | Use in this repository | Limit |
|---|---|---|
| `nist-ai-rmf-1.0.md` | continuous `GOVERN / MAP / MEASURE / MANAGE` crosswalk | voluntary, version-bound framework; not certification |
| `nist-ai-600-1.md` | GAI lifecycle, information-integrity and incident/evaluation crosswalk | companion profile; not subjectivity research evidence |
| `fda-capa-qsit-1999.md` | CAPA completeness, root-cause, effectiveness and management-review analogy | historical medical-device inspection guide; analogy only |

## Verification and acquisition

From repository root:

```powershell
python scripts/fetch_quality_method_sources.py
python scripts/fetch_quality_method_sources.py --download-cache ../aion-quality-source-cache
```

The first command is offline. The second verifies or creates an external cache only.
Unexpected upstream bytes, existing mismatched cache content, a repository-internal
cache destination, non-HTTPS redirect, card drift or attempted registry promotion all
fail closed. Source changes require a new reviewed receipt rather than overwrite.
