from fastapi import APIRouter
from pydantic import BaseModel
from rag.vector_store import client, COLLECTION_NAME
from sentence_transformers import SentenceTransformer

router = APIRouter()
model = SentenceTransformer("all-MiniLM-L6-v2")  # chargé une seule fois au démarrage

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/search")
def search(request: SearchRequest):
    query_vector = model.encode(request.query).tolist()
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=request.top_k
    ).points

    return [
        {"score": r.score, "text": r.payload["text"]}
        for r in results
    ]