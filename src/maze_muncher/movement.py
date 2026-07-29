from enum import Enum

from maze_muncher.board import Position


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


def next_position(position: Position, direction: Direction) -> Position:
    row_change, column_change = direction.value

    return Position(
        row=position.row + row_change,
        column=position.column + column_change,
    )
