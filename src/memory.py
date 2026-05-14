from __future__ import annotations
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Message:
    role: str
    content: str


class ConversationMemory:
    """Memoria conversacional persistente en un archivo JSON."""

    def __init__(self, memory_path: str | Path, max_messages: int = 12):
        self.memory_path = Path(memory_path)
        self.max_messages = max_messages
        self.messages: list[Message] = []
        self.load()

    def load(self) -> None:
        if not self.memory_path.exists():
            self.messages = []
            return

        raw = json.loads(self.memory_path.read_text(encoding="utf-8"))
        self.messages = [Message(**item) for item in raw]

    def save(self) -> None:
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [asdict(message) for message in self.messages]
        self.memory_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add_user_message(self, content: str) -> None:
        self.messages.append(Message(role="usuario", content=content))
        self._trim()
        self.save()

    def add_assistant_message(self, content: str) -> None:
        self.messages.append(Message(role="asistente", content=content))
        self._trim()
        self.save()

    def clear(self) -> None:
        self.messages = []
        self.save()

    def format_for_prompt(self) -> str:
        if not self.messages:
            return "Sin historial previo."

        return "\n".join(
            f"{message.role.capitalize()}: {message.content}"
            for message in self.messages[-self.max_messages:]
        )

    def _trim(self) -> None:
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
