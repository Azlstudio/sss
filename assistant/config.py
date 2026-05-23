import yaml
import os
from pathlib import Path
from typing import Any, Dict

class Config:
    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = config_file
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Load configuration from YAML file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.data = yaml.safe_load(f) or {}
        else:
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value with dot notation support (e.g., 'llm.model')."""
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value

    def __getitem__(self, key: str) -> Any:
        """Allow dict-like access."""
        return self.get(key)

    @property
    def llm_config(self) -> Dict[str, Any]:
        return self.data.get('llm', {})

    @property
    def memory_config(self) -> Dict[str, Any]:
        return self.data.get('memory', {})

    @property
    def embedding_config(self) -> Dict[str, Any]:
        return self.data.get('embeddings', {})

    @property
    def permissions_config(self) -> Dict[str, Any]:
        return self.data.get('permissions', {})

    @property
    def specialization_config(self) -> Dict[str, Any]:
        return self.data.get('specialization', {})

# Global config instance
_config = None

def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config
