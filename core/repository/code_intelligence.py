from .context import RepositoryContext
from .context_search import repository_context_search
from .service import RepositoryAnalysisService


class CodeIntelligenceService:

    def __init__(self):
        self.analysis_service = RepositoryAnalysisService()

    def analyze(
        self,
        root_path: str,
    ) -> RepositoryContext:
        analysis = self.analysis_service.analyze(
            root_path
        )

        return RepositoryContext.from_analysis(
            analysis
        )

    def search_files(
        self,
        context: RepositoryContext,
        query: str,
    ) -> list:
        return repository_context_search.search_files(
            context,
            query,
        )

    def search_symbols(
        self,
        context: RepositoryContext,
        query: str,
    ) -> list:
        return repository_context_search.search_symbols(
            context,
            query,
        )

    def search_locations(
        self,
        context: RepositoryContext,
        query: str,
    ) -> list:
        return repository_context_search.search_locations(
            context,
            query,
        )


code_intelligence_service = CodeIntelligenceService()