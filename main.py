import chess
import search
import math
import time

board = chess.Board("r2r2k1/4qpp1/1pn4p/2p1p3/p3P3/2B5/PP3PPP/R2Q1RK1 w - - 1 24")
start_time = time.time()
    # Jouer le coup du bot
print(board)
move = search.search(2, board, -math.inf, math.inf, True, start_time)[1]
print(f"FINAL MOVE : {move}")
board.push(move)
print(board)
print("----------------")

#Jouer le coup de l'utilisateur
move = search.search(4, board, -math.inf, math.inf, False, start_time)[1]
board.push(move)
print(f"FINAL MOVE : {move}")
print(board)
print("----------------")