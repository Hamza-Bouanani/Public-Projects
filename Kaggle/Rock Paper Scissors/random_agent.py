from random import randint
from kaggle_environments import evaluate, make, utils
def random_agent (observation, configuration):
    return randint(0,2)

def only_rock (observation, configuration):
    return 0

agent = random_agent
opponents = only_rock
env = make('rps')
env.reset()
env.run([agent, opponents])
env.render(mode='ipython', width=500, height=500)

# fight(agent, opponents, n_fights=1)