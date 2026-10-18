import argparse
import sys

from .batch import read_prompts, run_batch
from .client import Client
from .errors import QuickLLMError
from .tasks import summarize_file


def build_parser():
    parser = argparse.ArgumentParser(prog="quickllm", description="Talk to chat LLM APIs.")
    parser.add_argument("--provider", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--no-validate", action="store_true", help="skip model validation")
    sub = parser.add_subparsers(dest="command", required=True)

    ask = sub.add_parser("ask", help="ask a single question")
    ask.add_argument("prompt")
    ask.add_argument("--system", default=None)

    batch = sub.add_parser("batch", help="run one prompt per line of a file")
    batch.add_argument("path")
    batch.add_argument("--system", default=None)

    sub.add_parser("models", help="list available models")

    summ = sub.add_parser("summarize", help="summarize a text file")
    summ.add_argument("path")
    return parser


def make_client(args):
    return Client(provider=args.provider, model=args.model, validate_models=not args.no_validate)


def main(argv=None, client_factory=make_client):
    args = build_parser().parse_args(argv)
    try:
        client = client_factory(args)
        if args.command == "ask":
            print(client.ask(args.prompt, system=args.system))
        elif args.command == "batch":
            prompts = read_prompts(args.path)
            for prompt, answer in zip(prompts, run_batch(client, prompts, system=args.system)):
                print(f"> {prompt}\n{answer}\n")
        elif args.command == "models":
            for model in sorted(client.models()):
                print(model)
        elif args.command == "summarize":
            print(summarize_file(client, args.path))
    except QuickLLMError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if client.history:
        print(f"[{client.total_tokens()} tokens, ${client.total_cost():.4f}]", file=sys.stderr)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
