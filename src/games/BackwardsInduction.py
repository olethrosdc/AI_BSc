import game
import numpy as np

## Define algorithm
## policy[state, time] gives you index of the action played at any state for any time.
## Assume player 1 plays at time 0, 2, ..., player 2 at times 1, 3, 5
## Every player has the same action space
def backwards_induction(game, policy, T):
    V = np.zeros([T, game.n_states])
    Q = np.zeros([T, game.n_states, game.n_actions])
    policy = np.zeros([T, game.n_states])
    ## to fill in
    # First fill in the value at time T:
    for s in range(game.n_states):
        V[T-1, s] = game.get_reward(s)
        for a in range(game.n_actions): 
            Q[T-1, s, a] = game.get_reward(s)
        
    for t in range(T-2, 0, -1):
        if (t % 2)==0:
            sign = 1
        else:
            sign = -1
            
        # V_t = max_a sign * Q_t(s,a)
        # Q_t(s,a) = r_t + sum_j P(j | s,a) V_{t+1}(j)
        for a in range(game.n_actions): 
            Q[t, s, a] = game.get_reward(s)
            for j in range(game.n_states):
                Q[t, s, a] += game.get_transition_probability(s, a, j) * V[t+1, j]
            a_opt = np.argmax(sign * Q[t,s,:])
            policy[t, s] = a_opt
            V[t, s] = Q[t,s,a_opt]
    return policy, V, Q

n_actions = 2
n_states = 2
T = 2
game = game.DiscreteGame(n_states, n_actions)

policy = np.zeros([n_states, T], int) #this plays action 0 all the time
policy, V, Q = backwards_induction(game,  policy, T)


for s in range(game.n_states):
    for a in range(game.n_actions):
        print("S:", s, "A:", a, game.get_transition_probabilities(s,a))


for t in range(T):
    print(policy[:,t])
        
for t in range(T):
    print(V[:,t])

    



    
