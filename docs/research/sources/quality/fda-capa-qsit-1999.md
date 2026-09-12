# Source card: FDA QSIT CAPA guide

- Source: *Guide to Inspections of Quality Systems*
- Publisher: U.S. Food and Drug Administration
- Publication date: August 1999
- Official URL: https://www.fda.gov/files/Guide-to-Inspections-of-Quality-Systems.pdf
- Reviewed upstream bytes: `975229`
- Reviewed upstream SHA-256: `2bd078f1ce4f3a45c35379f609f819916255d0a86504d9118935fa7ff1f60ee0`
- Intake date: 2026-09-13 (Asia/Taipei)
- Registry role: `GOVERNANCE_REFERENCE / METHOD / CANDIDATE / REFERENCE_ONLY`

## Verified sections and bounded findings

The review used the CAPA inspection objectives and narrative on printed pages 47–58.
The guide asks whether quality inputs are complete, accurate and timely; whether data
are compared across sources; whether investigation depth is proportionate to risk;
whether root cause is determined where possible; whether corrective and preventive
actions are documented; and whether effectiveness is verified or validated without
creating adverse effects. It also routes relevant information to management review.

## Repository transformation

The repository applies these as a research-quality analogy:

```text
nonconformity -> containment -> root-cause account -> corrective action
              -> preventive action -> effectiveness test -> evidence -> closure
```

`CAPA_APPLIED` is therefore insufficient for closure. A closed record needs an explicit
effectiveness test and verification references. Quality checkpoints with defects need a
linked NCR/CAPA path; failed checkpoints cannot be relabelled as a pass.

## Limits

- The guide addresses medical-device quality-system inspections and is historical.
- AION is not represented here as a medical device or FDA-regulated manufacturer.
- This is a transferable quality-method analogy, not a legal or regulatory claim.
- `FDA_GUIDE_REFERENCE != FDA_COMPLIANCE`; `CAPA_CLOSURE != SCIENTIFIC_TRUTH`.
