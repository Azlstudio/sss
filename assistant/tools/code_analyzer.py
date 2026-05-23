import os
import re
from typing import Dict, List, Any, Optional
from .file_tools import FileTool

class CodeAnalyzer:
    """Analyze code files to understand project structure and extract knowledge."""

    def __init__(self):
        self.file_tool = FileTool()

    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze a single code file."""

        content = self.file_tool.read(filepath)
        if not content or content.startswith("ERROR"):
            return {'error': content}

        ext = os.path.splitext(filepath)[1]

        analysis = {
            'filepath': filepath,
            'extension': ext,
            'lines': len(content.split('\n')),
            'size': len(content),
            'language': self._detect_language(ext)
        }

        if ext in ['.py']:
            analysis.update(self._analyze_python(content))
        elif ext in ['.lua']:
            analysis.update(self._analyze_lua(content))
        elif ext in ['.js', '.ts']:
            analysis.update(self._analyze_javascript(content))
        elif ext in ['.cpp', '.c', '.h']:
            analysis.update(self._analyze_c(content))

        return analysis

    def analyze_project(self, directory: str) -> Dict[str, Any]:
        """Analyze entire project directory."""

        files = self.file_tool.search_files(directory)
        analysis = {
            'directory': directory,
            'total_files': len(files),
            'files_by_type': {},
            'summary': ''
        }

        for filepath in files:
            ext = os.path.splitext(filepath)[1]
            if ext not in analysis['files_by_type']:
                analysis['files_by_type'][ext] = []
            analysis['files_by_type'][ext].append(filepath)

        # Analyze structure
        analysis['structure'] = self._analyze_directory_structure(directory)

        return analysis

    def _detect_language(self, extension: str) -> str:
        """Detect programming language from extension."""
        lang_map = {
            '.py': 'Python',
            '.lua': 'Lua',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C Header',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust'
        }
        return lang_map.get(extension, 'Unknown')

    def _analyze_python(self, content: str) -> Dict[str, Any]:
        """Extract Python code structure."""

        analysis = {
            'functions': [],
            'classes': [],
            'imports': [],
            'docstring': ''
        }

        # Extract docstring
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if docstring_match:
            analysis['docstring'] = docstring_match.group(1).strip()

        # Extract imports
        analysis['imports'] = re.findall(r'^(?:from|import)\s+(.+)$', content, re.MULTILINE)

        # Extract function definitions
        analysis['functions'] = re.findall(r'^def\s+(\w+)\s*\(', content, re.MULTILINE)

        # Extract class definitions
        analysis['classes'] = re.findall(r'^class\s+(\w+)\s*(?:\(|:)', content, re.MULTILINE)

        return analysis

    def _analyze_lua(self, content: str) -> Dict[str, Any]:
        """Extract Lua code structure."""

        analysis = {
            'functions': [],
            'tables': [],
            'comments': []
        }

        # Extract function definitions
        analysis['functions'] = re.findall(r'^function\s+(\w+)', content, re.MULTILINE)
        analysis['functions'].extend(re.findall(r'local\s+function\s+(\w+)', content, re.MULTILINE))

        # Extract comments
        analysis['comments'] = re.findall(r'--\s*(.*?)$', content, re.MULTILINE)

        # Extract table definitions
        analysis['tables'] = re.findall(r'(\w+)\s*=\s*\{', content)

        return analysis

    def _analyze_javascript(self, content: str) -> Dict[str, Any]:
        """Extract JavaScript/TypeScript structure."""

        analysis = {
            'functions': [],
            'classes': [],
            'exports': [],
            'imports': []
        }

        analysis['functions'] = re.findall(r'(?:function|const|let|var)\s+(\w+)\s*(?:=\s*)?(?:function|\()', content)
        analysis['classes'] = re.findall(r'class\s+(\w+)', content)
        analysis['exports'] = re.findall(r'export\s+(?:function|const|class|default)?\s*(\w+)', content)
        analysis['imports'] = re.findall(r'import\s+(?:\{[^}]*\}|.*?)\s+from\s+["\']([^"\']+)["\']', content)

        return analysis

    def _analyze_c(self, content: str) -> Dict[str, Any]:
        """Extract C/C++ code structure."""

        analysis = {
            'functions': [],
            'structs': [],
            'defines': []
        }

        analysis['functions'] = re.findall(r'^\w+\s+(\w+)\s*\([^)]*\)\s*\{', content, re.MULTILINE)
        analysis['structs'] = re.findall(r'(?:struct|class)\s+(\w+)', content)
        analysis['defines'] = re.findall(r'#define\s+(\w+)', content)

        return analysis

    def _analyze_directory_structure(self, directory: str) -> Dict[str, Any]:
        """Analyze directory structure."""

        structure = {
            'subdirs': [],
            'files': []
        }

        try:
            for item in os.listdir(directory):
                if item.startswith('.'):
                    continue

                path = os.path.join(directory, item)
                if os.path.isdir(path):
                    structure['subdirs'].append(item)
                else:
                    structure['files'].append(item)
        except:
            pass

        return structure

    def extract_knowledge(self, filepath: str) -> List[str]:
        """Extract learnable knowledge from a code file."""

        content = self.file_tool.read(filepath)
        if not content or content.startswith("ERROR"):
            return []

        knowledge = []

        # Extract comments as knowledge
        comments = re.findall(r'#\s*(.+)$', content, re.MULTILINE)  # Python/Lua style
        comments.extend(re.findall(r'//\s*(.+)$', content, re.MULTILINE))  # C/JS style
        comments.extend(re.findall(r'/\*\s*(.+?)\s*\*/', content, re.DOTALL))  # Block comments

        knowledge.extend([f"Code note: {c}" for c in comments[:10]])  # Limit to 10

        # Extract important patterns
        patterns = [
            (r'TODO:\s*(.+)', 'TODO'),
            (r'FIXME:\s*(.+)', 'FIXME'),
            (r'NOTE:\s*(.+)', 'NOTE'),
        ]

        for pattern, prefix in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            knowledge.extend([f"{prefix}: {m}" for m in matches])

        return knowledge
