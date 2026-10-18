"""quickllm: one small interface for several chat-completion providers."""

from .client import Client, PROVIDERS
from .conversation import Conversation
from .errors import ConfigError, ProviderError, QuickLLMError, RateLimitError
from .types import Completion, Message, Usage

__version__ = "0.3.1"

__all__ = [
    "Client",
    "Completion",
    "ConfigError",
    "Conversation",
    "Message",
    "PROVIDERS",
    "ProviderError",
    "QuickLLMError",
    "RateLimitError",
    "Usage",
]
