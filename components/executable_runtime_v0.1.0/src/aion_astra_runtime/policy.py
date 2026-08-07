"""Fail-closed runtime boundaries."""

from __future__ import annotations

from pathlib import Path, PurePath
from urllib.parse import urlparse

from .errors import PolicyDenied
from .models import NetworkPolicy, TaskSpec


ALLOWED_TOOLS = frozenset({"list_files", "read_text", "write_candidate", "sha256_candidate", "complete"})


def relative_path(value: str) -> str:
    pure = PurePath(value)
    if not value or pure.is_absolute() or ".." in pure.parts or value.startswith(("\\\\", "//")):
        raise PolicyDenied("absolute, traversal, blank, or UNC path rejected")
    return str(Path(*pure.parts)).replace("\\", "/")


def validate_task_paths(task: TaskSpec) -> None:
    for value in (*task.input_paths, task.output_path):
        relative_path(value)
    if task.output_path in task.input_paths:
        raise PolicyDenied("output_path cannot overwrite an input")


def validate_endpoint(url: str, policy: NetworkPolicy) -> None:
    parsed = urlparse(url)
    if policy is NetworkPolicy.OFFLINE:
        raise PolicyDenied("network policy is OFFLINE")
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise PolicyDenied("only loopback HTTP is admitted")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise PolicyDenied("endpoint credentials, query and fragment are rejected")


def deny_privileged_operation(operation: str) -> None:
    if operation in {"canonical_write", "identity_mutation", "memory_write", "deployment", "privilege_escalation"}:
        raise PolicyDenied(f"{operation} is not admitted by this runtime candidate")

