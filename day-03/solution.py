"""
Day 3: Binary Diagnostic
https://adventofcode.com/2021/day/3

Usage:
$ python solution.py input.txt
"""
import sys
from operator import ge, lt


def main(path: str) -> None:
    """Load input data and assert the solution."""
    assert part1(load(path)) == 4001724
    assert part2(load(path)) == 587895


def load(path: str) -> list[int]:
    """Return a list of decimal numbers.

    Sample output:
    [4, 30, 22, 23, 21, 15, 7, 28, 16, 25, 2, 10]
    """
    with open(path, encoding="utf-8") as file:
        return [int(line, 2) for line in file]


def part1(numbers: list[int]) -> int:
    """Return the power consumption of the submarine."""
    return (g := gamma(numbers)) * epsilon(g)


def part2(numbers: list[int]) -> int:
    """Return the life support rating of the submarine."""
    return oxygen(numbers) * co2_scrubber(numbers)


def gamma(numbers: list[int]) -> int:
    """Return a number obtained from counting the bits at each position."""
    result = 0
    for bit_index in range(max(numbers).bit_length()):
        bit_count = sum(1 for number in numbers if number & (1 << bit_index))
        if bit_count > len(numbers) - bit_count:
            result |= 1 << bit_index
    return result


def epsilon(gamma: int) -> int:
    """Return an inverted number using the bitwise NOT operator."""
    mask = 2 ** gamma.bit_length() - 1  # 0xfff...
    return ~gamma & mask  # Use a bitmask to disregard the implicit sign bit


def oxygen(numbers: list[int]) -> int:
    """Return the oxygen generator rating."""
    return iterative_filter(numbers, most_common_bit=True)


def co2_scrubber(numbers: list[int]) -> int:
    """Return the CO2 scrubber rating."""
    return iterative_filter(numbers, most_common_bit=False)


def iterative_filter(numbers, most_common_bit: bool = True) -> int:
    """Return a single number after filtering out all the other ones."""
    compare = ge if most_common_bit else lt
    for bit_index in reversed(range(max(numbers).bit_length())):
        bit_count = sum(1 for number in numbers if number & (1 << bit_index))
        keep_ones = compare(bit_count, len(numbers) - bit_count)
        criteria = lambda number: not keep_ones ^ bool(number & (1 << bit_index))
        numbers = list(filter(criteria, numbers))
        if len(numbers) <= 1:
            break
    return numbers.pop()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "input.txt")
