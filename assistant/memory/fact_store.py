import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..config import get_config

class FactStore:
    """Structured knowledge storage using SQLite."""

    def __init__(self):
        config = get_config()
        self.db_path = config.get('memory.fact_store.path', './brain/facts/knowledge.db')

        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        """Initialize database schema."""
        cursor = self.conn.cursor()

        # Facts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                predicate TEXT NOT NULL,
                object TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                source TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(subject, predicate, object)
            )
        ''')

        # Preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Projects table (for workspace scanning)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                path TEXT NOT NULL,
                language TEXT,
                description TEXT,
                last_scanned TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Interactions table (for learning)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                response TEXT,
                was_helpful INTEGER,
                domain TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def add_fact(self, subject: str, predicate: str, obj: str, confidence: float = 1.0, source: str = None):
        """Add a fact (subject-predicate-object triple)."""
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                '''INSERT OR REPLACE INTO facts (subject, predicate, object, confidence, source)
                   VALUES (?, ?, ?, ?, ?)''',
                (subject, predicate, obj, confidence, source or 'user_input')
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def add_facts(self, facts: List[tuple]):
        """Add multiple facts. Each tuple: (subject, predicate, object, confidence, source)."""
        cursor = self.conn.cursor()

        for fact in facts:
            subject, predicate, obj = fact[0], fact[1], fact[2]
            confidence = fact[3] if len(fact) > 3 else 1.0
            source = fact[4] if len(fact) > 4 else 'batch'

            try:
                cursor.execute(
                    '''INSERT OR REPLACE INTO facts (subject, predicate, object, confidence, source)
                       VALUES (?, ?, ?, ?, ?)''',
                    (subject, predicate, obj, confidence, source)
                )
            except sqlite3.IntegrityError:
                pass

        self.conn.commit()

    def get_facts(self, subject: Optional[str] = None, predicate: Optional[str] = None) -> List[Dict]:
        """Query facts."""
        cursor = self.conn.cursor()

        query = "SELECT * FROM facts WHERE 1=1"
        params = []

        if subject:
            query += " AND subject = ?"
            params.append(subject)
        if predicate:
            query += " AND predicate = ?"
            params.append(predicate)

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def set_preference(self, key: str, value: str):
        """Store user preference."""
        cursor = self.conn.cursor()
        cursor.execute(
            '''INSERT OR REPLACE INTO preferences (key, value)
               VALUES (?, ?)''',
            (key, value)
        )
        self.conn.commit()

    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        """Retrieve user preference."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row['value'] if row else default

    def add_project(self, name: str, path: str, language: str = None, description: str = None):
        """Store project information."""
        cursor = self.conn.cursor()
        cursor.execute(
            '''INSERT OR REPLACE INTO projects (name, path, language, description, last_scanned)
               VALUES (?, ?, ?, ?, ?)''',
            (name, path, language, description, datetime.now().isoformat())
        )
        self.conn.commit()

    def get_projects(self) -> List[Dict]:
        """Get all stored projects."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects")
        return [dict(row) for row in cursor.fetchall()]

    def log_interaction(self, query: str, response: str, was_helpful: int = None, domain: str = None):
        """Log an interaction for learning."""
        cursor = self.conn.cursor()
        cursor.execute(
            '''INSERT INTO interactions (query, response, was_helpful, domain)
               VALUES (?, ?, ?, ?)''',
            (query, response, was_helpful, domain or 'general')
        )
        self.conn.commit()

    def get_interaction_history(self, domain: str = None, limit: int = 100) -> List[Dict]:
        """Get interaction history."""
        cursor = self.conn.cursor()

        if domain:
            cursor.execute(
                "SELECT * FROM interactions WHERE domain = ? ORDER BY timestamp DESC LIMIT ?",
                (domain, limit)
            )
        else:
            cursor.execute(
                "SELECT * FROM interactions ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )

        return [dict(row) for row in cursor.fetchall()]

    def stats(self) -> Dict[str, Any]:
        """Get fact store statistics."""
        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) as count FROM facts")
        facts_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM preferences")
        prefs_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM projects")
        projects_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM interactions")
        interactions_count = cursor.fetchone()['count']

        return {
            'facts': facts_count,
            'preferences': prefs_count,
            'projects': projects_count,
            'interactions': interactions_count
        }

    def close(self):
        """Close database connection."""
        self.conn.close()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
