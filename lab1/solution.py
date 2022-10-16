import numpy as np

# modified A* search algorithm

def a_star(graph, start_node, N): 

    def h(i, goal):
        node = graph.nodes[i]
        h = 0        
        for x in node.value:
            if x in goal:
                h -= 1
            else:
                h += 1
        return h

    def current_goal(goal, n):
        reconst_path = []

        while parents[n] != n:
            reconst_path += graph.nodes[n].value
            n = parents[n]

        reconst_path = reconst_path + graph.nodes[start_node].value
        new_goal = set([x for x in goal if x not in reconst_path])

        return new_goal

    goal = set(range(N))

    # open_list is a list of nodes which have been visited, but who's neighbors
    # haven't all been inspected, starts off with the start node
    # closed_list is a list of nodes which have been visited
    # and who's neighbors have been inspected
    open_list = set([start_node])
    closed_list = set([])

    # g contains current distances from start_node to all other nodes
    # the default value (if it's not found in the map) is +infinity
    g = {}

    g[start_node] = graph.nodes[start_node].cost

    # parents contains an adjacency map of all nodes
    parents = {}
    parents[start_node] = start_node

    n = None

    while len(open_list) > 0:
        if n == None:
            new_goal = goal
        else:
            new_goal = current_goal(goal, n)
        # find a node with the lowest value of f() - evaluation function
        for v in open_list:
            if n == None or g[v] + h(v, new_goal) < g[n] + h(n, new_goal):
                n = v

        if n == None:
            print('Path does not exist!')
            return None


        # if the current node is the stop_node
        # then we begin reconstructin the path from it to the start_node

        if len(current_goal(goal, n)) == 0:
            reconst_path = []
            w = 0

            while parents[n] != n:
                reconst_path.append(graph.nodes[n].value)
                w += graph.nodes[n].cost
                n = parents[n]

            reconst_path.append(graph.nodes[start_node].value)
            w += graph.nodes[start_node].cost

            reconst_path.reverse()

            print(f'Path found with A* search: \n{reconst_path} \n W = {w}')
            return w


        # for all neighbors of the current node do
        for m in graph.adjacency_list[n]:
            cost = graph.nodes[m].cost
            # if the current node isn't in both open_list and closed_list
            # add it to open_list and note n as it's parent
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n
                g[m] = g[n] + cost
            

            # otherwise, check if it's quicker to first visit n, then m
            # and if it is, update parent data and g data
            # and if the node was in the closed_list, move it to open_list
            else:
                if g[m] + h(m, new_goal) > g[n] + cost + h(n, new_goal):
                    g[m] = g[n] + cost
                    parents[m] = n
                    
                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)

        # remove n from the open_list, and add it to closed_list
        # because all of his neighbors were inspected
        open_list.remove(n)
        closed_list.add(n)
        
    print('Path does not exist!')
    return None