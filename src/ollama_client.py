from __future__ import annotations
import requests
from typing import Iterable
from .config import settings


class OllamaClient:
    def __init__(self, base_url: str = settings.ollama_base_url):
        self.base_url = base_url.rstrip("/")

    def embed(self, text: str, model: str = settings.embedding_model) -> list[float]:
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={"model": model, "prompt": text},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def embed_many(self, texts: Iterable[str], model: str = settings.embedding_model) -> list[list[float]]:
        return [self.embed(text, model=model) for text in texts]

    def generate(self, prompt: str, model: str = settings.llm_model, temperature: float = settings.temperature) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature},
            },
            timeout=180,
        )
        response.raise_for_status()
        return response.json()["response"]
