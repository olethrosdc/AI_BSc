from MDP import DiscreteMDP
from enum import Enum
import numpy as np

## This defines the Chain environment
class GridWorld(DiscreteMDP):


    def get_state(self, x, y):
        return x + y*self.width
    
    def __init__(self, width, height, randomness):
        self.state = 0
        self.width = width
        self.height = height
        n_states = width * height + 1
        n_actions = 4
        self.maze = np.zeros([width, height])
        self.EMPTY = 0
        self.WALL = 1
        self.HOLE = 2
        self.GOAL = 3
        self.UP = 0
        self.DOWN = 1
        self.LEFT = 2
        self.RIGHT = 3
        
        for x in range(width):
            for y in range(height):
                if (np.random.uniform()<.2):
                    self.maze[x, y] = self.WALL


        hole_x = hole_y = 0
        while (hole_x == 0 and hole_y == 0):
            hole_x = np.random.choice(width)
            hole_y = np.random.choice(width)
        self.maze[hole_x, hole_y] = self.HOLE
        
        goal_x = goal_y = 0
        while (goal_x == 0 and goal_y == 0):
            goal_x = np.random.choice(width)
            goal_y = np.random.choice(width)
        self.maze[goal_x, goal_y] = self.GOAL


        P = np.zeros([n_states, n_actions, n_states])
        R = -np.ones([n_states, n_actions]) # initialise all rewards to -1

        for x in range(width):
            for y in range(height):
                s = self.get_state(x, y)

                xr = min(max(0, x+1), self.width - 1)
                yr = min(max(0, y), self.height - 1)
                if (self.maze[xr, yr] == self.WALL):
                    xr = x
                    yr = y
                
                xl = min(max(0, x-1), self.width    - 1)
                yl = min(max(0, y), self.height - 1)
                if (self.maze[xl, yl] == self.WALL):
                    xl = x
                    yl = y
                    
                xu = min(max(0, x), self.width - 1)
                yu = min(max(0, y-1), self.height - 1)
                if (self.maze[xu, yu] == self.WALL):
                    xu = x
                    yu = y
                    
                xd = min(max(0, x), self.width - 1)
                yd = min(max(0, y+1), self.height - 1)
                if (self.maze[xd, yd] == self.WALL):
                    xd = x
                    yd = y                

                    
                sr = self.get_state(xr, yr)
                sl = self.get_state(xl, yl)
                su = self.get_state(xu, yu)
                sd = self.get_state(xd, yd)

                P[s, self.RIGHT, sr] = 1 - randomness
                P[s, self.LEFT, sl] = 1 - randomness
                P[s, self.UP, su] = 1 - randomness
                P[s, self.DOWN, sd] = 1 - randomness

                P[s, self.RIGHT, s] += randomness/4
                P[s, self.RIGHT, sl] += randomness/4
                P[s, self.RIGHT, su] += randomness/4
                P[s, self.RIGHT, sd] += randomness/4

                P[s, self.LEFT, s] += randomness/4
                P[s, self.LEFT, sr] += randomness/4
                P[s, self.LEFT, su] += randomness/4
                P[s, self.LEFT, sd] += randomness/4

                P[s, self.UP, s] += randomness/4
                P[s, self.UP, sr] += randomness/4
                P[s, self.UP, sl] += randomness/4
                P[s, self.UP, sd] += randomness/4

                P[s, self.DOWN, s] += randomness/4
                P[s, self.DOWN, sr] += randomness/4
                P[s, self.DOWN, sl] += randomness/4
                P[s, self.DOWN, su] += randomness/4


        ## The terminal state
        for a in range(n_actions):
            P[n_states - 1, a, :] = 0
            P[n_states - 1, a, n_states - 1] = 1
            R[n_states - 1, a] = 0

            
        # the hole gets you to the terminal state with -100
        s = self.get_state(hole_x, hole_y)
        for a in range(n_actions):
            P[s, a, :] = 0
            P[s, a, n_states - 1] = 1
            R[s,a] = -100
            

        # the goal gets you to the terminal state with + 1
        s = self.get_state(goal_x, goal_y)
        for a in range(n_actions):
            P[s, a, :] = 0
            P[s, a, n_states - 1] = 1
            R[s,a] = 1

        super().__init__(n_states, n_actions, P, R)
        
    def step(self, action):
        assert self.action_space.contains(action)
        done = False
        reward = np.random.binomial(1, self.r_dist[self.state])



    def reset(self):
        self.state = 0
        self.x = 0
        self.y = 0
        return 0

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[x,y]==self.WALL:
                    print("#", end="")
                elif self.maze[x,y]==self.EMPTY:
                    print(".", end="")
                elif self.maze[x,y]==self.HOLE:
                    print("O", end="")
                elif self.maze[x,y]==self.GOAL:
                    print("X", end="")
                else:
                    print("!", end="")
            print("")
            

# test

def main():
    print("Testing")
    height = 4
    width = 4
    environment = GridWorld(width, height, 0)
    environment.render()

    from ValueIteration import value_iteration
    print("Calculating optimal policy")
    policy, V, Q = value_iteration(environment, 100, 1)

    print("Policy, ", policy)
    policy_string="^v<>"
    for y in range(height):
        for x in range(width):
            s = environment.get_state(x,y)
            print(policy_string[policy[s]], end="")
        print("")

    print("Values")
    for y in range(height):
        for x in range(width):
            print(V[environment.get_state(x,y)], end=" ")
        print("")


import sys
if __name__ == '__main__':
    sys.exit(main())
