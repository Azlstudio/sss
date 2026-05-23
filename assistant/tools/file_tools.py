import os
from pathlib import Path
from typing import Optional, List
from ..config import get_config

class FileTool:
    """File operations with permission-based access control."""

    def __init__(self):
        config = get_config()
        self.allowed_dirs = config.get('permissions.allowed_directories', ['./workspace', './brain'])
        self.require_confirmation = config.get('permissions.require_confirmation', ['delete', 'edit_config'])

    def _check_permission(self, filepath: str, operation: str) -> bool:
        """Check if file operation is allowed."""

        filepath = os.path.abspath(filepath)

        # Check if file is in allowed directories
        for allowed_dir in self.allowed_dirs:
            allowed_path = os.path.abspath(allowed_dir)
            if filepath.startswith(allowed_path):
                return True

        return False

    def _require_confirmation(self, operation: str) -> bool:
        """Check if operation requires confirmation."""
        return operation in self.require_confirmation

    def read(self, filepath: str) -> Optional[str]:
        """Read file contents."""

        if not self._check_permission(filepath, 'read'):
            return f"ERROR: Permission denied. {filepath} is not in allowed directories."

        if not os.path.exists(filepath):
            return f"ERROR: File not found: {filepath}"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"ERROR: {str(e)}"

    def create(self, filepath: str, content: str) -> bool:
        """Create new file."""

        if not self._check_permission(filepath, 'create'):
            return False

        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return False

    def edit(self, filepath: str, content: str, append: bool = False) -> bool:
        """Edit existing file (append or overwrite)."""

        if not self._check_permission(filepath, 'edit'):
            return False

        if not os.path.exists(filepath):
            return self.create(filepath, content)

        try:
            mode = 'a' if append else 'w'
            with open(filepath, mode, encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return False

    def delete(self, filepath: str, ask_confirmation: bool = True) -> bool:
        """Delete file (requires confirmation)."""

        if not self._check_permission(filepath, 'delete'):
            return False

        if not os.path.exists(filepath):
            return False

        if ask_confirmation and self._require_confirmation('delete'):
            response = input(f"Are you sure you want to delete {filepath}? (yes/no): ")
            if response.lower() != 'yes':
                return False

        try:
            os.remove(filepath)
            return True
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return False

    def list_directory(self, directory: str, recursive: bool = False) -> List[str]:
        """List files in directory."""

        if not self._check_permission(directory, 'read'):
            return []

        if not os.path.isdir(directory):
            return []

        try:
            if recursive:
                files = []
                for root, dirs, filenames in os.walk(directory):
                    for f in filenames:
                        files.append(os.path.join(root, f))
                return files
            else:
                return [os.path.join(directory, f) for f in os.listdir(directory)]
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return []

    def get_file_info(self, filepath: str) -> Optional[dict]:
        """Get file metadata."""

        if not self._check_permission(filepath, 'read'):
            return None

        if not os.path.exists(filepath):
            return None

        try:
            stat = os.stat(filepath)
            return {
                'path': filepath,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'is_file': os.path.isfile(filepath),
                'is_dir': os.path.isdir(filepath)
            }
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return None

    def search_files(self, directory: str, pattern: str = None, extension: str = None) -> List[str]:
        """Search for files by pattern or extension."""

        if not self._check_permission(directory, 'read'):
            return []

        import fnmatch

        results = []
        for root, dirs, files in os.walk(directory):
            for f in files:
                filepath = os.path.join(root, f)

                if extension and f.endswith(extension):
                    results.append(filepath)
                elif pattern and fnmatch.fnmatch(f, pattern):
                    results.append(filepath)
                elif not extension and not pattern:
                    results.append(filepath)

        return results
