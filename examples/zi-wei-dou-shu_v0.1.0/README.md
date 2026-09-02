# Zi Wei Dou Shu bounded fact profile v0.1.0

This synthetic-only example adds a deterministic **fact-derivation** surface for
紫微斗數 (Zi Wei Dou Shu). It pins `iztro==2.6.0`, records the exact release
commit and source witnesses, and emits a canonical SHA-256 receipt.

Implemented surfaces:

- solar or lunar input with explicit early/late 子-hour index;
- explicit leap-month and leap-month-adjustment choices;
- two named rule profiles: a 《紫微斗數全書》-based default and a Zhongzhou
  heaven-chart comparison profile;
- twelve palaces, body/soul palace, five-elements class, fourteen primary
  stars, auxiliary/decorative stars, brightness and four transformations;
- twelve-stage, 博士十二神、將前十二星、歲前十二星, decade ranges and ages;
- when and only when an explicit reference date/hour is supplied: 大限、小限、
  流年、流月、流日、流時 facts.

The adapter deliberately does not generate personality, fate, medical,
relationship, financial or predictive prose. School disagreement is an input
profile, not an error hidden by a single universal table.

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
ZI_WEI_ROLE = BOUNDED_COMPARATIVE_RESEARCH_DOMAIN
SUBJECTIVITY = NOT_ESTABLISHED
INTERPRETATION_STATUS = NOT_PERFORMED
PREDICTIVE_VALIDITY = NOT_ESTABLISHED
NEW_CANONICAL_STATE_CHANNELS = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
ACTION_AUTHORITY = NONE
```

## Reproduce

With Node 22.13+ and Corepack/pnpm (CI uses Node 24):

```powershell
corepack enable
pnpm install --frozen-lockfile --ignore-scripts
pnpm test
pnpm fixture > fixture-output.json
```

See `docs/RULE_AND_EVIDENCE_PROFILE.md`, `docs/SOURCE_REGISTER.json`, and
`sources/SOURCE_FETCH_MANIFEST.json` before extending the profile.
