from maze_muncher.board import Board, Position
from maze_muncher.enemy import Enemy
from maze_muncher.game import Game, GameState
from maze_muncher.movement import Direction
from maze_muncher.player import Player


def test_game_accepts_multiple_enemies() -> None:
    first_enemy = Enemy(Position(1, 3))
    second_enemy = Enemy(Position(1, 5))

    game = Game(
        board=Board(
            [
                "#######",
                "#.....#",
                "#######",
            ]
        ),
        player=Player(Position(1, 1)),
        enemies=[
            first_enemy,
            second_enemy,
        ],
    )

    assert game.enemies == [
        first_enemy,
        second_enemy,
    ]

    # Compatibility access returns the first meanie.
    assert game.enemy is first_enemy


def test_move_enemy_moves_all_enemies() -> None:
    first_enemy = Enemy(
        position=Position(1, 2),
        last_direction=Direction.RIGHT,
    )
    second_enemy = Enemy(
        position=Position(1, 4),
        last_direction=Direction.LEFT,
    )

    game = Game(
        board=Board(
            [
                "#######",
                "#.....#",
                "#######",
            ]
        ),
        player=Player(Position(1, 5)),
        enemies=[
            first_enemy,
            second_enemy,
        ],
        powered_moves_remaining=2,
    )

    assert game.move_enemy()

    assert first_enemy.position == Position(1, 3)
    assert second_enemy.position == Position(1, 3)


def test_collision_with_any_enemy_loses_one_life() -> None:
    first_enemy = Enemy(Position(1, 4))
    second_enemy = Enemy(Position(1, 2))

    game = Game(
        board=Board(
            [
                "#######",
                "#.....#",
                "#######",
            ]
        ),
        player=Player(Position(1, 1)),
        enemies=[
            first_enemy,
            second_enemy,
        ],
    )

    assert game.move_player(Direction.RIGHT)

    assert game.lives == 2
    assert game.player.position == Position(1, 1)

    assert first_enemy.position == Position(1, 4)
    assert second_enemy.position == Position(1, 2)


def test_life_loss_resets_every_enemy() -> None:
    first_enemy = Enemy(Position(1, 4))
    second_enemy = Enemy(Position(1, 5))

    game = Game(
        board=Board(
            [
                "#######",
                "#.....#",
                "#######",
            ]
        ),
        player=Player(Position(1, 1)),
        enemies=[
            first_enemy,
            second_enemy,
        ],
    )

    first_enemy.position = Position(1, 2)
    second_enemy.position = Position(1, 3)

    assert game.move_player(Direction.RIGHT)

    assert game.lives == 2
    assert first_enemy.position == Position(1, 4)
    assert second_enemy.position == Position(1, 5)


def test_powered_player_eats_only_colliding_enemy() -> None:
    first_enemy = Enemy(Position(1, 4))
    second_enemy = Enemy(Position(1, 5))

    game = Game(
        board=Board(
            [
                "#######",
                "#.....#",
                "#######",
            ]
        ),
        player=Player(Position(1, 1)),
        enemies=[
            first_enemy,
            second_enemy,
        ],
        powered_moves_remaining=3,
    )

    first_enemy.position = Position(1, 2)
    second_enemy.position = Position(1, 3)

    assert game.move_player(Direction.RIGHT)

    assert game.lives == 3
    assert game.score == (
        Game.PELLET_SCORE
        + Game.ENEMY_SCORE
    )

    assert first_enemy.position == Position(1, 4)
    assert second_enemy.position == Position(1, 3)


def test_powered_player_can_eat_multiple_enemies_on_same_tile() -> None:
    first_enemy = Enemy(Position(1, 4))
    second_enemy = Enemy(Position(1, 5))

    game = Game(
        board=Board(
            [
                "#######",
                "#.....#",
                "#######",
            ]
        ),
        player=Player(Position(1, 1)),
        enemies=[
            first_enemy,
            second_enemy,
        ],
        powered_moves_remaining=3,
    )

    first_enemy.position = Position(1, 2)
    second_enemy.position = Position(1, 2)

    assert game.move_player(Direction.RIGHT)

    assert game.lives == 3
    assert game.score == (
        Game.PELLET_SCORE
        + Game.ENEMY_SCORE * 2
    )

    assert first_enemy.position == Position(1, 4)
    assert second_enemy.position == Position(1, 5)


def test_multiple_enemies_cannot_move_after_game_over() -> None:
    first_enemy = Enemy(Position(1, 2))
    second_enemy = Enemy(Position(1, 3))

    game = Game(
        board=Board(
            [
                "#####",
                "#...#",
                "#####",
            ]
        ),
        player=Player(Position(1, 1)),
        enemies=[
            first_enemy,
            second_enemy,
        ],
        lives=1,
    )

    assert game.move_player(Direction.RIGHT)
    assert game.state is GameState.GAME_OVER

    assert not game.move_enemy()
    