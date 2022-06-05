
from pickle import FALSE
from game.constants import *
from envs.loa_env import LoaEnv
from stable_baselines3 import A2C, PPO, HerReplayBuffer, DQN
from sb3_contrib import TRPO
from stable_baselines3.common.env_checker import check_env
import matplotlib.pyplot as plt

import pygame
import numpy as np
import gym
import time
import os



WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
EPISODES_NUM = 100

TIMESTEPS = 120000

models_dir = f"models/"
log_dir = f"logs/"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def test(MODEL):
    clock = pygame.time.Clock()     # Object to help track timeƒ
    env = LoaEnv(WINDOW)
    STOP = False            # Game Loop Flag
         
    if(MODEL == "PPO"):
        model = PPO.load(f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL", env=env)
    elif MODEL == "A2C":
        model = A2C.load(f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL", env=env)
    elif MODEL == "TRPO":
        model = TRPO.load(f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL", env=env)
    all_episode_rewards = []
    all_episode_length = []
    for episode in range (1, EPISODES_NUM + 1):
        observation = env.reset()
        env.render()
        print(env.game.board.npBoard)
        episode_rewards = []
        done = False
        
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

            
            if(done):
                env.close()
                print("Episode = ", episode, "has ended!\n")
                print("Moves made = ", counter_moves, "has ended!\n")

        all_episode_length.append(counter_moves)
        all_episode_rewards.append(sum(episode_rewards))
        if(STOP):
            break

    mean_episode_reward = np.mean(all_episode_rewards)
    print("Mean moves made per episode:", np.mean(all_episode_length))
    print("Mean reward:", mean_episode_reward, "Num episodes:", EPISODES_NUM)
    pygame.quit()
    x = range(EPISODES_NUM)
    plt.plot(x, all_episode_rewards)
    plt.xlabel('Episodes')
    plt.ylabel('Rewards')
    plt.title('Mean episodic training reward')
    plt.savefig('books_read1.png')

    plt.clf()
    plt.plot(x, all_episode_length)
    plt.xlabel('Episodes')
    plt.ylabel('Number of Moves')
    plt.title('Mean episode length')
    plt.savefig('books_read2.png')



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
    
    model.learn(total_timesteps=TIMESTEPS, tb_log_name=MODEL)
    filename = f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL"
    model.save(filename)
    return filename


def run_model(MODEL):
    env = LoaEnv(WINDOW)
    
    if(MODEL == "PPO"):
        model = PPO.load(f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL", env=env)
    elif MODEL == "A2C":
        model = A2C.load(f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL", env=env)
    elif MODEL == "TRPO":
        model = TRPO.load(f"{models_dir}/{MODEL}_{TIMESTEPS}_STEPS_MODEL", env=env)
    clock = pygame.time.Clock()     # Object to help track timeƒ
    counter_moves = 0
    total_reward = 0
    observation = env.reset()
    

    env.render()
    done = False
    while not done:

        clock.tick(FPS)    
        # ----------- GUI stuff -------------
         
        for event in pygame.event.get():                
            if event.type == pygame.QUIT:  
                STOP = True
                done = True    
                break
            
        # -----------------------------------
        # action = env.action_space.sample()   # Random Action
        action, _ = model.predict(observation, deterministic=True) # most likely will make the same move for every episode if there is one to solve the game
        observation, reward, done, info = env.step(action)

        if(reward != 0):
            time.sleep(1) 
            total_reward += reward 
            counter_moves +=1
            env.render()
            print_status(action, env.game.board.npBoard, reward)
        
        if(done):
            time.sleep(5) 
            env.close()
    print(f"Total reward = {total_reward}\n")
    print("Moves made = ", counter_moves, "has ended!\n")
    pygame.quit()




# training the model
train_model("PPO")   
train_model("A2C")    
train_model("TRPO")
#---------------------


# test("TRPO")
model = "A2C"   # Either "PPO", "A2C", "TRPO"
run_model(model)



