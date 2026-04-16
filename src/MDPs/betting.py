# A betting example

import numpy as np

def get_betting_MDP(initial_money, p_win, T):

    # Here we have the starting state, plus all reachable states
    if (initial_money > T):
        n_states = 1 + 2 * T # no more states are possible
    else:
        n_states =  1 + initial_money + T # you can at best win T, or lose all your money
    n_actions = 2
    P = np.zeros([n_states, n_states, n_actions])
    R = np.zeros([n_states, n_actions])
    ## The probabilities and rewards
    for s in range(1, n_states-1):
        P[s+1, s, 1] = p_win
        P[s-1, s, 1] = 1 - p_win
        P[0, s, 0] = 1
        R[s, 0] = s # we only get a reward at the end. If you change
                    # this to s - c, where c > 0, then your policies will
                    # be different. Why is that?


    P[0, 0, 0] = 1
    P[0, 0, 1] = 1
    P[0, n_states-1, 0] = 1
    P[n_states -1, n_states-1, 1] = 1 # because T = n_states, we can only reach this at the last step.
    return DiscreteMDP(n_states, n_actions, P, R)




# Construct an MDP
mdp = get_betting_MDP(initial_money=1, p_win=0.5, T=5)
## Run The backwards induction algorithm
V, Q, policy = BackwardsInduction(P, R, T)

print("Value function")
for t in range(T):
    print("t = ", t, "V = ", V[:,t])
print("Q function (for t = 0)")
print(Q)
print("Policy over all time steps")
print(policy)
