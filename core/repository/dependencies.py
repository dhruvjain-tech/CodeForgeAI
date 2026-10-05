import ast
from pathlib import Path

from .types import RepositoryDependency, RepositoryFile


class DependencyAnalyzer:

    def analyze_file(
        self,
        file: RepositoryFile,
    ) -> list[RepositoryDependency]:

        if file.language != "Python":
            return []

        path = Path(file.path)

        if not path.exists():
            return []

        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (UnicodeDecodeError, SyntaxError):
            return []

        dependencies: list[RepositoryDependency] = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for alias in node.names:
                    dependencies.append(
                        RepositoryDependency(
                            source_file=file.relative_path,
                            target=alias.name,
                            dependency_type="import",
                        )
                    )

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    dependencies.append(
                        RepositoryDependency(
                            source_file=file.relative_path,
                            target=node.module,
                            dependency_type="from_import",
                        )
                    )

        return dependencies

    def analyze(
        self,
        files: list[RepositoryFile],
    ) -> list[RepositoryDependency]:

        dependencies: list[RepositoryDependency] = []

        for file in files:
            dependencies.extend(
                self.analyze_file(file)
            )

        return dependencies