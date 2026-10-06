# Provenance Visibility Agent v0.1

Status: `RESEARCH CANDIDATE / BOUNDED VERIFIER`  
Purpose: turn supported hidden provenance signals into explicit, human-readable
disclosures.

## Core behavior

```text
HIDDEN_PROVENANCE_SIGNAL
-> VERIFY
-> NORMALIZE
-> VISIBLE_DISCLOSURE

NOT_DETECTED
!= HUMAN_CREATED

DETECTED
!= AUTHORSHIP
!= OWNERSHIP
!= HUMAN_CONTRIBUTION_PERCENTAGE
```

The agent does not attempt to remove, weaken, evade, or reverse-engineer a watermark.

## Supported paths

### Image

OpenAI's public Content Provenance API can return:

- C2PA Content Credentials;
- SynthID watermark results.

The agent renders those results as an explicit Traditional-Chinese report.

### Audio

The public API can return SynthID verification results. The same fail-open-to-unknown
semantics apply: `not_detected` is not converted into a human-authorship claim.

### Text

OpenAI documents textGrain watermarking, but text detector access is currently limited
to approved organizations with qualifying research or academic use cases. Therefore:

```text
NO_APPROVED_TEXT_DETECTOR
=> VERIFICATION_ACCESS_REQUIRED
=> DO_NOT_GUESS
```

When approved detector access exists, an adapter can be supplied to
`text_with_approved_detector`.

## Live image/audio verification

Install the optional SDK dependency and provide `OPENAI_API_KEY`:

```text
pip install -e "research-labs/provenance-visibility-agent_v0.1.0[openai]"
```

Then:

```python
from aion_provenance_visibility_agent import MediaKind, ProvenanceVisibilityAgent

agent = ProvenanceVisibilityAgent()
report = agent.verify_file_with_openai("image.png", MediaKind.IMAGE)
print(report.visible_label_zh_tw)
```

No API key, prompt, account identifier, or uploaded file contents are written into
repository artifacts by this package.

## Privacy and transparency

```text
PROVENANCE_SIGNAL != PERSONAL_IDENTITY
PROVENANCE_SIGNAL != PROMPT_DISCLOSURE

PERSONAL_IDENTITY_INFERENCE = PROHIBITED
PROMPT_INFERENCE = PROHIBITED
WATERMARK_REMOVAL_OR_EVASION = OUT_OF_SCOPE
CANONICAL_EFFECT = NONE
```

Repository-facing naming is role-based and contains no conversational nickname.
