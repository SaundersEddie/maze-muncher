from maze_muncher.board import Board, Position
from maze_muncher.enemy import Enemy
from maze_muncher.game import Game, GameState
from maze_muncher.movement import Direction
from maze_muncher.player import Player


def test_collecting_power_pellet_activates_power() -> None:
    board = Board(
        [
            "#####",
            "#o..#",
            "#####",
        ]
    )
    game = Game(
        board=board,
        player=Player(Position(1, 2)),
    )

    assert game.move_player(Direction.LEFT)

    assert game.is_powered_up
    assert (
        game.powered_moves_remaining
        == Game.POWERED_MOVE_COUNT
    )
    assert game.score == Game.POWER_PELLET_SCORE


def test_powered_move_count_decreases_after_later_move() -> None:
    board = Board(
        [
            "######",
            "#o...#",
            "######",
        ]
    )
    game = Game(
        board=board,
        player=Player(Position(1, 2)),
    )

    assert game.move_player(Direction.LEFT)
    assert (
        game.powered_moves_remaining
        == Game.POWERED_MOVE_COUNT
    )

    assert game.move_player(Direction.RIGHT)
    assert (
        game.powered_moves_remaining
        == Game.POWERED_MOVE_COUNT - 1
    )


def test_blocked_move_does_not_reduce_power() -> None:
    board = Board(
        [
            "#####",
            "#o..#",
            "#####",
        ]
    )
    game = Game(
        board=board,
        player=Player(Position(1, 2)),
    )

    assert game.move_player(Direction.LEFT)

    powered_moves = game.powered_moves_remaining

    assert not game.move_player(Direction.UP)
    assert game.powered_moves_remaining == powered_moves


def test_powered_player_eats_enemy() -> None:
    board = Board(
        [
            "#####",
            "#.o.#",
            "#####",
        ]
    )
    enemy = Enemy(Position(1, 2))
    game = Game(
        board=board,
        player=Player(Position(1, 1)),
        enemy=enemy,
    )

    assert game.move_player(Direction.RIGHT)

    assert game.lives == 3
    assert game.score == (
        Game.POWER_PELLET_SCORE
        + Game.ENEMY_SCORE
    )
    assert enemy.position == Position(1, 2)
    assert game.state is GameState.PLAYING


def test_enemy_is_reset_after_being_eaten() -> None:
    board = Board(
        [
            "#######",
            "#.....#",
            "#######",
        ]
    )
    enemy = Enemy(Position(1, 5))
    game = Game(
        board=board,
        player=Player(Position(1, 2)),
        enemy=enemy,
        powered_moves_remaining=3,
    )

    enemy.position = Position(1, 3)

    assert game.move_player(Direction.RIGHT)

    assert enemy.position == Position(1, 5)
    assert game.lives == 3
    assert game.score == (
        Game.PELLET_SCORE
        + Game.ENEMY_SCORE
    )


def test_collision_after_power_expires_loses_life() -> None:
    board = Board(
        [
            "#####",
            "#...#",
            "#####",
        ]
    )
    game = Game(
        board=board,
        player=Player(Position(1, 1)),
        enemy=Enemy(Position(1, 2)),
        powered_moves_remaining=0,
    )

    assert game.move_player(Direction.RIGHT)

    assert game.lives == 2
    assert game.player.position == Position(1, 1)


def test_losing_life_clears_remaining_power() -> None:
    board = Board(
        [
            "#####",
            "#...#",
            "#####",
        ]
    )
    game = Game(
        board=board,
        player=Player(Position(1, 1)),
        enemy=Enemy(Position(1, 2)),
        powered_moves_remaining=0,
    )

    assert game.move_player(Direction.RIGHT)

    assert not game.is_powered_up
    assert game.powered_moves_remaining == 0
    