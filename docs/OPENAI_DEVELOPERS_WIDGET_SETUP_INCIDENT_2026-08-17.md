# OpenAI Developers Secure API-Key Widget Setup Incident — 2026-08-17

> **RESEARCH-ONLY INCIDENT RECORD**
>
> - **Incident ID:** `AION-INC-2026-08-17-OPENAI-WIDGET-001`
> - **Branch:** `review/four-domain-research-materialization`
> - **Status:** `OPEN / SURFACE_DIVERGENCE_OBSERVED`
> - **Canonical effect:** `NONE`
> - **Scope:** ChatGPT OpenAI Developers / OpenAI Platform secure API-key setup path used during Launch Desk setup
> - **Main branch impact:** `NONE`
> - **Architecture change:** `NONE`

## Incident summary

During Launch Desk credential setup, the Human Owner observed that the interactive secure API-key setup interface did not appear as expected. A controlled A/B test was then performed across two ChatGPT surfaces.

The result was divergent:

- **A — current ChatGPT / Atlas surface:** backend secure-setup invocation was accepted, but the Human Owner reported that no interactive API-key widget became visible.
- **B — standard ChatGPT Web full-page new conversation:** the OpenAI Developers secure API-key setup card visibly rendered. A separate `Too many requests` access-limit dialog then appeared over the page.

This A/B result narrows the incident substantially. The evidence now supports a surface-dependent rendering difference more strongly than a missing Plugin/App installation, missing local download, general OpenAI Platform authentication failure, or missing organization/project target.

The evidence does **not** yet establish a confirmed Atlas product defect. Session state, transient feature delivery, access throttling, and other client-specific conditions remain possible confounders.

## Source attribution

### Human Owner observations

The Human Owner reported and visually demonstrated the following:

1. The expected secure API-key setup interface had failed to appear during the Launch Desk setup path.
2. A comparable absence had previously been observed on both mobile and desktop workflows, motivating a controlled surface test rather than assuming a device-only failure.
3. The OpenAI Developers bundle UI showed:
   - `OpenAI Platform` application — connected;
   - `Openai-api-key-local-confirmation` MCP server — present;
   - `Agents SDK` — enabled;
   - `Build ChatGPT App` — enabled;
   - `ChatGPT App Submission` — enabled;
   - `OpenAI API Troubleshooting` — enabled;
   - `OpenAI API Key Setup` — enabled.
4. During controlled test A on the current ChatGPT / Atlas surface, no secure API-key setup widget was visible after the backend setup action was invoked.
5. During controlled test B on standard ChatGPT Web, the secure API-key setup card visibly appeared.
6. During test B, a separate dialog appeared stating that too many requests had been made and that conversation access was temporarily limited, with a request to retry after several minutes.

The screenshots used for these observations were supplied in the ChatGPT conversation and are not embedded in this repository record.

The Human Owner suggested that the access-limit dialog may have been related to the high volume of preceding diagnostic attempts. That causal interpretation is recorded only as a hypothesis; the screenshot itself establishes the rate-limit/access-limit event, not its exact cause.

### ChatGPT diagnostic interpretation

ChatGPT first ranked Plugin/App registration as the leading suspect because `OpenAI Developers` returned `not_installed` when queried through the app-permission registry. After inspecting the actual bundle/component state, ChatGPT revised that interpretation: the `not_installed` response must not be treated as proof that the OpenAI Developers bundle itself is absent.

After the controlled A/B test, ChatGPT further revised the diagnosis. The standard ChatGPT Web surface successfully rendered the secure setup UI while the current ChatGPT / Atlas surface did not. The current leading interpretation is therefore a surface- or client-dependent rendering/handoff difference, with transient session/feature state still retained as an alternative explanation.

The `Too many requests` condition observed during B is treated as a secondary event because the secure setup card had already rendered behind the dialog. It therefore does not explain the original A-side failure to render.

### Connector/tool observations

The diagnostic tools returned the following operational evidence during the same investigation:

1. `OpenAI Platform` permission lookup returned a valid application record (`found`) and showed that it inherits the current default ChatGPT app permission setting.
2. A permission lookup using `OpenAI Developers` returned `not_installed`.
3. A standalone plugin-directory search for `OpenAI Developers` / `openai-developers` returned no installable result.
4. `OpenAI Platform` target discovery successfully returned:
   - organization: `Personal`;
   - project: `Default project`.
5. The secure setup action `start_api_key_setup` was accepted by the OpenAI Platform connector without a connector error during diagnostic invocation.

These observations establish that Platform target discovery and the backend setup invocation path were operational during the diagnostic session. They do **not** by themselves prove client-side rendering; that question was resolved separately through Human Owner visual observation in the A/B test.

## Diagnostic chronology

### Stage 1 — Original symptom

The expected interactive API-key setup UI did not appear during Launch Desk setup. Because similar behavior had been seen across more than one device workflow, a device-only explanation became less likely.

### Stage 2 — Initial registration hypothesis

A permission-registry lookup for `OpenAI Developers` returned `not_installed`. This temporarily raised Plugin/App registration to the top of the suspect list.

### Stage 3 — Component inventory

The Human Owner then provided the OpenAI Developers bundle view. It showed the underlying OpenAI Platform app connected, the local-confirmation MCP component present, and all five visible skills enabled.

This evidence materially changed the diagnosis. The prior `not_installed` result could no longer be interpreted as evidence that the entire OpenAI Developers bundle was missing.

### Stage 4 — Platform verification

Direct Platform target discovery succeeded and returned the expected Personal organization and Default project. This substantially reduced the likelihood of a general OpenAI Platform authentication or target-resolution failure.

### Stage 5 — Secure setup invocation

The secure API-key setup action was invoked diagnostically and the connector accepted the request without an error. No API key was intentionally created as part of this rendering test.

### Stage 6 — Controlled A test: current ChatGPT / Atlas surface

The same secure setup path was invoked on the current ChatGPT / Atlas conversation surface.

Observed result:

- backend invocation accepted: `PASS`;
- connector error: none observed;
- Human Owner visible widget result: `FAIL` — no interactive secure API-key setup card was visible.

This establishes a backend-pass / client-visible-render-fail observation for surface A.

### Stage 7 — Controlled B test: standard ChatGPT Web

The Human Owner opened a standard ChatGPT Web full-page new conversation and requested the same secure API-key setup flow without creating a key.

Observed result:

- OpenAI Developers secure API-key setup card: `VISIBLE / PASS`;
- an overlaid `Too many requests` dialog then appeared;
- no intentional API-key creation was completed as part of the test.

Because the secure setup card was already visible behind the dialog, the rate-limit/access-limit event is classified as a secondary condition rather than a rendering failure.

## A/B result

| Test | Surface | Backend setup accepted | Widget visible to Human Owner | Secondary condition | Result |
|---|---|---:|---:|---|---|
| A | Current ChatGPT / Atlas | `PASS` | `NO` | none needed to explain result | `RENDER FAIL` |
| B | Standard ChatGPT Web full-page new conversation | setup flow visibly opened | `YES` | `Too many requests` access-limit dialog | `RENDER PASS` |

### Bounded interpretation

The A/B divergence is consistent with a surface/client-specific rendering or handoff difference.

It is **not yet sufficient** to assert any of the following as fact:

- Atlas contains a confirmed product defect;
- the behavior is permanent;
- every Atlas session will reproduce it;
- every standard ChatGPT Web session will render successfully;
- the `Too many requests` event caused or was caused by the widget incident;
- Launch Desk itself is defective.

## Current diagnostic matrix

| Layer | Current status | Evidence / interpretation |
|---|---|---|
| OpenAI Developers bundle presence | `PASS` | Visible bundle with skills/components present |
| OpenAI Platform app connection | `PASS` | UI shows connected; permission lookup resolves app |
| OpenAI Developers skills | `PASS` | Five visible skills enabled |
| Local confirmation MCP component | `PRESENT` | `Openai-api-key-local-confirmation` visible |
| Platform authentication / target discovery | `PASS` | Personal org and Default project returned |
| Secure setup backend invocation | `PASS` | `start_api_key_setup` accepted without connector error |
| Widget rendering — Atlas/current surface | `FAIL_OBSERVED` | Backend accepted; Human Owner saw no widget |
| Widget rendering — standard ChatGPT Web | `PASS_OBSERVED` | Secure setup card visibly rendered |
| Surface/client compatibility hypothesis | `SUPPORTED_BY_A_B` | Controlled divergence observed; defect status not yet proven |
| Rate/access limit during B | `SECONDARY_OBSERVED` | Dialog appeared after widget was already visible |
| API-key creation | `NOT_COMPLETED_IN_TEST` | Rendering test did not require intentional key creation |
| Launch Desk OpenAI API call | `NOT_PERFORMED` | No evidence of model invocation in this diagnostic |
| API model cost from this diagnostic | `NONE_OBSERVED` | No model API call was performed as part of this test |

## Revised hypothesis ranking

1. **Surface-specific widget rendering / client compatibility** — now directly supported by the controlled A/B divergence.
2. **Transient surface session / feature-delivery state** — remains plausible and should be distinguished from a persistent renderer defect.
3. **Interactive widget ↔ client handoff condition specific to Atlas/current surface** — plausible mechanism class, not yet isolated.
4. **Temporary access throttling / request limiting** — observed during B, but currently secondary because B rendered successfully before/behind the dialog.
5. **OpenAI Platform authentication failure** — strongly reduced by successful target discovery.
6. **Organization/project target failure** — strongly reduced by successful resolution.
7. **Missing local download / executable / SDK** — no supporting evidence from the component inventory.
8. **Missing OpenAI Developers bundle** — contradicted by the visible installed bundle/component state.

## Next experiment

Do **not** immediately repeat the same calls while the standard ChatGPT Web surface is showing an access-limit condition.

After the temporary access limitation clears, perform at most one low-frequency reproduction check per surface if further evidence is needed:

1. Re-run A once on the current ChatGPT / Atlas surface.
2. Re-run B once on standard ChatGPT Web.
3. Record whether the A/B divergence persists.
4. Do not create additional API keys merely to test rendering.

If A repeatedly fails while B repeatedly succeeds under comparable session conditions, confidence in a persistent surface-specific compatibility problem increases. If A later renders successfully, classify the incident as transient or session-dependent unless further evidence supports a stable defect.

## Safety and resource controls

1. Do not create repeated diagnostic API keys merely to test rendering.
2. Do not make a paid/model API request until the credential path is intentionally validated and Launch Desk is ready for an explicit API-call test.
3. Do not download third-party executables, browser extensions, SDK bundles, or unofficial OpenAI key tools without independent need and provenance review.
4. Reuse existing diagnostic evidence where possible instead of repeating equivalent calls.
5. Mark contradictory states explicitly rather than forcing premature convergence.
6. When rate/access limits appear, stop repeated probing and allow the service to recover before any further controlled reproduction attempt.

## Governance disposition

This document records an observed integration incident and its current evidence state. It is **not** a canonical claim that ChatGPT, OpenAI Platform, Atlas, the OpenAI Developers plugin, or Launch Desk contains a confirmed product defect.

The current evidence supports a bounded statement: the secure setup backend path was operational, the expected widget was not visible on the tested current ChatGPT / Atlas surface, and the same class of secure setup UI did render on the tested standard ChatGPT Web surface. A separate temporary access-limit event occurred during the successful Web rendering test.

Any future promotion of this incident into a canonical architecture conclusion, product-defect claim, governance rule, or permanent compatibility statement requires fresh evidence review. Under the AION dual-review rule, Human Owner approval and ChatGPT architecture/evidence/provenance review remain independent; neither one substitutes for the other.

## Update conditions

Update this incident record when one of the following occurs:

- the A/B surface test is repeated after the access-limit condition clears;
- the Atlas/current-surface rendering failure is reproduced under controlled conditions;
- Atlas/current surface renders successfully in a later controlled test;
- an official OpenAI source identifies a relevant known limitation or incident;
- a successful API-key creation test becomes necessary and is explicitly authorized;
- Launch Desk performs its first intentional OpenAI API request and the result can be separated from the widget incident.
