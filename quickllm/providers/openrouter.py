from .openai import OpenAIProvider


class OpenRouterProvider(OpenAIProvider):
    name = "openrouter"
    base_url = "https://openrouter.ai/api/v1"
    chat_path = "chat/completions"

    app_url = "https://github.com/quickllm/quickllm"
    app_title = "quickllm"

    def headers(self):
        headers = super().headers()
        headers["HTTP-Referer"] = self.app_url
        headers["X-Title"] = self.app_title
        return headers
