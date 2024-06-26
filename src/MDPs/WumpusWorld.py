from MDP import DiscreteMDP
from enum import Enum
import numpy as np

## This defines the Gridworld environment
class ObsWumpusWorld(DiscreteMDP):
    def get_state(self, x, y, wx, wy):
        return x + y*self.width + wx*self.width*self.height + wy*self.width*self.width*self.height
    
    def __init__(self, width, height, density=0.3, randomness=0.2, r_step=-1, r_goal=1, r_hole=-10, r_wumpus=-10):
        
        self.state = 0
        self.width = width
        self.height = height
        n_states = (width * height)**2 + 1
        n_actions = 4
        self.maze = np.zeros([width, height])
        self.EMPTY = 0
        self.WALL = 1
        self.HOLE = 2
        self.GOAL = 3
        self.WUMPUS = 4
        self.UP = 0
        self.DOWN = 1
        self.LEFT = 2
        self.RIGHT = 3
        
        print("Generating Fully Observable Wumpus World with the following characteristics")
        print(n_states, "states")
        print(r_step, "step reward")
        print(r_hole, "hole reward")
        print(r_goal, "goal reward")
        print(r_wumpus, "wumpus reward")
        print(randomness, "randomness")
        
        for x in range(width):
            for y in range(height):
                if (np.random.uniform()<density):
                    self.maze[x, y] = self.WALL


        hole_x = hole_y = 0
        while (1):
            hole_y = np.random.choice(height)
            hole_x = np.random.choice(width)
            if (self.maze[hole_x, hole_y]==self.EMPTY):
                self.maze[hole_x, hole_y] = self.HOLE
                break
                
        goal_x = goal_y = 0
        while (1):
            goal_y = np.random.choice(height)
            goal_x = np.random.choice(width)
            if (self.maze[goal_x, goal_y]==self.EMPTY):
                self.maze[goal_x, goal_y] = self.GOAL
                break

        while (1):
            self.wumpus_y = np.random.choice(height)
            self.wumpus_x = np.random.choice(width)
            if (self.maze[self.wumpus_x, self.wumpus_y]==self.EMPTY):
                self.maze[self.wumpus_x, self.wumpus_y] = self.WUMPUS
                break

        
        # Here $P[s,a,j] = \Pr(s_{t+1} = j | s_t = s, a_t = a]$
        P = np.zeros([n_states, n_actions, n_states])
        R = r_step + np.zeros([n_states, n_actions]) # initialise all rewards to -1

        for self.wumpus_x in range(width):
            for self.wumpus_y in range(height):
                for x in range(width):
                    for y in range(height):                      
                        self.local_transitions(P, R, x, y, randomness)
                # the hole gets you to the terminal state with -100
                s = self.get_state(hole_x, hole_y, self.wumpus_x, self.wumpus_y)
                for a in range(n_actions):
                    P[s, a, :] = 0
                    P[s, a, n_states - 1] = 1
                    R[s,a] = r_hole
                    
        
                # the goal gets you to the terminal state with + 1
                s = self.get_state(goal_x, goal_y, self.wumpus_x, self.wumpus_y)
                for a in range(n_actions):
                    P[s, a, :] = 0
                    P[s, a, n_states - 1] = 1
                    R[s,a] = r_goal
                    
                # the wumpus gets you to the terminal state with - 1
                s = self.get_state(self.wumpus_x, self.wumpus_y, self.wumpus_x, self.wumpus_y)
                for a in range(n_actions):
                    P[s, a, :] = 0
                    P[s, a, n_states - 1] = 1
                    R[s,a] = r_wumpus

        ## The terminal state
        for a in range(n_actions):
            P[n_states - 1, a, :] = 0
            P[n_states - 1, a, n_states - 1] = 1
            R[n_states - 1, a] = 0

        super().__init__(n_states, n_actions, P, R)
        self.terminal_state = n_states - 1
        

    def local_transitions(self, P, R, x, y, randomness):
        s = self.get_state(x, y, self.wumpus_x, self.wumpus_y)

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

        # Make the wumpus move directly towards you
        w_x = self.wumpus_x
        w_y = self.wumpus_y
        d_x = np.abs(x - w_x)
        d_y = np.abs(y - w_y)
        if (d_x > d_y):
            w_x += np.sign(x - w_x)
        else:
            w_y += np.sign(y - w_y)

        # The wumpus cannot go through walls, but it can go over holes
        if (self.maze[w_x, w_y] == self.WALL):
            w_x = self.wumpus_x
            w_y = self.wumpus_y

        # These are the resulting states from your movements
        # if there is no randomness
        sr = self.get_state(xr, yr, w_x, w_y)
        sl = self.get_state(xl, yl, w_x, w_y)
        su = self.get_state(xu, yu, w_x, w_y)
        sd = self.get_state(xd, yd, w_x, w_y)

        # you go to these states with probability 1 - p
        P[s, self.RIGHT, sr] = 1 - randomness
        P[s, self.LEFT, sl] = 1 - randomness
        P[s, self.UP, su] = 1 - randomness
        P[s, self.DOWN, sd] = 1 - randomness

        # otherwise you go to one of the neighbouring states
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
                elif self.maze[x,y]==self.WUMPUS:
                    print("%", end="")
                else:
                    print("!", end="")
            print("")
            

# test

def main():
    print("Testing")
    height = 4
    width = 4
    environment = GridWorld(width, height, 0.2, 0)
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
