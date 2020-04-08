from enum import Enum
from chap8.board import Move, Board, Piece
from collections import Counter


class C4Piece(Piece, Enum):
    Y = "Y"
    R = "R"
    E = " "

    @property
    def opposite(self):
        if self == C4Piece.Y:
            return C4Piece.R
        elif self == C4Piece.R:
            return C4Piece.Y
        else:
            return C4Piece.E

    def __str__(self):
        return self.value


def generate_segments(num_columns, num_rows, segment_length):
    segments = []
    for c in range(num_columns):
        for r in range(num_rows - segment_length + 1):
            segment = [(c, r + t) for t in range(segment_length)]
            segments.append(segment)

    for c in range(num_columns - segment_length + 1):
        for r in range(num_rows):
            segment = [(c + t, r) for t in range(segment_length)]
            segments.append(segment)

    for c in range(num_columns - segment_length + 1):
        for r in range(num_rows - segment_length + 1):
            segment = [(c + t, r + t) for t in range(segment_length)]
            segments.append(segment)

    for c in range(num_columns - segment_length + 1):
        for r in range(segment_length - 1, num_rows):
            segment = [(c + t, r - t) for t in range(segment_length)]
            segments.append(segment)
    return segments


class C4Board(Board):
    NUM_COLS = 8
    NUM_ROWS = 8
    SEGMENT_LENGTH = 4
    SEGMENTS = generate_segments(NUM_COLS, NUM_ROWS, SEGMENT_LENGTH)

    def __init__(self, position=None, turn=C4Piece.Y):
        if position is None:
            self.position = [C4Board.Column() for _ in range(C4Board.NUM_COLS)]
        else:
            self.position = position
        self._turn = turn

    @property
    def turn(self):
        return self._turn

    def move(self, location):
        new_position = self.position.copy()
        for c in range(C4Board.NUM_COLS):
            new_position[c] = self.position[c].copy()
        new_position[location].push(self._turn)
        return C4Board(new_position, self._turn.opposite)

    @property
    def legal_moves(self):
        return [
            Move(c) for c in range(C4Board.NUM_COLS) if not self.position[c].is_full
        ]

    def _count_segment(self, segment):
        counter = Counter([self.position[c][r] for c, r in segment])
        return counter[C4Piece.Y], counter[C4Piece.R]

    @property
    def is_win(self):
        for segment in C4Board.SEGMENTS:
            yellows, reds = self._count_segment(segment)
            if yellows == 4 or reds == 4:
                return True
        return False

    def _evaluate_segment(self, segment, player):
        yellows, reds = self._count_segment(segment)
        if yellows > 0 and reds > 0:
            return 0
        count = max(yellows, reds)
        score = 0
        if count == 2:
            score = 1
        elif count == 3:
            score = 100
        elif count == 4:
            score = 1000000
        color = C4Piece.Y if yellows > reds else C4Piece.R
        if color != player:
            return -score
        return score

    def evaluate(self, player):
        total = 0
        for segment in C4Board.SEGMENTS:
            total += self._evaluate_segment(segment, player)
        return total

    def __repr__(self):
        display = ""
        for r in reversed(range(C4Board.NUM_ROWS)):
            display += "|"
            for c in range(C4Board.NUM_COLS):
                display += f"{self.position[c][r]}|"
            display += "\n"
        return display

    class Column:
        def __init__(self):
            self._container = []

        @property
        def is_full(self):
            return len(self._container) == C4Board.NUM_ROWS

        def push(self, piece):
            if self.is_full:
                raise OverflowError("Trying to push piece to full column.")
            self._container.append(piece)

        def __getitem__(self, index):
            if index > len(self._container) - 1:
                return C4Piece.E
            return self._container[index]

        def __repr__(self):
            return repr(self._container)

        def copy(self):
            copied = C4Board.Column()
            copied._container = self._container.copy()
            return copied

