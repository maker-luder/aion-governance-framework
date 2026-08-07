# Security boundary

Offline tests use no GPU, model, Ollama, cloud API, crawler, weight file, private key, formal memory, or tool activation. Runtime manifests allow only explicit loopback endpoints. Writes are new-file-only and reject duplicates and unsafe relative paths. Canonical writeback, merge, approval, memory writeback, permission inheritance and privilege escalation are denied by default.
