# Source card: NIST AI 600-1

- Source: *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*
- Identifier: NIST AI 600-1; DOI `10.6028/NIST.AI.600-1`
- Publication date: July 2024
- Official URL: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- Reviewed upstream bytes: `1174643`
- Reviewed upstream SHA-256: `6e73620ab6b64e90ef2c04bf0e0d6246185a2f4b1b13cab0df494496cff89b6a`
- Intake date: 2026-09-13 (Asia/Taipei)
- Registry role: `GOVERNANCE_REFERENCE / METHOD / CANDIDATE / REFERENCE_ONLY`

## Verified sections and bounded findings

The review used sections 1–3, including the information-integrity discussion and the
suggested actions aligned to AI RMF functions. The profile is a cross-sector companion
to AI RMF 1.0. It treats GAI risk across the lifecycle and stresses documented context,
measurement and evaluation, incident disclosure, provenance, monitoring and review.
Its information-integrity treatment distinguishes fact, opinion and inference, makes
uncertainty and vetting level visible, and links claims to traceable sources.

## Repository transformation

The project uses these points to require:

- exact source-state and runtime references;
- explicit separation of observation, inference and claim;
- upstream-to-card chain of custody with byte count and digest;
- counterevidence and uncertainty retention;
- incident/NCR routing rather than silent correction;
- versioned re-evaluation rather than overwriting prior predictions.

## Limits

- This profile does not validate the repository's code or scientific conclusions.
- Information integrity is a quality-control concern; it is not evidence of experience.
- The card does not import NIST authority into AION release or research decisions.
- `PROFILE_CROSSWALK != CONFORMITY`; `QUALITY_PASS != SUBJECTIVITY_SUPPORT`.
