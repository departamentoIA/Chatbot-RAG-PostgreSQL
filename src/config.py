from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3"
    # "mxbai-embed-large" or "embeddinggemma"
    embedding_model: str = "mxbai-embed-large"
    chunk_size: int = 100
    chunk_overlap: int = 20
    top_k: int = 5
    temperature: float = 0.1
    memory_path: str = "data/memory/conversation.json"
    memory_max_messages: int = 10

    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "")
    postgres_user: str = os.getenv("POSTGRES_USER", "")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")
    postgres_schema: str = os.getenv("POSTGRES_SCHEMA", "public")

    sql_max_rows: int = 100


settings = Settings()
