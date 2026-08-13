# Power-analysis and effect-size uncertainty source notes

## 1. National Academies — Confidence in Science

URL: https://www.nationalacademies.org/read/25303/chapter/10

The chapter explains that research synthesis can examine variation in effect sizes and possible moderators, but that meta-analysis may lack sufficient power when only a few studies are available. It also emphasizes that empirical results are probabilistic and that isolated replication failures should not be converted into broad certainty claims.

For the prototype, this supports treating power calculations as conditional on explicit assumptions and reporting `UNKNOWN`/`INDETERMINATE` when effect-size, variance, alpha, or target-power assumptions are missing. The contract must not translate a nominal target power into a guarantee, and it must not infer a scientific conclusion from a sample-size calculation.

## Design consequence

The next bounded unit should implement a transparent normal-approximation planning contract with explicit fields for standardized effect bound, standard deviation, alpha, target power, planned sample size, and whether the assumptions were preregistered. It will report an assumption-dependent required sample size and a disposition, not an achieved scientific power or evidence conclusion. Sensitivity cases will vary the assumed effect bound to expose uncertainty.

## References

[1]: https://www.nationalacademies.org/read/25303/chapter/10 "National Academies — Chapter 7: Confidence in Science"

## 2. University of Michigan Meera — Power Analysis, Statistical Significance, and Effect Size

URL: https://meera.seas.umich.edu/power-analysis-statistical-significance-effect-size.html

The educational resource describes power as the probability that a test will detect a statistically significant difference when a specified difference truly exists, and relates power planning to alpha, expected effect size, sample size, and test type. It distinguishes Type I and Type II errors and notes that statistical significance alone does not establish practical importance; effect size is needed to express meaningful magnitude.

The resource also makes clear that effect size for planning is an estimate supplied before data collection, not an observed fact. The prototype therefore reports assumption-dependent planning outputs and exposes sensitivity across effect-size bounds; it does not call the result achieved power, does not infer a true effect, and does not treat a conventional target such as 0.80 as a guarantee.

[2]: https://meera.seas.umich.edu/power-analysis-statistical-significance-effect-size.html "University of Michigan Meera — Power Analysis, Statistical Significance, and Effect Size"
