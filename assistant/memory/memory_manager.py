from typing import List, Dict, Any, Tuple
from .vector_store import VectorStore
from .fact_store import FactStore
from .conversation import ConversationHistory
from ..config import get_config

class MemoryManager:
    """Unified interface for all memory systems."""

    def __init__(self):
        self.vector_store = VectorStore()
        self.fact_store = FactStore()
        self.conversation = ConversationHistory()
        config = get_config()
        self.similarity_threshold = config.get('memory.retrieval.similarity_threshold', 0.6)

    def retrieve_context(self, query: str, include_conversation: bool = True) -> str:
        """
        Retrieve relevant context for answering a query.

        Combines semantic search + facts + conversation history.
        """

        context_parts = []

        # Semantic search from vector store
        semantic_results = self.vector_store.search(query, top_k=5)
        if semantic_results:
            context_parts.append("RELEVANT MEMORIES:")
            for text, score, metadata in semantic_results:
                context_parts.append(f"- {text} (relevance: {score:.2f})")

        # Get related facts
        # Simple keyword extraction to search facts
        keywords = query.split()
        context_parts.append("\nRELATED FACTS:")
        for keyword in keywords[:3]:  # Search by first 3 words
            facts = self.fact_store.get_facts(subject=keyword)
            for fact in facts[:3]:
                context_parts.append(
                    f"- {fact['subject']} {fact['predicate']} {fact['object']}"
                )

        # Include recent conversation if enabled
        if include_conversation:
            recent = self.conversation.get_context(max_messages=10)
            context_parts.append(f"\n{recent}")

        return "\n".join(context_parts)

    def store_memory(
        self,
        content: str,
        memory_type: str = "general",
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Store new memory in appropriate system.

        memory_type: 'general', 'fact', 'preference', 'project'
        """

        if metadata is None:
            metadata = {}

        metadata['type'] = memory_type

        memory_id = None

        if memory_type == 'general':
            ids = self.vector_store.add([content], [metadata])
            memory_id = ids[0]

        elif memory_type == 'fact':
            # Parse as triple (subject, predicate, object)
            parts = content.split('|')
            if len(parts) >= 3:
                subject, predicate, obj = parts[0].strip(), parts[1].strip(), parts[2].strip()
                self.fact_store.add_fact(subject, predicate, obj, source=metadata.get('source'))
                memory_id = f"fact_{subject}_{predicate}"
            else:
                # Store as general if can't parse
                ids = self.vector_store.add([content], [metadata])
                memory_id = ids[0]

        elif memory_type == 'preference':
            # Parse as key:value
            if ':' in content:
                key, value = content.split(':', 1)
                self.fact_store.set_preference(key.strip(), value.strip())
                memory_id = f"pref_{key.strip()}"

        elif memory_type == 'project':
            # metadata should contain name, path, language, description
            self.fact_store.add_project(
                name=metadata.get('name', 'unknown'),
                path=metadata.get('path', ''),
                language=metadata.get('language'),
                description=metadata.get('description')
            )
            memory_id = f"proj_{metadata.get('name')}"

        return memory_id

    def extract_facts(self, text: str) -> List[str]:
        """
        Extract key facts from text.
        (In a real system, you'd use NLP/LLM for this)
        """

        facts = []

        # Simple extraction: look for common patterns
        import re

        # Pattern: "X is Y" or "X are Y"
        is_pattern = re.findall(r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:is|are)\s+([^.!?]+)', text)
        for subject, obj in is_pattern:
            facts.append(f"{subject.strip()}|is|{obj.strip()}")

        # Pattern: "X has Y" or "X have Y"
        has_pattern = re.findall(r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:has|have)\s+([^.!?]+)', text)
        for subject, obj in has_pattern:
            facts.append(f"{subject.strip()}|has|{obj.strip()}")

        return facts

    def update_from_response(self, query: str, response: str, was_helpful: bool = True):
        """Update memory after successful response."""

        # Log interaction
        self.fact_store.log_interaction(query, response, was_helpful=int(was_helpful))

        # Extract and store new facts from response
        facts = self.extract_facts(response)
        for fact in facts:
            self.store_memory(fact, memory_type='fact', metadata={'source': 'response'})

        # Store the Q&A as semantic memory
        qa_memory = f"Q: {query}\nA: {response}"
        self.store_memory(qa_memory, memory_type='general', metadata={'source': 'qa_pair'})

    def add_conversation_turn(self, role: str, content: str):
        """Add turn to conversation history."""
        self.conversation.add_message(role, content)

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get overall memory statistics."""
        return {
            'vector_store': self.vector_store.stats(),
            'fact_store': self.fact_store.stats(),
            'conversation': self.conversation.stats()
        }

    def clear_all(self):
        """Clear all memory (use with caution!)."""
        self.vector_store.clear()
        self.conversation.clear()
        self.fact_store.conn.execute("DELETE FROM facts")
        self.fact_store.conn.execute("DELETE FROM preferences")
        self.fact_store.conn.execute("DELETE FROM projects")
        self.fact_store.conn.execute("DELETE FROM interactions")
        self.fact_store.conn.commit()

    def export_memory(self, output_dir: str):
        """Export all memory to files."""
        import os
        os.makedirs(output_dir, exist_ok=True)

        # Export vector memories
        with open(f"{output_dir}/vector_memories.json", 'w') as f:
            import json
            memories = self.vector_store.get_all()
            json.dump(memories, f, indent=2)

        # Export conversation
        self.conversation.export(f"{output_dir}/conversation.txt")

        # Export conversation as JSON
        with open(f"{output_dir}/conversation.json", 'w') as f:
            import json
            json.dump(self.conversation.messages, f, indent=2)

        print(f"Memory exported to {output_dir}")
