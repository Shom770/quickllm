from abc import ABC, abstractmethod

from ..config import get_api_key
from ..http import HTTPClient


class Provider(ABC):
    name = ""
    base_url = ""
    chat_path = ""
    models_path = "models"

    def __init__(self, api_key=None, http=None):
        self._api_key = api_key
        self._http = http

    @property
    def api_key(self):
        return self._api_key or get_api_key(self.name)

    def http(self):
        if self._http is not None:
            return self._http
        return HTTPClient(self.base_url, headers=self.headers())

    @abstractmethod
    def headers(self):
        """Auth and content headers for this provider."""

    @abstractmethod
    def build_payload(self, messages, model, **params):
        """Turn Messages into a provider request body."""

    @abstractmethod
    def parse_response(self, data, model):
        """Turn a provider response body into a Completion."""

    def complete(self, messages, model, **params):
        payload = self.build_payload(messages, model, **params)
        data = self.http().post(self.chat_path, payload)
        return self.parse_response(data, model)

    def list_models(self):
        data = self.http().get(self.models_path)
        return [m["id"] for m in data.get("data", [])]
