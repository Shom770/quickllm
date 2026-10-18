class QuickLLMError(Exception):
    """Base error for quickllm."""


class ConfigError(QuickLLMError):
    """Missing or invalid configuration (keys, models, providers)."""


class ProviderError(QuickLLMError):
    """A provider returned an error response."""

    def __init__(self, status, body, message=None):
        self.status = status
        self.body = body
        super().__init__(message or f"provider returned HTTP {status}: {body}")


class RateLimitError(ProviderError):
    """HTTP 429 from a provider."""
