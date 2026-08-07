class LanguageLabError(Exception):
    """Base language-lab error."""


class ValidationError(LanguageLabError):
    """Input failed validation."""


class RegistryError(LanguageLabError):
    """Registry operation was rejected."""


class RuntimeFailure(LanguageLabError):
    """Local runtime request failed."""


class ArtifactExistsError(LanguageLabError):
    """A write would overwrite an existing artifact."""
