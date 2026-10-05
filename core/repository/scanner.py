from pathlib import Path

from .types import RepositoryFile


class RepositoryScanner:

    DEFAULT_IGNORED_DIRECTORIES = {
        ".git",
        ".next",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
        "coverage",
    }

    LANGUAGE_MAP = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".java": "Java",
        ".cpp": "C++",
        ".cc": "C++",
        ".c": "C",
        ".h": "C/C++",
        ".hpp": "C++",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust",
        ".php": "PHP",
        ".rb": "Ruby",
        ".kt": "Kotlin",
        ".swift": "Swift",
        ".sql": "SQL",
        ".html": "HTML",
        ".css": "CSS",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".md": "Markdown",
    }

    def __init__(
        self,
        ignored_directories: set[str] | None = None,
    ):
        self.ignored_directories = (
            ignored_directories
            or self.DEFAULT_IGNORED_DIRECTORIES
        )

    def scan(
        self,
        root_path: str | Path,
    ) -> list[RepositoryFile]:

        root = Path(root_path)

        if not root.exists():
            raise FileNotFoundError(
                f"Repository path not found: {root}"
            )

        if not root.is_dir():
            raise NotADirectoryError(
                f"Repository path is not a directory: {root}"
            )

        files: list[RepositoryFile] = []

        for path in root.rglob("*"):

            if not path.is_file():
                continue

            if self._is_ignored(path, root):
                continue

            extension = path.suffix.lower()

            language = self.LANGUAGE_MAP.get(extension)

            files.append(
                RepositoryFile(
                    path=str(path),
                    relative_path=str(
                        path.relative_to(root)
                    ),
                    extension=extension,
                    size_bytes=path.stat().st_size,
                    language=language,
                )
            )

        return files

    def _is_ignored(
        self,
        path: Path,
        root: Path,
    ) -> bool:

        relative_parts = path.relative_to(root).parts

        return any(
            part in self.ignored_directories
            for part in relative_parts
        )