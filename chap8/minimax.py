from chap8.board import Piece, Board, Move


def minimax(board, maximizing, original_player, max_depth=8):
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    if maximizing:
        best_eval = float("-inf")
        for move in board.legal_moves:
            result = minimax(board.move(move), False, original_player, max_depth - 1)
            best_eval = max(best_eval, result)
        return best_eval
    else:
        worst_eval = float("inf")
        for move in board.legal_moves:
            result = minimax(board.move(move), True, original_player, max_depth - 1)
            worst_eval = min(worst_eval, result)
        return worst_eval


def find_best_move(board, max_depth=8):
    best_eval = float("-inf")
    best_move = Move(-1)
    for move in board.legal_moves:
        result = alphabeta(board.move(move), False, board.turn, max_depth)
        if result > best_eval:
            best_eval = result
            best_move = move
    return best_move

def alphabeta(board, maximizing, original_player, max_depth=8, alpha=float('-inf'), beta=float('inf')):
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    if maximizing:
        for move in board.legal_moves:
            result = alphabeta(board.move(move), False, original_player, max_depth-1, alpha, beta)
            alpha = max(result, alpha)
            if beta <= alpha:
                break
        return alpha
    else:
        for move in board.legal_moves:
            result = alphabeta(board.move(move), True, original_player, max_depth-1, alpha, beta)
            beta = min(result, beta)
            if beta <= alpha:
                break
        return beta
