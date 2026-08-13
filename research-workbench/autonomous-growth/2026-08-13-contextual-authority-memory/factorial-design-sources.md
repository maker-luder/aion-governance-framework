# Full-factorial completeness source notes

## 1. NIST Engineering Statistics Handbook — Full factorial example

URL: https://www.itl.nist.gov/div898/handbook/pri/section3/pri3332.htm

NIST states that running the full complement of all possible factor combinations permits estimation of all main and interaction effects in the full model. Its three-factor two-level example has eight combinations and includes three main effects, three two-factor interactions, and one three-factor interaction. The page presents a standard order for coded factor settings and discusses replication, randomization, and center-point runs. It also notes that replication can support checking dispersion assumptions across the experimental space.

For the prototype, this supports a deterministic coverage contract: enumerate the Cartesian product of declared factor levels, compare it with observed run keys, and distinguish complete coverage from missing, duplicate, or out-of-domain cases. The prototype will not estimate coefficients or infer effects.

## 2. NIST Engineering Statistics Handbook — Process Improvement overview

URL: https://www.itl.nist.gov/div898/handbook/pri/pri.htm

The overview places full factorial designs within a broader design-of-experiments workflow: set objectives, select process variables and levels, select a design, execute with appropriate design controls, analyze data, test/revise models, interpret results, and confirm results. It distinguishes full factorial from fractional factorial and other designs, and separately lists replication, randomization, center points, model testing, and confirmation as relevant topics.

This supports keeping matrix completeness separate from replication validity, execution provenance, model interpretation, and confirmation. A complete matrix is a design property, not scientific proof.

## Design consequence

The next bounded unit should be `factorial-completeness-contract_v0.1.0`. It will test Cartesian-product enumeration, missing-cell detection, duplicate-cell detection, level validation, explicit replication labels, run-order/provenance completeness, and a conservative `HOLD`/`INDETERMINATE` disposition when completeness or execution metadata is insufficient.

## References

[1]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri3332.htm "NIST — Full factorial example"
[2]: https://www.itl.nist.gov/div898/handbook/pri/pri.htm "NIST — Process Improvement and design-of-experiments overview"

## 3. SciRep computational-experiment framework

URL: https://arxiv.org/html/2503.07080v3

SciRep describes a reproducibility framework organized around experiment configuration, data management, computational environment, code execution, validation, and research-artifact packaging. Its design treats configuration and execution as explicit records and emphasizes that a re-executable artifact must preserve the information needed to run the experiment again. The framework also distinguishes reproducibility/replicability validation from the artifact packaging step.

For the prototype, this supports requiring each factorial cell to carry a stable run identifier, factor-level key, execution status, protocol/configuration reference, and provenance reference. A complete Cartesian matrix with missing execution metadata should not be classified as a complete executed experiment. The prototype remains standard-library-only and does not build containers or claim cross-environment reproducibility.

[3]: https://arxiv.org/html/2503.07080v3 "Costa, Barbosa & Cunha — A Framework for Supporting the Reproducibility of Computational Experiments in Multiple Scientific Domains"
