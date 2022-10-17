from graph import Graph, Node
from problem import problem, greedy
from solution import a_star

N = 5

nodes = problem(N, seed=42)
# nodes = [[0], [1], [0], [4], [0], [1], [4], [4], [4], [1, 3], [0, 1], [2], [1], [0], [0, 2], [2, 4], [3], [3], [4], [2, 4], [0], [1], [0, 1], [3], [2, 3]]
# nodes = [[0], [0,2], [1,2,3,4], [1], [2], [4], [3], [1]]

graph = Graph().list_to_graph(nodes)

w = a_star(graph, 0, N)

