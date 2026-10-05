from core.repository.context import RepositoryContext
from core.repository.service import RepositoryAnalysisService


def test_context_serialization_contains_code_locations(tmp_path):
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

    data = context.to_dict()

    assert "locations" in data
    assert len(data["locations"]) == 2

    location = data["locations"][0]

    assert "file_path" in location
    assert "line_start" in location
    assert "line_end" in location
    assert "symbol_name" in location
    assert "symbol_type" in location