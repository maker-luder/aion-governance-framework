# Astrology and Bazi bounded-completion matrix

This matrix records what “complete” means for the repository's deterministic,
offline research fixtures. It does not claim that any divination tradition is
scientifically validated or that every historical school agrees.

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
ASTROLOGY_BAZI_ROLE = BOUNDED_COMPARATIVE_RESEARCH_DOMAIN
NEW_CANONICAL_STATE_CHANNELS = NONE
SCIENTIFIC_CLAIM_CHANGE = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Western astrology

| Surface | Status | Boundary |
|---|---|---|
| Traditional seven, tropical zodiac, whole-sign houses | Implemented | versioned synthetic facts |
| Domicile, exaltation, detriment, fall | Implemented | sign-based classical table |
| Triplicity, Egyptian bounds, Chaldean faces | Implemented v0.3 | named historical profiles |
| Sect and planetary joys | Implemented | Mercury uncertainty preserved where needed |
| Five classical aspects | Implemented | explicit orb table |
| Uranus, Neptune, Pluto | Implemented modern overlay | traditional rulers retained |
| Minor aspects and motion/phase | Implemented modern overlay | versioned, missing vectors unresolved |
| True lunar nodes and Chiron | Implemented v0.3 as points | no classical dignity/sect/rulership |
| High-precision ephemeris | Upstream contract | source/version required; not bundled |
| Predictive/personality synthesis | Not performed | validity not established |

## Bazi

| Surface | Status | Boundary |
|---|---|---|
| Calendar normalization and four pillars | Implemented | pinned calendar/rule profile |
| Hidden stems, ten gods, NaYin, twelve stages | Implemented | deterministic facts |
| Stem/branch relations | Implemented | named relation tables |
| Luck direction/start and decade/annual/monthly cycles | Implemented | explicit school inputs |
| Fixed-qi 24 solar terms | Implemented | official 15-degree invariant |
| Seasonal/day-master evidence | Implemented v0.3 | raw counts, no score |
| Combination/harmony/meeting targets | Implemented v0.3 | conditions not evaluated |
| Strength, 格局, 用神 | Evidence-ready, unresolved | requires a named owner-frozen school profile |
| Free-form prediction or identity binding | Not performed | no runtime/authority effect |

## Source acquisition

Run `scripts/fetch_astrology_bazi_sources.py`. Redistributable public-domain or
attributed text witnesses are retained; large scans and sources with unresolved
redistribution terms are downloaded, hashed, and discarded. Both component
manifests record every result and prove runtime network access is unnecessary.
