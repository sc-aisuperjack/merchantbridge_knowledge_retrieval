"""Usage:
python -m mbfs ask "What's your chargeback fee?" [--llm] [--json]
python -m mbfs eval [--llm]
"""

import argparse
import json
import os
from pathlib import Path

from mbfs.answer import ask
from mbfs.evaluate import evaluate, report
from mbfs.ingest import load_corpus
from mbfs.search import Index

ROOT = Path(__file__).parent.parent


def openai_llm():
    from dotenv import load_dotenv
    from openai import OpenAI, OpenAIError

    load_dotenv(ROOT / ".env")
    try:
        client = OpenAI()  # reads OPENAI_API_KEY
    except OpenAIError:
        raise SystemExit("OPENAI_API_KEY is not set. Copy .env.example to .env and add your key.")
    model = os.getenv("OPENAI_MODEL") or "gpt-5.4-mini"

    def complete(prompt):
        response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content

    return complete


def main():
    parser = argparse.ArgumentParser(prog="mbfs")
    commands = parser.add_subparsers(dest="command", required=True)
    ask_cmd = commands.add_parser("ask")
    ask_cmd.add_argument("question")
    ask_cmd.add_argument("--llm", action="store_true", help="write the answer with OpenAI (key in .env)")
    ask_cmd.add_argument("--json", action="store_true")
    eval_cmd = commands.add_parser("eval")
    eval_cmd.add_argument("--llm", action="store_true", help="LLM writes answers and judges key facts")
    args = parser.parse_args()

    index = Index(load_corpus(ROOT / "corpus"))

    if args.command == "eval":
        llm = openai_llm() if args.llm else None
        results = evaluate(index, ROOT / "eval" / "tricky_queries.json", llm)
        (ROOT / "eval" / "report.md").write_text(report(results), encoding="utf-8")
        print(report(results))
        return

    answer = ask(index, args.question, openai_llm() if args.llm else None)
    if args.json:
        print(json.dumps(answer.to_dict(), indent=2, ensure_ascii=False))
        return
    conf = answer.confidence
    print(f"[{answer.outcome}] confidence {conf['score']} ({conf['level']}), not found: {conf['not_found']}")
    print(f"\n{answer.text}\n")
    for i, (chunk, line) in enumerate(answer.citations, 1):
        print(f"[{i}] {chunk.source} line {line.line_no} (chars {line.start}-{line.end}): {chunk.title}")


if __name__ == "__main__":
    main()
