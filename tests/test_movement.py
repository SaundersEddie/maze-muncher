import pytest

from maze_muncher.board import Position
from maze_muncher.movement import Direction, next_position


@pytest.mark.parametrize(
    ("direction", "expected"),
    [
        (Direction.UP, Position(1, 2)),
        (Direction.DOWN, Position(3, 2)),
        (Direction.LEFT, Position(2, 1)),
        (Direction.RIGHT, Position(2, 3)),
    ],
)
def test_next_position(
    direction: Direction,
    expected: Position,
) -> None:
    start = Position(2, 2)

    assert next_position(start, direction) == expected
    