from DecisionDiagram import DiscreteDeterministicDecisionDiagram
from enum import Enum
import numpy as np

## This defines the Chain environment
class GridWorld(DiscreteDeterministicDecisionDiagram):


    def get_state(self, x, y):
        return x + y*self.width
    
    def __init__(self, width, height):
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


        P = np.zeros([n_states, n_actions], dtype=int)
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

                P[s, self.UP] = su
                P[s, self.DOWN] = sd
                P[s, self.LEFT] = sl
                P[s, self.RIGHT] = sr


        ## The terminal state
        for a in range(n_actions):
            P[n_states - 1, a] =  n_states - 1
            R[n_states - 1, a] = 0

            
        # the hole gets you to the terminal state with r=-10
        s = self.get_state(hole_x, hole_y)
        for a in range(n_actions):
            P[s, a] = n_states - 1
            R[s,a] = -10
            

        # the goal gets you to the terminal state with r=+ 1
        s = self.get_state(goal_x, goal_y)
        for a in range(n_actions):
            P[s, a] =  n_states - 1
            R[s,a] = 1

        super().__init__(n_states, n_actions, P, R)
        

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

    from DynamicProgramming import dynamic_programming
    print("Calculating optimal policy")
    policy, V, Q = dynamic_programming(environment, 100)

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
