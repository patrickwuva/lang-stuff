from dataclasses import dataclass, field
import string

@dataclass
class LetterContext:
    before: dict[str, int] = field(default_factory=lambda: {ch: 0 for ch in string.ascii_lowercase})
    after: dict[str, int] = field(default_factory=lambda: {ch: 0 for ch in string.ascii_lowercase})

