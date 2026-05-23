from typing import Optional, Dict, Any
import os
from .config import get_config
from .core import LLMClient, EmbeddingEngine, ReasoningEngine
from .memory import MemoryManager
from .tools import FileTool, CodeAnalyzer, MemoryTool
from .specialization import SpecializationLoader

class LocalAIAssistant:
    """
    Fully local AI assistant with persistent memory and specialization.

    Core components:
    - Local LLM inference (via Ollama)
    - Semantic memory (vector embeddings)
    - Fact storage (SQLite)
    - Conversation history
    - Code analysis
    - Multi-domain specialization
    """

    def __init__(self, config_file: str = "config.yaml"):
        print("🚀 Initializing LocalAI Assistant...")

        self.config = get_config()
        self.llm = LLMClient()
        self.embeddings = EmbeddingEngine()
        self.reasoning = ReasoningEngine()
        self.memory = MemoryManager()
        self.file_tool = FileTool()
        self.code_analyzer = CodeAnalyzer()
        self.memory_tool = MemoryTool(self.memory)
        self.specialization = SpecializationLoader()

        # Check if LLM is available
        if not self.llm.is_available():
            print("⚠️  WARNING: Ollama not running. Start with: ollama serve")
            print("📌 Recommended models: mistral, llama2, neural-chat")

        print("✅ Assistant initialized successfully!")
        self._print_status()

    def chat(self, query: str, domain: str = "general", verbose: bool = False) -> Dict[str, Any]:
        """
        Process a user query with full context retrieval and reasoning.

        Args:
            query: User's input question/command
            domain: Specialization domain (fivem, mta, programming, design, general)
            verbose: Print reasoning steps

        Returns:
            Dict with 'response', 'thinking', 'sources', etc.
        """

        print(f"\n🤔 Processing: {query}")

        # Step 1: Retrieve context from memory
        context = self.memory.retrieve_context(query, include_conversation=True)

        # Step 2: Specialization context
        specialization_context = self.specialization.get_context(domain)
        if specialization_context:
            context += f"\n\nDOMAIN EXPERTISE ({domain.upper()}):\n{specialization_context}"

        # Step 3: Get system prompt with specialization
        system_prompt = self.specialization.get_system_prompt(domain)

        # Step 4: Step-by-step reasoning
        reasoning = self.reasoning.reason(query, context, verbose=verbose)

        # Step 5: Generate response
        response_prompt = f"""
Based on your thinking and analysis, provide a comprehensive response to the user's query.

USER QUERY: {query}

YOUR THINKING:
{reasoning['thinking']}

YOUR ANALYSIS:
{reasoning['analysis']}

Now provide a clear, helpful response that:
1. Directly answers the question
2. References relevant memories/facts when applicable
3. Provides examples or code if relevant
4. Offers next steps or related information
"""

        response = self.llm.generate(
            response_prompt,
            system_prompt=system_prompt,
            max_tokens=2000
        )

        # Step 6: Update memory with new knowledge
        self.memory.update_from_response(query, response)
        self.memory.add_conversation_turn('user', query)
        self.memory.add_conversation_turn('assistant', response)

        # Extract domain from query for logging
        if domain == 'general':
            domain = self._detect_domain(query)

        return {
            'query': query,
            'response': response,
            'thinking': reasoning['thinking'],
            'analysis': reasoning['analysis'],
            'facts_learned': reasoning['facts_to_store'],
            'domain': domain,
            'memory_context_used': len(context.split('\n')) if context else 0
        }

    def learn_from_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze and learn from a code file."""

        print(f"📚 Learning from: {filepath}")

        content = self.file_tool.read(filepath)
        if content.startswith("ERROR"):
            return {'error': content}

        # Analyze file
        analysis = self.code_analyzer.analyze_file(filepath)

        # Extract knowledge
        knowledge = self.code_analyzer.extract_knowledge(filepath)

        # Store in memory
        for item in knowledge:
            self.memory.store_memory(item, memory_type='general')

        print(f"✅ Learned {len(knowledge)} facts from {filepath}")

        return {
            'filepath': filepath,
            'analysis': analysis,
            'facts_extracted': knowledge,
            'stored_count': len(knowledge)
        }

    def learn_from_project(self, project_path: str, name: str = None) -> Dict[str, Any]:
        """Analyze entire project and learn from it."""

        print(f"📂 Analyzing project: {project_path}")

        if not os.path.isdir(project_path):
            return {'error': f"Directory not found: {project_path}"}

        if name is None:
            name = os.path.basename(project_path)

        # Analyze project structure
        analysis = self.code_analyzer.analyze_project(project_path)

        # Get all code files
        files = self.file_tool.search_files(project_path)
        code_files = [f for f in files if os.path.splitext(f)[1] in
                      ['.py', '.lua', '.js', '.ts', '.cpp', '.c', '.h']]

        # Learn from each file
        total_facts = 0
        for code_file in code_files[:20]:  # Limit to 20 files for performance
            knowledge = self.code_analyzer.extract_knowledge(code_file)
            total_facts += len(knowledge)
            for item in knowledge:
                self.memory.store_memory(item, memory_type='general')

        # Store project metadata
        self.memory_tool.learn_project(
            name=name,
            path=project_path,
            language=self._detect_project_language(analysis),
            description=f"Project with {len(code_files)} code files"
        )

        print(f"✅ Learned from {len(code_files)} files, extracted {total_facts} facts")

        return {
            'project': name,
            'files_analyzed': len(code_files),
            'facts_extracted': total_facts,
            'structure': analysis['structure']
        }

    def remember_preference(self, key: str, value: str):
        """Store a user preference."""
        self.memory_tool.remember_preference(key, value)
        print(f"💾 Remembered: {key} = {value}")

    def get_preference(self, key: str) -> Optional[str]:
        """Retrieve a user preference."""
        return self.memory_tool.get_preference(key)

    def memory_status(self) -> Dict[str, Any]:
        """Get memory system statistics."""
        return self.memory.get_memory_stats()

    def clear_memory(self, confirm: bool = False):
        """Clear all memory (careful!)."""
        if not confirm:
            response = input("⚠️  This will delete ALL memories. Type 'YES' to confirm: ")
            if response != 'YES':
                print("Cancelled.")
                return

        self.memory.clear_all()
        print("🗑️  All memory cleared.")

    def export_memory(self, output_dir: str = "./memory_export"):
        """Export all memory to files."""
        self.memory.export_memory(output_dir)
        print(f"📤 Memory exported to {output_dir}")

    def _detect_domain(self, query: str) -> str:
        """Detect domain from query keywords."""
        query_lower = query.lower()

        if any(kw in query_lower for kw in ['fivem', 'qbcore', 'esx', 'gta']):
            return 'fivem'
        elif any(kw in query_lower for kw in ['mta', 'san andreas', 'gta:sa']):
            return 'mta'
        elif any(kw in query_lower for kw in ['design', 'ui', 'ux', 'layout', 'color']):
            return 'design'
        elif any(kw in query_lower for kw in ['code', 'function', 'class', 'api']):
            return 'programming'
        else:
            return 'general'

    def _detect_project_language(self, analysis: Dict) -> Optional[str]:
        """Detect primary language from project analysis."""
        files_by_type = analysis.get('files_by_type', {})
        if not files_by_type:
            return None

        # Find most common language
        max_type = max(files_by_type.items(), key=lambda x: len(x[1]))
        ext = max_type[0]

        lang_map = {
            '.py': 'Python',
            '.lua': 'Lua',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.cpp': 'C++',
            '.c': 'C'
        }

        return lang_map.get(ext)

    def _print_status(self):
        """Print system status."""
        stats = self.memory_status()

        print("\n" + "="*60)
        print("📊 MEMORY STATUS")
        print("="*60)
        print(f"  Vector Memories: {stats['vector_store'].get('total_memories', 0)}")
        print(f"  Stored Facts: {stats['fact_store'].get('facts', 0)}")
        print(f"  Projects Known: {stats['fact_store'].get('projects', 0)}")
        print(f"  Interactions: {stats['fact_store'].get('interactions', 0)}")
        print(f"  Specializations: {', '.join(self.specialization.get_available_domains())}")
        print("="*60 + "\n")

    def __repr__(self) -> str:
        return f"<LocalAIAssistant v{get_config().get('assistant.version')}>"
