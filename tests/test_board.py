import pytest

from maze_muncher.board import Board, Position


def test_board_rejects_empty_layout() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        Board([])


def test_board_rejects_rows_with_different_widths() -> None:
    with pytest.raises(ValueError, match="same width"):
        Board(
            [
                "###",
                "##",
            ]
        )


def test_position_inside_board_is_detected() -> None:
    board = Board(
        [
            "###",
            "#.#",
            "###",
        ]
    )

    assert board.is_inside(Position(1, 1))


def test_position_outside_board_is_detected() -> None:
    board = Board(
        [
            "###",
            "#.#",
            "###",
        ]
    )

    assert not board.is_inside(Position(-1, 1))
    assert not board.is_inside(Position(3, 1))


def test_wall_position_cannot_be_entered() -> None:
    board = Board(
        [
            "###",
            "#.#",
            "###",
        ]
    )

    assert board.is_wall(Position(0, 0))
    assert not board.can_move_to(Position(0, 0))


def test_floor_position_can_be_entered() -> None:
    board = Board(
        [
            "###",
            "#.#",
            "###",
        ]
    )

    assert not board.is_wall(Position(1, 1))
    assert board.can_move_to(Position(1, 1))


def test_position_outside_board_cannot_be_entered() -> None:
    board = Board(
        [
            "###",
            "#.#",
            "###",
        ]
    )

    assert not board.can_move_to(Position(10, 10))


def test_board_detects_pellet() -> None:
    board = Board(
        [
            "###",
            "#.#",
            "###",
        ]
    )

    assert board.has_pellet(Position(1, 1))


def test_collecting_pellet_removes_it() -> None:
    board = Board(
        [
            "###",
            "#.#",
            "###",
        ]
    )

    assert board.collect_pellet(Position(1, 1))
    assert not board.has_pellet(Position(1, 1))


def test_pellet_cannot_be_collected_twice() -> None:
    board = Board(
        [
            "###",
            "#.#",
            "###",
        ]
    )

    assert board.collect_pellet(Position(1, 1))
    assert not board.collect_pellet(Position(1, 1))


def test_board_counts_remaining_pellets() -> None:
    board = Board(
        [
            "#####",
            "#...#",
            "#.#.#",
            "#####",
        ]
    )

    assert board.remaining_pellets() == 5

