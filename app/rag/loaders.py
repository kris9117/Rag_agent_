from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "data" / "knowledge_base"


def load_document(path: Path) -> list:
    """Load a supported knowledge-base document."""

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return PyPDFLoader(str(path)).load()

    if suffix in {".md", ".txt"}:
        return TextLoader(
            str(path),
            encoding="utf-8",
        ).load()

    raise ValueError(
        f"Unsupported document type: {path.suffix}"
    )


def load_all_documents() -> list:
    """Load all supported documents from the knowledge base."""

    documents = []

    for path in KNOWLEDGE_BASE_DIR.rglob("*"):
        if path.suffix.lower() in {".pdf", ".md", ".txt"}:
            documents.extend(load_document(path))

    return documents