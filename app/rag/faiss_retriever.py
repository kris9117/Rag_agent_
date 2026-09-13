from app.rag.embedding_service import EmbeddingService
from app.rag.faiss_index import (
    load_faiss_index,
    load_index_chunks,
)


class FAISSRetriever:
    """Semantic retrieval using the persisted FAISS index."""

    def __init__(self) -> None:
        self.index = load_faiss_index()
        self.chunks = load_index_chunks()
        self.embedding_service = EmbeddingService()

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """Return the top semantic matches for a query."""

        if not query.strip():
            return []

        query_vector = self.embedding_service.embed_query(query)

        import numpy as np
        import faiss

        vector = np.asarray(
            [query_vector],
            dtype="float32",
        )

        faiss.normalize_L2(vector)

        scores, indices = self.index.search(
            vector,
            top_k,
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index < 0 or index >= len(self.chunks):
                continue

            chunk = self.chunks[index]

            results.append(
                {
                    "score": float(score),
                    "text": chunk["text"],
                    "metadata": chunk["metadata"],
                }
            )

        return results