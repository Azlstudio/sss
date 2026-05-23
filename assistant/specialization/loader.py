from typing import Dict, List
from .fivem_kb import FiveMLLMKnowledge
from .mta_kb import MTAKnowledge
from .design_patterns import DesignPatterns
from ..config import get_config

class SpecializationLoader:
    """Load and manage specialization domains."""

    DOMAINS = {
        'fivem': FiveMLLMKnowledge,
        'qbcore': FiveMLLMKnowledge,  # QBCore is FiveM-based
        'esx': FiveMLLMKnowledge,     # ESX is FiveM-based
        'mta': MTAKnowledge,
        'design': DesignPatterns,
        'programming': DesignPatterns  # Reuse design patterns for general programming
    }

    def __init__(self):
        config = get_config()
        self.enabled_domains = config.get('specialization.domains', list(self.DOMAINS.keys()))

    def get_system_prompt(self, domain: str) -> str:
        """Get system prompt for a domain."""
        domain_lower = domain.lower()

        if domain_lower in self.DOMAINS:
            kb_class = self.DOMAINS[domain_lower]
            if hasattr(kb_class, 'SYSTEM_PROMPT'):
                return kb_class.SYSTEM_PROMPT

        return "You are a helpful AI assistant."

    def get_context(self, domain: str, topic: str = None) -> str:
        """Get specialized context for a topic in a domain."""
        domain_lower = domain.lower()

        if domain_lower not in self.DOMAINS:
            return f"Domain '{domain}' not found."

        kb_class = self.DOMAINS[domain_lower]

        if domain_lower in ['fivem', 'qbcore', 'esx']:
            if topic == 'frameworks':
                return kb_class.get_framework_info(domain_lower)
            elif topic:
                return kb_class.get_pattern(topic)

        elif domain_lower == 'mta':
            return kb_class.get_concept(topic) if topic else ""

        elif domain_lower == 'design':
            return kb_class.get_principle(topic) if topic else ""

        return ""

    def get_available_domains(self) -> List[str]:
        """Get list of available domains."""
        return list(self.DOMAINS.keys())

    def get_domain_info(self, domain: str) -> Dict:
        """Get information about a domain."""
        domain_lower = domain.lower()

        if domain_lower not in self.DOMAINS:
            return {'error': f"Domain '{domain}' not found."}

        kb_class = self.DOMAINS[domain_lower]

        return {
            'domain': domain_lower,
            'system_prompt': kb_class.SYSTEM_PROMPT if hasattr(kb_class, 'SYSTEM_PROMPT') else '',
            'has_knowledge_base': hasattr(kb_class, 'KNOWLEDGE_BASE')
        }

    def load_training_data(self, directory: str) -> Dict[str, List[str]]:
        """Load custom training data from files."""
        import os
        from pathlib import Path

        training_data = {}

        if not os.path.isdir(directory):
            return training_data

        for domain in os.listdir(directory):
            domain_path = os.path.join(directory, domain)
            if os.path.isdir(domain_path):
                files = []
                for filename in os.listdir(domain_path):
                    if filename.endswith(('.md', '.txt', '.lua', '.py', '.js')):
                        filepath = os.path.join(domain_path, filename)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                files.append(f.read())
                        except:
                            pass

                if files:
                    training_data[domain] = files

        return training_data

    @staticmethod
    def format_specialization_context(domain: str, context: str, query: str) -> str:
        """Format context for LLM with specialization."""
        loader = SpecializationLoader()
        system_prompt = loader.get_system_prompt(domain)

        return f"""{system_prompt}

SPECIALIZATION: {domain.upper()}

RELEVANT KNOWLEDGE:
{context}

USER QUERY: {query}

Respond with expertise in {domain} domain, referencing patterns and best practices where applicable."""
