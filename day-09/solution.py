# """
# Day 9: Smoke Basin
# https://adventofcode.com/2021/day/9
#
# Usage:
# $ python solution.py input.txt
# """

import sys
from math import prod as product
from typing import TypeAlias, Iterator

import numpy as np

Point: TypeAlias = tuple[int, int]


class HeightMap:
    @classmethod
    def from_file(cls, path: str) -> "HeightMap":
        with open(path, encoding="utf-8") as file:
            return cls([list(map(int, line.strip())) for line in file])

    def __init__(self, values: list[list[int]]) -> None:
        self.values = np.array(values)
        self.height, self.width = self.values.shape

    def __getitem__(self, yx: Point) -> int:
        return self.values[yx]

    @property
    def basin_sizes(self) -> Iterator[int]:
        """Return an iterator of all basin sizes."""

        def flood_fill(point: Point, flags: np.ndarray) -> None:
            """https://en.wikipedia.org/wiki/Flood_fill"""
            if self[point] < 9:
                flags[point] = True
                for yx in self.adjacent(*point):
                    if not flags[yx]:
                        flood_fill(yx, flags)

        for low_point in self.low_points:
            flags = np.zeros(shape=self.values.shape, dtype=bool)
            flood_fill(low_point, flags)
            yield len(flags[flags])

    @property
    def risk_levels(self) -> list[int]:
        """Return a list of risk levels associated with the low points."""
        return [self[yx] + 1 for yx in self.low_points]

    @property
    def low_points(self) -> Iterator[Point]:
        """Return an iterator of points lower than all its neighbors."""
        for y in range(self.height):
            for x in range(self.width):
                if all(self[yx] > self[y, x] for yx in self.adjacent(y, x)):
                    yield y, x

    def adjacent(self, y: int, x: int) -> Iterator[Point]:
        """Return an iterator of at most four adjacent neighbours."""
        if y > 0:
            yield y - 1, x
        if y < self.height - 1:
            yield y + 1, x
        if x > 0:
            yield y, x - 1
        if x < self.width - 1:
            yield y, x + 1


def main(height_map: HeightMap) -> None:
    assert part1(height_map) == 541
    assert part2(height_map) == 847504


def part1(height_map: HeightMap) -> int:
    """Return the total risk level."""
    return sum(height_map.risk_levels)


def part2(height_map: HeightMap) -> int:
    """Return the product of the three largest basin sizes."""
    return product(sorted(height_map.basin_sizes, reverse=True)[:3])


if __name__ == "__main__":
    main(HeightMap.from_file(sys.argv[1] if len(sys.argv) > 1 else "input.txt"))
