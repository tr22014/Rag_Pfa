import fitz  
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ExtractionError(Exception):
    """Levée quand un fichier ne peut pas être extrait correctement."""
    pass


def extract_pdf_pages(filepath: str, document_id: int) -> list[dict]:
    try:
        doc = fitz.open(filepath)
    except Exception as e:
        raise ExtractionError(f"Impossible d'ouvrir le PDF: {e}")

    pages = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        text = page.get_text("text")

        pages.append({
            "page_number": page_index + 1,
            "document_id": document_id,
            "text": text.strip(),
        })

    doc.close()

    if not pages:
        raise ExtractionError("Le PDF ne contient aucune page")

    return pages


def is_scanned_pdf(pages: list[dict], min_chars_threshold: int = 20) -> bool:
    if not pages:
        return True

    empty_pages = sum(1 for p in pages if len(p["text"]) < min_chars_threshold)
    return (empty_pages / len(pages)) > 0.7


if __name__ == "__main__":
    pdf_path = r"C:\Users\Lenovo\Desktop\rag-chatbot\Sujet de stage\internship-subject-rag-knowledge-platform.pdf"
    output_path = os.path.join(BASE_DIR, "extraction.txt")
    pages_json_path = os.path.join(BASE_DIR, "pages.json")

    try:
        pages = extract_pdf_pages(pdf_path, document_id=1)

        with open(output_path, "w", encoding="utf-8") as f:
            for page in pages:
                f.write(f"===== Page {page['page_number']} =====\n")
                f.write(page["text"])
                f.write("\n\n")

        with open(pages_json_path, "w", encoding="utf-8") as f:
            json.dump(pages, f, indent=4, ensure_ascii=False)

        print(f"Extraction terminée. Texte enregistré dans : {output_path}")
        print(f"Pages sauvegardées dans : {pages_json_path}")

        if is_scanned_pdf(pages):
            print("⚠️ Ce PDF semble être un PDF scanné.")

    except ExtractionError as e:
        print(f"Erreur : {e}")