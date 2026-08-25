# External Quality / AI Governance Crosswalk — 2026-08-23

This is a research crosswalk, not a certification claim.

## FDA CAPA inspection guidance
The FDA's CAPA inspection guidance describes CAPA as a subsystem that collects and analyzes quality information, identifies and investigates quality problems, takes corrective/preventive action, verifies or validates the action, communicates it, supports management review, and documents the activity.

Research implication: `CAPA_APPLIED != CAPA_EFFECTIVENESS_VERIFIED`.

Source: https://www.fda.gov/files/Guide-to-Inspections-of-Quality-Systems.pdf

## NIST AI RMF
The NIST AI RMF emphasizes continuous risk management across the lifecycle, rigorous testing and performance assessment, uncertainty documentation, and notes that independent review can improve testing effectiveness and mitigate internal bias/conflicts of interest.

Research implication: the current human–AI pair should not be the only evidence source used to clear a high-confidence result.

Sources:
- https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- https://www.nist.gov/ai-test-evaluation-validation-and-verification-tevv

## NIST 2026 deployed-AI monitoring
NIST's 2026 monitoring report emphasizes that pre-deployment evaluation is insufficient by itself and that real-world monitoring is needed to detect unforeseen outputs and consequences.

Research implication: quality control is not a one-time final gate; evidence can reopen an NCR after apparent completion.

Source: https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation

## ISO/IEC 42001
ISO/IEC 42001 specifies an AI management system and frames continual improvement using a Plan–Do–Check–Act management-system approach, with traceability, transparency, and reliability among its benefits.

Research implication: the factory should be cyclic and correction-capable rather than a linear one-shot approval pipeline.

Source: https://www.iso.org/standard/42001

## Repository crosswalk
The historical repository already contains:
- `components/iqc_quality_inspection_v0.1.0`
- `research-labs/integration-candidates/iqc-capa-contract_v0.1.0`
- `qa/NCR_CAPA_REGISTER.md`
- multiple NCR/CAPA governance records

This new lab does not replace them. It specializes their quality vocabulary for **coupled human–LLM epistemic production** and adds the mandatory counterevidence lane.
