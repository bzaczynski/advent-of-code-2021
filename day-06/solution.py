# """
# Day 6: Lanternfish
# https://adventofcode.com/2021/day/6
#
# Usage:
# $ python solution.py input.txt
# """

import sys
from collections import Counter
from functools import cache


def main(fish: list[int]) -> None:
    assert solve(fish, days=80) == 356190
    assert solve(fish, days=256) == 1617359101538


def solve(fish: list[int], days: int) -> int:
    """Return the total number of fish after the given number of days."""
    return sum(
        offsprings(days - state) * count for state, count in Counter(fish).items()
    )


@cache
def offsprings(days: int) -> int:
    """Return the number of fish offsprings after the given number of days."""
    total = 1
    while days > 0:
        total += offsprings(days - 9)
        days = days - 7
    return total


def load(path: str) -> list[int]:
    """Return a list of fish' initial states."""
    with open(path, encoding="utf-8") as file:
        return list(map(int, file.readline().split(",")))


if __name__ == "__main__":
    main(load(sys.argv[1] if len(sys.argv) > 1 else "input.txt"))
