from random import Random

from maze_muncher.board import Board, Position
from maze_muncher.enemy import Enemy
from maze_muncher.game import Game, GameState
from maze_muncher.movement import Direction
from maze_muncher.player import Player


def test_enemy_moves_after_successful_player_move() -> None:
    board = Board(
        [
            "#######",
            "#.....#",
            "#######",
        ]
    )
    enemy = Enemy(Position(1, 4))
    game = Game(
        board=board,
        player=Player(Position(1, 1)),
        enemy=enemy,
        random_source=Random(1),
    )

    assert game.move_player(Direction.RIGHT)
    assert enemy.position != Position(1, 4)
    assert board.can_move_to(enemy.position)


def test_enemy_does_not_move_after_blocked_player_move() -> None:
    board = Board(
        [
            "#####",
            "#...#",
            "#####",
        ]
    )
    enemy = Enemy(Position(1, 3))
    game = Game(
        board=board,
        player=Player(Position(1, 1)),
        enemy=enemy,
        random_source=Random(1),
    )

    assert not game.move_player(Direction.UP)
    assert enemy.position == Position(1, 3)


def test_player_loses_life_when_moving_onto_enemy() -> None:
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
    )

    assert game.move_player(Direction.RIGHT)

    assert game.lives == 2
    assert game.player.position == Position(1, 1)
    assert game.enemy is not None
    assert game.enemy.position == Position(1, 2)
    assert game.state is GameState.PLAYING


def test_player_loses_life_when_enemy_moves_onto_player() -> None:
    board = Board(
        [
            "######",
            "#...##",
            "######",
        ]
    )
    game = Game(
        board=board,
        player=Player(Position(1, 1)),
        enemy=Enemy(Position(1, 3)),
    )

    assert game.move_player(Direction.RIGHT)

    assert game.lives == 2
    assert game.player.position == Position(1, 1)
    assert game.enemy is not None
    assert game.enemy.position == Position(1, 3)
    assert game.state is GameState.PLAYING


def test_final_life_changes_state_to_game_over() -> None:
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
        lives=1,
    )

    assert game.move_player(Direction.RIGHT)

    assert game.lives == 0
    assert game.state is GameState.GAME_OVER


def test_player_cannot_move_after_game_over() -> None:
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
        lives=1,
    )

    assert game.move_player(Direction.RIGHT)
    assert game.state is GameState.GAME_OVER

    assert not game.move_player(Direction.LEFT)
    