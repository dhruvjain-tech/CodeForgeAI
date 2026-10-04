class LLMError(Exception):
    """Base exception for LLM errors."""


class LLMProviderUnavailableError(LLMError):
    """Raised when an LLM provider is unavailable."""


class LLMRequestError(LLMError):
    """Raised when an LLM request fails."""


class LLMConfigurationError(LLMError):
    """Raised when LLM configuration is invalid."""