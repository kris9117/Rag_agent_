from app.rag.chunker import split_documents
from app.rag.loaders import load_all_documents
from app.rag.metadata import enrich_metadata


def main() -> None:
    print("Loading documents...")

    documents = load_all_documents()

    print(f"Documents/pages loaded: {len(documents)}")

    documents = enrich_metadata(documents)

    chunks = split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    for index, chunk in enumerate(chunks[:10], start=1):
        print("\n" + "=" * 70)
        print(f"Chunk {index}")
        print(f"Document ID: {chunk.metadata.get('document_id')}")
        print(f"Category: {chunk.metadata.get('category')}")
        print(f"Source type: {chunk.metadata.get('source_type')}")
        print(f"Page: {chunk.metadata.get('page')}")
        print(f"Characters: {len(chunk.page_content)}")
        print("-" * 70)
        print(chunk.page_content[:500])


if __name__ == "__main__":
    main()