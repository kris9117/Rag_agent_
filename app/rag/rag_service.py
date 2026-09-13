from app.rag.hybrid_retriever import HybridRetriever
from app.rag.reranker import CrossEncoderReranker


class RAGService:
    def __init__(self) -> None:
        self.hybrid_retriever = HybridRetriever()
        self.reranker = CrossEncoderReranker()

    def retrieve(
        self,
        query: str,
        candidate_k: int = 10,
        top_k: int = 5,
    ) -> list[dict]:
        if not query.strip():
            return []

        candidates = self.hybrid_retriever.search(
            query=query,
            top_k=candidate_k,
            candidate_k=candidate_k,
        )

        reranked = self.reranker.rerank(
            query=query,
            candidates=candidates,
            top_k=top_k,
        )

        results = []

        for rank, result in enumerate(reranked, start=1):
            results.append(
                {
                    "rank": rank,
                    "text": result["text"],
                    "metadata": result["metadata"],
                    "rrf_score": result["rrf_score"],
                    "rerank_score": result["rerank_score"],
                }
            )

        return results