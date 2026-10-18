import copy
import json
import time


class ResponseCache:
    """In-memory cache of completions keyed by request contents."""

    def __init__(self, max_entries=512, ttl=None):
        self.max_entries = max_entries
        self.ttl = ttl
        self._entries = []
        self.hits = 0
        self.misses = 0

    def make_key(self, provider, model, messages, params):
        return json.dumps(
            {
                "provider": provider,
                "model": model,
                "messages": [m.to_dict() for m in messages],
                "params": params,
            }
        )

    def _expired(self, stored_at):
        return self.ttl is not None and time.time() - stored_at > self.ttl

    def get(self, key):
        for stored_key, value, stored_at in self._entries:
            if stored_key == key:
                if self._expired(stored_at):
                    self.misses += 1
                    return None
                self.hits += 1
                return copy.deepcopy(value)
        self.misses += 1
        return None

    def set(self, key, value):
        self._entries = [e for e in self._entries if e[0] != key]
        self._entries.append((key, copy.deepcopy(value), time.time()))
        while len(self._entries) > self.max_entries:
            self._entries.pop(0)

    def clear(self):
        self._entries = []
        self.hits = 0
        self.misses = 0

    def __len__(self):
        return len(self._entries)
