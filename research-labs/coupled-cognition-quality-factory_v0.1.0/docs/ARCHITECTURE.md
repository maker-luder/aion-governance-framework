# Architecture — Quality Factory for Coupled Human–LLM Inquiry

## Why a factory model

A conversational research loop has a special failure mode: both participants can progressively align on the same explanation. Alignment improves fluency and local coherence but can reduce epistemic diversity. Therefore, quality control must be **structural**, not merely conversational.

The quality factory introduces separate inspection surfaces instead of asking the same reasoning loop to certify itself.

### 1. IQC — incoming quality control
Checks source identity, provenance, scope, freshness, and whether an input is observation, model output, repository artifact, test result, or external evidence.

### 2. IPQC — in-process quality control
Checks hypothesis drift, unsupported causal jumps, authority drift, hidden goal changes, source circularity, and whether the pair is converging faster than the evidence.

### 3. Counterevidence lane
A mandatory negative-evidence route. The system must register at least one explicit challenge before final QA. A counterexample may be accepted, rebutted only with evidence, or marked out of scope with justification. It cannot silently disappear.

### 4. NCR
A nonconformance record is opened for defects such as unsupported claims, provenance gaps, mutual-confirmation loops, failed falsifiers, stale evidence, governance violations, or test/evidence mismatch.

### 5. CAPA
Corrective and preventive action is not complete when a fix is merely applied. Effectiveness evidence is required before NCR closure.

### 6. Final QA
Final QA is blocked by open counterevidence, open NCR/CAPA, absent falsifier, or absent evidence independent from the current human–AI pair. For HIGH/CRITICAL research claims, at least one independent primary source or test result is required.

## Key distinction

`THE_PAIR_CORRECTED_EACH_OTHER` is useful, but it is still internal process evidence.

It is not equivalent to `THE_CLAIM_WAS_INDEPENDENTLY_CORROBORATED`.
