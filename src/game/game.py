import pygame
from .board import Board
from .constants import *

incX = [-1, +1, 0, 0, -1, -1, +1, +1]
incY = [0, 0, -1, +1, -1, +1, -1, +1]


class Game:
    def __init__(self, window):
        self.window = window
        self.countMoves = [0,0]
        self.reset()

    # Function to update the game view
    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    # Resets/initializes the game states
    def reset(self):
        self.countMoves = [0,0]
        self.selected = None  # The current selected piece
        self.board = Board()  # Game board object
        self.turn = BLACK  # The current player turn
        self.valid_moves = []  # List of all valid moves


    # Moves the selected piece if it is a valid move
    def move(self, row, col):
        piece = self.board.get_piece(row, col)

        if self.selected and (row, col) in self.valid_moves:  # If it is a valid move
            if piece != 0:  # If it is a capture move
                self.board.remove(piece)

            self.board.move(self.selected, row, col)  # Moves the piece
            self.incrementMoveCount()
            self.change_turn()

        else:
            return False

        return True

    # Marks on the board the valid moves by the piece (Green Dot)
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, GREEN,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    # Changes the player turn
    def change_turn(self):
        self.refresh_state()
        # if self.turn == WHITE:
        #     self.turn = BLACK
        # else:
        #     self.turn = WHITE

    # Refreshes the state
    def refresh_state(self):
        self.selected = None
        self.valid_moves = []


    # returns 1 - Black wins
    # returns 2 - White wins
    # returns -1 - Game continues
    def check_gameover(self):
        pieceCount = self.countFirstGroup(self.turn)
        if self.turn == BLACK:
            if pieceCount == self.board.black_left:
                return BLACK_WINS

            else:
                pieceCount = self.countFirstGroup(WHITE)
                if pieceCount == self.board.white_left:
                    return WHITE_WINS

        else:  # White
            if pieceCount == self.board.white_left:
                return WHITE_WINS
            else:
                pieceCount = self.countFirstGroup(BLACK)
                if pieceCount == self.board.black_left:
                    return BLACK_WINS
        return GAME_CONTINUE

    # Finds the size of the first connected pieces of the provided color 
    def countFirstGroup(self, colorPiece):
        self.counter = 0
        self.visited = []

        for row in range(ROWS):
            self.visited.append([])
            for col in range(COLS):
                self.visited[row].append(False)

        for row in range(ROWS):
            for col in range(COLS):
                tempiece = self.board.get_piece(row, col)
                if tempiece != 0 and tempiece.color == colorPiece and not self.visited[row][col]:
                    self.counter = 0
                    self.dfs(row, col, colorPiece)
                    return self.counter
        return self.counter

    # Using DFS to search same color adjacent pieces on the board
    def dfs(self, row, col, colorPiece):
        if not (0 <= col < COLS and 0 <= row < ROWS) or self.visited[row][col]: return

        tempiece = self.board.get_piece(row, col)
        if tempiece == 0 or tempiece.color != colorPiece: return

        self.visited[row][col] = True
        self.counter += 1
        for i in range(8):
            self.dfs(row + incX[i], col + incY[i], colorPiece)

    # Getter function for board
    def get_board(self):
        return self.board
    
    # Update the moves made by the pieces, for final result output
    def incrementMoveCount(self):
        if self.turn == BLACK:
            self.countMoves = [self.countMoves[0] + 1, self.countMoves[1]]
        else:
            self.countMoves = [self.countMoves[0], self.countMoves[1] + 1]
