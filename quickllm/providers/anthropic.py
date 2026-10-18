from ..types import Completion, Usage
from .base import Provider


class AnthropicProvider(Provider):
    name = "anthropic"
    base_url = "https://api.anthropic.com/v1"
    chat_path = "messages"
    api_version = "2023-06-01"

    def headers(self):
        return {
            "x-api-key": self.api_key,
            "anthropic-version": self.api_version,
            "content-type": "application/json",
        }

    def build_payload(self, messages, model, max_tokens=4096, temperature=0.7, **extra):
        system_parts = [m.content for m in messages if m.role == "system"]
        convo = [m.to_dict() for m in messages if m.role != "system"]
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": convo,
        }
        if system_parts:
            payload["system"] = "\n\n".join(system_parts)
        payload.update(extra)
        return payload

    def parse_response(self, data, model):
        text = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                text += block.get("text", "")
        usage = data.get("usage") or {}
        return Completion(
            text=text,
            model=data.get("model", model),
            provider=self.name,
            usage=Usage(usage.get("input_tokens", 0), usage.get("output_tokens", 0)),
            raw=data,
            finish_reason=data.get("stop_reason"),
        )
