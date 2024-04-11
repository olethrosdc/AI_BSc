import numpy as np
import MDP

## This a discrete MDP with a finite number of states and actions
class simpleMDP(MDP.DiscreteMDP)::
    ## initalise a random MDP with
    ## n_states: the number of states
    ## n_actions: the number of actions
    def __init__(self):
        self.n_states = 2
        self.n_actions = 2
        self.P = np.zeros([n_states, n_actions, n_states]) # the transition probability matrix of the MDP so that P[s,a,s'] is the probabiltiy of going to s' from (s,a)
        self.R = np.zeros([n_states, n_actions]) # the expected reward for each action and state
        ## Fill in
                    

    

        
        
