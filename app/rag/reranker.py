from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ) -> None:
        self.model_name = model_name
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        candidates: list[dict],
        top_k: int = 5,
    ) -> list[dict]:
        if not query.strip() or not candidates:
            return []

        pairs = [
            (query, candidate["text"])
            for candidate in candidates
        ]

        scores = self.model.predict(pairs)

        reranked = []

        for candidate, score in zip(candidates, scores):
            result = dict(candidate)
            result["rerank_score"] = float(score)
            reranked.append(result)

        reranked.sort(
            key=lambda item: item["rerank_score"],
            reverse=True,
        )

        return reranked[:top_k]