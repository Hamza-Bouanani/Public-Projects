from random import randint
from kaggle_environments import evaluate, make, utils
from kaggle_environments.envs.rps.utils import get_score
from kaggle_environments.envs.rps.agents import *
from collections import Counter
import pandas as pd
import numpy as np

from xgboost import XGBClassifier

model = XGBClassifier()


agent_plays = []
opponent_plays = []
reward = 0

def gradient_boosting_agent_10_plays (observation, configuration) :
    global agent_plays, opponent_plays , reward
    global model
    nb_plays = 8 # nombre de plays utilisé pour apprendre.
    reward = observation['reward']
    step = observation['step']
    if step > 0 :
        opponent_plays.append(observation['lastOpponentAction'])
    if step <= 22:
        agent_action = randint(0,2)
    elif step <= 25: # pour éviter dans un pattern répititif contre une certaine ia, on prend le temps de comprendre l'ia adverse avant de commencer la notre
        train_agent_last_20_plays = agent_plays[-nb_plays-1:-1]
        train_opponent_last_20_plays = opponent_plays[-nb_plays-1:-1]
        # on train sur les 20 derniers coups de l'agent et de l'opposant et on essaie de prédire le move de l'opposant
        x_train = np.array([train_agent_last_20_plays + train_opponent_last_20_plays])
        y_train = np.array([opponent_plays[-1]]) # on s'entrainer à trouver le dernier play de l'opposant
        
        # fit the model
        model.fit(x_train, y_train)
        # décision
        agent_action = randint(0,2)
        
    else: # ici on entraîne encore le modèle et on l'utilise pour la solution aussi.
        train_agent_last_20_plays = agent_plays[-nb_plays-1:-1]
        train_opponent_last_20_plays = opponent_plays[-nb_plays-1:-1]
        # on train sur les 20 derniers coups de l'agent et de l'opposant et on essaie de prédire le move de l'opposant
        x_train = np.array([train_agent_last_20_plays + train_opponent_last_20_plays])
        y_train = np.array([opponent_plays[-1]]) # on s'entrainer à trouver le dernier play de l'opposant
        
        # fit the model
        model.fit(x_train, y_train)
        
        
        # preparer pour faire une prédiction
        prediction_agent_last_20_plays = agent_plays[-nb_plays:]
        prediction_opponent_last_20_plays = opponent_plays[-nb_plays:]
        
        x_prediction = np.array([prediction_agent_last_20_plays + prediction_opponent_last_20_plays])
        
        y_prediction = model.predict(x_prediction)
        
        #décision
        if y_prediction == 0:
            agent_action = 1
        elif y_prediction == 1:
            agent_action = 2
        else:
            agent_action = 0
    agent_plays.append(agent_action)    
    return agent_action
        