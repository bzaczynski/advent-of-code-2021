"""
Day 2: Dive!
https://adventofcode.com/2021/day/2

Usage:
$ python solution.py input.txt
"""
import sys

from models import Command, Position, PositionWithAim


def main(path: str) -> None:
    """Load input data and assert the solution."""
    assert part1(load(path)) == 1524750
    assert part2(load(path)) == 1592426537


def part1(commands: list[Command]) -> int:
    return solve(commands, Position())


def part2(commands: list[Command]) -> int:
    return solve(commands, PositionWithAim())


def solve(commands: list[Command], position: Position | PositionWithAim) -> int:
    for command in commands:
        position.apply(command)
    return position.product
q

def load(path: str) -> list[Command]:
    """Return a list of course commands.

    Sample output:
    [Command(direction=<Direction.FORWARD: 1>, distance=5), ...]
    """
    with open(path, encoding="utf-8") as file:
        return [Command.from_string(line) for line in file]


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "input.txt")
