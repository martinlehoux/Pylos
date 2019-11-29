"""Module defining the Position class, that store a position in a board."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Position:
    """Position instance stores a position on a board.

    Attributes:
        floor (int): The floor where the virtual ball is located.
        row (int): The row where the virtual ball is located.
        col (int): The col where the virtual ball is located.
    """
    floor: int
    row: int
    col: int

    def __post_init__(self):
        pass
        # TODO: Check position validity

    def __eq__(self, pos: Position):
        assert isinstance(pos, Position), "can't compare Position to other class"
        return self.floor == pos.floor and self.row == pos.row and self.col == pos.col

    def __str__(self):
        return f"[{self.floor}][{self.row}][{self.col}]"
