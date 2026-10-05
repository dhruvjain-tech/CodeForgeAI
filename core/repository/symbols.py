import ast
from pathlib import Path

from .types import RepositoryFile, RepositorySymbol


class SymbolAnalyzer:

    def analyze_file(
        self,
        file: RepositoryFile,
    ) -> list[RepositorySymbol]:

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

        symbols: list[RepositorySymbol] = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):
                symbols.append(
                    RepositorySymbol(
                        name=node.name,
                        symbol_type="class",
                        file_path=file.relative_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                    )
                )

            elif isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                symbols.append(
                    RepositorySymbol(
                        name=node.name,
                        symbol_type="function",
                        file_path=file.relative_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                    )
                )

        return symbols

    def analyze(
        self,
        files: list[RepositoryFile],
    ) -> list[RepositorySymbol]:

        symbols: list[RepositorySymbol] = []

        for file in files:
            symbols.extend(
                self.analyze_file(file)
            )

        return symbols