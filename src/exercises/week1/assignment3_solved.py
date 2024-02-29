# Exercise 2.8
# https://artint.info/3e/html/ArtInt3e.Ch2.S7.html
from matplotlib import pyplot as plt

from ai_python.agentEnv import Rob_env, Rob_body
from ai_python.agentMiddle import Rob_middle_layer
from ai_python.agentTop import Rob_top_layer, Plot_env
import math
import random
from exercise2_solved import Rob_top_layer_ex2


class Rob_top_layer_battery(Rob_top_layer_ex2):

    def __init__(self, middle, timeout, locations, wall_socket_location):
        locations["wall_socket"] = wall_socket_location
        super().__init__(middle, timeout, locations)


    def do(self, plan):
        """
        We add the possibility to recharge
        """

        to_do = plan['visit']
        recharge = False
        for loc in to_do:
            position = self.locations[loc]
            timeout = self.timeout
            arrived = False
            while not arrived and timeout > 0:
                info = self.middle.do({
                    # If we must recharge, then tell the middle layer to go to the wall socket
                    'go_to': self.locations["wall_socket"] if recharge
                             else position,
                    'timeout': timeout,
                    # We communicate to the middle layer that our goal is to recharge at the target location
                    'recharge': recharge}
                )
                recharge =  info["must_recharge"]
                timeout = info["timeout"]
                arrived = info["arrived"]



            self.display(1, "Arrived at", loc, arrived)

        # The robot cannot stop, we make it reach the charging stating indefinitely
        # We could do this in a cleaner manner
        while True:
            self.middle.do({'go_to': self.locations["wall_socket"], 'recharge':True})


class Rob_middle_layer_battery(Rob_middle_layer):

    def __init__(self, env):
        self.env = env
        self.percept = env.initial_percept()
        self.straight_angle = 11  # angle that is close enough to straight ahead
        self.close_threshold = 2  # distance that is close enough to arrived
        self.close_threshold_squared = self.close_threshold ** 2  # just compute it once

        self.recharge_threshold = 0.55 # We should ensure that the robot can always go back to the socket


    def initial_percept(self):
        return {}

    def low_battery(self):
        return self.percept["battery_level"] < self.recharge_threshold

    def must_recharge(self, top_action):
        return (
                    self.percept["battery_level"] < self.recharge_threshold
                or
                    # If we are currently recharging, keep recharging up to 100%
                    (top_action["recharge"] and self.percept["battery_level"] < 1 )
                )


    def do(self, action):

        if 'timeout' in action:
            remaining = action['timeout']
        else:
            remaining = -1  # will never reach 0

        arrived = False
        # Alert sent to the top layer if we need to recharge, this must stop the loop
        alert_must_recharge = False
        done_recharging = False
        go_to = action['go_to']

        while (
                not arrived
            and
                remaining != 0
            and
                # Stop the loop when we must send the recharge alert
                not alert_must_recharge
            and
                # Stop the loop when we are done recharging
                not done_recharging
        ):

            body_action = {
                "steer": self.steer(go_to),
                # If the top layer tells us to recharge, it means that the location is the wall socket and
                # we have to make a stop at it, send to the body that we must recharge if we are near the wall socket
                "recharge": action["recharge"] and self.close_enough(action["go_to"])
            }
            self.percept = self.env.do(body_action)

            must_recharge = self.must_recharge(action)
            if not action["recharge"]:
                # We are not done as long as we have not fully recharged
                arrived = self.close_enough(action['go_to'])
            elif not must_recharge:
                done_recharging = True

            # We need to alert the top layer if we are low on battery, and that we have not alerted the top layer
            # already
            alert_must_recharge = must_recharge and not action["recharge"]

            remaining -= 1


        return {'arrived': arrived, "timeout": remaining, "must_recharge": alert_must_recharge}



class Rob_body_battery(Rob_body):

    def __init__(self, env):
        super().__init__(env)

        self.battery_state = 300
        self.battery_state_max = 300


    def percept(self):
        perception = super().percept()
        perception["battery_level"] = self.battery_state / self.battery_state_max
        return perception

    initial_percept = percept

    def do(self, action):
        if action["recharge"]:
            self.battery_state = min([self.battery_state+10, self.battery_state_max])
            self.display(1, f"Charging... Battery level at {100*self.battery_state / self.battery_state_max:.0f}%")
            plt.pause(self.sleep_time)
            return self.percept()
        else:
            # Any other action costs energy
            self.battery_state = max([self.battery_state-1, 0])
            return super().do(action)


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
robot_body = Rob_body_battery(env)
robot_middle = Rob_middle_layer_battery(robot_body)
robot_top = Rob_top_layer_battery(robot_middle,
                    timeout=500,
                    locations=locations,
                    wall_socket_location=(0, 0)
                    )
                    
pl = Plot_env(robot_body,
              robot_top
              )

if __name__ == '__main__':

    robot_top.do({'visit': ['o103', 'storage', 'o109', 'o103']})