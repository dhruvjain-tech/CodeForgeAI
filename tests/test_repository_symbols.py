from core.repository.symbols import SymbolAnalyzer
from core.repository.types import RepositoryFile


def test_analyzer_detects_class_and_function(tmp_path):
    source = """
class UserService:
    def create_user(self):
        return True

def helper():
    return 1
"""

    path = tmp_path / "service.py"
    path.write_text(source, encoding="utf-8")

    file = RepositoryFile(
        path=str(path),
        relative_path="service.py",
        extension=".py",
        size_bytes=path.stat().st_size,
        language="Python",
    )

    analyzer = SymbolAnalyzer()
    symbols = analyzer.analyze_file(file)

    names = {symbol.name for symbol in symbols}
    types = {symbol.symbol_type for symbol in symbols}

    assert "UserService" in names
    assert "create_user" in names
    assert "helper" in names
    assert "class" in types
    assert "function" in types


def test_analyzer_returns_empty_for_non_python(tmp_path):
    path = tmp_path / "app.ts"
    path.write_text("function hello() {}", encoding="utf-8")

    file = RepositoryFile(
        path=str(path),
        relative_path="app.ts",
        extension=".ts",
        size_bytes=path.stat().st_size,
        language="TypeScript",
    )

    analyzer = SymbolAnalyzer()

    assert analyzer.analyze_file(file) == []


def test_analyzer_handles_invalid_python(tmp_path):
    path = tmp_path / "broken.py"
    path.write_text("class Broken(", encoding="utf-8")

    file = RepositoryFile(
        path=str(path),
        relative_path="broken.py",
        extension=".py",
        size_bytes=path.stat().st_size,
        language="Python",
    )

    analyzer = SymbolAnalyzer()

    assert analyzer.analyze_file(file) == []


def test_symbol_line_numbers(tmp_path):
    source = """class TestClass:
    def test_method(self):
        return True
"""

    path = tmp_path / "test.py"
    path.write_text(source, encoding="utf-8")

    file = RepositoryFile(
        path=str(path),
        relative_path="test.py",
        extension=".py",
        size_bytes=path.stat().st_size,
        language="Python",
    )

    symbols = SymbolAnalyzer().analyze_file(file)

    class_symbol = next(s for s in symbols if s.name == "TestClass")
    method_symbol = next(s for s in symbols if s.name == "test_method")

    assert class_symbol.line_start == 1
    assert method_symbol.line_start == 2