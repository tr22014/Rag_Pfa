import json
from sentence_transformers import SentenceTransformer

# -------------------------
# Chargement du modèle
# -------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------
# Lecture des chunks
# -------------------------

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"{len(chunks)} chunks chargés.")

# -------------------------
# Génération des embeddings
# -------------------------

for chunk in chunks:

    text = chunk["text"]

    embedding = model.encode(text).tolist()

    chunk["embedding"] = embedding

print("Embeddings générés.")

# -------------------------
# Sauvegarde
# -------------------------

with open("chunks_embeddings.json", "w", encoding="utf-8") as f:

    json.dump(
        chunks,
        f,
        indent=4,
        ensure_ascii=False
    )

print("Embeddings enregistrés dans chunks_embeddings.json")