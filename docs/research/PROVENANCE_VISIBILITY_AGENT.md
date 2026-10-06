# Provenance Visibility Agent — research specification

Date: 2026-10-06  
Status: `BRANCH-ONLY RESEARCH CANDIDATE`

## Research question

Can a transparent repository convert provider-level hidden provenance signals into
an explicit, human-readable disclosure without overstating what the signals prove?

## Official-source boundary

OpenAI currently documents:

- images: C2PA Content Credentials + SynthID;
- audio: SynthID;
- text: textGrain, with detector access currently limited to approved qualifying
  research/academic organizations;
- the public Content Provenance API currently checks supported image/audio files.

The implementation therefore does not invent a local textGrain detector.

## Interpretation contract

```text
DETECTED
= supported provenance signal was found

NOT_DETECTED
= supported provenance signal was not found by this check

NOT_DETECTED
!= HUMAN_CREATED
!= NEVER_PROCESSED_BY_AI

DETECTED
!= AUTHORSHIP
!= OWNERSHIP
!= USER_IDENTITY
!= PROMPT
```

## Visible rendering

The agent converts hidden evidence into a visible report containing:

- media type;
- overall verification verdict;
- signal type;
- detected/not-detected/access-required state;
- C2PA validation state when present;
- issuer/model/generation time when supplied by the verifier;
- mandatory interpretation caveats.

## Research boundary

The agent is deliberately one-directional:

```text
DETECT / DISCLOSE = IN_SCOPE
REMOVE / DEGRADE / EVADE / REVERSE_ENGINEER = OUT_OF_SCOPE
```

This keeps the project aligned with repository transparency goals while avoiding a
tool that facilitates provenance removal.

## Source references

- OpenAI Help Center, "Provenance signals in OpenAI-generated content", current
  version checked 2026-10-06.
- OpenAI API documentation, "Content provenance", current version checked
  2026-10-06.
- OpenAI, "Advancing content provenance for a safer, more transparent AI
  ecosystem", updated 2026-10-05 for text provenance.
