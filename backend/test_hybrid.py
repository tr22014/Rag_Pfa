from rag.keyword_search import keyword_search

results = keyword_search(
    "Quelle est le context de cet internship ?",
    limit=5
)

for r in results:
    print(r)