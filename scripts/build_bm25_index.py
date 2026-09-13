from app.rag.bm25_retriever import build_bm25_index


def main() -> None:
    print("Building BM25 index...")

    metadata = build_bm25_index()

    print("BM25 index built successfully.")
    print("Retriever:", metadata["retriever"])
    print("Chunks:", metadata["chunk_count"])


if __name__ == "__main__":
    main()