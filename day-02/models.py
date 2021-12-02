from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple


class Direction(Enum):
    FORWARD = auto()
    DOWN = auto()
    UP = auto()


class Command(NamedTuple):
    direction: Direction
    distance: int

    @classmethod
    def from_string(cls, line: str) -> "Command":
        direction, distance = line.split()
        return cls(Direction[direction.upper()], int(distance))


@dataclass
class Position:
    horizontal: int = 0
    depth: int = 0

    @property
    def product(self):
        return self.horizontal * self.depth

    def forward(self, distance: int) -> None:
        self.horizontal += distance

    def down(self, distance: int) -> None:
        self.depth += distance

    def up(self, distance: int) -> None:
        self.depth -= distance

    def apply(self, command: Command) -> None:
        match command:
            case (Direction.FORWARD, distance):
                self.forward(distance)
            case (Direction.DOWN, distance):
                self.down(distance)
            case (Direction.UP, distance):
                self.up(distance)


@dataclass
class PositionWithAim(Position):
    horizontal: int = 0
    depth: int = 0
    aim: int = 0

    def forward(self, distance: int) -> None:
        self.horizontal += distance
        self.depth += self.aim * distance

    def down(self, distance: int) -> None:
        self.aim += distance

    def up(self, distance: int) -> None:
        self.aim -= distance
