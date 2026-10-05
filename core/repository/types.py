from dataclasses import dataclass, field
from typing import Any


@dataclass
class RepositoryFile:
    path: str
    relative_path: str
    extension: str
    size_bytes: int
    language: str | None = None


@dataclass
class RepositorySymbol:
    name: str
    symbol_type: str
    file_path: str
    line_start: int
    line_end: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RepositoryDependency:
    source_file: str
    target: str
    dependency_type: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RepositoryAnalysis:
    root_path: str
    files: list[RepositoryFile] = field(default_factory=list)
    symbols: list[RepositorySymbol] = field(default_factory=list)
    dependencies: list[RepositoryDependency] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)