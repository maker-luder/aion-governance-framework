from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from .models import ExecutionGrant, GenerationRequest


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reasons: tuple[str, ...]
    request_fingerprint: str
    grant_id: str
    canonical_effect: str = "NONE"


@dataclass(frozen=True, slots=True)
class MediaExecutionPolicy:
    allowed_hosts: tuple[str, ...]
    max_prompt_chars: int = 4_000
    require_human_approval: bool = True

    def evaluate(self, request: GenerationRequest, grant: ExecutionGrant, *, endpoint: str) -> PolicyDecision:
        reasons: list[str] = []
        host = (urlparse(endpoint).hostname or "").lower()
        if host not in {item.lower() for item in self.allowed_hosts}:
            reasons.append("ENDPOINT_HOST_NOT_ALLOWLISTED")
        if request.provider not in grant.approved_providers:
            reasons.append("PROVIDER_NOT_GRANTED")
        if request.media_kind not in grant.approved_media:
            reasons.append("MEDIA_KIND_NOT_GRANTED")
        if not grant.network_egress:
            reasons.append("NETWORK_EGRESS_NOT_GRANTED")
        if self.require_human_approval and not grant.human_approved:
            reasons.append("HUMAN_APPROVAL_REQUIRED")
        if len(request.prompt) > self.max_prompt_chars:
            reasons.append("PROMPT_LIMIT_EXCEEDED")
        return PolicyDecision(
            allowed=not reasons,
            reasons=tuple(reasons),
            request_fingerprint=request.fingerprint,
            grant_id=grant.grant_id,
        )

    def authorize(self, request: GenerationRequest, grant: ExecutionGrant, *, endpoint: str) -> PolicyDecision:
        decision = self.evaluate(request, grant, endpoint=endpoint)
        if not decision.allowed:
            raise PermissionError("media execution denied: " + ",".join(decision.reasons))
        return decision
