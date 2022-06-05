from cv2 import connectedComponents
import gym
from gym import spaces
import numpy as np
from game.constants import BOARD_SIZE, NUMBER_PIECES


from game.game import Game



class LoaEnv(gym.Env):

    def __init__(self, window):
        # for board 4x4
        self.action_space = spaces.Discrete(NUMBER_PIECES*4) #4 directions (UP, DOWN, LEFT, RIGHT) 4 pieces
        self.observation_space = spaces.Box(low=0.0, high=float(NUMBER_PIECES), shape=(BOARD_SIZE*BOARD_SIZE, ), dtype=np.float64)
        self.max_connected_so_far = 0

        self.render_mode = 'terminal'
        self.max_turns = 200
        self.done = -1 # -1 = game continues, 1 game is over

        self.game = Game(window)


    # action = board
    def step(self, action):
        reward = 0
        pieceN = (action // 4) + 1
        moveDir = action % 4
        info = {}

        resultRow, resultCol = self.game.board.check_if_valid_move(pieceN, moveDir)
        
        if resultRow == -1: #invalid move
            return np.ravel(self.game.board.npBoard), reward, False, info


        self.game.board.move_piece(pieceN, resultRow, resultCol)

        self.done = self.game.check_gameover()
        
        
        if(self.done == 1):
            reward = 20
            return np.ravel(self.game.board.npBoard), reward, True, info
        
        # connected_pieces = self.game.board.maxGroupSize()
        # if(self.max_connected_so_far < connected_pieces):
        #     self.max_connected_so_far = connected_pieces
        #     return np.ravel(self.game.board.npBoard), self.max_connected_so_far*2, False, info
        
        reward = -1
        return np.ravel(self.game.board.npBoard), reward, False, info

    def reset(self):
        self.max_connected_so_far = 0
        self.done = -1 # -1 = game continues, 1 game is over
        self.game.reset()
        return np.ravel(self.game.board.npBoard)

    def render(self):
        self.game.update()
