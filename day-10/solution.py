# """
# Day 10: Syntax Scoring
# https://adventofcode.com/2021/day/10
#
# Usage:
# $ python solution.py input.txt
# """

import sys
from functools import reduce
from pathlib import Path

from parser import ParsedLine, parse


def main(lines: list[ParsedLine]) -> None:
    assert part1(lines) == 215229
    assert part2(lines) == 1105996483


def part1(lines: list[ParsedLine]) -> int:
    """Return the total score of all the corrupted lines."""
    points = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    return sum(points[line.last_symbol] for line in lines if line.status == "CORRUPTED")


def part2(lines: list[ParsedLine]) -> int:
    """Return the middle score of all the incomplete lines."""
    points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    scores = [
        reduce(lambda score, symbol: score * 5 + points[symbol], line.missing, 0)
        for line in lines if line.status == "INCOMPLETE"
    ]

    return sorted(scores)[len(scores) // 2]


def load(path: Path) -> list[ParsedLine]:
    """Return a list of parsed lines of code."""
    return [parse(line) for line in path.read_text().splitlines()]


if __name__ == "__main__":
    main(load(Path(sys.argv[1] if len(sys.argv) > 1 else "input.txt")))
