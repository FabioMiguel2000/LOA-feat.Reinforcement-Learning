
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
import sys



FPS = 60
EPISODES_NUM = 100

TIMESTEPS = 150000          # Change this value training time steps for different results, we recommend :
                            #       about ~50 000 for 4x4 Board
                            #       about ~150 000 for 5x5 Board
                            #       about ~500 000 for 6x6 Board

models_dir = f"models/"
log_dir = f"logs/"


def main():
    status, boardSize = parse_args(sys.argv)
    if not(status):
        print("\nUsage: main.py [--board=BOARD_SIZE]\n\n\n\t[--board=BOARD_SIZE] options:\n\t\t--board=4 : For 4x4 Board Size\n\t\t--board=5 : For 5x5 Board Size\n\t\t--board=6 : For 6x6 Board Size\n\n\t\tdefault= --board=5\n")
        return
    
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    train_model("PPO", boardSize)   
    train_model("A2C", boardSize)    
    train_model("TRPO", boardSize)

    run_model("PPO", boardSize)   
    run_model("A2C", boardSize)    
    run_model("TRPO", boardSize)

    return 

# Receives the arguments passed from the command line and sets the game mode
def parse_args(args):
    board_size = 5
    if len(args) == 1:
        return True, board_size
    elif len(args) != 2:
        return False
    
    if args[1] == '--board=4':
        board_size = 4
    elif args[1] == '--board=5':
        board_size = 5
    elif args[1] == '--board=6':
        board_size = 6
    else:
        return False, board_size

    return True, board_size


def print_move(action):
    pieceN = (action // 4) + 1
    moveDir = action % 4
    if moveDir == 0:
        print(f"ACTION: {action} Piece " +str(pieceN)+" UP")
    elif moveDir == 1:
        print(f"ACTION: {action} Piece " +str(pieceN)+" RIGHT")
    elif moveDir == 2:
        print(f"ACTION: {action} Piece " +str(pieceN)+" DOWN")
    elif moveDir == 3:
        print(f"ACTION: {action} Piece " +str(pieceN)+" LEFT")
    else:
        print("WRONG DIRECTION")

def print_status(action, board, reward):
    print("-------------------------")
    print(f"OBSERVATION:\n{board}")
    print_move(action)
    print(f"REWARD: {reward}")
    print("-------------------------")



def train_model(MODEL, boardSize=5):
    env = LoaEnv(boardSize = boardSize)
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


def run_model(MODEL, boardSize = 5):
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    env = LoaEnv(WINDOW, boardSize)
    
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

        if(not info.get('invalid_move')):
            time.sleep(0.75) 
            env.render()
            print_status(action, env.game.board.npBoard, reward)

        total_reward += reward 
        counter_moves +=1
        if info.get('max_moves_reached'):
            print("\033[91m")
            break

        if(done):
            print("\033[92m")
            time.sleep(2) 
            env.close()

    print(f"MODEL {MODEL}:")
    print(f"\tTOTAL REWARD: {total_reward}")
    print(f"\tMOVES MADES: {counter_moves}\033[0m\n")
    pygame.quit()

def test(MODEL, boardSize=5):
    clock = pygame.time.Clock()     # Object to help track timeƒ
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    env = LoaEnv(WINDOW, boardSize)
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

main()



