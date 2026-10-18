import json
import os
from pathlib import Path

from .errors import ConfigError

DEFAULT_CONFIG_PATH = Path.home() / ".quickllm.json"

ENV_KEYS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
}

DEFAULT_MODELS = {
    "openai": "gpt-4o",
    "anthropic": "claude-opus-5-5",
    "openrouter": "openai/gpt-4o",
}


def config_path():
    return Path(os.environ.get("QUICKLLM_CONFIG", DEFAULT_CONFIG_PATH))


def load_config():
    path = config_path()
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"invalid config file {path}: {exc}") from exc


def get_setting(name, default=None):
    return load_config().get(name, default)


def get_api_key(provider):
    env_name = ENV_KEYS.get(provider)
    if env_name is None:
        raise ConfigError(f"unknown provider: {provider}")
    value = os.environ.get(env_name)
    if value:
        return value
    key = load_config().get("keys", {}).get(provider)
    if not key:
        raise ConfigError(f"no API key for {provider}; set {env_name} or add it to {config_path()}")
    return key


def default_model(provider):
    configured = get_setting("default_models", {}).get(provider)
    return configured or DEFAULT_MODELS[provider]


def default_provider():
    return get_setting("default_provider", "openai")
