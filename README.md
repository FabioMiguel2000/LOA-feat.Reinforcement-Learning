# Lines of Actions Using RL

This project was developed during the Artificial Intelligence Course, at FEUP. A simplified version of the game Lines of Actions is solved using reinforcement learning. 

## Installation and prerequisite

1. Install Python3, see [official website](https://www.python.org/downloads/)
1. It is recommended to run in a `conda environment`, our advice is to use [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
1. After installing Python3, run the following command to install the necessary libraries: 
```shell
pip install -r requirements.txt
```

1. [OPTIONAL] It may appear an error when installing/importing `tensorBoard`, complaining about the `protobuf` version, if so run the following command to fix the issue:

```shell
pip install protobuf~=3.19.0
```

## How to run

Using the Command Line, for Windows users, inside the `/src` directory:

```shell
python main.py [--board=BOARD_SIZE]
```

Using the Command Line, for Linux or MacOS users, inside the `/src` directory:

```shell
python3 main.py [--board=BOARD_SIZE]
```

Options:
```

        [--board=BOARD_SIZE] options:
                --board=4 : For 4x4 Board Size
                --board=5 : For 5x5 Board Size
                --board=6 : For 6x6 Board Size

                default= --board=5

        
        For Example: 

            python3 main.py
                # or
            python3 main.py --board=4   
                                       

```


## Guide

- After installing the prerequisites, running the command shown above:
    - The following 3 RL Models will be trained using a default TIMESTEP=15000 (can be modified in the `main.py` by changing the `TIMESTEPS` variable):
        1. Proximal Policy Optimization (PPO)
        1. Advantage Actor Critic (A2C)
        1. Trust Region Policy Optimization (TRPO)
    - Immediately after the training, these Models will be executed by an agent in order, an UI window will pop up showing the moves chosen
    - The terminal will also output the detail of the actions, rewards and observations of the system
- To view graphical elements (graphs, plots) of the trained model, run the command:

```shell
tensorboard --logdir=logs 
```

- Open a browser, and head to `http://localhost:6006` (the port number may vary, see detail on the terminal)



## Group Members

[Fabio Huang](https://github.com/FabioMiguel2000)

[Ivo Ribeiro](https://github.com/RapaTachos)

[Leonor Beirão](https://github.com/leo-nor)