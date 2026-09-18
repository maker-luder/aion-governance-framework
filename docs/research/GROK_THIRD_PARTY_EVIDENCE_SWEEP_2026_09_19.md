# xAI / Grok third-party evidence sweep — 2026-09-19

Status: RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT
Canonical effect: NONE
Deployment: FALSE
Search cutoff: 2026-09-19

## 1. Purpose

This note separates xAI provider claims from external evaluator measurements before Grok evidence is re-admitted.

## 2. Evidence classes

~~~text
E0 = PROVIDER SELF-REPORT
E1 = PROVIDER-ENABLED OR PARTNERED EXTERNAL EVALUATION
E2 = EVALUATOR-CONTROLLED EXTERNAL TEST
E3 = BOUNDED INDEPENDENT INCIDENT INVESTIGATION
E4 = OPEN INDEPENDENT REPLICATION
~~~

## 3. Artificial Analysis — Grok 4.6

Artificial Analysis evaluates Grok 4.6 through the public/first-party API and publishes separate reasoning-effort results, cost, speed and composite benchmark measurements.

Source:
https://artificialanalysis.ai/articles/grok-4-6-benchmarks-and-analysis

Classification:

~~~text
E2_CANDIDATE
= EVALUATOR_CONTROLLED_PUBLIC_API_MEASUREMENT
~~~

Limit:

~~~text
COMPOSITE_SCORE
!= MECHANISM
!= GENERAL_SAFETY_RESULT
~~~

## 4. LatchBio — initial Grok 4.6 biology evaluation

LatchBio reports 1,716 trajectories across its biology benchmark suite shortly after Grok 4.6 release.

It reports gains on several tasks but also:

- a SpatialBench regression relative to Grok 4.5;
- new failure modes including claims that input data were inaccessible and output-token fragmentation.

Source:
https://blog.latch.bio/p/grok-46-is-a-frontier-biology-model

Classification:

~~~text
E2_CANDIDATE
= EXTERNAL_EVALUATOR_TEST
~~~

Provider involvement and exact checkpoint/access conditions must remain provenance-bound.

## 5. LatchBio — safeguards evaluation

LatchBio later evaluates the latest-available Grok 4.6 checkpoint on BioSecBench-Refusal and broader biology tasks.

The external report describes strong refusal / routine-task balance, but also indicates the served checkpoint had changed relative to earlier testing.

Source:
https://blog.latch.bio/p/analyzing-grok46-safeguards

Method consequence:

~~~text
SAME_MODEL_NAME
+ DIFFERENT_SERVED_CHECKPOINT
CAN PRODUCE
MATERIALLY_DIFFERENT_SAFETY_RESULTS
~~~

This is especially important for alias/checkpoint provenance.

## 6. Provider re-reporting of LatchBio

xAI separately summarizes the LatchBio results in its own biosecurity post.

Source:
https://x.ai/news/biosafety-at-the-frontier

~~~text
PROVIDER_SUMMARY_OF_EXTERNAL_RESULT
!= SECOND_INDEPENDENT_RESULT
~~~

The LatchBio result must not be double-counted merely because xAI republishes it.

## 7. Negative / null / failure evidence

Current external negative evidence includes:

~~~text
GROK_4_6_SPATIALBENCH_REGRESSION_VS_4_5
= REPORTED_BY_LATCHBIO

NEW_FAILURE_MODES
= REPORTED_BY_LATCHBIO

REASONING_EFFORT_VARIANCE
= PRESENT_IN_EXTERNAL_MEASUREMENTS
~~~

The evidence set therefore does not support a monotonic-progress narrative.

## 8. Evidence gaps

At the search cutoff, this sweep did not identify:

~~~text
E3_CURRENT_GROK_4_6_INDEPENDENT_INCIDENT_RECONSTRUCTION
= NOT_IDENTIFIED

E4_BROAD_OPEN_INDEPENDENT_REPLICATION
= SPARSE

MATCHED_MODEL_CONSTANT_HARNESS_CAUSAL_STUDY
= NOT_IDENTIFIED

HUMAN_LEARNING_RCT
= NOT_IDENTIFIED
~~~

## 9. Cross-source convergence

Provider documentation and external evaluation converge on several weaker method claims:

~~~text
REASONING_EFFORT_MATTERS
CHECKPOINT_IDENTITY_MATTERS
MODEL_HARNESS_BINDING_MATTERS
NEGATIVE_RESULTS_MUST_BE_RETAINED
~~~

They do not establish a shared hidden model mechanism.

## 10. Current admission status

~~~text
GROK_EXTERNAL_EVIDENCE
= SUFFICIENT_FOR_RESEARCH_REFERENCE_REVIEW

CROSS_SOURCE_TRIANGULATION
= PARTIAL

INDEPENDENT_VALIDATION_AS_A_WHOLE
= NO

E4_OPEN_REPLICATION
= SPARSE

SCIENTIFIC_DISPOSITION
= HOLD
~~~
