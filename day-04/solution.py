# """
# Day 4: Giant Squid
# https://adventofcode.com/2021/day/4
#
# Usage:
# $ python solution.py input.txt
# """

import sys
from dataclasses import dataclass
from operator import truediv as div
from typing import Iterator

import numpy as np


class Board:
    def __init__(self, numbers: np.ndarray) -> None:
        self.numbers = numbers
        self.marks = np.zeros(numbers.shape, dtype=int)

    @property
    def unmarked_numbers(self) -> np.ndarray:
        return self.numbers[self.marks == 0]

    @property
    def wins(self) -> bool:
        col_sums = self.marks.sum(axis=0)
        row_sums = self.marks.sum(axis=1)
        return len(col_sums) in col_sums or len(row_sums) in row_sums

    @property
    def score(self) -> int:
        return self.unmarked_numbers.sum()

    def play(self, number: int) -> None:
        self.marks[self.numbers == number] = True


@dataclass
class BingoGame:
    random_numbers: np.ndarray
    boards: list[Board]

    @property
    def first_score(self) -> int:
        return next(self.final_scores())

    @property
    def last_score(self) -> int:
        return list(self.final_scores())[-1]

    def final_scores(self) -> Iterator[int]:
        for number in self.random_numbers:
            for board in self.boards[:]:
                board.play(number)
                if board.wins:
                    yield board.score * number
                    self.boards.remove(board)


def main(path: str) -> None:
    bingo = load(path)
    assert bingo.first_score == 25023
    assert bingo.last_score == 2634


def load(path: str) -> BingoGame:
    with open(path, encoding="utf-8") as file:
        random_numbers = np.fromstring(file.readline(), dtype=int, sep=",")
        boards_numbers = np.vsplit(a := np.loadtxt(file, dtype=int), div(*a.shape))
        return BingoGame(random_numbers, [Board(x) for x in boards_numbers])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "input.txt")
