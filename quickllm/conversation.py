from .tokens import estimate_messages_tokens
from .types import Message


class Conversation:
    """Keeps chat history and trims the oldest turns to fit a context budget."""

    def __init__(self, client, system=None, max_context_tokens=8000, **params):
        self.client = client
        self.system = system
        self.max_context_tokens = max_context_tokens
        self.params = params
        self.messages = []

    def _window(self):
        history = list(self.messages)
        while len(history) > 1 and estimate_messages_tokens(history) > self.max_context_tokens:
            history.pop(0)
        return history

    def send(self, text):
        self.messages.append(Message("user", text))
        outgoing = self._window()
        if self.system:
            outgoing = [Message("system", self.system)] + outgoing
        completion = self.client.complete(outgoing, **self.params)
        self.messages.append(Message("assistant", completion.text))
        return completion.text

    def reset(self):
        self.messages = []

    def transcript(self):
        out = ""
        for m in self.messages:
            out += f"{m.role}: {m.content}\n"
        return out
