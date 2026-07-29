from dataclasses import dataclass
from random import Random
from typing import ClassVar

from maze_muncher.board import Board, Position
from maze_muncher.movement import Direction, next_position


@dataclass
class Enemy:
    position: Position
    last_direction: Direction | None = None

    OPPOSITE_DIRECTION: ClassVar[dict[Direction, Direction]] = {
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT,
    }

    def valid_directions(self, board: Board) -> list[Direction]:
        return [
            direction
            for direction in Direction
            if board.can_move_to(
                next_position(self.position, direction)
            )
        ]

    def movement_directions(
        self,
        board: Board,
    ) -> list[Direction]:
        directions = self.valid_directions(board)

        if self.last_direction is None:
            return directions

        reverse_direction = self.OPPOSITE_DIRECTION[
            self.last_direction
        ]

        non_reverse_directions = [
            direction
            for direction in directions
            if direction is not reverse_direction
        ]

        if non_reverse_directions:
            return non_reverse_directions

        return directions

    def move(
        self,
        board: Board,
        random_source: Random,
    ) -> bool:
        directions = self.movement_directions(board)

        if not directions:
            return False

        direction = random_source.choice(directions)

        self.position = next_position(
            self.position,
            direction,
        )
        self.last_direction = direction

        return True
    