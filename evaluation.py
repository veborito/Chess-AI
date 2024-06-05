# REFERENCES USED FOR INSPIRATION: 
# https://www.chessprogramming.org/Evaluation, and more generaly the whole website
# Sebastian Lague's video "Coding Adventure: Chess" (https://www.youtube.com/watch?v=U4ogK0MIzqk)

import math
import chess
import numpy as np


piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }
    # for the values, we followed the advice given on this website: https://www.chessprogramming.org/Simplified_Evaluation_Function

import math
import chess
import numpy as np

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Matrices de scores positionnels
pawn_positional_scores = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
])

knight_positional_scores = np.array([
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
])

bishop_positional_scores = np.array([
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
])

rook_positional_scores = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
])

queen_positional_scores = np.array([
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
])

king_middlegame_positional_scores = np.array([
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
])

king_endgame_positional_scores = np.array([
    [-50, -40, -30, -20, -20, -30, -40, -50],
    [-30, -20, -10, 0, 0, -10, -20, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -30, 0, 0, 0, 0, -30, -30],
    [-50, -30, -30, -30, -30, -30, -30, -50]
])

def get_piece_positional_score(piece, square, is_endgame):
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    
    if piece.piece_type == chess.PAWN:
        return pawn_positional_scores[rank][file]
    elif piece.piece_type == chess.KNIGHT:
        return knight_positional_scores[rank][file]
    elif piece.piece_type == chess.BISHOP:
        return bishop_positional_scores[rank][file]
    elif piece.piece_type == chess.ROOK:
        return rook_positional_scores[rank][file]
    elif piece.piece_type == chess.QUEEN:
        return queen_positional_scores[rank][file]
    elif piece.piece_type == chess.KING:
        if is_endgame:
            return king_endgame_positional_scores[rank][file]
        else:
            return king_middlegame_positional_scores[rank][file]
    return 0

def evaluate_board(board):
    white_value = 0
    black_value = 0

    mobility_score = evaluate_mobility(board)

    is_endgame = not board.pieces(chess.QUEEN, chess.WHITE) and not board.pieces(chess.QUEEN, chess.BLACK)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            positional_score = get_piece_positional_score(piece, square, is_endgame)
            
            if piece.color == chess.WHITE:
                white_value += value + positional_score
            else:
                black_value += value + positional_score

    perspective = 1 if board.turn == chess.WHITE else -1
    return perspective * (white_value - black_value + mobility_score) / 100

def evaluate_mobility(board):
    legal_moves = len(list(board.legal_moves))
    mobility_score = (legal_moves - 10) * 2
    return mobility_score   # we tried other more complex evaluations of the mobility (for example piece by piece), 
                            # but it was too costly in computing time


""" board = chess.Board("r2r2k1/4qpp1/1pn4p/2p1p3/p3P3/2B5/PP3PPP/R2Q1RK1 w - - 1 24")
print(evaluate_board(board)) """
