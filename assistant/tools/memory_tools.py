from typing import List, Dict, Any
from ..memory import MemoryManager

class MemoryTool:
    """Tools for managing and querying memory."""

    def __init__(self, memory_manager: MemoryManager):
        self.memory = memory_manager

    def learn_from_text(self, text: str, source: str = "user_input"):
        """Learn facts from provided text."""

        facts = self.memory.extract_facts(text)

        for fact in facts:
            self.memory.store_memory(
                fact,
                memory_type='fact',
                metadata={'source': source}
            )

        return {
            'extracted_facts': facts,
            'stored_count': len(facts)
        }

    def remember_preference(self, key: str, value: str) -> bool:
        """Store user preference."""
        self.memory.store_memory(
            f"{key}:{value}",
            memory_type='preference'
        )
        return True

    def get_preference(self, key: str) -> Any:
        """Retrieve user preference."""
        return self.memory.fact_store.get_preference(key)

    def learn_project(self, name: str, path: str, language: str = None, description: str = None):
        """Learn about a code project."""

        self.memory.fact_store.add_project(
            name=name,
            path=path,
            language=language,
            description=description
        )

        return {
            'project': name,
            'stored': True
        }

    def recall(self, query: str) -> str:
        """Recall relevant memories for a query."""
        return self.memory.retrieve_context(query)

    def get_memories(self) -> List[Dict[str, Any]]:
        """Get all stored memories."""
        return self.memory.vector_store.get_all()

    def forget(self, memory_id: str) -> bool:
        """Delete a specific memory."""
        try:
            self.memory.vector_store.delete([memory_id])
            return True
        except:
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        return self.memory.get_memory_stats()

    def export_memories(self, output_dir: str):
        """Export all memories."""
        self.memory.export_memory(output_dir)
