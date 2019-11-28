from __future__ import annotations
from typing import Tuple, List
from position import Position
from board import Board
import random


class Mind:
    
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def choose_action(self, board: Board, self_balls: int, opponent_balls: int) -> Tuple[str, List[Position]]:
        raise NotImplementedError("choose_action not implemented")


class UserMind(Mind):

    def choose_action(self, board: Board, self_balls: int, opponent_balls: int) -> Tuple[str, List[Position]]:
        line = input(f"action ? ").split()
        action = line.pop(0)
        positions: List[Position] = []
        for pos_data in line:
            positions.append(Position(*map(int, pos_data)))
        return action, positions


class RandomMind(Mind):

    def choose_action(self, board: Board, self_balls: int, opponent_balls: int) -> Tuple[str, List[Position]]:
        available_positions: List[Position] = []
        for floor in range(board.size):
            for row in range(board.get_floor_size(floor)):
                for col in range(board.get_floor_size(floor)):
                    pos = Position(floor, row, col)
                    if all(map(board.get_color, board.get_below_pos(pos))) and board.get_color(pos) is None:
                        available_positions.append(pos)
        return 'put', random.choices(available_positions, k=1)
