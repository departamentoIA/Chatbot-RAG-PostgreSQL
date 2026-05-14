from __future__ import annotations
from dataclasses import dataclass
from .document_loader import Document


@dataclass
class Chunk:
    text: str
    source: str
    chunk_id: int


def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap debe ser menor que chunk_size")

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks


def split_documents(documents: list[Document], chunk_size: int, chunk_overlap: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        for idx, text in enumerate(split_text(document.text, chunk_size, chunk_overlap)):
            chunks.append(
                Chunk(text=text, source=document.source, chunk_id=idx))
    return chunks
