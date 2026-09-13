from app.rag.bm25_retriever import BM25Retriever
from app.rag.faiss_retriever import FAISSRetriever


class HybridRetriever:
    def __init__(self) -> None:
        self.faiss_retriever = FAISSRetriever()
        self.bm25_retriever = BM25Retriever()

    def search(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: int = 10,
        rrf_k: int = 60,
    ) -> list[dict]:
        if not query.strip():
            return []

        faiss_results = self.faiss_retriever.search(
            query,
            top_k=candidate_k,
        )

        bm25_results = self.bm25_retriever.search(
            query,
            top_k=candidate_k,
        )

        fused = {}

        self._add_results(
            fused,
            faiss_results,
            "faiss",
            rrf_k,
        )

        self._add_results(
            fused,
            bm25_results,
            "bm25",
            rrf_k,
        )

        ranked = sorted(
            fused.values(),
            key=lambda item: item["rrf_score"],
            reverse=True,
        )

        return ranked[:top_k]

    @staticmethod
    def _add_results(
        fused: dict,
        results: list[dict],
        retriever_name: str,
        rrf_k: int,
    ) -> None:
        for rank, result in enumerate(results, start=1):
            metadata = result["metadata"]

            key = (
                metadata.get("document_id"),
                metadata.get("section"),
                result["text"],
            )

            if key not in fused:
                fused[key] = {
                    "text": result["text"],
                    "metadata": metadata,
                    "rrf_score": 0.0,
                    "retrievers": {},
                }

            fused[key]["rrf_score"] += 1 / (rrf_k + rank)
            fused[key]["retrievers"][retriever_name] = {
                "rank": rank,
                "score": result["score"],
            }