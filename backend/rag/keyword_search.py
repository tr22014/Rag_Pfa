from sqlalchemy import text
from database.database import SessionLocal


def keyword_search(question: str, limit: int = 10):

    db = SessionLocal()

    sql = text("""
        SELECT
            id,
            content,
            document_id,
            page_number,
            GREATEST(
                ts_rank(
                    to_tsvector('english', content),
                    plainto_tsquery('english', :query)
                ),
                ts_rank(
                    to_tsvector('french', content),
                    plainto_tsquery('french', :query)
                )
            ) AS score
        FROM chunks
        WHERE
            to_tsvector('english', content)
                @@ plainto_tsquery('english', :query)
            OR
            to_tsvector('french', content)
                @@ plainto_tsquery('french', :query)
        ORDER BY score DESC
        LIMIT :limit
    """)

    rows = db.execute(
        sql,
        {
            "query": question,
            "limit": limit
        }
    )

    results = []

    for row in rows:

        results.append(
            {
                "chunk_id": row.id,
                "score": float(row.score),
                "text": row.content,
                "document_id": row.document_id,
                "page": row.page_number
            }
        )

    db.close()

    return results