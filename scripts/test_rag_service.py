from app.rag.rag_service import RAGService


def main() -> None:
    rag = RAGService()

    queries = [
        "My VPN authentication keeps failing.",
        "What should I do after receiving a phishing email?",
    ]

    for query in queries:
        print(f"\nQUERY: {query}")
        print("=" * 90)

        results = rag.retrieve(
            query=query,
            candidate_k=10,
            top_k=5,
        )

        for result in results:
            metadata = result["metadata"]

            print(
                f"{result['rank']}. "
                f"rerank={result['rerank_score']:.4f} | "
                f"rrf={result['rrf_score']:.6f} | "
                f"{metadata.get('document_id')} | "
                f"{metadata.get('section')}"
            )

            print(f"   {result['text'][:200]}")


if __name__ == "__main__":
    main()