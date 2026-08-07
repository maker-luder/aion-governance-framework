# Security boundary

- Localhost HTTP is the only permitted Ollama endpoint.
- No model pull, download, shell command construction, cloud API, crawler, or telemetry.
- Model files are read and hashed; no weight writer or adapter merger exists.
- Artifacts use create-new semantics and cannot silently overwrite a run/report.
- Dataset coding fields are metadata only; this phase does not execute generated code.
- Candidate results cannot write canonical documents, production memory, or tool permissions.

