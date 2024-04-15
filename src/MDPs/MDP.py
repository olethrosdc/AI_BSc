import numpy as np

class RewardDistribution(Enum):
    deterministic = 0
    bernoulli = 1
    gaussian = 2
    
## This a discrete MDP with a finite number of states and actions
class DiscreteMDP:
    ## initalise a random MDP with
    ## n_states: the number of states
    ## n_actions: the number of actions
    ## Optional arguments:
    ## P: the state-action-state transition matrix so that P[s,a,s_next] is the probability of s_next given the current state-action pair (s,a)
    ## R: The state-action reward matrix so that R[s,a] is the reward for taking action a in state s.
    def __init__(self, n_states, n_actions, P = None, R = None):
        self.n_states = n_states # the number of states of the MDP
        self.n_actions = n_actions # the number of actions of the MDP
        self.reward_distribution = deterministic
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
                #print(s,a, ":", self.P[s,a,:])
                assert(abs(np.sum(self.P[s,a,:])-1) <= 1e-3)
                
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
        self.current_state = 0
        
    def step(self, action):
        done = False
        match (self.reward_distribution):
            case deterministic:
                reward = self.R[self.state, action]
            case bernoulli:
                reward = np.random.binomial(1, self.r_dist[self.state])
            ca
        move = action
    ## swap the move with a delta probability
    if (np.random.uniform()<self.delta):
        move = 1 - action
    if (move==0):
      self.state = 0
    else:
      self.state += 1
      if (self.state > self.n_states  - 1):
        self.state = self.n_states - 1
    return self.state, reward, done, {}


        
        
        
        
