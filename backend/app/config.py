from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:root@localhost:5432/Rag_Chatbot"

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    upload_dir: str = "uploads"

    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    chunk_size: int = 500
    chunk_overlap: int = 50

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()