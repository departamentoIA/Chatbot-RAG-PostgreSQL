from __future__ import annotations

import re
import sqlparse


FORBIDDEN_KEYWORDS = {
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "grant",
    "revoke",
    "copy",
    "execute",
    "call",
}


def validate_sql(sql: str) -> str:
    cleaned = sql.strip().strip(";")

    if not cleaned:
        raise ValueError("La consulta SQL está vacía.")

    statements = sqlparse.parse(cleaned)

    if len(statements) != 1:
        raise ValueError("Solo se permite una consulta SQL por pregunta.")

    first_token = statements[0].token_first(skip_cm=True)

    if not first_token or first_token.value.lower() != "select":
        raise ValueError("Solo se permiten consultas SELECT.")

    lowered = cleaned.lower()

    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", lowered):
            raise ValueError(
                f"La palabra clave '{keyword}' no está permitida.")

    return cleaned
