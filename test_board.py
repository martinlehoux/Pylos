from board import Board
from position import Position


def test_init():
    board = Board()
    assert board.size == 4
    for floor in board._board:
        for row in floor:
            for col in row:
                assert col is None

def test_get_below_pos():
    board = Board()

    init_pos = Position(0, 0, 0)
    positions = board.get_below_pos(init_pos)
    assert len(positions) == 0

    init_pos = Position(1, 0, 0)
    positions = board.get_below_pos(init_pos)
    assert len(positions) == 4
    assert Position(0, 0, 0) in positions

def test_get_above_pos():
