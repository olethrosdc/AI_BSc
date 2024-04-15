from MDP import DiscreteMDP
## This defines the Chain environment
class GridWorld(MDP):
  class Cell(Enum):
    EMPTY = 0
    WALL = 1
    HOLE = 2
    GOAL = 3

  class Move(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

  def get_state(self, x, y):
    return x + y*self.width
  
  def __init__(self, randomness, width, height, holes):
    self.state = 0
    self.width = width
    self.height = height
    n_states = width * height + 1
    n_actions = 4
    self.maze = np.zeros([width, height])

    for x in range(width):
      for y in range(height):
        if (np.random.uniform()<.2):
          self.maze[x, y] = Cell.WALL
          
    hole_x = hole_y = 0
    while (hole_x == 0 and hole_y == 0):
      hole_x = np.random.choice(width)
      hole_y = np.random.choice(width)
    self.maze[hole_x, hole_y] = Cell.HOLE
    
    goal_x = goal_y = 0
    while (goal_x == 0 and goal_y == 0):
      goal_x = np.random.choice(width)
      goal_y = np.random.choice(width)
    self.maze[goal_x, goal_y] = Cell.GOAL


    P = np.zeros(n_states, n_actions, n_states)
    R = np.zeros(n_states, n_actions)

    ## The terminal state
    for a in range(n_actions):
      P[n_states-1, a, n_states-1] = 1
      R[n_states-1, a] = 0


    # the hole get you to the terminal state with -100
    s = get_state(hole_x, hole_y)
    for a in range(n_actions):
      P[s, a, n_states - 1] = 1
      R[s,a] = -100
      
    s = get_state(goal_x, goal_y)
    # the goal gets you to the terminal state with + 10
    s = get_state(hole_x, hole_y)
    for a in range(n_actions):
      P[s, a, n_states - 1] = 1
      R[s,a] = 10

    
    DiscreteMDP.__init__(n_states, n_actions, P, R)
    
  def step(self, action):
    assert self.action_space.contains(action)
    done = False
    reward = np.random.binomial(1, self.r_dist[self.state])



  def reset(self):
    self.state = 0
    self.x = 0
    self.y = 0
    return 0

  def render(self):
    pass


