from dataclasses import dataclass

from maze_muncher.board import Board, Position
from maze_muncher.movement import Direction, next_position


@dataclass
class Player:
    position: Position

    def move(self, direction: Direction, board: Board) -> bool:
        destination = next_position(self.position, direction)

        if not board.can_move_to(destination):
            return False

        self.position = destination
        return True
    