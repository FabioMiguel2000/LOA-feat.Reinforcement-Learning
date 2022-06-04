import gym
from gym import spaces
import numpy as np


from game.game import Game

class LoaEnv(gym.Env):

    def __init__(self, window):
        # for board 4x4
        self.action_space = spaces.Discrete(4*4) #4 directions (UP, DOWN, LEFT, RIGHT) 4 pieces
        self.observation_space = spaces.Box(low=0.0, high=5.0, shape=(16, ), dtype=np.float64)


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
        
        reward = -1
        return np.ravel(self.game.board.npBoard), reward, False, info

    def reset(self):
        self.done = -1 # -1 = game continues, 1 game is over
        self.game.reset()
        return np.ravel(self.game.board.npBoard)

    def render(self):
        self.game.update()
