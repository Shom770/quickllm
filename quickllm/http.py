import time

import requests

from .errors import ProviderError, RateLimitError

DEFAULT_TIMEOUT = 600


def _to_error(resp):
    try:
        body = resp.json()
    except ValueError:
        body = resp.text
    if resp.status_code == 429:
        return RateLimitError(resp.status_code, body)
    return ProviderError(resp.status_code, body)


class HTTPClient:
    def __init__(self, base_url, headers=None, timeout=DEFAULT_TIMEOUT, max_retries=3, backoff=1.0):
        self.base_url = base_url
        self.headers = dict(headers or {})
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff = backoff

    def _session(self):
        session = requests.Session()
        session.headers.update(self.headers)
        return session

    def url_for(self, path):
        return self.base_url.rstrip("/") + "/" + path.lstrip("/")

    def request(self, method, path, json_body=None):
        url = self.url_for(path)
        last_error = None
        for attempt in range(self.max_retries + 1):
            session = self._session()
            try:
                resp = session.request(method, url, json=json_body, timeout=self.timeout)
            except requests.RequestException as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(self.backoff)
                continue
            if resp.status_code >= 400:
                last_error = _to_error(resp)
                if attempt < self.max_retries:
                    time.sleep(self.backoff)
                continue
            return resp.json()
        raise last_error

    def get(self, path):
        return self.request("GET", path)

    def post(self, path, body):
        return self.request("POST", path, body)
