# """
# Day 5: Hydrothermal Venture
# https://adventofcode.com/2021/day/5
#
# Usage:
# $ python solution.py input.txt
# """

import sys
from typing import Iterator, TypeAlias

import numpy as np

Line: TypeAlias = list[tuple[int, int]]


def main(path: str) -> None:
    assert 6267 == solve(load(path))
    assert 20196 == solve(load(path, use_diagonals=True))


def solve(lines: list[Line]) -> int:
    """Return the number of overlapping points."""
    diagram = make_diagram(lines)
    for line in lines:
        for point in line:
            diagram[point] += 1
    return len(diagram[diagram > 1])


def make_diagram(lines: list[Line]) -> np.ndarray:
    """Return a square matrix initialized with zeros."""
    size = np.concatenate([np.array(a).flatten() for a in lines]).max()
    return np.zeros(shape=[size + 1] * 2, dtype=int)


def load(path: str, use_diagonals: bool = False) -> list[Line]:
    """Return a list of lines comprised of points."""

    def load_lazy() -> Iterator:
        with open(path, encoding="utf-8") as file:
            for line in file:
                x1, y1, x2, y2 = np.fromstring(
                    line.replace("->", ","), dtype=int, sep=","
                )
                if x1 == x2:
                    yield vertical(x1, y1, y2)
                elif y1 == y2:
                    yield horizontal(y1, x1, x2)
                elif abs(x2 - x1) == (abs(y2 - y1)):
                    if use_diagonals:
                        yield diagonal(x1, y1, x2, y2)

    return list(load_lazy())


def vertical(x1: int, y1: int, y2: int) -> Line:
    """Return points of a vertical line."""
    y = np.linspace(y1, y2, dtype=int, num=abs(y2 - y1) + 1)
    x = np.repeat(x1, len(y))
    return list(zip(y, x))


def horizontal(y1: int, x1: int, x2: int) -> Line:
    """Return points of a horizontal line."""
    x = np.linspace(x1, x2, dtype=int, num=abs(x2 - x1) + 1)
    y = np.repeat(y1, len(x))
    return list(zip(y, x))


def diagonal(x1: int, y1: int, x2: int, y2: int) -> Line:
    """Return points of a diagonal line."""
    x = np.linspace(x1, x2, dtype=int, num=abs(x2 - x1) + 1)
    y = np.linspace(y1, y2, dtype=int, num=abs(y2 - y1) + 1)
    return list(zip(y, x))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "input.txt")
