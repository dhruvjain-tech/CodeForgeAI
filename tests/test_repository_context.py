from core.repository.context import RepositoryContext
from core.repository.service import RepositoryAnalysisService


def test_repository_context_from_analysis(tmp_path):
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

    context = RepositoryContext.from_analysis(
        analysis
    )

    assert context.root_path == str(tmp_path)
    assert len(context.files) == 1
    assert len(context.symbols) == 2
    assert len(context.locations) == 2


def test_repository_context_to_dict(tmp_path):
    file = tmp_path / "sample.py"

    file.write_text(
        "def hello():\n"
        "    return 'hi'\n",
        encoding="utf-8",
    )

    analysis = RepositoryAnalysisService().analyze(
        tmp_path
    )

    context = RepositoryContext.from_analysis(
        analysis
    )

    data = context.to_dict()

    assert data["root_path"] == str(tmp_path)
    assert data["metadata"]["file_count"] == 1
    assert len(data["files"]) == 1
    assert len(data["symbols"]) == 1
    assert len(data["locations"]) == 1