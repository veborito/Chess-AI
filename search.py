import chess
import math
import evaluation
import time

# Define board for demonstration
board = chess.Board()

def sorting_legal_moves(board, moves):
    move_scores = []

    for move in moves:
        score = 0
        move_piece_type = board.piece_type_at(move.from_square)
        capture_piece_type = board.piece_type_at(move.to_square)

        if capture_piece_type is not None:
            score = 10 * evaluation.piece_values[capture_piece_type] - evaluation.piece_values[move_piece_type]

        if move_piece_type == chess.PAWN:
            if move.promotion == chess.QUEEN:
                score += evaluation.piece_values[chess.QUEEN]
            elif move.promotion == chess.KNIGHT:
                score += evaluation.piece_values[chess.KNIGHT]
            elif move.promotion == chess.ROOK:
                score += evaluation.piece_values[chess.ROOK]
            elif move.promotion == chess.BISHOP:
                score += evaluation.piece_values[chess.BISHOP]
        else:
            if board.is_attacked_by(not board.turn, move.to_square):
                score -= 100
                attackers = board.attackers(not board.turn, move.to_square)
                for attacker in attackers:
                    if board.piece_type_at(attacker) == chess.PAWN:
                        score -= 500

        move_scores.append((score, move))

    sorted_moves = [move for score, move in sorted(move_scores, key=lambda x: x[0], reverse=True)]
    return sorted_moves

def search(depth, position, alpha, beta, maximizing_player, start_time):    
    if depth == 0:
        return evaluation.evaluate_board(position), None
    
    moves = sorting_legal_moves(position, list(position.legal_moves))
    if not moves:
        if position.is_checkmate():
            return -math.inf if maximizing_player else math.inf, None
        return 0, None  # Stalemate
    
    best_move = None
    if maximizing_player:
        max_eval = -math.inf
        for move in moves:
            position.push(move)
            eval, _ = search(depth - 1, position, alpha, beta, False, start_time)
            position.pop()
            print(eval, max_eval, move, depth)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
            if (time.time() - start_time > 10):
                return max_eval, best_move
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in moves:
            position.push(move)
            eval, _ = search(depth - 1, position, alpha, beta, True, start_time)
            position.pop()
            print(eval, min_eval, move, depth)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
            if (time.time() - start_time > 10):
                return min_eval, best_move
        return min_eval, best_move

def iterative_deepening(position, max_time):
    best_move = None
    start_time = time.time()
    depth = 1
    
    while True:
        current_time = time.time()
        if current_time - start_time >= max_time:
            break
        eval, best_move = search(depth, position, -math.inf, math.inf, position.turn == chess.WHITE, start_time)    # il y a qqch à faire ici, pcq on réutilise pas bien l'evaluation de l'itération précédente
        print(f'Depth: {depth}, Eval: {eval}, Best Move: {best_move}')
        depth += 1

    return best_move, eval

def play(board, max_time):
    search_result = iterative_deepening(board, max_time)
    return search_result


""" board = chess.Board()
max_time_per_move = 4
print(f'Best Move: {search_result[0]}, Eval: {search_result[1]}') """

