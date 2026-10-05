from core.repository.code_intelligence import (
    CodeIntelligenceService,
)


def build_repository(tmp_path):
    file = tmp_path / "sample.py"

    file.write_text(
        "class Demo:\n"
        "    def hello(self):\n"
        "        return 'hi'\n",
        encoding="utf-8",
    )

    return tmp_path


def test_analyze_repository(tmp_path):
    root = build_repository(tmp_path)

    service = CodeIntelligenceService()

    context = service.analyze(str(root))

    assert context.root_path == str(root)
    assert len(context.files) == 1
    assert len(context.symbols) == 2
    assert len(context.locations) == 2


def test_search_files(tmp_path):
    root = build_repository(tmp_path)

    service = CodeIntelligenceService()
    context = service.analyze(str(root))

    results = service.search_files(
        context,
        "sample",
    )

    assert len(results) == 1


def test_search_symbols(tmp_path):
    root = build_repository(tmp_path)

    service = CodeIntelligenceService()
    context = service.analyze(str(root))

    results = service.search_symbols(
        context,
        "hello",
    )

    assert len(results) == 1
    assert results[0].name == "hello"


def test_search_locations(tmp_path):
    root = build_repository(tmp_path)

    service = CodeIntelligenceService()
    context = service.analyze(str(root))

    results = service.search_locations(
        context,
        "hello",
    )

    assert len(results) == 1
    assert results[0].symbol_name == "hello"
    assert results[0].line_start == 2