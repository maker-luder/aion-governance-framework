# DeepSeek Harness Adapter Profile v0.1.0

## Pinned upstream

```text
UPSTREAM_REPOSITORY = deepseek-ai/deepseek-harness
UPSTREAM_REF = b150a551b8d465e31e418e1b2eaf5e79bbb7d28e
UPSTREAM_RELEASE_LABEL = dsh@0.1.1-rc.2
UPSTREAM_STATE = DEVELOPER_PREVIEW
```

The pin is an interoperability reference, not a vendored dependency and not an endorsement of upstream stability.

## Upstream concepts represented

The profile is designed around the current DSH plugin architecture: model adapter, tool registry, session log, agent loop, filesystem/sandbox, storage, subagents, teams, and UI may be composed as plugins/services.

The AION/Astra contract intentionally abstracts those into substrate capabilities. Future harnesses may implement the same contract without using DSH.

## Event admission

The adapter accepts already-captured durable DSH session-event objects only. It does not connect to a DSH process.

Admitted durable families:

```text
turn/*
step/*
user/message
assistant/*
tool/*
```

Rejected as durable evidence:

```text
agent/*
llm/stream
tools/*
other transient/live extension points
```

This prevents a transient extension callback from being mislabeled as a durable session fact.

## Payload handling

Raw payload values are not copied into normalized trajectory evidence. The adapter records:

- payload SHA-256;
- sorted payload-key names;
- event type;
- event order;
- session binding.

If the provider payload exposes a key named `reasoning`, `reasoning_content`, or `analysis`, the adapter labels visibility as `PROVIDER_EXPOSED_ONLY`.

It does not claim complete hidden chain-of-thought.

`PROVIDER_EXPOSED_REASONING != COMPLETE_INTERNAL_COGNITION`

## Experimental DSH surfaces

Agent Teams and other developer-preview surfaces may change upstream. AION/Astra therefore treat the pinned profile as an inspection target rather than a production runtime dependency.

No automatic upstream tracking is performed.

## Execution status

```text
DSH_IMPORT = NO
DSH_INSTALL = NO
DSH_PROCESS_LAUNCH = NO
MODEL_EXECUTION = FALSE
SUBAGENT_EXECUTION = FALSE
NETWORK_ACCESS = FALSE
PLUGIN_MUTATION = FALSE
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
```
