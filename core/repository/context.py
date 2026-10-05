from dataclasses import dataclass, field

from .location_extractor import LocationExtractor
from .locations import CodeLocation
from .types import (
    RepositoryAnalysis,
    RepositoryDependency,
    RepositoryFile,
    RepositorySymbol,
)


@dataclass
class RepositoryContext:
    root_path: str
    files: list[RepositoryFile] = field(default_factory=list)
    symbols: list[RepositorySymbol] = field(default_factory=list)
    dependencies: list[RepositoryDependency] = field(
        default_factory=list
    )
    locations: list[CodeLocation] = field(
        default_factory=list
    )
    metadata: dict = field(default_factory=dict)

    @classmethod
    def from_analysis(
        cls,
        analysis: RepositoryAnalysis,
    ) -> "RepositoryContext":

        location_extractor = LocationExtractor()
        locations: list[CodeLocation] = []

        for file in analysis.files:
            locations.extend(
                location_extractor.extract(file)
            )

        return cls(
            root_path=analysis.root_path,
            files=analysis.files,
            symbols=analysis.symbols,
            dependencies=analysis.dependencies,
            locations=locations,
            metadata=analysis.metadata,
        )

    def to_dict(self) -> dict:
        return {
            "root_path": self.root_path,
            "files": [
                {
                    "path": file.path,
                    "relative_path": file.relative_path,
                    "extension": file.extension,
                    "size_bytes": file.size_bytes,
                    "language": file.language,
                }
                for file in self.files
            ],
            "symbols": [
                {
                    "name": symbol.name,
                    "symbol_type": symbol.symbol_type,
                    "file_path": symbol.file_path,
                    "line_start": symbol.line_start,
                    "line_end": symbol.line_end,
                }
                for symbol in self.symbols
            ],
            "dependencies": [
                {
                    "source_file": dependency.source_file,
                    "target": dependency.target,
                    "dependency_type": dependency.dependency_type,
                }
                for dependency in self.dependencies
            ],
            "locations": [
                location.to_dict()
                for location in self.locations
            ],
            "metadata": self.metadata,
        }