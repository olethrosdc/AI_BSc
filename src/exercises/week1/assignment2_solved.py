# Exercise 2.7
# https://artint.info/3e/html/ArtInt3e.Ch2.S7.html

from ai_python.agentEnv import Rob_env, Rob_body
from ai_python.agentMiddle import Rob_middle_layer
from ai_python.agentTop import Rob_top_layer, Plot_env
import math
import random

class Rob_top_layer_sensing(Rob_top_layer):
    """
    The top layer has only location names now
    """

    def do(self, plan):

        to_do = plan['visit']
        for loc in to_do:
            arrived = self.middle.do({'go_to': loc, 'timeout': self.timeout})
            self.display(1, "Arrived at", loc, arrived)

        last_loc = loc
        # The robot cannot stop, we make it reach the final location indefinitely
        # We could do this in a cleaner manner
        position = self.locations[last_loc]
        while True:
            self.middle.do({'go_to': position})


class Rob_middle_layer_sensing(Rob_middle_layer):

    def get_target_position(self, name):
        """
        If the name of our location was sensed, return its coordinates
        otherwise return None
        """
        return self.percept["locations"].get(name, None)


    def do(self, action):

        if 'timeout' in action:
            remaining = action['timeout']
        else:
            remaining = -1  # will never reach 0

        loc_name = action["go_to"]

        sensed_target_position = self.get_target_position(loc_name)

        arrived = self.close_enough(sensed_target_position)

        while not arrived and remaining != 0:
            sensed_target_position = self.get_target_position(loc_name)
            steer_dir = self.steer(sensed_target_position)

            self.percept = self.env.do({"steer": steer_dir})

            for name, position in self.percept["locations"].items():
                self.display(1, f"Location {name} sensed at {position}.")

            remaining -= 1
            arrived = self.close_enough(sensed_target_position)
        return {'arrived': arrived}

    def steer(self, target_pos):
        if self.percept['whisker']:
            self.display(3, 'whisker on', self.percept)
            return "left"
        elif target_pos is None:
            # We cannot sense the location coordinates, randomly explore (could be improved)
            return random.choice(["left", "right", "straight"])
        else:
            return self.head_towards(target_pos)

    def close_enough(self,target_pos):
        if target_pos is None:
            # We can't sense the location, we are too far away from it
            return False

        return super().close_enough(target_pos)


class Rob_body_sensing(Rob_body):

    def __init__(self, env, locations):
        super().__init__(env)

        self.locations = locations

        # We suppose we cannot know the coordinates of locations if we are not near them,
        # We need to sense them.
        self.sensing_radius = 30

    def can_sense(self, position):
        """
        We assume the body provides the position
        Emulates sensing
        """
        gx, gy = position
        return (gx - self.rob_x) ** 2 + (gy - self.rob_y) ** 2 <= self.sensing_radius ** 2


    def percept(self):
        perception = super().percept()
        perception["locations"] = {}
        for loc_name, position in self.locations.items():
            if self.can_sense(position):
               perception["locations"][loc_name] = position
        return perception
    initial_percept = percept


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
robot_body = Rob_body_sensing(env, locations=locations) # We assume the body can sense the locations
robot_middle = Rob_middle_layer_sensing(robot_body)
robot_top = Rob_top_layer_sensing(robot_middle,
                    timeout=500,
                    locations=locations # We suppose that the coordinates are hidden to the top layer, but we still use them
                                  # for plotting
                    )
                    
pl = Plot_env(robot_body,
              robot_top
              )

if __name__ == '__main__':
    random.seed(10)
    robot_top.do({'visit': ['o103', 'o109', 'storage', 'o103']})