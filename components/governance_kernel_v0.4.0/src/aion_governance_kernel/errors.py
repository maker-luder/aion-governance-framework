
class GovernanceKernelError(Exception):
    """Base exception for controlled kernel failures."""

class InputValidationError(GovernanceKernelError):
    pass

class RiskEvaluationError(GovernanceKernelError):
    pass

class AuditDatabaseError(GovernanceKernelError):
    pass

class SchemaVersionError(AuditDatabaseError):
    pass
