from dataclasses import dataclass, field
from enum import Enum, auto
from typing import ClassVar

from maze_muncher.board import Board
from maze_muncher.movement import Direction
from maze_muncher.player import Player


class GameState(Enum):
    PLAYING = auto()
    WON = auto()


@dataclass
class Game:
    board: Board
    player: Player
    score: int = 0
    state: GameState = field(init=False)

    PELLET_SCORE: ClassVar[int] = 10

    def __post_init__(self) -> None:
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

        if self.board.remaining_pellets() == 0:
            self.state = GameState.WON

        return True
