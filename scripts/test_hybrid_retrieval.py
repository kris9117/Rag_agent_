from app.rag.hybrid_retriever import HybridRetriever


def run_test(query: str) -> None:
    retriever = HybridRetriever()
    results = retriever.search(
        query,
        top_k=5,
        candidate_k=10,
    )

    print(f"\nQUERY: {query}")
    print("-" * 90)

    for rank, result in enumerate(results, start=1):
        metadata = result["metadata"]

        print(
            f"{rank}. RRF={result['rrf_score']:.6f} | "
            f"document={metadata.get('document_id')} | "
            f"section={metadata.get('section')}"
        )

        print(
            f"   retrievers={result['retrievers']}"
        )

        print(
            f"   {result['text'][:180].replace(chr(10), ' ')}"
        )


def main() -> None:
    queries = [
        "How do I recover a locked employee account?",
        "My VPN authentication keeps failing.",
        "My laptop has a network connection problem.",
        "What are the MFA security requirements?",
        "What should I do after receiving a phishing email?",
    ]

    for query in queries:
        run_test(query)


if __name__ == "__main__":
    main()