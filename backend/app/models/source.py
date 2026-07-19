from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_text = Column(String, nullable=True)
    page_number = Column(Integer, nullable=True)
    relevance_score = Column(Float, nullable=True)

    message = relationship("Message", back_populates="sources")
    document = relationship("Document", back_populates="sources")