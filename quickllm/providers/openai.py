from ..types import Completion, Usage
from .base import Provider


class OpenAIProvider(Provider):
    name = "openai"
    base_url = "https://api.openai.com/v1"
    chat_path = "chat/completions"

    def headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def build_payload(self, messages, model, max_tokens=4096, temperature=0.7, **extra):
        payload = {
            "model": model,
            "messages": [m.to_dict() for m in messages],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        payload.update(extra)
        return payload

    def parse_response(self, data, model):
        choice = data["choices"][0]
        usage = data.get("usage") or {}
        return Completion(
            text=choice["message"].get("content") or "",
            model=data.get("model", model),
            provider=self.name,
            usage=Usage(usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)),
            raw=data,
            finish_reason=choice.get("finish_reason"),
        )
