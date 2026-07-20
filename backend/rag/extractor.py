import fitz  # pymupdf


class ExtractionError(Exception):
    """Levée quand un fichier ne peut pas être extrait correctement."""
    pass


def extract_pdf_pages(filepath: str) -> list[dict]:
    """
    Extrait le texte d'un PDF, page par page.

    Retourne une liste de dicts :
    [
        {"page_number": 1, "text": "..."},
        {"page_number": 2, "text": "..."},
        ...
    ]
    """
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
            "text": text.strip(),
        })

    doc.close()

    if not pages:
        raise ExtractionError("Le PDF ne contient aucune page")

    return pages


def is_scanned_pdf(pages: list[dict], min_chars_threshold: int = 20) -> bool:
    """
    Heuristique simple : si la grande majorité des pages ont très peu
    de texte extrait, c'est probablement un PDF scanné (image sans OCR).
    """
    if not pages:
        return True

    empty_pages = sum(1 for p in pages if len(p["text"]) < min_chars_threshold)
    return (empty_pages / len(pages)) > 0.7

if __name__ == "__main__":
    pdf_path = r"C:\Users\Lenovo\Desktop\rag-chatbot\Sujet de stage\internship-subject-rag-knowledge-platform.pdf"      # PDF à lire
    output_path = "extraction.txt"     # Fichier de sortie

    try:
        pages = extract_pdf_pages(pdf_path)

        with open(output_path, "w", encoding="utf-8") as f:
            for page in pages:
                f.write(f"===== Page {page['page_number']} =====\n")
                f.write(page["text"])
                f.write("\n\n")

        print(f"Extraction terminée. Texte enregistré dans : {output_path}")

        if is_scanned_pdf(pages):
            print("⚠️ Ce PDF semble être un PDF scanné.")

    except ExtractionError as e:
        print(f"Erreur : {e}")