from app.rag.bm25_retriever import BM25Retriever


def run_test(query: str) -> None:
    retriever = BM25Retriever()
    results = retriever.search(query, top_k=5)

    print(f"\nQUERY: {query}")
    print("-" * 80)

    for rank, result in enumerate(results, start=1):
        metadata = result["metadata"]

        print(
            f"{rank}. score={result['score']:.4f} | "
            f"document={metadata.get('document_id')} | "
            f"section={metadata.get('section')}"
        )
        print(f"   {result['text'][:180].replace(chr(10), ' ')}")


def main() -> None:
    queries = [
        "EMP0001",
        "INC000001",
        "MFA",
        "VPN authentication",
        "failed authentication attempts",
    ]

    for query in queries:
        run_test(query)


if __name__ == "__main__":
    main()