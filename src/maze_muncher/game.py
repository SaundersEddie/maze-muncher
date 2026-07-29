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
    powered_moves_remaining: int = 0
    random_source: Random = field(
        default_factory=Random,
        repr=False,
        compare=False,
    )
    state: GameState = field(init=False)
    player_start: Position = field(init=False)
    enemy_start: Position | None = field(init=False)

    PELLET_SCORE: ClassVar[int] = 10
    POWER_PELLET_SCORE: ClassVar[int] = 50
    ENEMY_SCORE: ClassVar[int] = 200
    POWERED_MOVE_COUNT: ClassVar[int] = 8

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

    @property
    def is_powered_up(self) -> bool:
        return self.powered_moves_remaining > 0

    def move_player(self, direction: Direction) -> bool:
        if self.state is not GameState.PLAYING:
            return False

        moved = self.player.move(direction, self.board)

        if not moved:
            return False

        collected_power_pellet = self._collect_current_tile()

        if self._has_collision():
            self._resolve_collision()

            if (
                self.state is GameState.PLAYING
                and self.board.remaining_pellets() == 0
            ):
                self.state = GameState.WON

            return True

        if self.board.remaining_pellets() == 0:
            self.state = GameState.WON
            return True

        if self.enemy is not None:
            self.enemy.move(self.board, self.random_source)

            if self._has_collision():
                self._resolve_collision()

        if (
            not collected_power_pellet
            and self.is_powered_up
            and self.state is GameState.PLAYING
        ):
            self.powered_moves_remaining -= 1

        return True

    def _collect_current_tile(self) -> bool:
        if self.board.collect_power_pellet(
            self.player.position
        ):
            self.score += self.POWER_PELLET_SCORE
            self.powered_moves_remaining = (
                self.POWERED_MOVE_COUNT
            )
            return True

        if self.board.collect_pellet(
            self.player.position
        ):
            self.score += self.PELLET_SCORE

        return False

    def _has_collision(self) -> bool:
        return (
            self.enemy is not None
            and self.player.position == self.enemy.position
        )

    def _resolve_collision(self) -> None:
        if self.is_powered_up:
            self._eat_enemy()
        else:
            self._lose_life()

    def _eat_enemy(self) -> None:
        self.score += self.ENEMY_SCORE

        if (
            self.enemy is not None
            and self.enemy_start is not None
        ):
            self.enemy.position = self.enemy_start

    def _lose_life(self) -> None:
        self.lives -= 1
        self.powered_moves_remaining = 0

        if self.lives == 0:
            self.state = GameState.GAME_OVER
            return

        self.player.position = self.player_start

        if (
            self.enemy is not None
            and self.enemy_start is not None
        ):
            self.enemy.position = self.enemy_start
            