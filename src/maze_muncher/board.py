from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    row: int
    column: int


class Board:
    WALL = "#"
    PELLET = "."
    POWER_PELLET = "o"
    EMPTY = " "

    def __init__(self, layout: list[str]) -> None:
        if not layout:
            raise ValueError("Board layout cannot be empty.")

        width = len(layout[0])

        if width == 0:
            raise ValueError("Board rows cannot be empty.")

        if any(len(row) != width for row in layout):
            raise ValueError(
                "All board rows must have the same width."
            )

        self._layout = [list(row) for row in layout]
        self.height = len(layout)
        self.width = width

    def is_inside(self, position: Position) -> bool:
        return (
            0 <= position.row < self.height
            and 0 <= position.column < self.width
        )

    def is_wall(self, position: Position) -> bool:
        if not self.is_inside(position):
            return True

        return (
            self._layout[position.row][position.column]
            == self.WALL
        )

    def can_move_to(self, position: Position) -> bool:
        return (
            self.is_inside(position)
            and not self.is_wall(position)
        )

    def has_pellet(self, position: Position) -> bool:
        if not self.is_inside(position):
            return False

        return (
            self._layout[position.row][position.column]
            == self.PELLET
        )

    def has_power_pellet(
        self,
        position: Position,
    ) -> bool:
        if not self.is_inside(position):
            return False

        return (
            self._layout[position.row][position.column]
            == self.POWER_PELLET
        )

    def collect_pellet(
        self,
        position: Position,
    ) -> bool:
        if not self.has_pellet(position):
            return False

        self._layout[position.row][position.column] = (
            self.EMPTY
        )
        return True

    def collect_power_pellet(
        self,
        position: Position,
    ) -> bool:
        if not self.has_power_pellet(position):
            return False

        self._layout[position.row][position.column] = (
            self.EMPTY
        )
        return True

    def remaining_pellets(self) -> int:
        return sum(
            tile in (
                self.PELLET,
                self.POWER_PELLET,
            )
            for row in self._layout
            for tile in row
        )
        