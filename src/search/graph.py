# A Graph (or Network) is composed of 
# Nodes (or Vertices)
# Edges (or Arcs) connecting the nodes
# every edge e is a pair (i,j).
# If the graph is undirected, then edges can be traverse in either way.
class Graph:
    def __init__(self, n_nodes = 1):
        self.n_nodes = n_nodes # the nodes are not explicitly stored in the network, we assume they are the integers {0,1,.., n-1}.
        self.edges = set() # the edges are simple tuples of integers
        self.directed = True
    # This function returns the children of any node.
    # The implementation is very lazy
    def children(self, node):
        children = set()
        for edge in self.edges:
            #print(edge[0], edge[1])
            if (edge[0]==node):
                children.add(edge[1])
        return children
    # add the edge (src, dst) to the graph
    
    def add_edge(self, src, dst):
        assert(src >= 0)
        assert(dst >= 0)
        if (src > self.n_nodes):
            self.n_nodes = src
        if (dst > self.n_nodes):
            self.n_nodes = dstph

        if (self.directed or src < dst):
            self.edges.add(tuple([src, dst]))
        else:
            self.edges.add(tuple([dst, src]))

        
    def size(self):
        return self.n_nodes
    
