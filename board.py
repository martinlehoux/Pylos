from typing import List
from position import Position

class Board:
    _board: List[List[List[str]]] = []
    size: int = 4

    def __init__(self, size: int = 4):
        self.size = size
        for i in reversed(range(1, size + 1)):
            self._board.append([[None for j in range(i)] for k in range(i)])

    def __str__(self):
        _output = ""
        i = self.size
        for floor in reversed(self._board):
            _floor = ""
            for line in floor:
                _line = " "*i + " ".join(map(lambda x: "_" if x is None else x, line))
                _floor += _line + "\n"
            _output += _floor + "\n"
            i -= 1
        return _output

    def get_below_pos(self, pos: Position) -> List[Position]:
        positions: List[Position] = []
        if pos.floor == 0:
            return positions
        for i in range(2):
            for j in range(2):
                positions.append(Position(pos.floor-1, pos.row+i, pos.col+j))
        return positions

    def get_above_pos(self, pos: Position) -> List[Position]:
        positions: List[Position] = []
        if self.get_floor_size(pos.floor) == 1:
            return positions
        for i in range(2):
            for j in range(2):
                if 0 <= pos.row - i < self.get_floor_size(pos.floor) and 0 <= pos.col - j < self.get_floor_size(pos.floor):
                    positions.append(Position(pos.floor+1, pos.row-i, pos.col-j))
        return positions

    def get_floor_size(self, floor: int) -> int:
        if not 0 <= floor < self.size:
            raise AssertionError(f"floor:{floor} doesn't exist")
        return len(self._board[floor])

    def get_color(self, pos: Position) -> str:
        assert 0 <= pos.row < self.get_floor_size(pos.floor), f"row {pos.floor}:{pos.row} doesn't exist"
        assert 0 <= pos.col < self.get_floor_size(pos.floor), f"col {pos.floor}:{pos.col} doesn't exist"
        return self._board[pos.floor][pos.row][pos.col]