# Exercise 2.5
# https://artint.info/3e/html/ArtInt3e.Ch2.S7.html

from ai_python.agentEnv import Rob_env, Rob_body
from ai_python.agentMiddle import Rob_middle_layer
from ai_python.agentTop import Rob_top_layer, Plot_env
from ai_python.agents import Environment
import math


class Rob_top_layer_ex2(Environment):
    def __init__(self, middle, timeout, locations):
        """middle is the middle layer
        timeout is the number of steps the middle layer goes before giving up
        locations is a loc:pos dictionary
            where loc is a named location, and pos is an (x,y) position.
        """
        self.middle = middle
        self.timeout = timeout  # number of steps before the middle layer should give up
        self.locations = locations

    def do(self, plan):
        """carry out actions.
        actions is of the form {'visit':list_of_locations}
        It visits the locations in turn.
        """

        to_do = plan['visit']
        for loc in to_do:
            position = self.locations[loc]
            arrived = self.middle.do({'go_to': position, 'timeout': self.timeout})
            self.display(1, "Arrived at", loc, arrived)

        last_loc = loc
        # The robot cannot stop, we make it reach the final location indefinitely
        # We could do this in a cleaner manner
        position = self.locations[last_loc]
        while True:
            self.middle.do({'go_to': position})

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
robot_middle = Rob_middle_layer(robot_body)
robot_top = Rob_top_layer_ex2(robot_middle,
                    timeout=200,
                    locations=locations
                    )
                    
pl = Plot_env(robot_body,
              robot_top
              )

if __name__ == '__main__':

    # The top layer allows you to make the robot visit points
    robot_top.do({'visit': ['o109', 'storage', 'o109', 'o103']})