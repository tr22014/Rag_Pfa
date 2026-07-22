from app.services.retriever import Retriever

r = Retriever()
chunks = r.retrieve("What is the Target Architecture?")
for c in chunks:
    print(c["score"], "-", c["document_id"], "-", c["page"], "-", c["text"][:80])