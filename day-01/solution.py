"""
Day 1: Sonar Sweep
https://adventofcode.com/2021/day/1

Usage:
$ python solution.py input.txt
"""

import sys


def main(path: str) -> None:
    """Load input data and assert the solution."""

    # Part 1
    assert 1711 == count(load(path))

    # Part 2
    assert 1743 == count(summed(windows(load(path))))


def load(path: str) -> list[int]:
    """Return a list of seafloor depth measurements.

    Sample output:
    [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    """
    with open(path, encoding="utf-8") as file:
        return [int(line) for line in file]


# Straightforward implementation:
# def count(depths: list[int]) -> int:
#     """Return the number of times the depth increases."""
#     count = 0
#     last_depth = depths[0]
#     for depth in depths[1:]:
#         diff = depth - last_depth
#         if diff > 0:
#             count += 1
#         last_depth = depth
#     return count


def count(depths: list[int]) -> int:
    """Return the number of times the depth increases."""
    return sum(1 for x, y in zip(depths, depths[1:]) if y - x > 0)


def windows(depths: list[int]) -> list[list[int]]:
    """Return a list of three-element sliding windows.

    Sample output:
    [[199, 200, 208], [200, 208, 210], ..., [269, 260, 263]]
    """
    return [depths[i : i + 3] for i in range(len(depths) - 2)]


def summed(windows):
    """Return a list of sliding window totals.

    Sample output:
    [607, 618, 618, 617, 647, 716, 769, 792]"""
    return [sum(window) for window in windows]


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "input.txt")
