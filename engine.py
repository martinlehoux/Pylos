"""Module defining the game engine, handling concurrency and actions.
"""

from __future__ import annotations

import os
import pickle
import sys
from os.path import isfile
from typing import Tuple

from board import Board
from mind import Mind, RandomMind, UserMind
from position import Position


class Player:
    """Defines the playing mind, by associating a color and balls.

    Attributes:
        mind (Mind): The intelligence playing.
        balls (int): Init balls number.
        color (str): Player balls color.
    """
    mind: Mind
    balls: int = 15
    color: str = None

    def __init__(self, mind: Mind, color: str):
        assert color in Engine.COLORS, f"color not in {Engine.COLORS}"
        self.color = color
        assert isinstance(mind, Mind), "mind is not a Mind"
        self.mind = mind

    def __str__(self):
        return f"{self.mind}({self.color})"


class Engine:
    """Defines the game Egnine, handling actions from minds and on the board.

    Attributes:
        size (int): The size, ie the size of the base floor.
        board (Board): The board storing the game state.
        players (Player, Player): The two players playing the game.
        round (int): Current game round.

    Const:
        COLORS (str, str): Available balls colors.
        ACTIONS (dict): Available actions for minds, with the number of positions to give as value.
    """
    size: int = 4
    board: Board = None
    players: Tuple[Player, Player] = (None, None)
    round = 0
    COLORS = ('B', 'W')
    ACTIONS = dict(put=1, remove=1, move=2, save=0)

    def __init__(self, minds: Tuple[Mind, Mind] = (None, None), size: int = 4):
        if isfile('save.data'):
            if input('save found, load it ? (y)') == 'y':
                self.load()
                return
        self.size = size
        self.board = Board(size)
        assert len(minds) == 2, "2 players required"
        for mind in minds:
            assert isinstance(mind, Mind), f"{mind} is not a Player"
        self.players = (
            Player(minds[0], 'W'),
            Player(minds[1], 'B')
        )

    def __str__(self):
        raise NotImplementedError()

    ## GETTERS

    def get_winner(self) -> Mind:
        """Gets the winner if it exists on the board.

        Returns:
            Player if he has won, None if the top cell is empty.
        """
        pos = Position(self.size - 1, 0, 0)
        color = self.board.get_color(pos)
        if color is None:
            return None
        for player in self.players:
            if player.color == color:
                return player
        raise AssertionError(f"no winner found for color {color}")

    ## ACTIONS

    def _put_ball(self, color: str, pos: Position):
        assert color in self.COLORS, f"color not in {self.COLORS}"
        assert self.board.get_color(pos) is None, f"ball already in {pos}"
        for below_pos in self.board.get_below_pos(pos):
            assert self.board.get_color(below_pos) is not None, f"{below_pos} is empty"
        self._set_color(color, pos)

    def _player_put_ball(self, player: Player, pos: Position):
        assert player.balls > 0, f"no more balls for player:{player}"
        self._put_ball(player.color, pos)
        player.balls -= 1

    def _set_color(self, color: str, pos: Position):
        self.board._board[pos.floor][pos.row][pos.col] = color

    def _move_ball(self, from_pos: Position, to_pos: Position):
        assert from_pos != to_pos, f"move ball to same pos {from_pos}"
        assert from_pos.floor < to_pos.floor, "ball must be moved to higher floor"
        for pos in self.board.get_above_pos(from_pos):
            assert self.board.get_color(pos) is None
        color = self.board.get_color(from_pos)
        self._set_color(None, from_pos)
        try:
            for pos in self.board.get_below_pos(to_pos):
                assert self.board.get_color(pos) is not None
        except AssertionError:
            self._set_color(color, from_pos)
            raise AssertionError(f"missing ball below {to_pos}")
        self._set_color(color, to_pos)

    def _player_move_ball(self, player: Player, from_pos: Position, to_pos: Position):
        color = self.board.get_color(from_pos)
        assert color == player.color, f"{player} player can't move {color} ball"
        self._move_ball(from_pos, to_pos)


    ## SCRIPTS
    def save(self):
        """Saves the game state to save file."""
        with open('save.data', 'wb') as file:
            pickle.dump((self.board, self.players, self.round), file)

    def load(self):
        """Loads the game state from save file if it exists."""
        if isfile('save.data'):
            with open('save.data', 'rb') as file:
                self.board, self.players, self.round = pickle.load(file)

    def run(self):
        """Runs the main engine event loop."""
        print(self.board)
        while self.get_winner() is None:
            # sleep(0.1)
            player = self.players[self.round % 2]
            opponent = self.players[(self.round + 1) % 2]
            print(f"[{player}:{player.balls}] ", end="")
            try:
                action, positions = player.mind.choose_action(
                    self.board,
                    player.balls,
                    opponent.balls
                )
            except AssertionError as err:
                print(err)
                continue
            if action not in self.ACTIONS:
                print(f"action:{action} doesn't exist")
                continue
            if len(positions) != self.ACTIONS.get(action):
                print(f"action:{action} requires {len(positions)} positions")
                continue
            if action == 'save':
                self.save()
                self.round += 1
                sys.exit()
            elif action == 'put':
                try:
                    self._player_put_ball(player, *positions)
                    self.round += 1
                except AssertionError as err:
                    print(err)
                    continue
            elif action == 'move':
                try:
                    self._player_move_ball(player, *positions)
                    self.round += 1
                except AssertionError as err:
                    print(err)
                    continue
            print(self.board)

        winner = self.get_winner()
        print(f"player:{winner} has won !")
        if isfile('save.data'):
            os.remove('save.data')


if __name__ == "__main__":
    # engine = Engine((UserMind('kaga'), UserMind('eno')), 4)
    ENGINE = Engine((UserMind('kaga'), RandomMind('bot2')), 4)
    # for i in range(3):
    #     for j in range(3):
    #         pos = Position(0, i, j)
    #         engine._put_ball(engine.COLORS[(i+j)%2], pos)
    # engine._move_ball(Position(0, 2, 2), Position(1, 0, 0))
    ENGINE.run()
