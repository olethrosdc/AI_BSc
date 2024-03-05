# Exercise 2.2
# https://artint.info/3e/html/ArtInt3e.Ch2.S7.html

from ai_python.agentEnv import Rob_env, Rob_body
from ai_python.agentMiddle import Rob_middle_layer
from ai_python.agentTop import Rob_top_layer, Plot_env
from ai_python.agents import Environment
import math


class Rob_middle_layer_ex3(Environment):
    def __init__(self,env):
        self.env=env
        self.percept = env.initial_percept()
        self.straight_angle = 11 # angle that is close enough to straight ahead
        self.close_threshold = 2  # distance that is close enough to arrived
        self.close_threshold_squared = self.close_threshold**2 # just compute it once

        # History of 10 last actions
        # Incremented each time we steer in the same direction in a row
        self.steer_count = 0
        self.previous_steer_dir = "straight"
        # How many times do we need to steer in the same direction in a row before doing a circle ?
        self.max_steer_count = 360 / self.env.turning_angle

    def initial_percept(self):
        return {}

    def do(self, action):

        if 'timeout' in action:
            remaining = action['timeout']
        else:
            remaining = -1    # will never reach 0
        target_pos = action['go_to']
        arrived = self.close_enough(target_pos)
        while not arrived and remaining != 0:

            steer_dir = self.steer(target_pos)
            if steer_dir in ("left", "right") and steer_dir == self.previous_steer_dir:
                self.steer_count += 1
                # Did we perform a full loop ? Are we facing a wall ?
                # Go straight once to deviate from the current trajectory, only if we are not facing a wall
                if self.steer_count >= self.max_steer_count and not self.percept["whisker"]:
                    steer_dir = "straight"
            else:
                self.steer_count = 0

            self.previous_steer_dir = steer_dir

            self.percept = self.env.do({"steer": steer_dir})
            remaining -= 1
            arrived = self.close_enough(target_pos)
        return {'arrived':arrived}

    def steer(self,target_pos):
        if self.percept['whisker']:
            self.display(3,'whisker on', self.percept)
            return "left"
        else:
            return self.head_towards(target_pos)

    def head_towards(self,target_pos):
            """ given a target position, return the action that heads towards that position
            """
            gx,gy = target_pos
            rx,ry = self.percept['rob_x_pos'],self.percept['rob_y_pos']
            goal_dir = math.acos((gx-rx)/math.sqrt((gx-rx)*(gx-rx)
                                                   +(gy-ry)*(gy-ry)))*180/math.pi
            if ry>gy:
                goal_dir = -goal_dir
            goal_from_rob = (goal_dir - self.percept['rob_dir']+540)%360-180
            assert -180 < goal_from_rob <= 180
            if goal_from_rob > self.straight_angle:
                return "left"
            elif goal_from_rob < -self.straight_angle:
                return "right"
            else:
                return "straight"

    def close_enough(self,target_pos):
        gx,gy = target_pos
        rx,ry = self.percept['rob_x_pos'],self.percept['rob_y_pos']
        return (gx-rx)**2 + (gy-ry)**2 <= self.close_threshold_squared
        

locations = {
    'G': (-5, 0),
    'G2': (70, 70)
}

walls = {
}

env = Rob_env(walls)



# Controller setup
robot_body = Rob_body(env)
robot_middle = Rob_middle_layer_ex3(robot_body)
robot_top = Rob_top_layer(robot_middle,
                    timeout=500,
                    locations=locations
                    )
                    
pl = Plot_env(robot_body,
              robot_top
              )

if __name__ == '__main__':

    # The top layer allows you to make the robot visit points
    robot_top.do({'visit': ['G', 'G2']})
