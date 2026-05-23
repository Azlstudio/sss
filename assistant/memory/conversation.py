import json
import os
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
from ..config import get_config

class ConversationHistory:
    """Manage conversation history and context."""

    def __init__(self):
        config = get_config()
        self.history_path = config.get('memory.conversation.history_path', './brain/conversations')
        self.max_context = config.get('memory.conversation.max_context_messages', 20)

        Path(self.history_path).mkdir(parents=True, exist_ok=True)

        self.current_session_file = os.path.join(
            self.history_path,
            f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        self.messages: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """Add message to current conversation."""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.messages.append(message)
        self._save()

    def get_context(self, max_messages: int = None) -> str:
        """Get last N messages as formatted context."""
        if max_messages is None:
            max_messages = self.max_context

        recent = self.messages[-max_messages:]

        context = "RECENT CONVERSATION:\n"
        for msg in recent:
            context += f"{msg['role'].upper()}: {msg['content']}\n\n"

        return context

    def get_messages(self, max_messages: int = None) -> List[Dict[str, Any]]:
        """Get last N messages."""
        if max_messages is None:
            max_messages = self.max_context

        return self.messages[-max_messages:]

    def clear(self):
        """Clear current session."""
        self.messages = []
        self._save()

    def _save(self):
        """Save current conversation to file."""
        with open(self.current_session_file, 'w') as f:
            json.dump(self.messages, f, indent=2)

    def load_session(self, session_file: str):
        """Load previous conversation session."""
        if os.path.exists(session_file):
            with open(session_file, 'r') as f:
                self.messages = json.load(f)

    def get_all_sessions(self) -> List[str]:
        """List all saved conversation sessions."""
        if not os.path.exists(self.history_path):
            return []

        sessions = [f for f in os.listdir(self.history_path) if f.startswith('session_')]
        return sorted(sessions, reverse=True)

    def export(self, output_file: str):
        """Export current conversation to text file."""
        with open(output_file, 'w') as f:
            for msg in self.messages:
                f.write(f"{msg['role'].upper()}: {msg['content']}\n\n")

    def stats(self) -> Dict[str, Any]:
        """Get conversation statistics."""
        user_messages = [m for m in self.messages if m['role'] == 'user']
        assistant_messages = [m for m in self.messages if m['role'] == 'assistant']

        return {
            'total_messages': len(self.messages),
            'user_messages': len(user_messages),
            'assistant_messages': len(assistant_messages),
            'total_tokens_estimate': sum(len(m['content'].split()) for m in self.messages),
            'session_file': self.current_session_file
        }
