from graph import Graph
searched = set()

## This function greedily searches for a path to the goal.  For a
## fixed-depth search it does not make a huge difference if we use DFS
## or not, as the complexity is the same. Indeed, it might be easier
## to expand the search frontier using DFS.
def GoalDFS(graph, current, goals):
    searched.add(current)
    if (current in goals):
        return True
    found = False
    #print (current, graph.children(current))
    for c in graph.children(current):
        if (not (c in searched)):
            if (GoalDFS(graph, c, goals)):
                found = True
    return found

## Now we wan to try the shortest path version of 
def ShortestPathDFS(graph, current, goals):
    searched.add(current)
    if (current in goals):
        print ("Goal found: ", current)
        return True
    found = False
    #print (current, graph.children(current))
    for c in graph.children(current):
        if (not (c in searched)):
            if (GoalDFS(graph, c, goals)):
                print (current, "->", c)
                found = True
    return found


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

GoalDFS(graph, 0, set([3]))

