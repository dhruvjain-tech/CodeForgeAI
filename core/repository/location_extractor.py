import ast
from pathlib import Path

from .locations import CodeLocation
from .types import RepositoryFile


class LocationExtractor:

    def extract(self, file: RepositoryFile) -> list[CodeLocation]:
        if file.language != "Python":
            return []

        path = Path(file.path)

        try:
            source = path.read_text(
                encoding="utf-8"
            )
            tree = ast.parse(source)
        except (OSError, UnicodeDecodeError, SyntaxError):
            return []

        locations: list[CodeLocation] = []

        for node in ast.walk(tree):
            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                ),
            ):
                symbol_type = (
                    "class"
                    if isinstance(node, ast.ClassDef)
                    else "function"
                )

                locations.append(
                    CodeLocation(
                        file_path=file.relative_path,
                        line_start=node.lineno,
                        line_end=getattr(
                            node,
                            "end_lineno",
                            node.lineno,
                        ),
                        column_start=getattr(
                            node,
                            "col_offset",
                            None,
                        ),
                        column_end=getattr(
                            node,
                            "end_col_offset",
                            None,
                        ),
                        symbol_name=node.name,
                        symbol_type=symbol_type,
                    )
                )

        return locations