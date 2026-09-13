from app.rag.faiss_index import build_faiss_index


def main() -> None:
    print("Building FAISS index...")

    metadata = build_faiss_index()

    print("FAISS index built successfully.")
    print("Embedding model:", metadata["embedding_model"])
    print("Dimensions:", metadata["dimension"])
    print("Vectors:", metadata["vector_count"])
    print("Metric:", metadata["metric"])


if __name__ == "__main__":
    main()