"""Hybrid search: BM25 for exact terms (MOTO, BridgeAdvance, MMSC), embeddings for paraphrase.
The two rankings are merged with reciprocal rank fusion, so their scores never need comparing."""

import math
import re
from collections import Counter
from functools import cache

import numpy as np
from model2vec import StaticModel

STOPWORDS = set(
    """a an and are as at be by can could do does for from get got have how i if in is it its me my of
on or our so that the their them there this to was we what when where which who why will with
would you your much many any anything some please tell need want he she his her they whats im
ive dont long should happen happens""".split()
)


def tokenize(text):
    words = re.findall(r"[a-z0-9]{2,}", text.lower().replace("'", ""))
    # crude plural folding: fees -> fee, cards -> card
    return [
        w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith(("ss", "us")) else w
        for w in words
        if w not in STOPWORDS
    ]


@cache
def embedding_model():
    # static embeddings: ~30MB, no torch, fast on CPU. Weaker than a transformer encoder.
    return StaticModel.from_pretrained("minishlab/potion-base-8M")


def embed(texts):
    vectors = embedding_model().encode(list(texts))
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


class Index:
    def __init__(self, chunks):
        self.chunks = chunks
        texts = [f"{c.title}\n{c.text}" for c in chunks]
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.doc_freq = Counter(term for doc in self.docs for term in doc)
        self.lengths = np.array([sum(doc.values()) for doc in self.docs])
        self.vectors = embed(texts)

    def idf(self, term):
        n, df = len(self.docs), self.doc_freq[term]
        return math.log(1 + (n - df + 0.5) / (df + 0.5))

    def bm25(self, query, k1=1.5, b=0.75):
        scores = np.zeros(len(self.docs))
        norm = k1 * (1 - b + b * self.lengths / self.lengths.mean())
        for term in set(tokenize(query)):
            tf = np.array([doc[term] for doc in self.docs])
            scores += self.idf(term) * tf * (k1 + 1) / (tf + norm)
        return scores

    def search(self, query, k=8):
        """Returns [(chunk, cosine similarity)], best first."""
        lexical = self.bm25(query)
        semantic = self.vectors @ embed([query])[0]
        fused = np.zeros(len(self.chunks))
        for scores in (lexical, semantic):
            ranks = np.argsort(np.argsort(-scores, kind="stable")) + 1
            fused += np.where(scores > 0, 1 / (60 + ranks), 0)
        top = np.argsort(-fused, kind="stable")[:k]
        return [(self.chunks[i], float(semantic[i])) for i in top if fused[i] > 0]
