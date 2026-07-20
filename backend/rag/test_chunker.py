import json
from extractor import extract_pdf_pages
from chunker import chunk_pages

pdf_path = r"C:\Users\Lenovo\Desktop\rag-chatbot\Sujet de stage\internship-subject-rag-knowledge-platform.pdf"

pages = extract_pdf_pages(pdf_path)

chunks = chunk_pages(
    pages,
    max_chunk_size=1000,
    overlap_sentences=1,
    min_chunk_size=200,
)

with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print(f"{len(chunks)} chunks enregistrés dans chunks.json")