from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from pypdf import PdfReader


@dataclass
class Document:
    text: str
    source: str


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_pdf_file(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def load_documents(docs_dir: str | Path) -> list[Document]:
    docs_path = Path(docs_dir)
    if not docs_path.exists():
        raise FileNotFoundError(f"No existe el directorio: {docs_path}")

    documents: list[Document] = []
    for path in docs_path.rglob("*"):
        if not path.is_file():
            continue

        suffix = path.suffix.lower()
        if suffix in {".txt", ".md"}:
            text = read_text_file(path)
        elif suffix == ".pdf":
            text = read_pdf_file(path)
        else:
            continue

        clean_text = text.strip()
        if clean_text:
            documents.append(Document(text=clean_text, source=str(path)))

    return documents
