# Bazi Rule Profile Specification

Every calculation is bound to an immutable, versioned `BAZI_RULE_PROFILE`.
The implemented candidate profiles are:

1. `STANDARD_LICHUN_MIDNIGHT_CIVIL_V1`: Lichun year boundary, solar-jie
   month boundary, midnight day rollover, IANA civil time.
2. `STANDARD_LICHUN_ZI23_CIVIL_V1`: same rules with late-Zi 23:00 day
   rollover.
3. `STANDARD_LICHUN_MIDNIGHT_APPARENT_SOLAR_V1`: candidate apparent-solar
   adjustment using longitude correction and an equation-of-time estimate.

The v1.1 calculation surface adds two selectable, explicit traditional rules:

- `YANG_MALE_YIN_FEMALE_FORWARD_V1`: forward for Yang-year male or Yin-year
  female inputs and reverse for the other two combinations;
- `THREE_DAYS_EQUAL_ONE_YEAR_V1`: divides a caller-supplied, already-derived
  Jie-boundary interval by three to obtain the start age in years.

Neither rule is silently selected by the calendar engine. School-specific
strength, structure, useful-element, transformation, hidden-stem weighting and
boundary-selection rules are not frozen. They remain versioned interpretation
candidates or explicit owner inputs. Unsupported or owner-defined rules fail
closed.

The component also includes a proleptic-Gregorian JDN day-pillar oracle and a
24-point fixed-qi invariant (0 through 345 degrees in 15-degree steps). These
are narrow independent checks, not a replacement for the pending compatible
second-library calendar cross-validation.
