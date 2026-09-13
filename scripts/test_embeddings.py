from app.rag.embedding_service import EmbeddingService


def main() -> None:
    service = EmbeddingService()

    text = "Employees cannot connect to the corporate VPN."

    embedding = service.embed_query(text)

    print("Embedding generated successfully.")
    print("Model:", service.model)
    print("Dimensions:", len(embedding))
    print("First 5 values:", embedding[:5])


if __name__ == "__main__":
    main()