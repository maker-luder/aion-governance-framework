# Bazi Rule Profile Specification

Every calculation is bound to an immutable, versioned `BAZI_RULE_PROFILE`.
The implemented candidate profiles are:

1. `STANDARD_LICHUN_MIDNIGHT_CIVIL_V1`: Lichun year boundary, solar-jie
   month boundary, midnight day rollover, IANA civil time.
2. `STANDARD_LICHUN_ZI23_CIVIL_V1`: same rules with late-Zi 23:00 day
   rollover.
3. `STANDARD_LICHUN_MIDNIGHT_APPARENT_SOLAR_V1`: candidate apparent-solar
   adjustment using longitude correction and an equation-of-time estimate.

School-specific strength, structure, useful-element, transformation and luck
start rules are not frozen. They remain versioned interpretation candidates
or explicit owner inputs. Unsupported or owner-defined rules fail closed.
