"""Module defining the board, storing the state of the game board and where are the balls on it."""

from typing import List

from position import Position


class Board:
    """Stores the state of the game board and where are the balls on it.

    Attributes:
        size (int): The size, ie the size of the base floor.
    """
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
        """Gets the positions below the given position.

        Args:
            pos (Position): The position to look below.

        Returns:
            positions (list): The list of positions located below the given position.
        """
        positions: List[Position] = []
        if pos.floor == 0:
            return positions
        for i in range(2):
            for j in range(2):
                positions.append(Position(pos.floor-1, pos.row+i, pos.col+j))
        return positions

    def get_above_pos(self, pos: Position) -> List[Position]:
        """Gets the positions above the given position.

        Args:
            pos (Position): The position to look above.

        Returns:
            positions (list): The list of positions located above the given position.
        """
        positions: List[Position] = []
        if self.get_floor_size(pos.floor) == 1:
            return positions
        for i in range(2):
            for j in range(2):
                if 0 <= pos.row - i < self.get_floor_size(pos.floor):
                    if 0 <= pos.col - j < self.get_floor_size(pos.floor):
                        positions.append(Position(pos.floor+1, pos.row-i, pos.col-j))
        return positions

    def get_floor_size(self, floor: int) -> int:
        """Gets given floor size.

        Args:
            floor (int): The floor index.

        Returns:
            size (int): The floor is size*size.
        """
        if not 0 <= floor < self.size:
            raise AssertionError(f"floor:{floor} doesn't exist")
        return len(self._board[floor])

    def get_color(self, pos: Position) -> str:
        """Gets color of given position.

        Args:
            pos (Position): The position to fetch the color of.

        Returns:
            color (str): The color of the ball found at pos. None if no ball was found.
        """
        if not 0 <= pos.row < self.get_floor_size(pos.floor):
            raise AssertionError(f"row {pos.floor}:{pos.row} doesn't exist")
        if not 0 <= pos.col < self.get_floor_size(pos.floor):
            raise AssertionError(f"col {pos.floor}:{pos.col} doesn't exist")
        return self._board[pos.floor][pos.row][pos.col]
