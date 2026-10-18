from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Message:
    role: str
    content: str

    def to_dict(self):
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data):
        return cls(role=data["role"], content=data["content"])


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total(self):
        return self.input_tokens + self.output_tokens


@dataclass
class Completion:
    text: str
    model: str
    provider: str
    usage: Usage = field(default_factory=Usage)
    raw: Dict[str, Any] = field(default_factory=dict)
    finish_reason: Optional[str] = None


def coerce_messages(messages):
    """Accept a string, dicts, or Message objects and return a list of Messages."""
    if isinstance(messages, str):
        return [Message("user", messages)]
    out = []
    for m in messages:
        if isinstance(m, Message):
            out.append(m)
        elif isinstance(m, dict):
            out.append(Message.from_dict(m))
        else:
            raise TypeError(f"cannot convert {type(m).__name__} to Message")
    return out
