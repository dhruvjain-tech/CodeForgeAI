from dataclasses import dataclass, field


@dataclass
class TechnologyOption:
    name: str
    category: str
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)