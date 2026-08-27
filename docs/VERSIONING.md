# Versioning

The repository uses experimental pre-1.0 semantics for current research components unless a component declares a narrower policy in its own metadata.

- `REPOSITORY_VERSION`: repository/release identity; not a scientific maturity claim.
- `COMPONENT_VERSION`: the version in a component-local `pyproject.toml`.
- `SCHEMA_VERSION`: the version carried by an individual JSON Schema or record.
- `RESEARCH_PROTOCOL_VERSION`: a protocol or study-design identifier.

These values are distinct. `VERSION_NUMBER != MATURITY`, and a compatibility change must be documented in `CHANGELOG.md` with affected component/schema/protocol scope.

A `1.0` designation requires a separately governed readiness decision; elapsed time, CI success, or documentation volume is insufficient.
