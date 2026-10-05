from core.repository.location_extractor import LocationExtractor
from core.repository.types import RepositoryFile


def test_extract_python_locations(tmp_path):
    file = tmp_path / "sample.py"

    file.write_text(
        "class Demo:\n"
        "    def hello(self):\n"
        "        return 'hi'\n",
        encoding="utf-8",
    )

    repository_file = RepositoryFile(
        path=str(file),
        relative_path="sample.py",
        extension=".py",
        size_bytes=file.stat().st_size,
        language="Python",
    )

    locations = LocationExtractor().extract(
        repository_file
    )

    assert len(locations) == 2

    names = {location.symbol_name for location in locations}

    assert "Demo" in names
    assert "hello" in names

    for location in locations:
        assert location.line_start >= 1
        assert location.line_end >= location.line_start


def test_non_python_returns_empty(tmp_path):
    file = tmp_path / "sample.js"
    file.write_text(
        "function hello() {}",
        encoding="utf-8",
    )

    repository_file = RepositoryFile(
        path=str(file),
        relative_path="sample.js",
        extension=".js",
        size_bytes=file.stat().st_size,
        language="JavaScript",
    )

    locations = LocationExtractor().extract(
        repository_file
    )

    assert locations == []


def test_invalid_python_returns_empty(tmp_path):
    file = tmp_path / "invalid.py"
    file.write_text(
        "def broken(:",
        encoding="utf-8",
    )

    repository_file = RepositoryFile(
        path=str(file),
        relative_path="invalid.py",
        extension=".py",
        size_bytes=file.stat().st_size,
        language="Python",
    )

    locations = LocationExtractor().extract(
        repository_file
    )

    assert locations == []