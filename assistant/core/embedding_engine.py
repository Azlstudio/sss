from sentence_transformers import SentenceTransformer
from typing import List
from ..config import get_config

class EmbeddingEngine:
    """Generate embeddings locally using sentence-transformers."""

    def __init__(self):
        config = get_config()
        model_name = config.get('embeddings.model', 'sentence-transformers/all-MiniLM-L6-v2')
        device = config.get('embeddings.device', 'cpu')

        print(f"Loading embedding model: {model_name} on {device}...")
        self.model = SentenceTransformer(model_name, device=device)

    def embed(self, texts: str | List[str]) -> List[float] | List[List[float]]:
        """
        Generate embedding(s) for text(s).

        Args:
            texts: Single string or list of strings

        Returns:
            Single embedding or list of embeddings
        """
        if isinstance(texts, str):
            return self.model.encode(texts, convert_to_tensor=False).tolist()
        else:
            return self.model.encode(texts, convert_to_tensor=False).tolist()

    def similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two texts."""
        embeddings = self.model.encode([text1, text2])
        return float((embeddings[0] @ embeddings[1]) /
                    (sum(embeddings[0]**2)**0.5 * sum(embeddings[1]**2)**0.5))

    def batch_similarity(self, query: str, texts: List[str]) -> List[tuple]:
        """
        Compute similarity between query and multiple texts.

        Returns:
            List of (text, similarity_score) tuples sorted by score
        """
        query_embedding = self.model.encode(query)
        text_embeddings = self.model.encode(texts)

        similarities = []
        for i, text in enumerate(texts):
            sim = float((query_embedding @ text_embeddings[i]) /
                       (sum(query_embedding**2)**0.5 * sum(text_embeddings[i]**2)**0.5))
            similarities.append((text, sim))

        return sorted(similarities, key=lambda x: x[1], reverse=True)
