from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base de données
    database_url: str = "postgresql://postgres:root@localhost:5432/Rag_Chatbot"

    # Authentification
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Upload
    upload_dir: str = "uploads"

    # Embeddings
    embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    embedding_dimension: int = 768

    # Chunking
    chunk_size: int = 500
    chunk_overlap: int = 50

    # Redis (Celery)
    redis_url: str = "redis://redis:6379/0"

    # Qdrant
    qdrant_url: str = "http://qdrant:6333"

    # Ollama
    ollama_base_url: str = "http://host.docker.internal:11434"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()