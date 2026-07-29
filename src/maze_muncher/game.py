from dataclasses import dataclass, field
from enum import Enum, auto
from random import Random
from typing import ClassVar

from maze_muncher.board import Board, Position
from maze_muncher.enemy import Enemy
from maze_muncher.movement import Direction
from maze_muncher.player import Player


class GameState(Enum):
    PLAYING = auto()
    WON = auto()
    GAME_OVER = auto()


@dataclass
class Game:
    board: Board
    player: Player
    enemy: Enemy | None = None
    score: int = 0
    lives: int = 3
    random_source: Random = field(
        default_factory=Random,
        repr=False,
        compare=False,
    )
    state: GameState = field(init=False)
    player_start: Position = field(init=False)
    enemy_start: Position | None = field(init=False)

    PELLET_SCORE: ClassVar[int] = 10

    def __post_init__(self) -> None:
        self.player_start = self.player.position
        self.enemy_start = (
            self.enemy.position
            if self.enemy is not None
            else None
        )

        self.state = (
            GameState.WON
            if self.board.remaining_pellets() == 0
            else GameState.PLAYING
        )

    def move_player(self, direction: Direction) -> bool:
        if self.state is not GameState.PLAYING:
            return False

        moved = self.player.move(direction, self.board)

        if not moved:
            return False

        if self.board.collect_pellet(self.player.position):
            self.score += self.PELLET_SCORE

        if self._has_collision():
            self._lose_life()
            return True

        if self.board.remaining_pellets() == 0:
            self.state = GameState.WON
            return True

        if self.enemy is not None:
            self.enemy.move(self.board, self.random_source)

            if self._has_collision():
                self._lose_life()

        return True

    def _has_collision(self) -> bool:
        return (
            self.enemy is not None
            and self.player.position == self.enemy.position
        )

    def _lose_life(self) -> None:
        self.lives -= 1

        if self.lives == 0:
            self.state = GameState.GAME_OVER
            return

        self.player.position = self.player_start

        if self.enemy is not None and self.enemy_start is not None:
            self.enemy.position = self.enemy_start
            