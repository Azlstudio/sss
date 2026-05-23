import requests
import json
from typing import Dict, Any, Optional, List
from ..config import get_config

class LLMClient:
    """Interface with Ollama for local LLM inference."""

    def __init__(self):
        config = get_config()
        self.base_url = config.get('llm.base_url')
        self.model = config.get('llm.model', 'mistral')
        self.params = config.get('llm.parameters', {})

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> str:
        """Generate response from local LLM."""

        if temperature is None:
            temperature = self.params.get('temperature', 0.7)
        if max_tokens is None:
            max_tokens = self.params.get('max_tokens', 2048)

        # Build message context
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "top_p": self.params.get('top_p', 0.9),
            "top_k": self.params.get('top_k', 40),
            "num_predict": max_tokens,
            "stream": stream
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=120
            )
            response.raise_for_status()

            if stream:
                return self._handle_stream(response)
            else:
                result = response.json()
                return result['message']['content']

        except requests.exceptions.ConnectionError:
            return f"ERROR: Cannot connect to Ollama at {self.base_url}. Is it running?"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _handle_stream(self, response) -> str:
        """Handle streaming responses."""
        full_response = ""
        try:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        full_response += content
                        print(content, end='', flush=True)
        except Exception as e:
            print(f"ERROR: {str(e)}")
        return full_response

    def embed(self, text: str) -> Optional[List[float]]:
        """Generate embedding using Ollama's embedding API."""
        payload = {
            "model": self.model,
            "prompt": text
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result.get('embedding')
        except Exception as e:
            print(f"Embedding error: {str(e)}")
            return None

    def is_available(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
