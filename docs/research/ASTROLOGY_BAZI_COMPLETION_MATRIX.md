# Astrology, Bazi and Zi Wei Dou Shu bounded-completion matrix

This matrix records what “complete” means for the repository's deterministic,
offline research fixtures. It does not claim that any divination tradition is
scientifically validated or that every historical school agrees.

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
ASTROLOGY_BAZI_ZIWEI_ROLE = BOUNDED_COMPARATIVE_RESEARCH_DOMAIN
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
| High-precision ephemeris | Independent pinned local trial completed | no public provider integration; [trial/license disposition](SWISS_EPHEMERIS_LOCAL_TRIAL_2026_09_03.md) |
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
| Named month-structure profile | Owner-selected; raw exposure/root evidence implemented | `AION_ZIPING_MONTH_STRUCTURE_V1`; [method decision](DOMAIN_METHOD_DECISION_2026_09_03.md) |
| Strength, 格局成敗, 用神 selection | Interpretation remains unresolved | named profile does not turn raw evidence into an automatic judgment |
| Free-form prediction or identity binding | Not performed | no runtime/authority effect |

## Source acquisition

Run `scripts/fetch_astrology_bazi_sources.py`. Redistributable public-domain or
attributed text witnesses are retained; large scans and sources with unresolved
redistribution terms are downloaded, hashed, and discarded. Both component
manifests record every result and prove runtime network access is unnecessary.

## Zi Wei Dou Shu

| Surface | Status | Boundary |
|---|---|---|
| Solar/lunar normalization | Implemented, pinned upstream | explicit calendar type and hour index |
| Leap month and late 子 hour | Implemented | caller must choose named behavior |
| Twelve palaces, 命/身, 五行局 | Implemented | deterministic facts under rule profile |
| Fourteen primary stars | Implemented | exact-count invariant |
| Auxiliary/decorative stars and four transformations | Implemented | upstream tables remain school-configurable |
| 大限、小限、流年、流月、流日、流時 | Implemented | explicit reference date/hour only |
| Classical-default / Zhongzhou comparison | Implemented | no universal-school claim |
| Free-form prediction/personality synthesis | Not performed | predictive validity not established |
| AION canonical state or subjectivity promotion | No effect | central question preserved; no eighth state |

Run `scripts/fetch_ziwei_sources.py` for the Zi Wei source set. Its manifest pins
the classical transcription revision, `iztro` release/commit/package hash, and
official calendar witnesses; runtime remains offline.
