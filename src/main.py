
from pickle import FALSE
from game.constants import *
from envs.loa_env import LoaEnv
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.env_checker import check_env

import pygame
import numpy as np
import gym
import time
import os



WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
EPISODES_NUM = 100
ACTION_SPACE = (BOARD_SIZE -2) * 2 * 4
TIMESTEPS = 10000

models_dir = f"models/"
log_dir = f"logs/PPO-{int(time.time())}"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)


def main(MODEL):
    clock = pygame.time.Clock()     # Object to help track timeƒ
    env = LoaEnv(WINDOW)
    STOP = False            # Game Loop Flag
         
    if(MODEL == "PPO"):
        model = PPO.load(f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL", env=env)
    elif MODEL == "A2C":
        model = A2C.load(f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL", env=env)
    
    all_episode_rewards = []
    for episode in range (1, EPISODES_NUM + 1):
        observation = env.reset()
        env.render()
        print(env.game.board.npBoard)
        episode_rewards = []
        done = False
        # time.sleep(1)
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
            action, _ = model.predict(observation, deterministic=True)
            observation, reward, done, info = env.step(action)
            episode_rewards.append(reward)

            if(reward != 0):
                env.render()
                print_status(action, env.game.board.npBoard, reward)
                # time.sleep(1)
            
            if(done):
                env.close()
                print("Episode = ", episode, "has ended!\n")
        
        all_episode_rewards.append(sum(episode_rewards))
        if(STOP):
            break

    mean_episode_reward = np.mean(all_episode_rewards)
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
        model = PPO("MlpPolicy", env, verbose=1)
    elif MODEL == "A2C":
        model = A2C("MlpPolicy", env, verbose=1)
    
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps= False, tb_log_name=model)
    filename = f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL"
    model.save(filename)
    return filename

model = "PPO"
# train_model(model)    #to train a model
main(model)



