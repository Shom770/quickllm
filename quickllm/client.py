from .cache import ResponseCache
from .config import default_model, default_provider
from .cost import estimate_cost
from .errors import ConfigError
from .providers import AnthropicProvider, OpenAIProvider, OpenRouterProvider
from .types import Message, coerce_messages

PROVIDERS = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "openrouter": OpenRouterProvider,
}


class Client:
    def __init__(
        self,
        provider=None,
        model=None,
        api_key=None,
        cache=None,
        use_cache=True,
        validate_models=True,
        http=None,
    ):
        self.provider_name = provider or default_provider()
        if self.provider_name not in PROVIDERS:
            raise ConfigError(f"unknown provider: {self.provider_name}")
        self.model = model or default_model(self.provider_name)
        self._api_key = api_key
        self._http = http
        self.use_cache = use_cache
        self.cache = cache if cache is not None else ResponseCache()
        self.validate_models = validate_models
        self.history = []

    def _provider(self):
        return PROVIDERS[self.provider_name](api_key=self._api_key, http=self._http)

    def models(self):
        return self._provider().list_models()

    def _check_model(self, model):
        if not self.validate_models:
            return
        if model not in self.models():
            raise ConfigError(f"model {model!r} is not available from {self.provider_name}")

    def complete(self, messages, model=None, **params):
        model = model or self.model
        messages = coerce_messages(messages)
        self._check_model(model)

        key = None
        if self.use_cache:
            key = self.cache.make_key(self.provider_name, model, messages, params)
            cached = self.cache.get(key)
            if cached is not None:
                return cached

        completion = self._provider().complete(messages, model, **params)
        if key is not None:
            self.cache.set(key, completion)
        self.history.append(completion)
        return completion

    def ask(self, prompt, system=None, **params):
        messages = []
        if system:
            messages.append(Message("system", system))
        messages.append(Message("user", prompt))
        return self.complete(messages, **params).text

    def total_cost(self):
        return sum(estimate_cost(c) for c in self.history)

    def total_tokens(self):
        return sum(c.usage.total for c in self.history)
