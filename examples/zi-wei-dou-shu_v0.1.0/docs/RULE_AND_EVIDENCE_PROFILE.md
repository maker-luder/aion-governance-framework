# Zi Wei Dou Shu rule and evidence profile

## Frozen rule profiles

| ID | Algorithm | Chart | Purpose |
|---|---|---|---|
| `quanshu-default-v1` | `iztro` `default` | heaven | classical default documented upstream as based on 《紫微斗數全書》 |
| `zhongzhou-heaven-v1` | `iztro` `zhongzhou` | heaven | explicit modern school comparison |

The default is not labelled “the one true Zi Wei Dou Shu.” Upstream documents
differences among schools in transformations and star brightness, and provides
configuration/plugin surfaces for them. This component therefore rejects an
unknown profile and records the chosen algorithm in every output.

## Calendar boundary

Calendar conversion is owned by the pinned upstream dependency. The repository
keeps official Hong Kong Observatory calendar tables as independent,
hash-addressed witnesses. Input must state:

- solar or lunar date;
- hour index `0..12`, distinguishing early and late 子 hour;
- whether the lunar month is intercalary;
- whether the intercalary month is split at day 15 (`fixLeap`).

The adapter does not silently substitute solar-term pillars for lunar-date
placement. Upstream's recent changelog explicitly records corrections involving
late 子 hour, leap months and using lunar rather than solar-term stems/branches.

## Fact/interpretation boundary

Palace, star, transformation and time-layer placement are deterministic facts
under a named profile. They are useful here as a complex provenance and
school-variance research domain. No placement becomes evidence that an AI has
subjectivity; no placement becomes a claim about a real person's fate or traits.

The only permitted relationship to the durable AION research core is an
additive, no-effect comparison fixture:

```text
ZI_WEI_FACTS -> governed evidence fixture
ZI_WEI_FACTS != subjectivity evidence
ZI_WEI_FACTS != scientific validation
ZI_WEI_FACTS != action authority
```
