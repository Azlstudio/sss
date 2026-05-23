from typing import Dict, List, Any
from .llm_client import LLMClient
from ..config import get_config

class ReasoningEngine:
    """Implements chain-of-thought reasoning for step-by-step analysis."""

    def __init__(self):
        self.llm = LLMClient()
        config = get_config()
        self.system_prompt = config.get('system_prompts.reasoning', '')

    def reason(self, query: str, context: str = "", verbose: bool = False) -> Dict[str, Any]:
        """
        Perform step-by-step reasoning.

        Returns:
            {
                'thinking': str,  # reasoning steps
                'analysis': str,  # detailed analysis
                'answer': str,    # final answer
                'facts_to_store': List[str]  # new facts discovered
            }
        """

        reasoning_prompt = f"""
{self.system_prompt}

CONTEXT FROM MEMORY:
{context if context else "No relevant memories found."}

USER QUERY:
{query}

Please think through this step by step:
1. What is the core question?
2. What relevant knowledge do I have?
3. What approach should I take?
4. What is my analysis?
5. What is the final answer?
6. What facts should I remember?

Format your response as:
THINKING: [your step-by-step reasoning]
ANALYSIS: [detailed analysis]
ANSWER: [final answer]
FACTS TO REMEMBER: [comma-separated list of key facts]
"""

        response = self.llm.generate(
            reasoning_prompt,
            system_prompt=None,
            max_tokens=3000
        )

        if "ERROR:" in response:
            return {
                'thinking': '',
                'analysis': '',
                'answer': response,
                'facts_to_store': []
            }

        # Parse response
        sections = {
            'thinking': '',
            'analysis': '',
            'answer': '',
            'facts_to_store': []
        }

        for line in response.split('\n'):
            if line.startswith('THINKING:'):
                sections['thinking'] = line.replace('THINKING:', '').strip()
            elif line.startswith('ANALYSIS:'):
                sections['analysis'] = line.replace('ANALYSIS:', '').strip()
            elif line.startswith('ANSWER:'):
                sections['answer'] = line.replace('ANSWER:', '').strip()
            elif line.startswith('FACTS TO REMEMBER:'):
                facts_str = line.replace('FACTS TO REMEMBER:', '').strip()
                sections['facts_to_store'] = [f.strip() for f in facts_str.split(',') if f.strip()]

        if verbose:
            print("\n=== REASONING TRACE ===")
            print(f"Thinking: {sections['thinking']}")
            print(f"Analysis: {sections['analysis']}")
            print(f"Facts: {sections['facts_to_store']}")
            print("=" * 50)

        return sections

    def evaluate_relevance(self, query: str, memory_items: List[str], threshold: float = 0.6) -> List[str]:
        """Filter memory items by relevance to query."""

        if not memory_items:
            return []

        evaluation_prompt = f"""
Given this user query: "{query}"

Evaluate which of these memory items are relevant (score 0-1):
{chr(10).join(f'{i+1}. {item}' for i, item in enumerate(memory_items))}

Return only the numbers of relevant items (threshold: {threshold}).
Format: [1, 3, 5] (without explanation)
"""

        response = self.llm.generate(evaluation_prompt, max_tokens=100)

        try:
            # Parse the response to extract relevant indices
            import re
            matches = re.findall(r'\d+', response)
            relevant_indices = [int(m) - 1 for m in matches if int(m) - 1 < len(memory_items)]
            return [memory_items[i] for i in relevant_indices]
        except:
            return memory_items  # Return all if parsing fails
