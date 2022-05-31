from copy import deepcopy
import pygame
from game.constants import ALPHA_BETA

BLACK = (0,0,0)
WHITE = (255, 255, 255)

nodes = 0

def increment_node():
    global nodes
    nodes +=1


def minimax(board, depth, max_player, game, currentTurn, alpha, beta):

    if depth == 0 or game.check_gameover2(board) != -1:
        return board.evaluate(game.turn), board
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(board, currentTurn, game):
            increment_node()
            evaluation, temp_move = minimax(move, depth-1, False, game, currentTurn, alpha, beta)
            maxEval = max(maxEval, evaluation)
            if ALPHA_BETA:
                alpha = max(alpha, evaluation)
                if beta < alpha:
                    break
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
        
    else: # min_player
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(board, changeTurn(currentTurn), game):
            increment_node()
            evaluation, temp_move = minimax(move, depth-1, True, game, currentTurn, alpha, beta)
            minEval = min(minEval, evaluation)
            if ALPHA_BETA:
                beta = min(beta, evaluation)
                if beta < alpha:
                    break
            if minEval == evaluation:
                best_move = move
                
        return minEval, best_move
        
def simulate_move(piece,move,board,game):
    delPiece = board.get_piece(move[0], move[1])
    if( delPiece != 0 ):
        board.remove(delPiece)
        
    board.move(piece, move[0], move[1])

    return board

def get_all_moves(board, color, game):
    moves = []
    
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        # for move, capturedPiece in valid_moves.items():
        for move in valid_moves:
            # Discomment if would like to see all the possible branches of minimax
            # draw_moves(game, board, piece)    
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game)
            moves.append(new_board)
    
    return moves

def changeTurn(Turn):
    return WHITE if Turn == BLACK else BLACK


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.window)
    pygame.draw.circle(game.window, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves)
    pygame.display.update()
