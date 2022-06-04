
from pickle import FALSE
from game.constants import *
from envs.loa_env import LoaEnv
from stable_baselines3 import A2C
from stable_baselines3.common.env_checker import check_env

import pygame
import numpy as np
import gym
import time

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
EPISODES_NUM = 1000
ACTION_SPACE = (BOARD_SIZE -2) * 2 * 4

def main():
    
    clock = pygame.time.Clock()     # Object to help track time
    env = LoaEnv(WINDOW)
    STOP = False            # Game Loop Flag
         
    model = A2C("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100)

    all_episode_rewards = []
    for episode in range (1, EPISODES_NUM + 1):
        env.reset()
        episode_rewards = []
        done = False
        while not done:

            # ----------- GUI stuff -------------
            clock.tick(FPS)             
            for event in pygame.event.get():                
                if event.type == pygame.QUIT:  
                    STOP = True
                    done = True    
                    break
                
            env.render()
            print(env.game.board.npBoard)
            
            # -----------------------------------
            

            # action = np.random.randint(ACTION_SPACE)    # Random Action
            random_action = env.action_space.sample()
            # print(action)
            observation, reward, done, info = env.step(random_action)
            # if(reward != 0):
            #     time.sleep(1)
            episode_rewards.append(reward)
            print(reward)
            

            if(done):
                env.render()
                print(env.game.board.npBoard)
                env.close()
                print("Episode = ", episode, "has ended!\n")
        
        all_episode_rewards.append(sum(episode_rewards))
        if(STOP):
            break

    mean_episode_reward = np.mean(all_episode_rewards)
    print("Mean reward:", mean_episode_reward, "Num episodes:", EPISODES_NUM)
    pygame.quit()



main()

# check_env
# env = LoaEnv(WINDOW)
# check_env(env)


