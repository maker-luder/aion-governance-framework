"""Trusted-layer caller identity.

White paper AIR-08: request-body role/actor/authority fields have no
authorization effect. Only AuthContext constructed by the caller of the
service (the trusted layer) is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

PRINCIPAL_ROLES = frozenset(
    {
        "RESEARCH_OWNER",
        "AIR_SERVICE",
        "INSTANCE",
        "ASTRA_ASSISTANT",
        "SUCCESSOR",
        "EXTERNAL_AGENT",
        "UNAUTHENTICATED",
    }
)


@dataclass(frozen=True)
class AuthContext:
    principal: str
    roles: FrozenSet[str]

    def __post_init__(self) -> None:
        unknown = set(self.roles) - PRINCIPAL_ROLES
        if unknown:
            raise ValueError(f"unknown roles: {sorted(unknown)}")

    def has(self, role: str) -> bool:
        return role in self.roles


def ignore_body_role(body: dict | None) -> None:
    """Body roles are recorded only as untrusted claims; never used."""
    return None
