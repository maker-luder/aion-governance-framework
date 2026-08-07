# Bazi Storage Integrity Corrective Report

Version: 0.1.1 candidate  
Finding: `F_BZ_001`  
Result: `PASS_PENDING_OWNER_REVIEW`

## Correction

- Added SQLite `BEFORE UPDATE` and `BEFORE DELETE` triggers for pillars, hidden stems, ten gods, relations, luck cycles, and materialization snapshots.
- Separated deterministic derivation identity from the hash of the rows actually stored in SQLite.
- Added versioned canonical serialization `BAZI_MATERIALIZED_FACTS_V1`.
- Added append-only materialization snapshots containing category counts and the stored-facts hash.
- Added `verify_derivation_identity`, `verify_materialized_facts_integrity`, and `verify_complete_calculation_integrity`.
- Complete verification reads persisted rows, checks exact expected membership, rejects missing/extra/tampered rows, and checks run/profile linkage.

## Rule semantics

- Luck-cycle direction and start-age inputs retain their declared source; they are not inferred as an Owner school rule.
- Gregorian month, solar-term month, and Yin-month ordinal remain distinct.
- `EARLY_LATE_ZI_PROFILE` remains a candidate rule profile and is not promoted.
- No AION/Astra natal binding was created.

## Non-claims

This is a component-level corrective candidate. It does not implement AION Runtime, establish subjectivity, deploy a service, or create canonical effect.
