from random import randint
from kaggle_environments import evaluate, make, utils
from kaggle_environments.envs.rps.utils import get_score
from kaggle_environments.envs.rps.agents import *
from collections import Counter

agent_plays = []
opponent_plays = []
reward = 0




def probability_agent (observation, configuration):
    
   
    global agent_plays, opponent_plays , reward
    reward = observation['reward']
    if observation['step'] > 0:
        opponent_plays.append(observation['lastOpponentAction'])
    if observation['step'] == 0:
        agent_action = randint(0,2)
    else:
        ## décision
        proba_rock = (Counter(opponent_plays)[0] / len(opponent_plays)) *100
        proba_paper = (Counter(opponent_plays)[1] / len(opponent_plays)) *100
        proba_scissors = (Counter(opponent_plays)[2] / len(opponent_plays)) *100
        tresh = randint(0,100)
        if tresh <= proba_rock:
            # then we think he might play rock so we play paper
            agent_action = 1
        elif tresh <= proba_rock + proba_paper:
            # then we think he might play paper then we play sciccors
            agent_action = 2
        else:
            # then we think he might play scissors then we play rock
            agent_action = 0
        
        
    # final
    
    agent_plays.append(agent_action)
    return agent_action