from app.rag.faiss_retriever import FAISSRetriever


def run_query(retriever: FAISSRetriever, query: str) -> None:
    print("\n" + "=" * 70)
    print("QUERY:", query)
    print("=" * 70)

    results = retriever.search(
        query=query,
        top_k=5,
    )

    for rank, result in enumerate(results, start=1):
        print(f"\n--- Rank {rank} ---")
        print(f"Score: {result['score']:.4f}")
        print(f"Document: {result['metadata'].get('document_id')}")
        print(f"Category: {result['metadata'].get('category')}")
        print(f"Section: {result['metadata'].get('section')}")
        print(f"Text: {result['text'][:300]}")


def main() -> None:
    retriever = FAISSRetriever()

    run_query(
        retriever,
        "How do I recover a locked employee account?"
    )

    run_query(
        retriever,
        "My VPN authentication keeps failing."
    )

    run_query(
        retriever,
        "My laptop has a network connection problem."
    )


if __name__ == "__main__":
    main()