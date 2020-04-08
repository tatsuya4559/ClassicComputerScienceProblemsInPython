from __future__ import annotations
from typing import List
from enum import Enum
from chap8.board import Board, Piece, Move


class TTTPiece(Piece, Enum):
    X = "X"
    O = "O"
    E = " "

    @property
    def opposite(self) -> TTTPiece:
        if self == TTTPiece.X:
            return TTTPiece.O
        elif self == TTTPiece.O:
            return TTTPiece.X
        else:
            return TTTPiece.E

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class TTTBoard(Board):
    def __init__(
        self, position: List[TTTPiece] = [TTTPiece.E] * 9, turn: TTTPiece = TTTPiece.X
    ) -> None:
        self.position: List[TTTPiece] = position
        self._turn: TTTPiece = turn

    @property
    def turn(self) -> Piece:
        return self._turn

    def move(self, location: Move) -> Board:
        temp_position: List[TTTPiece] = self.position.copy()
        temp_position[location] = self._turn
        return TTTBoard(temp_position, self._turn.opposite)

    @property
    def legal_moves(self) -> List[Move]:
        return [Move(i) for i, p in enumerate(self.position) if p == TTTPiece.E]

    @property
    def is_win(self) -> bool:
        win_pattern = (
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        )
        return any(
            TTTPiece.E != self.position[i] == self.position[j] == self.position[k]
            for i, j, k in win_pattern
        )

    # 型システムが汚いー
    # やっぱり強制力がない型はあまり意味ないなあ
    def evaluate(self, player: Piece) -> float:
        if self.is_win:
            return -1 if self.turn == player else 1
        return 0

    def __repr__(self) -> str:
        return """{0}|{1}|{2}
-----
{3}|{4}|{5}
-----
{6}|{7}|{8}""".format(
            *self.position
        )
