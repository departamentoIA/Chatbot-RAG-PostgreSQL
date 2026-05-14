from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3"
    embedding_model: str = "mxbai-embed-large"
    chunk_size: int = 900
    chunk_overlap: int = 150
    top_k: int = 5
    temperature: float = 0.2
    memory_path: str = "data/memory/conversation.json"
    memory_max_messages: int = 12


settings = Settings()
