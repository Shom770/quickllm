import re

from .types import Message

_WORD = re.compile(r"\w+|[^\w\s]")


def estimate_tokens(text):
    """Rough token estimate: words and punctuation, scaled for subword splits."""
    if not text:
        return 0
    pieces = _WORD.findall(text)
    return int(len(pieces) * 1.3) + 1


def estimate_messages_tokens(messages):
    total = 0
    for m in messages:
        total += 4 + estimate_tokens(m.content)
    return total


def count_tokens_exact(client, text, model=None):
    """Exact input-token count, as reported by the provider."""
    completion = client.complete([Message("user", text)], model=model, max_tokens=1, temperature=0)
    return completion.usage.input_tokens


def truncate_to_tokens(text, limit):
    words = text.split(" ")
    while words and estimate_tokens(" ".join(words)) > limit:
        words.pop()
    return " ".join(words)


def chunk_text(text, max_chars):
    chunks = []
    current = ""
    for paragraph in text.split("\n\n"):
        candidate = current + ("\n\n" if current else "") + paragraph
        if len(candidate) > max_chars and current:
            chunks.append(current)
            current = paragraph
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks
