import pytest

from maze_muncher.board import Board, Position
from maze_muncher.movement import Direction
from maze_muncher.player import Player


def create_board() -> Board:
    return Board(
        [
            "#####",
            "#...#",
            "#.#.#",
            "#...#",
            "#####",
        ]
    )


def test_player_moves_to_open_position() -> None:
    board = create_board()
    player = Player(Position(1, 1))

    moved = player.move(Direction.RIGHT, board)

    assert moved
    assert player.position == Position(1, 2)


def test_player_cannot_move_into_wall() -> None:
    board = create_board()
    player = Player(Position(1, 1))

    moved = player.move(Direction.UP, board)

    assert not moved
    assert player.position == Position(1, 1)


def test_player_cannot_move_outside_board() -> None:
    board = Board(
        [
            "...",
            "...",
            "...",
        ]
    )
    player = Player(Position(0, 0))

    moved = player.move(Direction.UP, board)

    assert not moved
    assert player.position == Position(0, 0)


def test_player_can_move_multiple_times() -> None:
    board = create_board()
    player = Player(Position(1, 1))

    assert player.move(Direction.RIGHT, board)
    assert player.move(Direction.DOWN, board)

    assert player.position == Position(2, 2)


def test_player_can_move_multiple_times_double_right() -> None:
    board = create_board()
    player = Player(Position(1, 1))

    assert player.move(Direction.RIGHT, board)
    assert player.move(Direction.RIGHT, board)

    assert player.position == Position(1, 3)


@pytest.mark.xfail(reason="Demonstrates movement into a wall must fail")
def test_player_can_move_multiple_times() -> None:
    board = create_board()
    player = Player(Position(1, 1))

    assert player.move(Direction.RIGHT, board)
    assert player.move(Direction.DOWN, board)

    assert player.position == Position(2, 2)