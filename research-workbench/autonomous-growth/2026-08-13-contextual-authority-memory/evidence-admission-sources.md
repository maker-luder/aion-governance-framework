# Evidence admission and non-promotion source notes

## 1. National Academies — Standards for Synthesizing the Body of Evidence

URL: https://www.nationalacademies.org/read/13059/chapter/6

The chapter describes body-of-evidence appraisal domains including risk of bias, consistency, precision, directness, reporting bias, dose-response association, and plausible confounding. It explains consistency as similarity in direction and estimated size across studies, precision as certainty around an estimate, directness as whether the evidence addresses the intended intervention/outcome relationship and applicability, and reporting bias as selective availability of results.

The chapter also warns that inconsistency can reflect true differences or bias and that cross-study dose comparisons can be confounded. These points support a conservative contract in which evidence dimensions are recorded separately, contradictions and missing domains lower admissibility, and an evidence-admission status never becomes a scientific conclusion or governance effect by itself.

## 2. CDC source retrieval note

The initially selected CDC ACIP GRADE URL returned Page Not Found during retrieval. It is retained as a retrieval limitation rather than treated as evidence. The National Academies chapter was used as the accessible primary methodology source for the bounded prototype.

## Design consequence

The next bounded unit should be `evidence-admission-nonpromotion_v0.1.0`. It will validate claim type, evidence tier, provenance completeness, bias/consistency/precision/directness/reporting-bias fields, replication status, and contradiction handling. It will emit `ADMISSIBLE_FOR_REVIEW`, `INDETERMINATE`, or `HOLD`, but never a scientific conclusion, canonical effect, deployment, subjectivity, identity, or consciousness conclusion.

## References

[1]: https://www.nationalacademies.org/read/13059/chapter/6 "National Academies — Standards for Synthesizing the Body of Evidence"
[2]: https://www.cdc.gov/acip-grade/hcp/chapter-7-grade-criteria-determining-certainty-of-evidence/index.html "CDC ACIP GRADE criteria page (retrieval returned Page Not Found)"
