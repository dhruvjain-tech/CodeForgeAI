from .context import RepositoryContext


class RepositoryContextSearch:

    def search_files(
        self,
        context: RepositoryContext,
        query: str,
    ) -> list:
        query = query.lower()

        return [
            file
            for file in context.files
            if query in file.relative_path.lower()
        ]

    def search_symbols(
        self,
        context: RepositoryContext,
        query: str,
    ) -> list:
        query = query.lower()

        return [
            symbol
            for symbol in context.symbols
            if query in symbol.name.lower()
        ]

    def search_locations(
        self,
        context: RepositoryContext,
        query: str,
    ) -> list:
        query = query.lower()

        return [
            location
            for location in context.locations
            if (
                location.symbol_name
                and query in location.symbol_name.lower()
            )
            or query in location.file_path.lower()
        ]


repository_context_search = RepositoryContextSearch()