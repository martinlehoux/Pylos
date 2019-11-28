from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Position:
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
