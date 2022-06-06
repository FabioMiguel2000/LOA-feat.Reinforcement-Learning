import gym
from gym import spaces
import numpy as np
# from game.constants import BOARD_SIZE, NUMBER_PIECES


from game.game import Game



class LoaEnv(gym.Env):

    def __init__(self, window=None, boardSize = 5):
        # for board 4x4
        
        self.boardSize = boardSize
        self.number_pieces =  2*(self.boardSize-2)
        self.action_space = spaces.Discrete(self.number_pieces*4) #4 directions (UP, DOWN, LEFT, RIGHT) 4 pieces
        self.observation_space = spaces.Box(low=0.0, high=float(self.number_pieces), shape=(self.boardSize*self.boardSize, ), dtype=np.float64)
        # self.max_connected_so_far = int(NUMBER_PIECES/2)
        self.max_turns = 500             #TODO : change
        self.render_mode = 'terminal' 
        if(window != None):
            self.render_mode = 'graphical_interface' 
        self.max_turns = 200
        self.done = -1 # -1 = game continues, 1 game is over

        self.game = Game(window, boardSize=self.boardSize)


    # action = board
    def step(self, action):
        reward = 0
        pieceN = (action // 4) + 1
        moveDir = action % 4
        info = {'max_moves_reached': False, 'invalid_move': False}

        resultRow, resultCol = self.game.board.check_if_valid_move(pieceN, moveDir)

        self.max_turns -= 1

        if resultRow == -1: #invalid move
            reward = -1
            if(self.max_turns == 0): # More than maximum moves
                info.update({'max_moves_reached': True})
            info.update({'invalid_move': True})
            return np.ravel(self.game.board.npBoard), reward, False, info


        self.game.board.move_piece(pieceN, resultRow, resultCol)

        self.done = self.game.check_gameover()
        
        if(self.done == 1): # Completed the game
            reward = 20
            return np.ravel(self.game.board.npBoard), reward, True, info
        
        # connected_pieces = self.game.board.maxGroupSize()
        # if(self.max_connected_so_far < connected_pieces):
        #     self.max_connected_so_far = connected_pieces
        #     reward = 1
        #     return np.ravel(self.game.board.npBoard), 1, False, info
        
        reward = -1

        return np.ravel(self.game.board.npBoard), reward, False, info

    def reset(self):
        # self.max_connected_so_far = int(NUMBER_PIECES/2)
        self.done = -1 
        self.max_turns = 500
        self.game.reset()
        return np.ravel(self.game.board.npBoard)

    def render(self):
        if(self.render_mode == 'graphical_interface'):
            self.game.update()
