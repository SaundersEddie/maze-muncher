from maze_muncher.board import Board, Position
from maze_muncher.game import Game, GameState
from maze_muncher.movement import Direction
from maze_muncher.player import Player


def create_game() -> Game:
    board = Board(
        [
            "#####",
            "#...#",
            "#.#.#",
            "#...#",
            "#####",
        ]
    )
    player = Player(Position(1, 1))

    return Game(board=board, player=player)


def test_player_collects_pellet_after_moving() -> None:
    game = create_game()

    assert game.move_player(Direction.RIGHT)

    assert game.player.position == Position(1, 2)
    assert not game.board.has_pellet(Position(1, 2))


def test_collecting_pellet_increases_score() -> None:
    game = create_game()

    assert game.move_player(Direction.RIGHT)

    assert game.score == 10


def test_player_cannot_score_from_blocked_move() -> None:
    game = create_game()

    assert not game.move_player(Direction.UP)

    assert game.score == 0
    assert game.player.position == Position(1, 1)


def test_empty_tile_does_not_score_twice() -> None:
    board = Board(
        [
            "#####",
            "#. .#",
            "#####",
        ]
    )
    game = Game(
        board=board,
        player=Player(Position(1, 2)),
    )

    assert game.move_player(Direction.LEFT)
    assert game.score == 10

    assert game.move_player(Direction.RIGHT)
    assert game.score == 10

    assert game.move_player(Direction.LEFT)
    assert game.score == 10


def test_multiple_pellets_accumulate_score() -> None:
    game = create_game()

    assert game.move_player(Direction.RIGHT)
    assert game.move_player(Direction.RIGHT)

    assert game.score == 20


def test_game_starts_in_playing_state_when_pellets_remain() -> None:
    game = create_game()

    assert game.state is GameState.PLAYING


def test_game_starts_won_when_board_has_no_pellets() -> None:
    board = Board(
        [
            "#####",
            "#   #",
            "#####",
        ]
    )
    game = Game(
        board=board,
        player=Player(Position(1, 1)),
    )

    assert game.state is GameState.WON


def test_collecting_final_pellet_wins_game() -> None:
    board = Board(
        [
            "#####",
            "# . #",
            "#####",
        ]
    )
    game = Game(
        board=board,
        player=Player(Position(1, 1)),
    )

    assert game.move_player(Direction.RIGHT)

    assert game.score == 10
    assert game.board.remaining_pellets() == 0
    assert game.state is GameState.WON


def test_player_cannot_move_after_winning() -> None:
    board = Board(
        [
            "#####",
            "# . #",
            "#####",
        ]
    )
    game = Game(
        board=board,
        player=Player(Position(1, 1)),
    )

    assert game.move_player(Direction.RIGHT)
    assert game.state is GameState.WON

    assert not game.move_player(Direction.RIGHT)
    assert game.player.position == Position(1, 2)
    assert game.score == 10