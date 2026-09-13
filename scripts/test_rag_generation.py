from app.rag.rag_service import RAGService
from app.services.llm_service import LLMService


def run_test(
    query: str,
    rag_service: RAGService,
    llm_service: LLMService,
) -> None:
    print("=" * 80)
    print("QUERY:", query)
    print("=" * 80)

    retrieved_context = rag_service.retrieve(
        query=query,
        candidate_k=10,
        top_k=5,
    )

    print("\nRetrieved sources:")

    for item in retrieved_context:
        metadata = item.get("metadata", {})

        print(
            f"- {metadata.get('document_id')} | "
            f"{metadata.get('section')} | "
            f"rerank_score={item.get('rerank_score'):.4f}"
        )

    response = llm_service.generate_rag_response(
        query=query,
        retrieved_context=retrieved_context,
    )

    print("\nGenerated response:")
    print(response)
    print()


def main() -> None:
    rag_service = RAGService()
    llm_service = LLMService()

    run_test(
        "My VPN authentication keeps failing.",
        rag_service,
        llm_service,
    )

    run_test(
        "How should I report a phishing email?",
        rag_service,
        llm_service,
    )


if __name__ == "__main__":
    main()