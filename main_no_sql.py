from __future__ import annotations
import argparse
from src.rag import LocalRAG


def print_sources(sources: list[dict]) -> None:
    print("\nFuentes recuperadas:")
    for idx, source in enumerate(sources, start=1):
        print(
            f"{idx}. {source['source']} | fragmento {source['chunk_id']} | score {source['score']:.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat RAG local")
    parser.add_argument("--index-dir", default="data/indexes/main",
                        help="Directorio del índice FAISS")
    parser.add_argument(
        "--memory-path",
        default="data/memory/conversation.json",
        help="Archivo JSON donde se guarda la memoria conversacional",
    )
    parser.add_argument("--top-k", type=int, default=5,
                        help="Número de fragmentos a recuperar")
    parser.add_argument("--clear-memory", action="store_true",
                        help="Borra la memoria antes de iniciar el chat")
    args = parser.parse_args()

    rag = LocalRAG(index_dir=args.index_dir, memory_path=args.memory_path)
    if args.clear_memory:
        rag.clear_memory()
        print("Memoria conversacional borrada.\n")

    print("RAG local iniciado. Escribe 'salir' para terminar.")
    print("La memoria se guarda en:", args.memory_path)
    print()

    while True:
        question = input("Pregunta: ").strip()
        if question.lower() in {"salir", "exit", "quit"}:
            break
        if not question:
            continue

        result = rag.ask(question, top_k=args.top_k)
        print("\nRespuesta:\n")
        print(result["answer"])
        print_sources(result["sources"])
        print()


if __name__ == "__main__":
    main()
