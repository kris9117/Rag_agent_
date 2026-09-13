from pathlib import Path


def enrich_metadata(documents: list) -> list:
    """Normalize and enrich metadata for retrieval."""

    enriched = []

    for index, document in enumerate(documents):
        source = document.metadata.get("source", "")
        source_path = Path(source)

        category = source_path.parent.name
        document_id = source_path.stem

        document.metadata.update(
            {
                "document_id": document_id,
                "category": category,
                "source_type": source_path.suffix.lower().lstrip("."),
                "chunk_source": "internal_kb",
            }
        )

        document.metadata["document_index"] = index

        enriched.append(document)

    return enriched