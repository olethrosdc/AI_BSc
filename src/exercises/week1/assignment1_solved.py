# Exercise 2.2
# https://artint.info/3e/html/ArtInt3e.Ch2.S7.html
import random

from matplotlib import pyplot as plt

from ai_python.agentEnv import Rob_env, Rob_body
from ai_python.agentMiddle import Rob_middle_layer
from ai_python.agentTop import Rob_top_layer, Plot_env
from ai_python.agents import Environment
import math

from ai_python.display import Displayable
from exercise2_solved import Rob_top_layer_ex2

class Rob_middle_layer_moving_targets(Rob_middle_layer):

    def do(self, action):
        """
        We update the do function to only apply one step, not all of them, before returning
        We move the loop in the top layer, and report the next timeout
        """

        if 'timeout' in action:
            remaining = action['timeout']
        else:
            remaining = -1    # will never reach 0

        steer_dir = self.steer(action['go_to'])
        self.percept = self.env.do({"steer": steer_dir})

        remaining -= 1

        arrived = self.close_enough(action['go_to'])

        return {'arrived': arrived,
                'timeout': remaining}


def move_locations(loc_dict):
    for loc_name, (x, y) in loc_dict.items():
        loc_dict[loc_name] = x + 5*(random.random() - 0.5), y + 5*(random.random() -0.5)
        plt.text(x + 1.0, y + 0.5, loc_name)  # print the label above and to the right


class Rob_top_layer_moving_targets(Rob_top_layer_ex2):

    def __init__(self, middle, timeout, locations):

        # For plotting
        self.locations_history = []
        super().__init__(middle, timeout, locations)

    def do(self, plan):
        """
        We take care of the timeout/arrived loop here rather than in the middle layer, this allows us to communicate
        the updated locations each time.
        """

        to_do = plan['visit']
        for loc in to_do:
            timeout = self.timeout
            arrived = False
            while timeout > 0 and not arrived:
                # Steps only once the robot in the environment
                info = self.middle.do({'go_to': self.locations[loc], 'timeout': timeout})
                # Emulate moving targets:
                # Note that it does not show on the visualization
                self.locations_history.append(self.locations.copy())
                move_locations(self.locations)

                # Actualise the position of the targets in the renderer
                self.redraw()

                timeout = info["timeout"]
                arrived = info["arrived"]

            self.display(1, "Arrived at", loc, arrived)

        last_loc = loc
        # The robot cannot stop, we make it reach the final location indefinitely
        position = self.locations[last_loc]
        while True:
            arrived = self.middle.do({'go_to': position})




locations = {
    'mail': (-5, 10),
    'o103': (50, 10),
    'o109': (100, 10),
    'storage': (101, 51)
}

walls = {
    ((20, 0), (30, 20)),
    ((70, -5), (70, 25))
}

env = Rob_env(walls)



# Controller setup
robot_body = Rob_body(env)
robot_body.plotting = True
robot_middle = Rob_middle_layer_moving_targets(robot_body)
robot_top = Rob_top_layer_moving_targets(robot_middle,
                    timeout=500,
                    locations=locations
                    )

class Plot_env_moving_targets(Plot_env):

    def __init__(self, robot_body, robot_top):
        super().__init__(robot_body, robot_top)
        robot_top.redraw = self.redraw

    def redraw(self):
        plt.clf()
        for wall in self.body.env.walls:
            ((x0,y0),(x1,y1)) = wall
            plt.plot([x0,x1],[y0,y1],"-k",linewidth=3)
        for loc in self.top.locations:
            (x,y) = self.top.locations[loc]
            plt.plot([x],[y],"k<")
            plt.text(x+1.0,y+0.5,loc) # print the label above and to the right
        plt.plot([self.body.rob_x],[self.body.rob_y],"go")
        plt.gca().figure.canvas.draw()
        if self.body.history or self.body.wall_history:
            self.plot_run()

    def plot_run(self):
        """plots the history after the agent has finished.
        This is typically only used if body.plotting==False
        """
        if self.body.history:
            xs,ys = zip(*self.body.history)
            plt.plot(xs,ys,"go")
        if self.body.wall_history:
            wxs,wys = zip(*self.body.wall_history)
            plt.plot(wxs,wys,"ro")
                    
pl = Plot_env_moving_targets(robot_body,
              robot_top
              )

if __name__ == '__main__':

    robot_top.do({'visit': ['mail', 'o103', 'storage', 'o103']})
