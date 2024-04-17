import MDP
import mdp_examples
import numpy as np

## Define algorithm
def dynamic_programming(model, n_iterations:
    policy = np.zeros([model.n_states], dtype=int)
    V = np.zeros([model.n_states])

    Q = np.zeros([model.n_states, model.n_actions])
    ## to fill in
    for n in range(n_iterations):
        V_old = V.copy()
        for s in range(model.n_states):
            for a in range(model.n_actions):
                Q[s, a] = model.get_reward(s, a) + V_old[model.get_next_state(s,a)]
            V[s] = max(Q[s,:])
            policy[s] = np.argmax(Q[s,:])
    return policy, V, Q


    
