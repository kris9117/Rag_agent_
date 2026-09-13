import re

from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_text_splitter() -> RecursiveCharacterTextSplitter:
    """Create the recursive splitter used for oversized sections."""

    return RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )


def split_documents(documents: list) -> list:
    """Split documents while preserving logical Markdown sections."""

    splitter = create_text_splitter()
    final_chunks = []

    for document in documents:
        source = document.metadata.get("source", "")
        document_id = document.metadata.get("document_id")
        category = document.metadata.get("category")

        text = document.page_content

        sections = re.split(
            r"(?m)^##\s+(.+)$",
            text,
        )

        if sections[0].strip():
            section_text = sections[0].strip()

            split_parts = splitter.split_text(section_text)

            for part in split_parts:
                final_chunks.append(
                    _build_chunk(
                        document=document,
                        text=part,
                        section="Introduction",
                        source=source,
                        document_id=document_id,
                        category=category,
                    )
                )

        for index in range(1, len(sections), 2):
            section_title = sections[index].strip()

            if index + 1 >= len(sections):
                break

            section_text = sections[index + 1].strip()

            if not section_text:
                continue

            split_parts = splitter.split_text(section_text)

            for part in split_parts:
                final_chunks.append(
                    _build_chunk(
                        document=document,
                        text=part,
                        section=section_title,
                        source=source,
                        document_id=document_id,
                        category=category,
                    )
                )

    return final_chunks


def _build_chunk(
    document: object,
    text: str,
    section: str,
    source: str,
    document_id: str,
    category: str,
) -> object:
    """Create a chunk while preserving retrieval metadata."""

    from langchain_core.documents import Document

    metadata = dict(document.metadata)

    metadata.update(
        {
            "document_id": document_id,
            "category": category,
            "section": section,
            "source": source,
            "chunk_source": "internal_kb",
        }
    )

    return Document(
        page_content=text,
        metadata=metadata,
    )