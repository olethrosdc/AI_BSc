from enum import Enum

import numpy as np


    
## This a discrete MDP with a finite number of states and actions
class DiscreteMDP:
    ## initalise a random MDP with
    ## n_states: the number of states
    ## n_actions: the number of actions
    ## Optional arguments:
    ## P: the state-action-state transition matrix so that P[s,a,s_next] is the probability of s_next given the current state-action pair (s,a)
    ## R: The state-action reward matrix so that R[s,a] is the reward for taking action a in state s.
    def __init__(self, n_states, n_actions, P = None, R = None):
        self.DETERMINISTIC = 0
        self.BERNOULLI = 1
        self.GAUSSIAN = 2
        self.n_states = n_states # the number of states of the MDP
        self.n_actions = n_actions # the number of actions of the MDP
        self.reward_distribution = self.DETERMINISTIC
        self.terminal_state = - 1
        if (P is None):
            self.P = np.zeros([n_states, n_actions, n_states]) # the transition probability matrix of the MDP so that P[s,a,s'] is the probabiltiy of going to s' from (s,a)
            for s in range(self.n_states):
                for a in range(self.n_actions):
                    self.P[s,a] = np.random.dirichlet(np.ones(n_states)) # generalisation of Beta to multiple outcome
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
        
        # check transitions
        for s in range(self.n_states):
            for a in range(self.n_actions):
                #print(s,a, ":", self.P[s,a,:], " = ", sum(self.P[s,a,:]))
                assert(abs(np.sum(self.P[s,a,:])-1) <= 1e-3)
                for s2 in range(self.n_states):
                    assert(self.P[s,a,s2] >= 0)
                    assert(self.P[s,a,s2] <= 1)

        self.reset()
        
    # get the probability of next state j given current state s, action a, i.e. P(j|s,a)
    def get_transition_probability(self, state, action, next_state):
        return self.P[state, action, next_state]
    
    # get the vector of probabilities over next states P( . | s,a)
    def get_transition_probabilities(self, state, action):
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
        if self.state == self.terminal_state:
            done = True
        return self.state, reward, done, {}


        
        
        
        
