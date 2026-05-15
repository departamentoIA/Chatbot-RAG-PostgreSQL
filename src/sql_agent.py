from __future__ import annotations

from .config import settings
from .memory import ConversationMemory
from .ollama_client import OllamaClient
from .sql_database import PostgresDatabase
from .sql_guard import validate_sql
from .sql_prompts import SQL_GENERATION_PROMPT, ANSWER_PROMPT
from .sql_utils import extract_sql, rows_to_text


class LocalSQLAgent:
    def __init__(self, memory_path: str = settings.memory_path):
        self.client = OllamaClient()
        self.db = PostgresDatabase()
        self.memory = ConversationMemory(
            memory_path=memory_path,
            max_messages=settings.memory_max_messages,
        )

    def generate_sql(self, question: str, schema: str) -> str:
        prompt = SQL_GENERATION_PROMPT.format(
            schema=schema,
            question=question,
            max_rows=settings.sql_max_rows,
        )

        raw_sql = self.client.generate(prompt)
        sql = extract_sql(raw_sql)

        if sql.strip() == "NO_SQL":
            raise ValueError(
                "No se puede generar SQL con el esquema disponible.")

        return validate_sql(sql)

    def ask(self, question: str) -> dict:
        schema = self.db.get_schema_description()
        sql = self.generate_sql(question, schema)
        rows = self.db.query(sql)

        results_text = rows_to_text(rows)

        answer_prompt = ANSWER_PROMPT.format(
            question=question,
            sql=sql,
            results=results_text,
        )

        answer = self.client.generate(answer_prompt)

        self.memory.add_user_message(question)
        self.memory.add_assistant_message(answer)

        return {
            "answer": answer,
            "sql": sql,
            "rows": rows,
        }

    def clear_memory(self) -> None:
        self.memory.clear()

    def close(self) -> None:
        self.db.close()
