import json
from pathlib import Path

import faiss
import numpy as np

from app.config import get_settings
from app.rag.chunker import split_documents
from app.rag.embedding_service import EmbeddingService
from app.rag.loaders import load_all_documents
from app.rag.metadata import enrich_metadata


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INDEX_DIR = PROJECT_ROOT / "data" / "index"

FAISS_PATH = INDEX_DIR / "faiss.index"
CHUNKS_PATH = INDEX_DIR / "chunks.json"
METADATA_PATH = INDEX_DIR / "index_metadata.json"


def build_faiss_index() -> dict:
    """Build and persist a FAISS cosine-similarity index."""

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    documents = load_all_documents()
    documents = enrich_metadata(documents)
    chunks = split_documents(documents)

    if not chunks:
        raise RuntimeError("No chunks available for indexing.")

    texts = [chunk.page_content for chunk in chunks]

    embedding_service = EmbeddingService()
    embeddings = embedding_service.embed_texts(texts)

    vectors = np.asarray(
        embeddings,
        dtype="float32",
    )

    # Normalize vectors so inner product is equivalent to cosine similarity.
    faiss.normalize_L2(vectors)

    dimension = vectors.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    faiss.write_index(index, str(FAISS_PATH))

    serialized_chunks = []

    for chunk in chunks:
        serialized_chunks.append(
            {
                "text": chunk.page_content,
                "metadata": chunk.metadata,
            }
        )

    CHUNKS_PATH.write_text(
        json.dumps(
            serialized_chunks,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    settings = get_settings()

    index_metadata = {
        "embedding_model": settings.openai_embedding_model,
        "dimension": dimension,
        "vector_count": index.ntotal,
        "metric": "cosine_similarity_via_normalized_inner_product",
    }

    METADATA_PATH.write_text(
        json.dumps(
            index_metadata,
            indent=2,
        ),
        encoding="utf-8",
    )

    return index_metadata


def load_faiss_index() -> faiss.Index:
    """Load the persisted FAISS index."""

    if not FAISS_PATH.exists():
        raise FileNotFoundError(
            f"FAISS index not found: {FAISS_PATH}"
        )

    return faiss.read_index(str(FAISS_PATH))


def load_index_chunks() -> list[dict]:
    """Load chunk text and metadata corresponding to FAISS vectors."""

    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"Chunk metadata not found: {CHUNKS_PATH}"
        )

    return json.loads(
        CHUNKS_PATH.read_text(encoding="utf-8")
    )