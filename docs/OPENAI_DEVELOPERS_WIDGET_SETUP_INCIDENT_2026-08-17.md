# OpenAI Developers Secure API-Key Widget Setup Incident — 2026-08-17

> **RESEARCH-ONLY INCIDENT RECORD**
>
> - **Incident ID:** `AION-INC-2026-08-17-OPENAI-WIDGET-001`
> - **Branch:** `review/four-domain-research-materialization`
> - **Status:** `OPEN / UNDER_DIAGNOSIS`
> - **Canonical effect:** `NONE`
> - **Scope:** ChatGPT OpenAI Developers / OpenAI Platform secure API-key setup path used during Launch Desk setup
> - **Main branch impact:** `NONE`
> - **Architecture change:** `NONE`

## Incident summary

During Launch Desk credential setup, the Human Owner observed that the interactive secure API-key setup interface did not appear as expected. The same general symptom was observed on both mobile and desktop surfaces: the surrounding workflow could continue, but the expected interactive key-setup UI was absent.

The investigation initially suspected a ChatGPT Plugin/App registration mismatch because a permission-registry lookup using the display name `OpenAI Developers` returned `not_installed`. Subsequent evidence showed that this interpretation was too strong and had to be revised: the OpenAI Developers bundle was visibly present, its OpenAI Platform application was connected, the local-confirmation MCP component was present, and all five visible OpenAI Developers skills were enabled.

The current unresolved question is therefore narrower: whether the failure is in surface-specific interactive widget rendering, client compatibility, or another transient handoff/rendering condition after the backend setup action is accepted.

## Source attribution

### Human Owner observations

The Human Owner reported and visually demonstrated the following:

1. The expected secure API-key setup interface had failed to appear during the Launch Desk setup path.
2. The symptom was not limited to a single device class; a comparable failure had been observed on both mobile and desktop.
3. The OpenAI Developers bundle UI showed:
   - `OpenAI Platform` application — connected;
   - `Openai-api-key-local-confirmation` MCP server — present;
   - `Agents SDK` — enabled;
   - `Build ChatGPT App` — enabled;
   - `ChatGPT App Submission` — enabled;
   - `OpenAI API Troubleshooting` — enabled;
   - `OpenAI API Key Setup` — enabled.

The screenshot used for this observation was supplied in the ChatGPT conversation and is not embedded in this repository record.

### ChatGPT diagnostic interpretation

ChatGPT first ranked Plugin/App registration as the leading suspect because `OpenAI Developers` returned `not_installed` when queried through the app-permission registry. After inspecting the actual bundle/component state, ChatGPT revised that interpretation: the `not_installed` response must not be treated as proof that the OpenAI Developers bundle itself is absent.

The revised diagnosis separates the bundle/display name from the underlying `OpenAI Platform` application registration and treats surface/widget rendering as the current primary unresolved area.

### Connector/tool observations

The diagnostic tools returned the following operational evidence during the same investigation:

1. `OpenAI Platform` permission lookup returned a valid application record (`found`) and showed that it inherits the current default ChatGPT app permission setting.
2. A permission lookup using `OpenAI Developers` returned `not_installed`.
3. A standalone plugin-directory search for `OpenAI Developers` / `openai-developers` returned no installable result.
4. `OpenAI Platform` target discovery successfully returned:
   - organization: `Personal`;
   - project: `Default project`.
5. The secure setup action `start_api_key_setup` was accepted by the OpenAI Platform connector without a connector error.

These observations establish that Platform target discovery and the backend setup invocation path were operational during the diagnostic session. They do **not** by themselves prove that the user-visible widget rendered correctly.

## Diagnostic chronology

### Stage 1 — Original symptom

The expected interactive API-key setup UI did not appear during Launch Desk setup. Because the symptom appeared on more than one device surface, a device-only explanation became less likely.

### Stage 2 — Initial registration hypothesis

A permission-registry lookup for `OpenAI Developers` returned `not_installed`. This temporarily raised Plugin/App registration to the top of the suspect list.

### Stage 3 — Component inventory

The Human Owner then provided the OpenAI Developers bundle view. It showed the underlying OpenAI Platform app connected, the local-confirmation MCP component present, and all five visible skills enabled.

This evidence materially changed the diagnosis. The prior `not_installed` result could no longer be interpreted as evidence that the entire OpenAI Developers bundle was missing.

### Stage 4 — Platform verification

Direct Platform target discovery succeeded and returned the expected Personal organization and Default project. This substantially reduced the likelihood of a general OpenAI Platform authentication or target-resolution failure.

### Stage 5 — Secure setup invocation

The secure API-key setup action was invoked diagnostically and the connector accepted the request without an error. No conclusion was made from this alone about user-visible rendering.

## Current diagnostic matrix

| Layer | Current status | Evidence / interpretation |
|---|---|---|
| OpenAI Developers bundle presence | `PASS` | Visible bundle with skills/components present |
| OpenAI Platform app connection | `PASS` | UI shows connected; permission lookup resolves app |
| OpenAI Developers skills | `PASS` | Five visible skills enabled |
| Local confirmation MCP component | `PRESENT` | `Openai-api-key-local-confirmation` visible |
| Platform authentication / target discovery | `PASS` | Personal org and Default project returned |
| Secure setup backend invocation | `PASS` | `start_api_key_setup` accepted without connector error |
| Interactive widget rendering | `UNRESOLVED` | Backend acceptance does not prove client rendering |
| Surface/client compatibility | `PRIMARY_SUSPECT` | Cross-surface behavior requires controlled A/B test |
| API-key creation | `NOT_TESTED` | No need to create another key for rendering diagnosis |
| Launch Desk OpenAI API call | `NOT_PERFORMED` | No evidence of model invocation in this diagnostic |
| API model cost from this diagnostic | `NONE_OBSERVED` | No model API call was performed as part of this test |

## Revised hypothesis ranking

1. **Surface-specific widget rendering / client compatibility** — current leading unresolved hypothesis.
2. **Interactive widget ↔ client handoff after backend acceptance** — closely related and still unresolved.
3. **Transient account/session/feature-state mismatch** — possible, but not yet isolated.
4. **OpenAI Platform authentication failure** — substantially reduced by successful target discovery.
5. **Organization/project target failure** — substantially reduced by successful resolution.
6. **Missing local download / executable / SDK** — no supporting evidence from the current component inventory.
7. **Missing OpenAI Developers bundle** — contradicted by the visible installed bundle/component state.

## Required next experiment

Perform a controlled A/B rendering test without creating additional API keys unless creation becomes necessary later.

### A — Current ChatGPT / Atlas surface

Invoke the same OpenAI API Key Setup path and record whether the secure interactive widget becomes visible.

### B — Standard ChatGPT Web full-page new conversation

Invoke the same OpenAI API Key Setup path under otherwise equivalent account/plugin conditions and record whether the same widget becomes visible.

### Interpretation

- **B renders, A does not:** strongly supports a surface/client renderer issue.
- **Neither renders while backend setup invocation succeeds:** supports a broader widget/handoff, account-feature, or session-state issue rather than Launch Desk itself.
- **Both render:** treat the original failure as potentially transient until reproduced again.

For each run, record surface, account state, plugin/app connection state, whether backend setup invocation was accepted, whether the widget became visible, and whether any user action was actually completed.

## Safety and resource controls

1. Do not create repeated diagnostic API keys merely to test rendering.
2. Do not make a paid/model API request until the credential path is intentionally validated and Launch Desk is ready for an explicit API-call test.
3. Do not download third-party executables, browser extensions, SDK bundles, or unofficial OpenAI key tools without independent need and provenance review.
4. Reuse existing diagnostic evidence where possible instead of repeating equivalent calls.
5. Mark contradictory states explicitly rather than forcing premature convergence.

## Governance disposition

This document records an observed integration incident and its current evidence state. It is **not** a canonical claim that ChatGPT, OpenAI Platform, Atlas, the OpenAI Developers plugin, or Launch Desk contains a confirmed product defect.

The current evidence supports a bounded statement only: the expected secure setup UI was observed missing during the reported workflow, while several backend/component checks succeeded.

Any future promotion of this incident into a canonical architecture conclusion, product-defect claim, governance rule, or permanent compatibility statement requires fresh evidence review. Under the AION dual-review rule, Human Owner approval and ChatGPT architecture/evidence/provenance review remain independent; neither one substitutes for the other.

## Update conditions

Update this incident record when one of the following occurs:

- the A/B surface test is completed;
- the widget failure is reproduced under controlled conditions;
- the widget renders successfully on one surface but not another;
- an official OpenAI source identifies a relevant known limitation or incident;
- a successful API-key creation test becomes necessary and is explicitly authorized;
- Launch Desk performs its first intentional OpenAI API request and the result can be separated from the widget incident.
