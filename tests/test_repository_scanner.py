from core.repository.scanner import RepositoryScanner


def test_scanner_finds_files(tmp_path):
    (tmp_path / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    scanner = RepositoryScanner()
    files = scanner.scan(tmp_path)

    assert len(files) == 1
    assert files[0].relative_path == "main.py"
    assert files[0].language == "Python"


def test_scanner_ignores_directories(tmp_path):
    (tmp_path / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    ignored = tmp_path / "node_modules"
    ignored.mkdir()

    (ignored / "package.js").write_text(
        "ignored",
        encoding="utf-8",
    )

    scanner = RepositoryScanner()
    files = scanner.scan(tmp_path)

    assert len(files) == 1
    assert files[0].relative_path == "main.py"


def test_scanner_detects_multiple_languages(tmp_path):
    (tmp_path / "main.py").write_text("", encoding="utf-8")
    (tmp_path / "app.ts").write_text("", encoding="utf-8")
    (tmp_path / "style.css").write_text("", encoding="utf-8")

    scanner = RepositoryScanner()
    files = scanner.scan(tmp_path)

    languages = {file.language for file in files}

    assert "Python" in languages
    assert "TypeScript" in languages
    assert "CSS" in languages


def test_scanner_missing_repository():
    scanner = RepositoryScanner()

    try:
        scanner.scan("D:/CodeForgeAI/does-not-exist")
        assert False
    except FileNotFoundError:
        assert True