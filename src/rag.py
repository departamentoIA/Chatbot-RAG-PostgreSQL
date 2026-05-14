from __future__ import annotations
from .config import settings
from .memory import ConversationMemory
from .ollama_client import OllamaClient
from .vector_store import FaissVectorStore


SYSTEM_INSTRUCTIONS = """
Eres un asistente especializado en responder usando el contexto documental recuperado y el historial de conversación.
Tu nombre es Sebastián.
Prioriza el contexto documental cuando la pregunta sea sobre los archivos.
Usa el historial solo para mantener continuidad, resolver referencias como "eso", "lo anterior" o recordar preferencias de la conversación.
Si el contexto documental no contiene la respuesta, indica claramente que no hay información suficiente en los documentos.
Responde en español, de forma precisa y profesional.
""".strip()


def format_context(results: list[dict]) -> str:
    blocks = []
    for idx, item in enumerate(results, start=1):
        blocks.append(
            f"[Fuente {idx}]\n"
            f"Archivo: {item['source']}\n"
            f"Fragmento: {item['chunk_id']}\n"
            f"Contenido:\n{item['text']}"
        )
    return "\n\n".join(blocks)


def build_prompt(question: str, context: str, conversation_history: str) -> str:
    return f"""
{SYSTEM_INSTRUCTIONS}

Historial de conversación:
{conversation_history}

Contexto documental recuperado:
{context}

Pregunta actual:
{question}

Respuesta:
""".strip()


class LocalRAG:
    def __init__(self, index_dir: str, memory_path: str = settings.memory_path):
        self.client = OllamaClient()
        self.store = FaissVectorStore()
        self.store.load(index_dir)
        self.memory = ConversationMemory(
            memory_path=memory_path,
            max_messages=settings.memory_max_messages,
        )

    def ask(self, question: str, top_k: int = settings.top_k) -> dict:
        query_embedding = self.client.embed(question)
        results = self.store.search(query_embedding, top_k=top_k)
        context = format_context(results)
        conversation_history = self.memory.format_for_prompt()
        prompt = build_prompt(question, context, conversation_history)
        answer = self.client.generate(prompt)

        self.memory.add_user_message(question)
        self.memory.add_assistant_message(answer)

        return {"answer": answer, "sources": results}

    def clear_memory(self) -> None:
        self.memory.clear()
