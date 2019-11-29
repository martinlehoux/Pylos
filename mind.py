"""Module defining the Mind class and its subclasses, intelligences playing the game.
"""

from __future__ import annotations

import random
from typing import List, Tuple

from board import Board
from position import Position


class Mind:
    """Abstract class for Intelligence playing.

    Attributes:
        name (str): Name of the mind, for display purpose only.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def choose_action(self, board: Board, self_balls: int, opponent_balls: int) -> Tuple[str, List[Position]]:
        """Choose an action for the engine by looking at the board.

        Args:
            board (Board): Board to look at for taking the decision.
            self_balls (int): The player remaining balls.
            opponent_balls (int): The opponent remaining balls.

        Returns:
            action (str): The action name.
            positions (list): The list of positions to pass as args to the action.
        """
        raise NotImplementedError("choose_action not implemented")


class UserMind(Mind):
    """Mind implementation that waits for user input."""

    def choose_action(self, board: Board, self_balls: int, opponent_balls: int) -> Tuple[str, List[Position]]:
        line = input(f"action ? ").split()
        action = line.pop(0)
        positions: List[Position] = []
        for pos_data in line:
            positions.append(Position(*map(int, pos_data)))
        return action, positions


class RandomMind(Mind):
    """Mind implementation that chooses a random 'put' position where it can play."""

    def choose_action(self, board: Board, self_balls: int, opponent_balls: int) -> Tuple[str, List[Position]]:
        available_positions: List[Position] = []
        for floor in range(board.size):
            for row in range(board.get_floor_size(floor)):
                for col in range(board.get_floor_size(floor)):
                    pos = Position(floor, row, col)
                    if all(map(board.get_color, board.get_below_pos(pos))):
                        if board.get_color(pos) is None:
                            available_positions.append(pos)
        return 'put', random.choices(available_positions, k=1)
