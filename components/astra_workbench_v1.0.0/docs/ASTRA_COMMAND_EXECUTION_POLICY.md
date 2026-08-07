# Command Execution Policy

All commands use explicit argv and `shell=False`.

Allowed families are local Python scripts, pytest, mypy, coverage, compileall, build, offline pip with `--no-index --no-deps`, JSON tooling, and read-only git status/diff. Network transfer, cloud CLIs, push/publish, service/system mutation and shell metacharacters are rejected.

Execution has a candidate-scoped working directory, sanitized environment, timeout, process-tree termination, bounded output, return code, result hash and append-only audit.
