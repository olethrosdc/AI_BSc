## Depth-First Search

from graph import Graph
import numpy as np


## This function greedily searches for a path to the goal.  It always
## expands the deepest node first.  DFS is very sensitive to how we
## add expanded nodes' children to the frontier.
## We need the searched variable to avoid loops.
## Inputs:
## - graph: The graph structure
## - current: node to search
## - goals: set of goal nodes
## Returns:
## - found: True if a goal was found
## - path: a path to the goal
class DepthFirstSearch:
    def __init__ (self, graph):
        self.graph = graph
    def GoalSearch(self, start_node, goals):
        self.goals = goals
        self.searched = set()
        return self.GoalDFS(start_node)
    def GoalDFS(self, current):
        self.searched.add(current)
        if (current in self.goals):
            return True, [current]
        print (current, self.graph.children(current))
        for c in self.graph.children(current):
            if (not (c in self.searched)):
                found, path = self.GoalDFS(c)
                if (found):
                    path.insert(0, current)
                    return found, path
        return false, []
    def ShortestPathSearch(self, start_node, goals):
        self.goals = goals
        self.searched = set()
        self.shortest = graph.size() + 1
        self.distances = np.zeros(graph.size()) + np.infty
        for i in self.goals:
            self.distances[i] = 0
        return self.ShortestPathDFS(start_node, 0)
    
    def ShortestPathDFS(self, current, path_length):
        self.searched.add(current)
        found = False
        best_path = []
        path_length += 1
        if (current in self.goals):
            return True, [current], path_length
        print (current, self.graph.children(current))
        for c in self.graph.children(current):
            if (not (c in self.searched)):
                was_found, path, length = self.ShortestPathDFS(c, path_length)
                if (was_found and length <= self.shortest):
                    self.shortest = length
                    found = True
                    best_path = path
            else:
                if (c in self.searched)
        if (found):
            best_path.insert(0, current)
        return found, best_path, self.shortest


# test graph
# This graph has a short-cut to node 3 (the goal)
# Node 4 is a dead-end.
#  ->4
# /
#0->1->2->3 
#    \->-/
graph = Graph(5)
graph.add_edge(0,1)
graph.add_edge(1,2)
graph.add_edge(1,3)
graph.add_edge(2,3)
graph.add_edge(0,4)

# When calling the simple GoalDFS, we get just one valid path to the goal, but not the shortest path

search = DepthFirstSearch(graph)
found, path = search.GoalSearch(0, set([3]))
print(found, path)

found, path, length = search.ShortestPathSearch(0, set([3]))
print(found, path, length)
