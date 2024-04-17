from enum import Enum

import numpy as np


    
## This a discrete Deterministic Decision Diagram, with a finite number of states and actions
class DiscreteDeterministicDecisionDiagram:
    ## initalise a random DDDD with
    ## n_states: the number of states
    ## n_actions: the number of actions
    ## Optional arguments:
    ## P: the state-action-state transition map
    ## R: The state-action reward matrix so that R[s,a] is the reward for taking action a in state s.
    def __init__(self, n_states, n_actions, P = None, R = None):
        self.n_states = n_states # the number of states of the MDP
        self.n_actions = n_actions # the number of actions of the MDP
        if (P is None):
            self.P = np.zeros([n_states, n_actions], dtype=int) # the probabiltiy of going to s' from (s,a)
            for s in range(self.n_states):
                for a in range(self.n_actions):
                    self.P[s,a] = np.random.choice(self.n_states)
        else:
            self.P = P
        if (R is None):
            self.R = np.zeros([n_states, n_actions]) # the expected reward for each action and state
            # generate uniformly random transitions and 0.1 bernoulli rewards
            for s in range(self.n_states):
                for a in range(self.n_actions):
                    self.R[s,a] = np.round(np.random.uniform(), decimals=1)
        else:
            self.R = R
        self.reset()
                
    # get the probability of next state j given current state s, action a, i.e. P(j|s,a)
    def get_next_state(self, state, action) -> int:
        return self.P[state, action]

    # Get the reward for the current state action.
    # It can also be interpreted as the expected reward for the state and action.
    def get_reward(self, state, action):
        return self.R[state, action]

    ## Help
    def reset(self):
        self.state = 0
        
    def step(self, action):
        done = False
        if (self.reward_distribution == self.DETERMINISTIC):
            reward = self.R[self.state, action]
        elif (self.reward_distribution == self.BERNOULLI):
            reward = np.random.binomial(1, self.R[self.state, action])
        P = get_transition_probabilities(self.state, action)
        self.state = np.random.choice(self.n_states, P)
        return self.state, reward, done, {}


        
        
        
        
