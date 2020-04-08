import unittest
from chap8.minimax import find_best_move
from chap8.tictactoe import TTTPiece, TTTBoard
from chap8.board import Move

class TTTMinimaxTest(unittest.TestCase):
    def test_easy_position(self):
        position = [
            TTTPiece.X, TTTPiece.O, TTTPiece.X,
            TTTPiece.X, TTTPiece.E, TTTPiece.O,
            TTTPiece.E, TTTPiece.E, TTTPiece.O,
        ]
        test_board = TTTBoard(position, TTTPiece.X)
        actual = find_best_move(test_board)
        self.assertEqual(6, actual)

    def test_block_position(self):
        position = [
            TTTPiece.X, TTTPiece.E, TTTPiece.E,
            TTTPiece.E, TTTPiece.E, TTTPiece.O,
            TTTPiece.E, TTTPiece.X, TTTPiece.O,
        ]
        test_board = TTTBoard(position, TTTPiece.X)
        actual = find_best_move(test_board)
        self.assertEqual(2, actual)

    def test_hard_position(self):
        '''このテストは期待をどうやって求めたのか'''
        position = [
            TTTPiece.X, TTTPiece.E, TTTPiece.E,
            TTTPiece.E, TTTPiece.E, TTTPiece.O,
            TTTPiece.O, TTTPiece.X, TTTPiece.E,
        ]
        test_board = TTTBoard(position, TTTPiece.X)
        actual = find_best_move(test_board)
        self.assertEqual(1, actual)

