from openai import OpenAI

from app.config import get_settings


class EmbeddingService:
    """Generate embeddings using the configured OpenAI embedding model."""

    def __init__(self) -> None:
        settings = get_settings()

        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured.")

        if not settings.openai_embedding_model:
            raise RuntimeError(
                "OPENAI_EMBEDDING_MODEL is not configured."
            )

        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_embedding_model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""

        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return [item.embedding for item in response.data]

    def embed_query(self, query: str) -> list[float]:
        """Generate an embedding for a single query."""

        embeddings = self.embed_texts([query])

        return embeddings[0]