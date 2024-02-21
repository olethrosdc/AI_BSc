# Exercise 2.2
# https://artint.info/3e/html/ArtInt3e.Ch2.S7.html

from ai_python.agentEnv import Rob_env, Rob_body
from ai_python.agentMiddle import Rob_middle_layer
from ai_python.agentTop import Rob_top_layer, Plot_env, setup_robot
from ai_python.agents import Environment


# TODO (1): try changing target locations and adding obtacles.
# TODO (2): update Rob_middle_layer in ai_python/agentMiddle to make the robot always reach its destination

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


robot_body, robot_middle, robot_top = setup_robot(environment=env,
                                                  timeout=200,
                                                  locations=locations
                                                  )
pl = Plot_env(robot_body,
              robot_top
              )

if __name__ == '__main__':

    # The top layer allows you to make the robot visit points
    robot_top.do({'visit': ['o109', 'storage', 'o109', 'o103']})
