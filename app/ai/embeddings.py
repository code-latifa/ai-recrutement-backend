from typing import List
from sentence_transformers import SentenceTransformer

# Modèle local (1 seule instance)
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str) -> List[float]:
    """
    Génère l'embedding d'un seul texte (LOCAL)
    """
    if not text or not text.strip():
        raise ValueError("Texte vide pour embedding")

    return model.encode(text).tolist()


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Génère les embeddings pour plusieurs textes (LOCAL)
    """
    if not texts:
        return []

    return model.encode(texts).tolist()
