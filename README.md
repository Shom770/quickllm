# quickllm

A small wrapper around the OpenAI, Anthropic and OpenRouter chat APIs with one
interface, a response cache, conversation memory, batch helpers, cost tracking
and a tiny CLI.

```python
from quickllm import Client

client = Client(provider="anthropic", model="claude-sonnet-5-5")
print(client.ask("Give me three names for a houseplant shop"))
print(f"spent ${client.total_cost():.4f}")
```

## Keys

Set `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` or `OPENROUTER_API_KEY`, or put them
in `~/.quickllm.json`:

```json
{"keys": {"openai": "sk-...", "anthropic": "sk-ant-..."}, "default_provider": "openai"}
```

## CLI

```
quickllm ask "what's the capital of peru" --provider openai --model gpt-4o-mini
quickllm batch prompts.txt --provider openrouter --model openai/gpt-4o-mini
quickllm models --provider anthropic
quickllm summarize notes.md
```

## Development

```
python -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
```
