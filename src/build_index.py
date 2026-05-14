from __future__ import annotations
import argparse
from .config import settings
from .document_loader import load_documents
from .ollama_client import OllamaClient
from .text_splitter import split_documents
from .vector_store import FaissVectorStore


def build_index(docs_dir: str, index_dir: str) -> None:
    documents = load_documents(docs_dir)
    if not documents:
        raise ValueError(
            "No se encontraron documentos .txt, .md o .pdf con contenido")

    chunks = split_documents(
        documents,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    client = OllamaClient()
    embeddings = client.embed_many([chunk.text for chunk in chunks])

    store = FaissVectorStore()
    store.build(embeddings, chunks)
    store.save(index_dir)

    print(f"Documentos cargados: {len(documents)}")
    print(f"Fragmentos indexados: {len(chunks)}")
    print(f"Índice guardado en: {index_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Construye un índice FAISS para RAG local")
    parser.add_argument("--docs-dir", default="data/docs",
                        help="Directorio con documentos")
    parser.add_argument("--index-dir", default="data/indexes/main",
                        help="Directorio de salida del índice")
    args = parser.parse_args()
    build_index(args.docs_dir, args.index_dir)


if __name__ == "__main__":
    main()
