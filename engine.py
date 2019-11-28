from __future__ import annotations
from typing import List, Tuple
from mind import Mind, UserMind, RandomMind
from position import Position
import pickle
from os.path import isfile
import os
from board import Board
from time import sleep

class Player:
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
        pos = Position(self.size - 1, 0, 0)
        color = self.board.get_color(pos)
        if color is None:
            return None
        for player in self.players:
            if player.color == color:
                return player
        raise ValueError(f"no winner found for color {color}")

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
        with open('save.data', 'wb') as f:
            pickle.dump((self.board, self.players, self.round), f)

    def load(self):
        if isfile('save.data'):
            with open('save.data', 'rb') as f:
                self.board, self.players, self.round = pickle.load(f)

    def run(self):
        print(self.board)
        while self.get_winner() is None:
            # sleep(0.1)
            player = self.players[self.round % 2]
            opponent = self.players[(self.round + 1) % 2]
            print(f"[{player}:{player.balls}] ", end="")
            try:
                action, positions = player.mind.choose_action(self.board, player.balls, opponent.balls)
            except AssertionError as err:
                print(err)
                continue
            if action not in self.ACTIONS:
                print(f"action:{action} doesn't exist")
                continue
            if len(positions) != self.ACTIONS.get(action):
                print(f"the number {len(positions)} of positions doesn't fit with the action:{action}")
                continue
            if action == 'save':
                self.save()
                self.round += 1
                quit(0)
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
        if isfile('save.data'): os.remove('save.data')


if __name__ == "__main__":
    # engine = Engine((UserMind('kaga'), UserMind('eno')), 4)
    engine = Engine((RandomMind('bot1'), RandomMind('bot2')), 4)
    # for i in range(3):
    #     for j in range(3):
    #         pos = Position(0, i, j)
    #         engine._put_ball(engine.COLORS[(i+j)%2], pos)
    # engine._move_ball(Position(0, 2, 2), Position(1, 0, 0))
    engine.run()