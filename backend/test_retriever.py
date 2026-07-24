from rag.retriever import Retriever

retriever = Retriever()

question = "Quelle est le context de cet internship ?"

results = retriever.retrieve(
    question=question,
    limit=5,
)

print(f"\nQuestion : {question}")
print("=" * 80)

for i, chunk in enumerate(results, 1):
    print(f"Résultat {i}")
    print(f"Source : {chunk['source']}")
    print(f"Document : {chunk['document_id']}")
    print(f"Page : {chunk['page']}")
    print(chunk["text"])
    print("-" * 80)