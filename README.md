# MerchantBridge Knowledge Retrieval

A small retrieval layer for the MerchantBridge support assistant. Given a question, it returns an answer, the exact source passages it is based on (file, line, and character range), and a confidence score. If the knowledge base doesn't cover the question, it refuses.

## How to run

Needs [uv](https://docs.astral.sh/uv/), which installs Python 3.14. The first run downloads a 30 MB embedding model.

```bash
uv sync
uv run python -m mbfs ask "What's your chargeback fee?"
uv run python -m mbfs ask "What's your chargeback fee?" --json
uv run python -m mbfs eval      # writes eval/report.md
uv run pytest

```

Without an API key, the answer is the cited source extracts (the mock). To have an LLM write the answer, copy `.env.example` to `.env`, add an `OPENAI_API_KEY`, and add `--llm`:

```bash
uv run python -m mbfs ask "What's your chargeback fee?" --llm
uv run python -m mbfs eval --llm    # LLM answers, then the LLM judges them against key_facts

```

The prompt is `build_prompt()` in `mbfs/answer.py`. It instructs the model to cite every sentence, show calculations, ask a clarifying question when needed, and tells it the document precedence: notices (from their effective date) over the fee schedule, over policies, over FAQs.

## What I built

- **Ingestion** (`mbfs/ingest.py`). Policies are split by `##` section, FAQs by question, notices by heading, and the fee schedule by row. Every citable line keeps its character offsets, so `source[start:end] == quote` holds for every citation, and the tests check it for every citation.
- **Tables.** Each fee-schedule row is its own chunk, indexed as `item: Chargeback fee | plan: Starter | fixed fee gbp: 20.00 | ...`. A bare "20.00" means nothing to search or to an agent without its column names. HTML table rows get the same treatment, which handles table lookups without needing a complex Text-to-SQL agent.
- **Search** (`mbfs/search.py`). BM25 plus a small static embedding model (model2vec, no GPU or PyTorch), merged with reciprocal rank fusion. BM25 handles exact terms like "MOTO" or "BridgeAdvance". The embeddings handle paraphrase. Everything is in memory: 270 chunks.
- **Answering** (`mbfs/answer.py`). Takes the top 3 chunks, picks the best-matching lines, and returns them as the answer with numbered citations. With `--llm`, the same lines go to the model, which must cite them. It can also reply `INSUFFICIENT_CONTEXT`, which becomes a refusal when the knowledge base doesn't cover the question.
- **Confidence.** Two numbers: similarity (how close the best chunk is) and coverage (the share of the question's words, weighted by rarity, that appear in the evidence). The response lists the words it couldn't find. Below 0.40 it refuses. The thresholds are set by hand from the eval set and 8 off-topic questions, so they aren't calibrated probabilities.

## Results

`uv run python -m mbfs eval` on the 20 queries in `eval/tricky_queries.json` (extracts, no LLM):

| Metric                                          | Score   |
| ----------------------------------------------- | ------- |
| Primary source documents found in the top 5     | 82%     |
| Citations from a primary or supporting document | 73%     |
| Wrongly refused                                 | 2 of 20 |
| Off-topic questions refused (tests)             | 8 of 8  |

- **Q12** ("someone nicked my BridgePay Go") and **Q13** (a long Scale + terminal cancellation question) are refused even though the right documents are found. Their confidence scores (0.31 and 0.34) overlap with the off-topic questions (up to 0.37), so a flat threshold can't safely separate them.
- **Missed primary sources:** Q05, Q07, Q13, Q19 and Q20 each have a primary document just outside the top 5. Several chunks from the same document fill those slots.
- **Answer quality:** Extracts can't be scored against the dataset's expected answers (Q01 needs a calculated £1.71). `eval --llm` has the LLM write each answer and then judge which of the query's `key_facts` it states. The judge is the same model, so treat that score as a rough signal rather than a definitive grade.

## What I didn't build

- **Conflict handling in code.** The corpus has a precedence rule and an out-of-date FAQ. Only the LLM path applies it, via the prompt. The extractive mock shows all sources together and leaves the agent to resolve them.
- **Clarifying questions.** The LLM is told to ask one when a question is ambiguous. The extractive mock doesn't.
- **Not built because the brief rules them out:** A UI, an HTTP endpoint (the brief accepts a function), auth, persistence, and scaling.

## With more time

1. Return at most one or two chunks per document, so other documents can reach the top 5.
2. Check the LLM judge against a handful of hand-scored answers before trusting its numbers.
3. Calibrate confidence on more labelled questions, including off-topic ones.
4. Apply the precedence rule in code, using each document's effective date.

## Dataset

I generated the corpus and queries with Claude using this prompt:

> Generate a zip file containing 25 synthetic customer support documents for 'MerchantBridge Financial Services'. Include 15 Markdown policy files, 5 HTML FAQ pages, and 1 CSV fee-and-rate schedule. Also generate a JSON file with 20 tricky customer queries (spanning multiple docs, out-of-scope topics, ambiguous phrasing, and table lookups), mapped to their ideal expected answers and edge-case handling.

The prompt asked for 25 documents, but its breakdown only added up to 21, so Claude added 4 plain-text service notices to reach 25. I kept the dataset exactly as generated because its traps (an outdated FAQ, a scheduled fee change, and a free-exit right) were exactly the conflicts I wanted to test the retrieval against. The generator's own notes are in `eval/DATASET.md`.

## AI tools

I used Claude to generate the dataset and the initial codebase scaffolding. This allowed me to focus my effort entirely on architectural judgment, edge-case testing, and evaluation rather than typing boilerplate code.
