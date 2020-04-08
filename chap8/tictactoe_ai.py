from chap8.minimax import find_best_move
from chap8.tictactoe import TTTBoard
from chap8.board import Move, Board


def get_player_move(board):
    player_move = Move(-1)
    while player_move not in board.legal_moves:
        player_move = Move(int(input("Enter a legal position: ")))
    return player_move


def main():
    board = TTTBoard()
    while True:
        print(board.legal_moves)
        human_move = get_player_move(board)
        board = board.move(human_move)
        if board.is_win:
            print("You win!")
            return
        elif board.is_draw:
            print("Draw.")
            return
        ai_move = find_best_move(board)
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
