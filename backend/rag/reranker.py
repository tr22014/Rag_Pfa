from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(question: str, chunks: list[dict]) -> list[dict]:

    if not chunks:
        return []

    pairs = [
        (question, chunk["text"])
        for chunk in chunks
    ]

    scores = reranker.predict(pairs)

    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)

    chunks.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return chunks