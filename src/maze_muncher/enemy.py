from dataclasses import dataclass
from random import Random

from maze_muncher.board import Board, Position
from maze_muncher.movement import Direction, next_position


@dataclass
class Enemy:
    position: Position

    def valid_directions(self, board: Board) -> list[Direction]:
        return [
            direction
            for direction in Direction
            if board.can_move_to(next_position(self.position, direction))
        ]

    def move(self, board: Board, random_source: Random) -> bool:
        directions = self.valid_directions(board)

        if not directions:
            return False

        direction = random_source.choice(directions)
        self.position = next_position(self.position, direction)

        return True
    