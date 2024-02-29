# Exercise 2.4
# https://artint.info/3e/html/ArtInt3e.Ch2.S7.html
from matplotlib import pyplot as plt

from ai_python.agentEnv import Rob_env, Rob_body, line_segments_intersect
from ai_python.agentMiddle import Rob_middle_layer
from ai_python.agentTop import Rob_top_layer, Plot_env
from ai_python.agents import Environment
import math

class Rob_middle_layer_ex4(Environment):
    def __init__(self,env):
        self.env=env
        self.percept = env.initial_percept()
        self.straight_angle = 11 # angle that is close enough to straight ahead
        self.close_threshold = 2  # distance that is close enough to arrived
        self.close_threshold_squared = self.close_threshold**2 # just compute it once

        # Variables to keep updated our belief state
        self.left_turns = 0
        self.right_turns = 0
        # Useful to know whether we are currently following a wall or not.
        self.follows_right_wall = False


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

            if steer_dir == "left":
                self.left_turns += 1
            elif steer_dir == "right":
                self.right_turns += 1

            self.percept = self.env.do({"steer": steer_dir})
            remaining -= 1
            arrived = self.close_enough(target_pos)
        return {'arrived': arrived}

    def steer(self,target_pos):

        if self.percept['whisker']:
            self.display(3,'whisker on', self.percept)

            # We have a wall in front of us, follow it with the "right hand rule"
            self.follows_right_wall = True

            return "left"

        # Do we want to follow the right-hand wall ?
        if self.keep_following_right_wall():
            return self.follow_right_wall()
        else:
            # Stop following the right-hand wall
            self.follows_right_wall = False

        # We are not following the right wall.
        self.left_turns = 0
        self.right_turns = 0
        return self.head_towards(target_pos)

    def has_wall_on_right(self):
        """
        This function is not trivial to implement with how the robot is working, we only have a whisker detecting
        walls at the front left of the robot.

        We assume the robot can percept on the right side too.
        """
        has_wall_on_right = self.percept['right_whisker']
        return has_wall_on_right

    def follow_right_wall(self):
        """
        Once again, this is not really possible to implement with the default robot.
        But our goal is proposing a logic that could be used to solve the maze.

        An updated bottom layer (was not asked for the assignments) with a right whisker is implemented below.
        """
        if not self.has_wall_on_right():
            # It means that we have to go right to keep following the wall
            # We will go left if the main whisker is activated
            return "right"
        else:
            return "straight"

    def keep_following_right_wall(self):
        """
        Do we keep following the right wall ?
        Until the number of left turns equals the number of right turns
        """
        return (self.left_turns != self.right_turns) and self.follows_right_wall

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


class Rob_body_front_right_whiskers(Rob_body):
    """
    Modified robot so that we can have a front whisker and right whisker for the "right hand rule"
    """

    def __init__(self, env):
        super().__init__(env)
        self.whisker_angle = 18
        self.right_whisker_angle = 90

    def percept(self):
        perception = super().percept()
        perception["right_whisker"] = self.right_whisker()
        return perception
    initial_percept = percept  # use percept function for initial percept too

    def right_whisker(self):
        """returns true whenever the whisker sensor intersects with a wall
        """
        whisk_ang_world = (self.rob_dir-self.right_whisker_angle)*math.pi/180
            # angle in radians in world coordinates
        wx = self.rob_x + self.whisker_length * math.cos(whisk_ang_world)
        wy = self.rob_y + self.whisker_length * math.sin(whisk_ang_world)
        whisker_line = ((self.rob_x,self.rob_y),(wx,wy))
        hit = any(line_segments_intersect(whisker_line,wall)
                    for wall in self.env.walls)
        if hit:
            self.wall_history.append((self.rob_x, self.rob_y))
            if self.plotting:
                plt.plot([self.rob_x],[self.rob_y],"ro")
                plt.draw()
        return hit


locations = {
    'goal': (71, 0)
}

# Robot trap environment
walls = {
    ((10, -21), (10, 0)),
    ((10, 10), (10, 31)),
    ((30, -10), (30, 0)),
    ((30, 10), (30, 20)),
    ((50, -21), (50, 31)),
    ((10, -21), (50, -21)),
    ((10, 0), (30, 0)),
    ((10, 10), (30, 10)),
    ((10, 31), (50, 31))
}

env = Rob_env(walls)

# Controller setup
robot_body = Rob_body_front_right_whiskers(env)
robot_middle = Rob_middle_layer_ex4(robot_body)
robot_top = Rob_top_layer(robot_middle,
                    timeout=2000,
                    locations=locations
                    )
                    
pl = Plot_env(robot_body,
              robot_top
              )

if __name__ == '__main__':

    # Our objective is to reach the goal state.
    robot_top.do({'visit':['goal']})
