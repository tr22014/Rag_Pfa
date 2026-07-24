import json
from sentence_transformers import SentenceTransformer
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

with open(os.path.join(BASE_DIR, "chunks.json"), "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"{len(chunks)} chunks chargés.")

for chunk in chunks:
    text = chunk["text"]
    embedding = model.encode(text).tolist()
    chunk["embedding"] = embedding

print("Embeddings générés.")

with open(os.path.join(BASE_DIR, "chunks_embeddings.json"), "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print("Embeddings enregistrés dans chunks_embeddings.json")