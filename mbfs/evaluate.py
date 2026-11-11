"""Run eval/tricky_queries.json and build a short markdown report.

Without an LLM this measures what the retrieval layer controls: did it find the documents a good
answer needs, did it cite them, and did it answer or refuse. With an LLM it also asks the model to
judge which of each query's key facts the answer states.
"""

import json
import re
from datetime import date
from pathlib import Path

from mbfs.answer import ask


def evaluate(index, queries_path, llm=None):
    data = json.loads(Path(queries_path).read_text(encoding="utf-8"))
    today = date.fromisoformat(data["dataset"]["reference_date"])
    results = []
    for q in data["queries"]:
        answer = ask(index, q["query"], llm, today)
        docs = {s["path"].removeprefix("corpus/"): s["role"] for s in q["source_documents"]}
        primary = {d for d, role in docs.items() if role == "primary"}
        top5 = {c.source for c, _ in index.search(q["query"], k=5)}
        cited = [c.source for c, _ in answer.citations]
        precision = None
        if cited:
            precision = sum(docs.get(s) in ("primary", "supporting") for s in cited) / len(cited)
        facts = None
        if llm:
            facts = 0.0 if answer.outcome == "refused" else judge(llm, answer.text, q["key_facts"])
        results.append(
            {
                "id": q["id"],
                "answer": answer,
                "found": len(primary & top5) / len(primary),
                "precision": precision,
                "facts": facts,
            }
        )
    return results


def judge(llm, answer, key_facts):
    """Share of the key facts that the answer states. Same model as the answerer, so treat it as
    a rough signal, not a grade."""
    facts = "\n".join(f"{i}. {fact}" for i, fact in enumerate(key_facts, 1))
    reply = llm(f"""For each numbered fact, does the answer state it (same figures and meaning)?
Reply with only a JSON list of 1s and 0s, one per fact.

Facts:
{facts}

Answer:
{answer}""")
    marks = re.search(r"\[[\d,\s]*\]", reply)
    return sum(json.loads(marks.group())) / len(key_facts) if marks else None


def average(values):
    values = [v for v in values if v is not None]
    return f"{sum(values) / len(values):.0%}" if values else "-"


def report(results):
    with_llm = any(r["facts"] is not None for r in results)
    lines = [
        "# Eval report",
        "",
        f"{len(results)} queries from `eval/tricky_queries.json`. "
        + ("Answers written by the LLM." if with_llm else "Answers were extracts (no LLM)."),
        "",
        f"- Primary source documents found in the top 5: **{average(r['found'] for r in results)}**",
        f"- Citations from a primary or supporting document: **{average(r['precision'] for r in results)}**",
        # every query in this set is at least partly answerable, so any refusal is wrong
        f"- Wrongly refused: **{sum(r['answer'].outcome == 'refused' for r in results)}**",
    ]
    if with_llm:
        lines.append(
            f"- Key facts stated in the answer (LLM judge): **{average(r['facts'] for r in results)}**"
        )
    lines += [
        "",
        "| ID | Primary docs found | Citation precision | Key facts | Outcome | Confidence |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        conf = r["answer"].confidence
        lines.append(
            f"| {r['id']} | {average([r['found']])} | {average([r['precision']])} | "
            f"{average([r['facts']])} | {r['answer'].outcome} | {conf['score']} ({conf['level']}) |"
        )
    return "\n".join(lines) + "\n"
