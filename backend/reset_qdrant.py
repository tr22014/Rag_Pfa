from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost",
    port=6333
)

if client.collection_exists("knowledge_base"):
    client.delete_collection("knowledge_base")
    print("Collection supprimée")
else:
    print("Collection inexistante")