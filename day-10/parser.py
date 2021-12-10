from dataclasses import dataclass
from typing import Literal, TypeAlias, Optional

Status: TypeAlias = Literal["CORRUPTED"] | Literal["INCOMPLETE"] | Literal["OKAY"]


class Brackets:
    opening = "(", "[", "{", "<"
    closing = ")", "]", "}", ">"
    matching = dict(zip(opening, closing)) | dict(zip(closing, opening))


@dataclass
class ParsedLine:
    @classmethod
    def corrupted(cls, line, last_symbol) -> "ParsedLine":
        return cls("CORRUPTED", line, last_symbol, None)

    @classmethod
    def incomplete(cls, line, missing) -> "ParsedLine":
        return cls("INCOMPLETE", line, None, missing)

    @classmethod
    def okay(cls, line) -> "ParsedLine":
        return cls("OKAY", line, None, None)

    status: Status
    line: str
    last_symbol: Optional[str]
    missing: Optional[str]


def parse(line: str) -> ParsedLine:
    """Return a parsed line of code with optional metadata."""
    stack = []
    for symbol in line:
        if symbol in Brackets.opening:
            stack.append(symbol)
        elif symbol in Brackets.closing:
            if Brackets.matching[symbol] != stack.pop():
                return ParsedLine.corrupted(line, symbol)

    if len(stack) > 0:
        missing = "".join(reversed([Brackets.matching[x] for x in stack]))
        return ParsedLine.incomplete(line, missing)

    return ParsedLine.okay(line)
