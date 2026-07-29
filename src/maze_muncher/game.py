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

    # Kept for compatibility with existing app/tests.
    enemy: Enemy | None = None

    # New multiple-enemy collection.
    enemies: list[Enemy] = field(default_factory=list)

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

    # First enemy start, retained for compatibility.
    enemy_start: Position | None = field(init=False)

    # Start position for every enemy.
    enemy_starts: list[Position] = field(init=False)

    PELLET_SCORE: ClassVar[int] = 10
    POWER_PELLET_SCORE: ClassVar[int] = 50
    ENEMY_SCORE: ClassVar[int] = 200
    POWERED_MOVE_COUNT: ClassVar[int] = 8

    def __post_init__(self) -> None:
        self.player_start = self.player.position

        self.enemies = list(self.enemies)

        if self.enemy is not None:
            enemy_already_present = any(
                existing_enemy is self.enemy
                for existing_enemy in self.enemies
            )

            if not enemy_already_present:
                self.enemies.insert(0, self.enemy)

        if self.enemies:
            self.enemy = self.enemies[0]
        else:
            self.enemy = None

        self.enemy_starts = [
            enemy.position
            for enemy in self.enemies
        ]

        self.enemy_start = (
            self.enemy_starts[0]
            if self.enemy_starts
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

        moved = self.player.move(
            direction,
            self.board,
        )

        if not moved:
            return False

        collected_power_pellet = (
            self._collect_current_tile()
        )

        colliding_enemies = self._colliding_enemies()

        if colliding_enemies:
            self._resolve_player_collisions(
                colliding_enemies
            )

            if (
                self.state is GameState.PLAYING
                and self.board.remaining_pellets() == 0
            ):
                self.state = GameState.WON

            return True

        if self.board.remaining_pellets() == 0:
            self.state = GameState.WON
            return True

        if (
            not collected_power_pellet
            and self.is_powered_up
        ):
            self.powered_moves_remaining -= 1

        return True

    def move_enemy(self) -> bool:
        """Move every meanie once.

        The singular method name is retained so the current app does not
        need to change until the rendering pass.
        """
        if self.state is not GameState.PLAYING:
            return False

        if not self.enemies:
            return False

        any_enemy_moved = False

        for enemy in self.enemies:
            moved = enemy.move(
                self.board,
                self.random_source,
            )

            if not moved:
                continue

            any_enemy_moved = True

            if enemy.position != self.player.position:
                continue

            if self.is_powered_up:
                self._eat_enemy(enemy)
            else:
                self._lose_life()
                break

        return any_enemy_moved

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

    def _colliding_enemies(self) -> list[Enemy]:
        return [
            enemy
            for enemy in self.enemies
            if enemy.position == self.player.position
        ]

    def _resolve_player_collisions(
        self,
        colliding_enemies: list[Enemy],
    ) -> None:
        if self.is_powered_up:
            for enemy in colliding_enemies:
                self._eat_enemy(enemy)
        else:
            self._lose_life()

    def _eat_enemy(self, enemy: Enemy) -> None:
        self.score += self.ENEMY_SCORE
        self._reset_enemy(enemy)

    def _reset_enemy(self, enemy: Enemy) -> None:
        for index, current_enemy in enumerate(
            self.enemies
        ):
            if current_enemy is not enemy:
                continue

            enemy.position = self.enemy_starts[index]
            enemy.last_direction = None
            return

    def _reset_all_enemies(self) -> None:
        for enemy, start_position in zip(
            self.enemies,
            self.enemy_starts,
            strict=True,
        ):
            enemy.position = start_position
            enemy.last_direction = None

    def _lose_life(self) -> None:
        self.lives -= 1
        self.powered_moves_remaining = 0

        if self.lives == 0:
            self.state = GameState.GAME_OVER
            return

        self.player.position = self.player_start
        self._reset_all_enemies()
        