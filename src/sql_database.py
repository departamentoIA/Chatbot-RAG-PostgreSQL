from __future__ import annotations

import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings


class PostgresDatabase:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
            cursor_factory=RealDictCursor,
        )

    def get_schema_description(self) -> str:
        query = """
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = %s
        ORDER BY table_name, ordinal_position;
        """

        rows = self.query(query, (settings.postgres_schema,))

        tables = {}
        for row in rows:
            table = row["table_name"]
            column = row["column_name"]
            data_type = row["data_type"]
            tables.setdefault(table, []).append(f"{column} ({data_type})")

        schema_blocks = []
        for table, columns in tables.items():
            schema_blocks.append(
                f"Tabla: {table}\nColumnas: {', '.join(columns)}")

        return "\n\n".join(schema_blocks)

    def query(self, sql: str, params: tuple | None = None) -> list[dict]:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            if cursor.description:
                return cursor.fetchall()

            self.connection.commit()
            return []

    def close(self) -> None:
        self.connection.close()
