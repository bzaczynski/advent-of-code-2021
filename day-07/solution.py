# """
# Day 7: The Treachery of Whales
# https://adventofcode.com/2021/day/7
#
# Usage:
# $ python solution.py input.txt
# """

import sys
from statistics import median, mean
from typing import Callable, TypeAlias

MetricFunction: TypeAlias = Callable[[list[int]], int]


def main(positions: list[int]) -> None:
    assert part1(positions) == 349357
    assert part2(positions) == 96708205


def part1(positions: list[int]) -> int:
    return sum(distances(positions, median))


def part2(positions: list[int]) -> int:
    return sum(cost(x) for x in distances(positions, mean))


def distances(positions: list[int], metric: MetricFunction) -> list[int]:
    """Return a list of distances to the average position."""
    x0 = int(metric(positions))  # FIXME Should round() instead?
    return [abs(x - x0) for x in positions]


def cost(n: int) -> int:
    """Return the sum of arithmetic progression [1 + 2 + ... + n]."""
    return n * (n + 1) // 2


def load(path: str) -> list[int]:
    """Return a list of crabs' horizontal positions."""
    with open(path, encoding="utf-8") as file:
        return list(map(int, file.readline().split(",")))


if __name__ == "__main__":
    main(load(sys.argv[1] if len(sys.argv) > 1 else "input.txt"))
