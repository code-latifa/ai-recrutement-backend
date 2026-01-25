from typing import List
from openai import OpenAI

from app.core.config import settings


# Client OpenAI (1 seule instance)
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def embed_text(text: str) -> List[float]:
    """
    Génère l'embedding d'un seul texte
    """
    if not text or not text.strip():
        raise ValueError("Texte vide pour embedding")

    response = client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Génère les embeddings pour plusieurs textes
    """
    if not texts:
        return []

    response = client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=texts
    )

    return [item.embedding for item in response.data]
