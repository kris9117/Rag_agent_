import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INDEX_DIR = PROJECT_ROOT / "data" / "index"

BM25_PATH = INDEX_DIR / "bm25.json"


def tokenize(text: str) -> list[str]:
    """Tokenize text for BM25 retrieval."""

    return re.findall(
        r"\b[a-zA-Z0-9_]+\b",
        text.lower(),
    )


class BM25Retriever:
    """Sparse keyword retrieval over the same chunks used by FAISS."""

    def __init__(self) -> None:
        if not BM25_PATH.exists():
            raise FileNotFoundError(
                f"BM25 index not found: {BM25_PATH}"
            )

        data = json.loads(
            BM25_PATH.read_text(encoding="utf-8")
        )

        self.chunks = data["chunks"]

        tokenized_chunks = [
            tokenize(chunk["text"])
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """Return the top BM25 matches."""

        if not query.strip():
            return []

        query_tokens = tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )[:top_k]

        results = []

        for index in ranked_indices:
            results.append(
                {
                    "score": float(scores[index]),
                    "text": self.chunks[index]["text"],
                    "metadata": self.chunks[index]["metadata"],
                }
            )

        return results


def build_bm25_index() -> dict:
    """Build and persist the BM25 corpus."""

    from app.rag.chunker import split_documents
    from app.rag.loaders import load_all_documents
    from app.rag.metadata import enrich_metadata

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    documents = load_all_documents()
    documents = enrich_metadata(documents)
    chunks = split_documents(documents)

    if not chunks:
        raise RuntimeError("No chunks available for BM25 indexing.")

    serialized_chunks = [
        {
            "text": chunk.page_content,
            "metadata": chunk.metadata,
        }
        for chunk in chunks
    ]

    data = {
        "retriever": "BM25Okapi",
        "chunk_count": len(serialized_chunks),
        "chunks": serialized_chunks,
    }

    BM25_PATH.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return {
        "retriever": "BM25Okapi",
        "chunk_count": len(serialized_chunks),
    }