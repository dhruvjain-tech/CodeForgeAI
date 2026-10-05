from dataclasses import dataclass


@dataclass
class CodeLocation:
    file_path: str
    line_start: int
    line_end: int
    column_start: int | None = None
    column_end: int | None = None
    symbol_name: str | None = None
    symbol_type: str | None = None

    def to_dict(self) -> dict:
        return {
            "file_path": self.file_path,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "column_start": self.column_start,
            "column_end": self.column_end,
            "symbol_name": self.symbol_name,
            "symbol_type": self.symbol_type,
        }