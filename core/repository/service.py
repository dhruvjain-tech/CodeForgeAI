from pathlib import Path

from .dependencies import DependencyAnalyzer
from .location_extractor import LocationExtractor
from .scanner import RepositoryScanner
from .symbols import SymbolAnalyzer
from .types import RepositoryAnalysis


class RepositoryAnalysisService:

    def __init__(self):
        self.scanner = RepositoryScanner()
        self.symbol_analyzer = SymbolAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
        self.location_extractor = LocationExtractor()

    def analyze(
        self,
        root_path: str | Path,
    ) -> RepositoryAnalysis:

        root = Path(root_path)

        files = self.scanner.scan(root)

        symbols = self.symbol_analyzer.analyze(files)

        dependencies = self.dependency_analyzer.analyze(files)

        locations = []

        for file in files:
            locations.extend(
                self.location_extractor.extract(file)
            )

        return RepositoryAnalysis(
            root_path=str(root),
            files=files,
            symbols=symbols,
            dependencies=dependencies,
            metadata={
                "file_count": len(files),
                "symbol_count": len(symbols),
                "dependency_count": len(dependencies),
                "location_count": len(locations),
            },
        )


repository_analysis_service = RepositoryAnalysisService()