
from __future__ import annotations
import hashlib, json
from .models import OperationRequest

def canonical_request_hash(request: OperationRequest) -> str:
    record = {
        "request_id": request.request_id,
        "source_type": request.source_type.value,
        "action": request.action.value,
        "target": request.target,
        "environment": request.environment.value,
        "authorization": request.authorization.value,
        "destructive": request.destructive,
        "network_access": request.network_access,
        "description": request.description,
        "metadata": dict(sorted(request.metadata.items())),
    }
    raw = json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
