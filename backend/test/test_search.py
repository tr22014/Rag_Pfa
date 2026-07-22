from sentence_transformers import SentenceTransformer
from vector_store import client, COLLECTION_NAME

model = SentenceTransformer("all-MiniLM-L6-v2")

def search(query, top_k=3):
    query_vector = model.encode(query).tolist()
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k
    ).points

    for r in results:
        print(r.score, "-", r.payload["text"][:100])
    return results


if __name__ == "__main__":
    search("what is the Target Architecture")