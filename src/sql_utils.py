from __future__ import annotations

import json


def extract_sql(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```sql", "").replace("```", "").strip()

    return text


def rows_to_text(rows: list[dict], max_chars: int = 6000) -> str:
    if not rows:
        return "[]"

    text = json.dumps(rows, ensure_ascii=False, default=str, indent=2)

    if len(text) > max_chars:
        return text[:max_chars] + "\n... RESULTADOS TRUNCADOS ..."

    return text
