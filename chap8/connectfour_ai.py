from chap8.minimax import find_best_move
from chap8.connectfour import C4Board
from chap8.board import Move, Board


def get_player_move(board):
    player_move = Move(-1)
    while player_move not in board.legal_moves:
        player_move = Move(int(input("Enter a legal col(0-6): ")))
    return player_move


def main():
    board = C4Board()
    while True:
        human_move = get_player_move(board)
        board = board.move(human_move)
        if board.is_win:
            print("You win!")
            return
        elif board.is_draw:
            print("Draw.")
            return
        ai_move = find_best_move(board, 3)
        print(f"AI move is {ai_move}.")
        board = board.move(ai_move)
        print(board)
        if board.is_win:
            print("You lose...")
            return
        elif board.is_draw:
            print("Draw.")
            return


if __name__ == "__main__":
    main()
