
from game.constants import *
from envs.loa_env import LoaEnv
import pygame
import numpy as np
import gym
import time

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
EPISODES_NUM = 10
ACTION_SPACE = (BOARD_SIZE -2) * 2 * 4


def main():
    
    clock = pygame.time.Clock()     # Object to help track time
    env = LoaEnv(WINDOW)
    

    done = False                    # Game Loop Flag
    for episode in range (1, EPISODES_NUM + 1):
        env.reset()
        total_rewards = 0

        done = False
        while not done:

            # ----------- GUI stuff -------------
            clock.tick(FPS)             
            for event in pygame.event.get():                
                if event.type == pygame.QUIT:  
                    episode = EPISODES_NUM
                    done = True    
                    break
                
            env.render()
            print(env.game.board.npBoard)
            
            # -----------------------------------
            

            action = np.random.randint(ACTION_SPACE)    
            print(action)
            board, reward, done = env.step(action)
            if(reward != 0):
                time.sleep(1)
            total_rewards += reward 
            print(reward)
            

            if(done):
                env.render()
                print(env.game.board.npBoard)
                env.close()
                print("Episode = ", episode, "has ended!\n")

    pygame.quit()



main()

