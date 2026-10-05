from pathlib import Path

from .types import RepositoryFile


class RepositoryAnalyzer:

    def analyze_file(
        self,
        file: RepositoryFile,
    ) -> RepositoryFile:
        path = Path(file.path)

        if not path.exists():
            return file

        if file.language is None:
            file.language = "Unknown"

        return file

    def analyze(
        self,
        files: list[RepositoryFile],
    ) -> list[RepositoryFile]:

        return [
            self.analyze_file(file)
            for file in files
        ]