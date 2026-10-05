from core.repository.service import RepositoryAnalysisService


def test_repository_analysis_includes_location_count(tmp_path):
    file = tmp_path / "sample.py"

    file.write_text(
        "class Demo:\n"
        "    def hello(self):\n"
        "        return 'hi'\n",
        encoding="utf-8",
    )

    result = RepositoryAnalysisService().analyze(
        tmp_path
    )

    assert result.metadata["file_count"] == 1
    assert result.metadata["location_count"] == 2