# """
# Day 8: Seven Segment Search
# https://adventofcode.com/2021/day/8
#
# Usage:
# $ python solution.py input.txt
# """

import sys
from collections import UserDict
from dataclasses import dataclass
from functools import cached_property
from typing import TypeAlias

Pattern: TypeAlias = frozenset[str]
Mapping: TypeAlias = [int | Pattern]


@dataclass
class Reading:
    pattern_line: str
    output_line: str

    @cached_property
    def patterns(self) -> list[Pattern]:
        """Return ten unique digit patterns sorted by length."""
        return sorted(map(frozenset, self.pattern_line.split()), key=len)

    @cached_property
    def output(self) -> list[Pattern]:
        """Return four patterns observed in the output."""
        return list(map(frozenset, self.output_line.split()))


class BidirectionalMap(UserDict):
    def __getitem__(self, mapping: Mapping) -> Mapping:
        """Return the value mapped by a key or vice versa."""
        if isinstance(mapping, int):
            for key, value in self.items():
                if value == mapping:
                    return key
        return super().__getitem__(mapping)


def main(readings: list[Reading]) -> None:
    assert part1(readings) == 245
    assert part2(readings) == 983026


def part1(readings: list[Reading]) -> int:
    """Return the total number of digits 1, 4, 7, or 8 in the output."""
    return sum(map(count_1_4_7_8, readings))


def part2(readings: list[Reading]) -> int:
    """Return the sum of the output values."""
    return sum(map(output_value, readings))


def count_1_4_7_8(reading: Reading) -> int:
    """Return the number of occurrences of digits 1, 4, 7, or 8."""
    lengths = map(len, reading.output)
    return sum(1 for length in lengths if length in [2, 4, 3, 7])


def output_value(reading: Reading) -> int:
    """Return a number based on the pattern translation."""
    return make_number(translate(reading.patterns), reading.output)


def translate(patterns: list[Pattern]) -> BidirectionalMap[Pattern, int]:
    """Return the mapping of ten unique patterns to decimal digits."""

    mapping = BidirectionalMap.fromkeys(patterns)

    # Determined upfront by pattern lengths:
    mapping[patterns[0]] = 1
    mapping[patterns[1]] = 7
    mapping[patterns[2]] = 4
    mapping[patterns[9]] = 8

    two_three_five = {p for p in patterns if len(p) == 5}
    zero_six_nine = {p for p in patterns if len(p) == 6}

    three = next(filter(mapping[7].issubset, two_three_five))
    two_five = two_three_five - {three}
    mapping[three] = 3

    nine = next(filter(mapping[4].issubset, zero_six_nine))
    zero_six = zero_six_nine - {nine}
    mapping[nine] = 9

    two = next(filter(lambda p: len(mapping[9] - p) == 2, two_five))
    five = next(iter(two_five - {two}))
    mapping[two] = 2
    mapping[five] = 5

    six = next(filter(mapping[5].issubset, zero_six))
    zero = next(iter(zero_six - {six}))
    mapping[zero] = 0
    mapping[six] = 6

    return mapping


def make_number(mapping: BidirectionalMap[Pattern, int], output: list[Pattern]) -> int:
    """Return the observed decimal number using a positional system."""
    return sum(mapping[p] * 10 ** i for i, p in enumerate(reversed(output)))


def load(path: str) -> list[Reading]:
    """Return a list of seven-segment display signal readings."""
    with open(path, encoding="utf-8") as file:
        return [Reading(*line.strip().split(" | ")) for line in file]


if __name__ == "__main__":
    main(load(sys.argv[1] if len(sys.argv) > 1 else "input.txt"))
