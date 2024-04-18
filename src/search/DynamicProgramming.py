import numpy as np

## Implements dynamic programming for deterministic environments
## $V_{n+1}(s) = \max_a [r(s, a) + V_{n}(\tau(s,a))]$
## in order to solve the problem of maximising
## $E^\pi_\mu(\sum_{t=1}^T \gamma^{t-1} r_t}$
## We can think of $\gamma$ as an effective horizon of $1 / (1 - \gamma)$.
## The nice thing about $\gamma < 1$ is that
## (a) You don't need to care about the time-step
## (b) You don't need to care about infinities, as the total reward is bounded $1 / ( 1-\gamma)$
def dynamic_programming(model, gamma, n_iterations, V = None):
    policy = np.zeros(model.n_states, dtype=int)
    if V is None:
        V = np.zeros(model.n_states)
    Q = np.zeros([model.n_states, model.n_actions])

                        
    for n in range(n_iterations):
        V_old = V.copy()
        for s in range(model.n_states):
            for a in range(model.n_actions):
                s2 = model.get_next_state(s,a)
                Q[s, a] = model.get_reward(s, a) + gamma * V_old[s2]
            V[s] = max(Q[s,:])
            policy[s] = np.argmax(Q[s,:])
    return policy, V, Q


    
