from __future__ import annotations

import argparse
from src.sql_agent import LocalSQLAgent


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chatbot local con SQL Agent y PostgreSQL")

    parser.add_argument(
        "--memory-path",
        default="data/memory/conversation.json",
        help="Archivo JSON donde se guarda la memoria conversacional",
    )

    parser.add_argument(
        "--clear-memory",
        action="store_true",
        help="Borra la memoria antes de iniciar el chat",
    )

    parser.add_argument(
        "--show-sql",
        action="store_true",
        help="Muestra la consulta SQL generada",
    )

    args = parser.parse_args()

    agent = LocalSQLAgent(memory_path=args.memory_path)

    if args.clear_memory:
        agent.clear_memory()
        print("Memoria conversacional borrada.\n")

    print("SQL Agent iniciado.")
    print("Escribe 'salir' para terminar.\n")

    try:
        while True:
            question = input("Pregunta: ").strip()

            if question.lower() in {"salir", "exit", "quit"}:
                break

            if not question:
                continue

            try:
                result = agent.ask(question)

                print("\nRespuesta:\n")
                print(result["answer"])

                if args.show_sql:
                    print("\nSQL generado:\n")
                    print(result["sql"])

                print()

            except Exception as error:
                print("\nNo fue posible responder la pregunta.")
                print(f"Detalle: {error}\n")

    finally:
        agent.close()


if __name__ == "__main__":
    main()
