"""Per-million-token prices in USD. Illustrative; check provider pricing pages."""

PRICING = {
    ("openai", "gpt-4o-mini"): (0.15, 0.60),
    ("openai", "gpt-4o"): (2.50, 10.00),
    ("anthropic", "claude-haiku-5-5"): (1.00, 5.00),
    ("anthropic", "claude-sonnet-5-5"): (3.00, 15.00),
    ("anthropic", "claude-opus-5-5"): (15.00, 75.00),
    ("openrouter", "openai/gpt-4o-mini"): (0.15, 0.60),
    ("openrouter", "openai/gpt-4o"): (2.50, 10.00),
}


def price_for(provider, model):
    matches = [
        (len(m), prices)
        for (p, m), prices in PRICING.items()
        if p == provider and model.startswith(m)
    ]
    if not matches:
        return None
    matches.sort(reverse=True)
    return matches[0][1]


def estimate_cost(completion):
    prices = price_for(completion.provider, completion.model)
    if prices is None:
        return 0.0
    input_price, output_price = prices
    return (
        completion.usage.input_tokens * input_price
        + completion.usage.output_tokens * output_price
    ) / 1_000_000
