import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from ..config import get_config
from ..core.embedding_engine import EmbeddingEngine

class VectorStore:
    """Semantic memory using Chroma vector database."""

    def __init__(self):
        config = get_config()
        persist_dir = config.get('memory.vector_db.persist_directory', './brain/vectors')

        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_dir,
            anonymized_telemetry=False
        )

        self.client = chromadb.Client(settings)
        self.embedding_engine = EmbeddingEngine()

        # Create or get default collection
        self.collection = self.client.get_or_create_collection(
            name="knowledge",
            metadata={"hnsw:space": "cosine"}
        )

    def add(
        self,
        texts: List[str],
        metadata: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Add texts to vector store."""

        if ids is None:
            # Generate IDs from timestamp and content hash
            import hashlib
            ids = [hashlib.md5(f"{datetime.now().isoformat()}{i}{t}".encode()).hexdigest()
                   for i, t in enumerate(texts)]

        if metadata is None:
            metadata = [{"timestamp": datetime.now().isoformat()} for _ in texts]
        else:
            # Ensure all metadata dicts have timestamp
            for m in metadata:
                if "timestamp" not in m:
                    m["timestamp"] = datetime.now().isoformat()

        # Generate embeddings
        embeddings = self.embedding_engine.embed(texts)

        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadata
        )

        self.client.persist()
        return ids

    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        similarity_threshold: Optional[float] = None
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """
        Search for relevant memories.

        Returns:
            List of (text, similarity_score, metadata) tuples
        """

        config = get_config()
        if top_k is None:
            top_k = config.get('memory.retrieval.top_k', 5)
        if similarity_threshold is None:
            similarity_threshold = config.get('memory.retrieval.similarity_threshold', 0.6)

        query_embedding = self.embedding_engine.embed(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k * 2  # Get more to filter by threshold
        )

        memories = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i, doc in enumerate(results['documents'][0]):
                distance = results['distances'][0][i] if results['distances'] else 1.0
                # Convert distance to similarity (cosine distance to similarity)
                similarity = 1 - distance

                if similarity >= similarity_threshold:
                    metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                    memories.append((doc, similarity, metadata))

        return sorted(memories, key=lambda x: x[1], reverse=True)[:top_k]

    def update(self, ids: List[str], texts: List[str], metadata: Optional[List[Dict]] = None):
        """Update existing memories."""

        embeddings = self.embedding_engine.embed(texts)

        if metadata is None:
            metadata = [{"timestamp": datetime.now().isoformat()} for _ in texts]

        self.collection.update(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadata
        )

        self.client.persist()

    def delete(self, ids: List[str]):
        """Delete memories by ID."""
        self.collection.delete(ids=ids)
        self.client.persist()

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all stored memories."""
        results = self.collection.get()

        memories = []
        if results['ids']:
            for i, doc_id in enumerate(results['ids']):
                memories.append({
                    'id': doc_id,
                    'text': results['documents'][i] if results['documents'] else '',
                    'metadata': results['metadatas'][i] if results['metadatas'] else {}
                })

        return memories

    def clear(self):
        """Clear all memories."""
        self.client.delete_collection(name="knowledge")
        self.collection = self.client.get_or_create_collection(
            name="knowledge",
            metadata={"hnsw:space": "cosine"}
        )
        self.client.persist()

    def stats(self) -> Dict[str, Any]:
        """Get vector store statistics."""
        count = self.collection.count()
        return {
            'total_memories': count,
            'collection_name': 'knowledge'
        }
