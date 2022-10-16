import numpy as np

# each list is a node of a graph with travel cost equal to its length
class Node():
    def __init__(self, value):
        self.value = value 
        self.cost = len(value)
        #self.visited = 0

# the representation of the problem is a fully connected graph
class Graph():
    def __init__(self) -> None:
        self.nodes = []
        self.adjacency_list = {}

    def list_to_graph(self, nodes): # creates a fully connected graph
        self.nodes = [Node(x) for x in nodes]
        nodes_index = np.array(range(len(nodes)))
        for i in nodes_index:
            self.adjacency_list[i] = np.delete(nodes_index, i)
        return self

    

