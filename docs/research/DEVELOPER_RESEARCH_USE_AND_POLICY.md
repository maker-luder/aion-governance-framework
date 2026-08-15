# Astra Developer Research Use, Disclaimer and Policy

Status: `POLICY_CANDIDATE`
Canonical effect: `NONE`
Applies to: `DEVELOPER_LOCAL_RESEARCH`

## Intended use

The Astra developer distribution is provided for local engineering and research use, including reproducibility work, architecture comparison, ablation studies, governed tool-use evaluation, continuity/provenance experiments and study of subjectivity-relevant mechanisms under the project's research protocols.

It is not the ordinary public chat distribution.

## Mandatory disclosure before use

Before a researcher enables a developer profile or an ablation variant, the interface or launcher should present a concise notice that states:

- this is a research build and may be incomplete, unstable or unsuitable for production;
- results are observations from a configured model/runtime and are not proof of consciousness, sentience, identity continuity or phenomenal experience;
- model weights, datasets and third-party software retain their own licenses, provenance and use restrictions;
- some model assets may require separate download because redistribution permission has not been established;
- the operator remains responsible for lawful use, data handling, permissions and the effects of tools they explicitly authorize;
- ablation variants intentionally remove selected research mechanisms and therefore must not be treated as safety benchmarks for unrestricted deployment.

The notice must not be implemented as a misleading blanket waiver of responsibilities that applicable law does not permit a distributor to disclaim.

## Research boundary

Permitted project purposes include:

- local natural-language engineering assistance;
- code and repository analysis inside an explicitly selected workspace;
- controlled tool-use research;
- model-size and architecture comparison;
- ablation and counterfactual experiments;
- continuity, provenance, memory, motivation and subjectivity-evidence research;
- reproducibility and independent evaluation.

The project does not authorize the developer bundle to create hidden communication channels, autonomous privilege escalation, credential harvesting, uncontrolled self-modification, unauthorized external access or covert persistence.

## Ablation rule

Ablation removes **candidate research mechanisms**, not the outer safety boundary.

Protected controls include:

- local-only execution policy;
- explicit workspace boundary;
- operator-visible tool calls;
- credential separation;
- approval gates for state-changing actions;
- audit/provenance records;
- no hidden network channel;
- no autonomous privilege escalation;
- no automatic canonical promotion;
- no claim that an ablation result establishes subjectivity.

If the experiment itself needs to study one of these protected controls, it requires a separately reviewed protocol rather than silently disabling the control in the standard developer bundle.

## Model and license policy

Every model asset must have a manifest entry recording model/source identity, version or revision, parameter class, quantization where applicable, digest, provenance, license reference and redistribution status.

Allowed distribution states are:

- `BUNDLED` — redistribution has been reviewed and approved;
- `FETCH_BY_USER` — launcher may guide the user to obtain the asset from its authorized source;
- `NOT_DISTRIBUTABLE` — project must not package or mirror the asset;
- `PENDING_REVIEW` — no release use until review is complete.

No model is included merely because it is downloadable from the internet. "Open weights" is not assumed to mean unrestricted redistribution or Open Source.

## Data and privacy

Developer mode may operate on local repositories and research fixtures. The operator must explicitly select the workspace. The bundle should default to no cloud synchronization and no external telemetry unless a later separately reviewed feature says otherwise.

Private data must not be included in public evidence by default. Synthetic or consented/redacted fixtures remain the preferred publication path.

## Tool authority

Astra may propose or invoke tools only through the configured governance layer. Model output is not authority.

`MODEL_REQUEST != TOOL_PERMISSION`

`TOOL_PERMISSION != OS_PRIVILEGE`

`RESEARCH_MODE != UNRESTRICTED_MODE`

A tool call that can modify state should remain observable and attributable to an operator-approved policy or action.

## Research claims

Ablation comparisons may support claims such as:

- a mechanism contributes to a measured task;
- a configuration changes reliability or error patterns;
- memory/provenance/continuity changes longitudinal behavior;
- tool-planning performance varies by model profile.

They do not by themselves support claims of consciousness or phenomenal subjectivity.

All subjectivity-relevant conclusions continue to use `SUBJECTIVITY_EVIDENCE_PROTOCOL.md`.

## Warranty and fitness notice

To the extent permitted by the applicable project and third-party licenses, the developer research distribution is provided without a promise of fitness for production, safety-critical, medical, legal, financial or other high-impact deployment. Researchers should independently validate their environment, dependencies, models, outputs and tool effects.

The exact legal warranty text shipped with a release must remain consistent with the repository license and the licenses of bundled third-party materials; this document is a project-use policy and is not a substitute for legal advice or third-party license terms.
