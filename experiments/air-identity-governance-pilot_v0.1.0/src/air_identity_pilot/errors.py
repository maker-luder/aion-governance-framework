class AirError(Exception):
    code = "air_error"


class AuthzError(AirError):
    code = "unauthorized"


class ConflictError(AirError):
    code = "conflict"


class NotFoundError(AirError):
    code = "not_found"


class SealedError(AirError):
    code = "sealed"


class ContinuityEndedError(AirError):
    code = "continuity_ended"


class IdempotencyConflictError(AirError):
    code = "idempotency_conflict"


class LeaseError(AirError):
    code = "lease_not_available"


class ValidationError(AirError):
    code = "validation_error"


class RoleBoundaryError(AirError):
    code = "role_boundary"
