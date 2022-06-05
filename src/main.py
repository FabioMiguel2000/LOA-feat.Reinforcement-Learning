
from pickle import FALSE
from game.constants import *
from envs.loa_env import LoaEnv
from stable_baselines3 import A2C, PPO, HerReplayBuffer, DQN
from sb3_contrib import TRPO
from stable_baselines3.common.env_checker import check_env

import pygame
import numpy as np
import gym
import time
import os



WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
EPISODES_NUM = 100

TIMESTEPS = 100000

models_dir = f"models/"
log_dir = f"logs/"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def main(MODEL):
    clock = pygame.time.Clock()     # Object to help track timeƒ
    env = LoaEnv(WINDOW)
    STOP = False            # Game Loop Flag
         
    if(MODEL == "PPO"):
        model = PPO.load(f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL", env=env)
    elif MODEL == "A2C":
        model = A2C.load(f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL", env=env)
    elif MODEL == "TRPO":
        model = TRPO.load(f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL", env=env)
    total_moves = 0
    all_episode_rewards = []
    for episode in range (1, EPISODES_NUM + 1):
        observation = env.reset()
        env.render()
        print(env.game.board.npBoard)
        episode_rewards = []
        done = False
        # time.sleep(1)
        
        counter_moves = 0
        while not done:

            # ----------- GUI stuff -------------
            clock.tick(FPS)             
            for event in pygame.event.get():                
                if event.type == pygame.QUIT:  
                    STOP = True
                    done = True    
                    break
                
            # -----------------------------------
            
            # action = env.action_space.sample()   # Random Action
            action, _ = model.predict(observation, deterministic=True) # most likely will make the same move for every episode if there is one to solve the game
            # action, _ = model.predict(observation)
            observation, reward, done, info = env.step(action)
            episode_rewards.append(reward)

            if(reward != 0):
                counter_moves +=1
                env.render()
                print_status(action, env.game.board.npBoard, reward)
                # time.sleep(1) 
            
            if(done):
                env.close()
                print("Episode = ", episode, "has ended!\n")
                print("Moves made = ", counter_moves, "has ended!\n")

        total_moves += counter_moves
        all_episode_rewards.append(sum(episode_rewards))
        if(STOP):
            break

    mean_episode_reward = np.mean(all_episode_rewards)
    print("Mean moves made per episode:", total_moves/EPISODES_NUM)
    print("Mean reward:", mean_episode_reward, "Num episodes:", EPISODES_NUM)
    pygame.quit()

def print_move(action):
    pieceN = (action // 4) + 1
    moveDir = action % 4
    if moveDir == 0:
        print("Piece " +str(pieceN)+" moved UP")
    elif moveDir == 1:
        print("Piece " +str(pieceN)+" moved RIGHT")
    elif moveDir == 2:
        print("Piece " +str(pieceN)+" moved DOWN")
    elif moveDir == 3:
        print("Piece " +str(pieceN)+" moved LEFT")
    else:
        print("WRONG DIRECTION")

def print_status(action, board, reward):
    print(board)
    print_move(action)
    print("Reward = " + str(reward))


def train_model(MODEL):
    env = LoaEnv(WINDOW)
    if(MODEL == "PPO"):
        model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_dir)
    elif MODEL == "A2C":
        model = A2C("MlpPolicy", env, verbose=1, tensorboard_log=log_dir)
    elif MODEL == "TRPO":
        model = TRPO("MlpPolicy", env, verbose=1, tensorboard_log=log_dir)
    
    model.learn(total_timesteps=TIMESTEPS*1.2, tb_log_name=MODEL)
    filename = f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL"
    model.save(filename)
    return filename


# train_model("PPO")    #to train a model
# train_model("A2C")    #to train a model 
# train_model("TRPO")
main("TRPO")



