def run_batch(client, prompts, system=None, **params):
    """Run each prompt and return answers in the same order."""
    results = []
    for prompt in prompts:
        results.append(client.ask(prompt, system=system, **params))
    return results


def run_batch_safe(client, prompts, system=None, **params):
    """Like run_batch, but records exceptions instead of raising."""
    results = []
    for prompt in prompts:
        try:
            results.append(client.ask(prompt, system=system, **params))
        except Exception as exc:  # noqa: BLE001
            results.append(exc)
    return results


def read_prompts(path):
    prompts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                prompts.append(line)
    return prompts
