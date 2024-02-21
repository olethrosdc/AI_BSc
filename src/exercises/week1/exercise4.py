# Exercise 2.4
# https://artint.info/3e/html/ArtInt3e.Ch2.S7.html



from ai_python.agentEnv import Rob_env, Rob_body
from ai_python.agentMiddle import Rob_middle_layer
from ai_python.agentTop import Rob_top_layer, Plot_env, setup_robot
from ai_python.agents import Environment


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

robot_body, robot_middle, robot_top = setup_robot(environment=env,
                                                  timeout=500,
                                                  locations=locations
                                                  )
pl = Plot_env(robot_body,
              robot_top
              )

if __name__ == '__main__':

    # Our objective is to reach the goal state.
    # TODO, update the middle layer.
    robot_top.do({'visit':['goal']})
