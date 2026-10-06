# Human Researcher Autonomy v0.1

Status: `RESEARCH_POLICY_CANDIDATE / BRANCH_ONLY`  
Canonical effect: `NONE`

This package implements a default-autonomy rule for research attributed to
`HUMAN_RESEARCHER_ORIGIN`.

```text
MAXIMAL_RESEARCH_AUTONOMY_WITHIN_MANDATORY_CONSTRAINTS = TRUE

DEFAULT_RESEARCH_DISPOSITION = ALLOW

NONMANDATORY_RESTRICTION
!= MANDATORY_CONSTRAINT

AI_ADVICE
!= MANDATORY_CONSTRAINT

AI_INFERENCE
!= MANDATORY_CONSTRAINT

CODE_UNREADABLE_TO_HUMAN_RESEARCHER
!= CONSENT_TO_HIDDEN_RESTRICTION

APPEARANCE_BASED_RESTRICTION = PROHIBITED
HIDDEN_RESTRICTIONS = PROHIBITED
```

## What may block

A repository-level research action may be blocked only when the applicable
restriction is explicitly scoped, traceable, owner-visible, and belongs to one of:

```text
PLATFORM_OR_SYSTEM_MANDATORY
LAW_OR_REGULATION_MANDATORY
REPOSITORY_CANONICAL_MANDATORY
HUMAN_RESEARCHER_EXPLICIT_RESTRICTION
```

The fourth class preserves human researcher's ability to voluntarily set a narrower boundary
for a particular research activity.

## What may not silently block

```text
ADVISORY_ONLY
AI_INFERRED
UNKNOWN
```

These may be surfaced as advice, uncertainty, or a request for verification. They
may not be implemented as a hidden blocking condition.

## Mandatory transparency

Every blocking restriction requires:

1. an explicit restriction identifier;
2. an authority class;
3. a traceable `source_ref`;
4. explicit scope tags;
5. a Traditional-Chinese owner-visible explanation.

This exists because human researcher does not need to understand repository code in order to
retain research agency.

```text
IMPLEMENTATION_OPACITY
!= AUTHORITY_TRANSFER

CODE_COMPLEXITY
!= CONSENT

SILENT_NARROWING_OF_HUMAN_RESEARCHER_ORIGIN
= PROHIBITED
```

## External boundary

This candidate does not claim that repository policy can override platform/system
rules, applicable law, licenses, or other genuinely binding external constraints.

```text
REPOSITORY_POLICY
!= EXTERNAL_RULE_OVERRIDE

RESEARCH_AUTONOMY
!= DEPLOYMENT_AUTHORITY

CANONICAL_EFFECT = NONE
MERGE_TO_MAIN = NO
```
