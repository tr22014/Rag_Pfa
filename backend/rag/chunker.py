import re

# Détection des titres
TITLE_PATTERN = re.compile(
    r"^(\d+(\.\d+)*)?\s*[A-Z][A-Za-z0-9\s:/()\-]{2,}$"
)


def is_title(text: str) -> bool:
    """
    Détecte un titre.
    """

    text = text.strip()

    if len(text) > 80:
        return False

    if text.endswith("."):
        return False

    return bool(TITLE_PATTERN.match(text))


def split_sentences(text: str):
    """
    Découpe un texte en phrases.
    """
    return [
        s.strip()
        for s in re.split(r'(?<=[.!?])\s+', text)
        if s.strip()
    ]


def split_long_sentence(sentence, max_chunk_size):
    """
    Découpe une phrase beaucoup trop longue.
    """

    words = sentence.split()

    pieces = []

    current = ""

    for word in words:

        candidate = word if not current else current + " " + word

        if len(candidate) <= max_chunk_size:

            current = candidate

        else:

            pieces.append(current)

            current = word

    if current:

        pieces.append(current)

    return pieces


def chunk_pages(
    pages,
    max_chunk_size=1000,
    overlap_sentences=1,
    min_chunk_size=200,
):

    chunks = []

    chunk_id = 0

    for page in pages:

        page_number = page["page_number"]

        text = page["text"]

        if not text.strip():
            continue

        paragraphs = [
            p.strip()
            for p in text.split("\n\n")
            if p.strip()
        ]

        i = 0

        while i < len(paragraphs):

            paragraph = paragraphs[i]

            # -------------------------
            # Fusion titre + contenu
            # -------------------------

            if is_title(paragraph):

                if i + 1 < len(paragraphs):

                    paragraph += "\n\n" + paragraphs[i + 1]

                    i += 1

            # -------------------------
            # Petit paragraphe
            # -------------------------

            if len(paragraph) <= max_chunk_size:

                if (
                    chunks
                    and chunks[-1]["page_number"] == page_number
                    and len(paragraph) < min_chunk_size
                ):

                    chunks[-1]["text"] += "\n\n" + paragraph

                else:

                    chunks.append({
                        "page_number": page_number,
                        "chunk_id": chunk_id,
                        "text": paragraph,
                    })

                    chunk_id += 1

                i += 1
                continue

            # -------------------------
            # Grand paragraphe
            # -------------------------

            sentences = split_sentences(paragraph)

            expanded = []

            for sentence in sentences:

                if len(sentence) > max_chunk_size:

                    expanded.extend(
                        split_long_sentence(
                            sentence,
                            max_chunk_size
                        )
                    )

                else:

                    expanded.append(sentence)

            current = []

            for sentence in expanded:

                candidate = " ".join(current + [sentence])

                if len(candidate) <= max_chunk_size:

                    current.append(sentence)

                else:

                    if current:

                        chunks.append({
                            "page_number": page_number,
                            "chunk_id": chunk_id,
                            "text": " ".join(current),
                        })

                        chunk_id += 1

                    overlap = (
                        current[-overlap_sentences:]
                        if overlap_sentences > 0
                        else []
                    )

                    current = overlap + [sentence]

            if current:

                text = " ".join(current)

                if (
                    chunks
                    and chunks[-1]["page_number"] == page_number
                    and len(text) < min_chunk_size
                ):

                    chunks[-1]["text"] += " " + text

                else:

                    chunks.append({
                        "page_number": page_number,
                        "chunk_id": chunk_id,
                        "text": text,
                    })

                    chunk_id += 1

            i += 1

    return chunks