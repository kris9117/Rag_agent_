from app.rag.hybrid_retriever import HybridRetriever
from app.rag.reranker import CrossEncoderReranker


def run_test(
    query: str,
    hybrid: HybridRetriever,
    reranker: CrossEncoderReranker,
) -> None:
    candidates = hybrid.search(
        query,
        top_k=10,
        candidate_k=10,
    )

    results = reranker.rerank(
        query,
        candidates,
        top_k=5,
    )

    print(f"\nQUERY: {query}")
    print("-" * 90)

    for rank, result in enumerate(results, start=1):
        metadata = result["metadata"]

        print(
            f"{rank}. rerank={result['rerank_score']:.4f} | "
            f"RRF={result['rrf_score']:.6f} | "
            f"document={metadata.get('document_id')} | "
            f"section={metadata.get('section')}"
        )

        print(
            f"   {result['text'][:220].replace(chr(10), ' ')}"
        )


def main() -> None:
    hybrid = HybridRetriever()
    reranker = CrossEncoderReranker()

    queries = [
        "How do I recover a locked employee account?",
        "My VPN authentication keeps failing.",
        "What are the MFA security requirements?",
        "What should I do after receiving a phishing email?",
    ]

    for query in queries:
        run_test(query, hybrid, reranker)


if __name__ == "__main__":
    main()