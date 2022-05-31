import gym
from gym import spaces
import numpy as np


from game.game import Game

class LoaEnv(gym.Env):

    def __init__(self, window):
        # for board 4x4
        self.action_space = spaces.Discrete(8*4) #8 directions 4 pieces
        self.observation_space = gym.spaces.Box(low=np.int8(0), high=np.int8(2), shape=(4, 4), dtype=np.int8)

        self.render_mode = 'terminal'
        self.max_turns = 200
        self.done = -1 # -1 = game continues, 1 game is over

        self.game = Game(window)


    # action = board
    def step(self, action):
        reward = 0
        pieceN = (action // 4) + 1
        moveDir = action % 4

        resultRow, resultCol = self.game.board.check_if_valid_move(pieceN, moveDir)
        
        if resultRow == -1: #invalid move
            return np.copy(self.game.board.npBoard), reward, False


        self.game.board.move_piece(pieceN, resultRow, resultCol)
        self.done = self.game.check_gameover()
        
        if(self.done == 1):
            reward = 20
            return np.copy(self.game.board.npBoard), reward, True
        
        reward = -1
        return np.copy(self.game.board.npBoard), reward, False

    def reset(self):
        self.game.reset()
        pass

    def render(self):
        self.game.update()
