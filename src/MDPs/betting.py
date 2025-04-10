import numpy as np

T = 5
initial_money = 1
p_win = 0.5 # This is the winning probability (between 0 and 1)

if (initial_money > T):
    n_states = 1 + 2 * T # no more states are possible
else:
    n_states =  1 + initial_money + T 

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


## The backwards induction algorithm
def BackwardsInduction(P, R, T):
    n_states = P.shape[0]
    n_actions = P.shape[2]

    # Initialise V = R for the last time-step.
    V = np.zeros([n_states, T])
    for s in range(n_states):
        V[s, T - 1] = max(R[s, :])

    # Do the recursion
    policy = np.zeros([n_states, T])
    for k in range(T-1):
        t = T - k - 2 # ensures we go from t = T-2, ... to t = 0.
        Q = np.zeros([n_states, n_actions])
        for s in range(n_states):
            for a in range(n_actions):
                # Start with the reward of the current step
                Q[s, a] = R[s, a]
                # Add the expected next-state value
                for s2 in range(n_states):
                    Q[s, a] += V[s2, t+1] * P[s2, s, a]
            # Maximise over actions
            V[s, t] = np.max(Q[s, :])
            policy[s,t] = np.argmax(Q[s, :])
    return V, Q, policy

V, Q, policy = BackwardsInduction(P, R, T)

print("Value function")
for t in range(T):
    print("t = ", t, "V = ", V[:,t])
print("Q function (for t = 0)")
print(Q)
print("Policy over all time steps")
print(policy)
