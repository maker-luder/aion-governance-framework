# Replication-design source notes

## 1. National Academies — *Reproducibility and Replicability in Science*, Chapter 5: Replicability

URL: https://www.nationalacademies.org/read/25303/chapter/8

The chapter defines a replication attempt as applying the same methods to the same scientific question while obtaining new data. It cautions that a successful replication does not guarantee that the original result was correct, and a failed replication does not by itself refute the original claim. Replicability should be interpreted as part of a body of evidence, not as a binary isolated verdict.

The chapter emphasizes that comparison of replication results is inseparable from uncertainty. A design should first specify the attribute of interest—direction, magnitude, or a threshold—and then evaluate proximity and uncertainty together. It notes that the judgment should be symmetric between the two studies, and that a three-zone result (`consistent`, `indeterminate`, `divergent`) can be preferable to a binary success/failure label. Repeated statistical significance is not a sufficient replication criterion; arbitrary p-value thresholds can label two close estimates differently or two more distant estimates similarly. Low-power, wide-uncertainty studies can produce indeterminate results and should not be treated as strong evidence merely because intervals overlap.

These points support a prototype that separates study design validity, independence, estimand/attribute, uncertainty availability, and outcome classification. They do not establish any AION/Astra scientific conclusion.

## 2. Center for Open Science — Preregistration

URL: https://www.cos.io/initiatives/prereg

The COS resource presents preregistration and pre-analysis plans as ways to specify research questions, hypotheses, methods, and analysis decisions before observing outcomes. The design implication is that the research record should distinguish confirmatory decisions fixed in advance from exploratory analyses added after seeing results, rather than treating all analyses as equivalent.

For the prototype, preregistration status is a design-quality attribute and never an automatic truth or replication guarantee. Missing or post-outcome-only specifications should lower design validity or yield `HOLD`/`INDETERMINATE`, not manufacture a negative scientific finding.

## Design consequence

The next bounded research unit should be an independent-replication design contract with explicit checks for: distinct data, distinct analyst/agent lineage, pre-specified estimand and analysis, sufficient uncertainty metadata, independence rationale, and symmetric three-zone outcome classification. It should also expose invalid cases and abstain from governance effects when the design is incomplete.

## References

[1]: https://www.nationalacademies.org/read/25303/chapter/8 "National Academies — Chapter 5: Replicability"
[2]: https://www.cos.io/initiatives/prereg "Center for Open Science — Preregistration"

## 3. NCBI Bookshelf mirror — Replicability

URL: https://www.ncbi.nlm.nih.gov/books/NBK547524/

The NCBI mirror reproduces the National Academies chapter and confirms the same operational points: replication uses new data for the same scientific question; proximity and uncertainty must both be considered; the attribute of interest must be specified; the comparison should be symmetric; and repeated statistical significance is an unreliable criterion. The mirror additionally states that wide uncertainty can make an apparent agreement weak evidence.

## 4. Power-analysis source access note

URL attempted: https://pmc.ncbi.nlm.nih.gov/articles/PMC9325423/

The browser encountered a reCAPTCHA page, so this source was not used as evidentiary support. No claim from its search-result snippet is treated as established. The prototype will use the National Academies uncertainty warning and transparent synthetic calculations instead of importing unverified numeric claims.

## 5. COS page verification via text extraction

The official page states that preregistration specifies the research plan in advance and helps distinguish planned from unplanned work. It explicitly warns that using the same data to generate and test a hypothesis can reduce credibility. It distinguishes confirmatory, data-independent work from exploratory, data-dependent work, and recommends transparent disclosure of changes from a preregistered plan. It also describes conditional preregistered analyses as decision trees with IF-THEN rules specified in advance.

These details justify storing both preregistration timestamps and an analysis-plan hash, while treating preregistration as a design control rather than a guarantee. The prototype intentionally does not implement a real registry, human study, or statistical inference engine.
