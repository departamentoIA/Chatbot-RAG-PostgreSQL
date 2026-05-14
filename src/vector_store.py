from __future__ import annotations
import json
from pathlib import Path
import faiss
import numpy as np
from .text_splitter import Chunk


class FaissVectorStore:
    def __init__(self):
        self.index: faiss.Index | None = None
        self.metadata: list[dict] = []

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        faiss.normalize_L2(vectors)
        return vectors

    def build(self, embeddings: list[list[float]], chunks: list[Chunk]) -> None:
        if not embeddings:
            raise ValueError("No hay embeddings para indexar")

        vectors = np.array(embeddings, dtype="float32")
        vectors = self._normalize(vectors)
        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(vectors)
        self.metadata = [
            {"text": chunk.text, "source": chunk.source, "chunk_id": chunk.chunk_id}
            for chunk in chunks
        ]

    def save(self, index_dir: str | Path) -> None:
        if self.index is None:
            raise ValueError("El índice FAISS no ha sido construido")

        path = Path(index_dir)
        path.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(path / "index.faiss"))
        (path / "metadata.json").write_text(
            json.dumps(self.metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load(self, index_dir: str | Path) -> None:
        path = Path(index_dir)
        self.index = faiss.read_index(str(path / "index.faiss"))
        self.metadata = json.loads(
            (path / "metadata.json").read_text(encoding="utf-8"))

    def search(self, query_embedding: list[float], top_k: int) -> list[dict]:
        if self.index is None:
            raise ValueError("El índice FAISS no ha sido cargado")

        query = np.array([query_embedding], dtype="float32")
        query = self._normalize(query)
        scores, indices = self.index.search(query, top_k)

        results: list[dict] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            item = dict(self.metadata[idx])
            item["score"] = float(score)
            results.append(item)
        return results
