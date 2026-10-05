from core.repository.context import RepositoryContext
from core.repository.context_search import (
    RepositoryContextSearch,
)
from core.repository.service import RepositoryAnalysisService


def build_context(tmp_path):
    file = tmp_path / "sample.py"

    file.write_text(
        "class Demo:\n"
        "    def hello(self):\n"
        "        return 'hi'\n",
        encoding="utf-8",
    )

    analysis = RepositoryAnalysisService().analyze(
        tmp_path
    )

    return RepositoryContext.from_analysis(
        analysis
    )


def test_search_files(tmp_path):
    context = build_context(tmp_path)

    search = RepositoryContextSearch()

    results = search.search_files(
        context,
        "sample",
    )

    assert len(results) == 1
    assert results[0].relative_path == "sample.py"


def test_search_symbols(tmp_path):
    context = build_context(tmp_path)

    search = RepositoryContextSearch()

    results = search.search_symbols(
        context,
        "hello",
    )

    assert len(results) == 1
    assert results[0].name == "hello"


def test_search_locations(tmp_path):
    context = build_context(tmp_path)

    search = RepositoryContextSearch()

    results = search.search_locations(
        context,
        "hello",
    )

    assert len(results) == 1
    assert results[0].symbol_name == "hello"
    assert results[0].line_start == 2


def test_search_is_case_insensitive(tmp_path):
    context = build_context(tmp_path)

    search = RepositoryContextSearch()

    results = search.search_symbols(
        context,
        "HELLO",
    )

    assert len(results) == 1


def test_search_no_results(tmp_path):
    context = build_context(tmp_path)

    search = RepositoryContextSearch()

    results = search.search_symbols(
        context,
        "does_not_exist",
    )

    assert results == []