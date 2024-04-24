import MDP
import mdp_examples
import numpy as np

## Implements dynamic programming for stochastic environments.
## An optional discount factor can be used.
## $V_{n+1}(s) = \max_a [r(s, a) + \gamma \sum_{s'} P(s' | s, a) V_{n}(s')$
def value_iteration(mdp, n_iterations, gamma = 1, V = None):
    policy = np.zeros([mdp.n_states], dtype=int)
    assert(gamma > 0)
    assert(gamma <= 1)
    if (V is None):
        V = np.zeros([mdp.n_states])
        
    Q = np.zeros([mdp.n_states, mdp.n_actions])
    ## to fill in
    for n in range(n_iterations):
        V_old = V.copy()
        for s in range(mdp.n_states):
            for a in range(mdp.n_actions):
                Q[s, a] = mdp.get_reward(s, a) + gamma * np.dot(mdp.get_transition_probabilities(s,a), V_old)
            V[s] = max(Q[s,:])
            policy[s] = np.argmax(Q[s,:])
    return policy, V, Q

def main() -> int:
    n_actions = 2
    n_states = 2
    n_iterations = 1000
    gamma = 0.9
    mdp = mdp_examples.ChainMDP()
    policy, V, Q = value_iteration(mdp, n_iterations, gamma)


    print (policy)
    print (V)
    print (Q)

import sys
if __name__ == '__main__':
    sys.exit(main())

    
