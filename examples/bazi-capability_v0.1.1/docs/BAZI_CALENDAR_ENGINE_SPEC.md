# Bazi Calendar Engine Specification

The engine accepts an ISO local datetime, IANA timezone, event UTC offset,
location and explicit rule profile. It validates the zone/offset pair, maps
the event to UTC, applies the selected civil/solar-time rule, then delegates
solar-term and calendar facts to `lunar_python==1.4.8`.

Supported civil years are 1900 through 2100. Values outside this range,
unknown zones, mismatched UTC offsets and unfrozen owner-defined rules fail
closed.

The apparent-solar profile is a research candidate. Longitude correction is
exact relative to the timezone meridian; the equation-of-time term is an
explicit approximation and must not be described as a high-precision
ephemeris.
