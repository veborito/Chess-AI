# REFERENCES USED FOR INSPIRATION: 
# https://www.chessprogramming.org/Evaluation, and more generaly the whole website
# Sebastian Lague's video "Coding Adventure: Chess" (https://www.youtube.com/watch?v=U4ogK0MIzqk)

import math
import chess
import numpy as np

board = chess.Board("r1bqkbnr/pp1p1ppp/8/2p1n3/3NPB2/8/PPP2PPP/RN1QKB1R w KQkq c6 0 6")

# Matrices à additionner en fonction de la position pour les différentes pièces
pawn_positional_scores = np.array([
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 0,  0,  0,  0,  0,  0,  0,  0]
])

knight_positional_scores = np.array([
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
])

bishop_positional_scores = np.array([
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
])

rook_positional_scores = np.array([
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [ 0,  0,  0,  5,  5,  0,  0,  0]
])

queen_positional_scores = np.array([
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [  0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
])

king_middlegame_positional_scores = np.array([
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20, 0 ,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]
])

king_endgame_positional_scores = np.array([
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
])


def get_piece_positional_score(piece, square):
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
        if board.pieces(chess.QUEEN, True) is False and board.pieces(chess.QUEEN, False) is False: 
            # S'il n'y a plus de dame (ni blanche ni noire) on considère que c'est le endgame
            return king_endgame_positional_scores[rank][file]
        return king_middlegame_positional_scores[rank][file]
    else:
        return 1.0

def evaluate_mobility(board):
    legal_moves = len(list(board.legal_moves))
    mobility_score = (legal_moves - 10) * 2
    return mobility_score   # we tried other more complex evaluations of the mobility (for example piece by piece), 
                            # but it was too costly in computing time

def evaluate_board(board):
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }
    # for the values, we followed the advice given on this website: https://www.chessprogramming.org/Simplified_Evaluation_Function
    
    white_value = 0
    black_value = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            positional_score = get_piece_positional_score(piece, square)
            mobility_score = evaluate_mobility(board)
            
            if piece.color == chess.WHITE:
                white_value += value + positional_score + mobility_score
            else:
                black_value += value + positional_score + mobility_score

    perspective = 1 if board.turn == chess.WHITE else -1
    return (perspective * (white_value - black_value)) / 100


print("eval:", evaluate_board(board))


# Prompt GPT pour modifier les matrices:
""" pawn_multipliers = np.array([
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 1.0],
    [1.0, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 1.0],
    [1.0, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
])

knight_multipliers = np.array([
    [0.75, 0.80, 0.85, 0.85, 0.85, 0.85, 0.80, 0.75],
    [0.80, 0.85, 0.90, 0.90, 0.90, 0.90, 0.85, 0.80],
    [0.85, 0.90, 1.00, 1.00, 1.00, 1.00, 0.90, 0.85],
    [0.85, 0.90, 1.00, 1.25, 1.25, 1.00, 0.90, 0.85],
    [0.85, 0.90, 1.00, 1.25, 1.25, 1.00, 0.90, 0.85],
    [0.85, 0.90, 1.00, 1.00, 1.00, 1.00, 0.90, 0.85],
    [0.80, 0.85, 0.90, 0.90, 0.90, 0.90, 0.85, 0.80],
    [0.75, 0.80, 0.85, 0.85, 0.85, 0.85, 0.80, 0.75]
])

bishop_multipliers = np.array([
    [0.75, 0.80, 0.85, 0.85, 0.85, 0.85, 0.80, 0.75],
    [0.80, 0.85, 0.90, 0.90, 0.90, 0.90, 0.85, 0.80],
    [0.85, 0.90, 1.00, 1.00, 1.00, 1.00, 0.90, 0.85],
    [0.85, 0.90, 1.00, 1.25, 1.25, 1.00, 0.90, 0.85],
    [0.85, 0.90, 1.00, 1.25, 1.25, 1.00, 0.90, 0.85],
    [0.85, 0.90, 1.00, 1.00, 1.00, 1.00, 0.90, 0.85],
    [0.80, 0.85, 0.90, 0.90, 0.90, 0.90, 0.85, 0.80],
    [0.75, 0.80, 0.85, 0.85, 0.85, 0.85, 0.80, 0.75]
])

rook_multipliers = np.array([
    [0.75, 0.80, 0.85, 0.85, 0.85, 0.85, 0.80, 0.75],
    [0.80, 0.85, 0.90, 0.90, 0.90, 0.90, 0.85, 0.80],
    [0.85, 0.90, 1.00, 1.00, 1.00, 1.00, 0.90, 0.85],
    [0.85, 0.90, 1.00, 1.25, 1.25, 1.00, 0.90, 0.85],
    [0.85, 0.90, 1.00, 1.25, 1.25, 1.00, 0.90, 0.85],
    [0.85, 0.90, 1.00, 1.00, 1.00, 1.00, 0.90, 0.85],
    [0.80, 0.85, 0.90, 0.90, 0.90, 0.90, 0.85, 0.80],
    [0.75, 0.80, 0.85, 0.85, 0.85, 0.85, 0.80, 0.75]
])

queen_multipliers = np.array([
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 1.0],
    [1.0, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 1.0],
    [1.0, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
])

king_multipliers = np.array([
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 1.0],
    [1.0, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 1.0],
    [1.0, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
])


Voici les matrices actuelles. Je veux que tu les modifie de la manière suivante:

Pions: il faut décourager les pions à rester sur les cases de la deuxième rangée devant le roi (0.75) car bloque la sortie des pièces et ne prend pas le controle du centre. Faire varier très légèrement en se rapprochant dans la promotion (un pion sur l'avant dernière rangée devrait être multiplié par 1.25 au moins).

Cavaliers, pas besoin de modifier

Fous: Décourager les bordures sauf les deux coins de notre côté, qui sont ok. Globalement plutôt encorager les cases centrales.

TOurs: Décourager de rester sur les deux colonnes latérales, encourager l'entrée sur la 7e rangée  et ne pas trop encourager les cases centrales

Dame: décourager les quatres cases des coins et plutôt encorager le centre, sans que cela ne soit trop marqué

Roi: encourager à se diriger dans les coins de son côté de l'échiquier, et décourager le fait de s'aventurer trop loin en avant. """
