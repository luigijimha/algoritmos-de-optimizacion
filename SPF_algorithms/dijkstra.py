import heapq

"""
dijkstra algorithm to find shortest path to read a node
@param {char} start      start node
@param {char} end        end node
@param {Object} graph    map that graph each node with its connections and costs
@return {Object}         list of nodes you need to jump over to reach end node
"""
def dijkstra(start, end, graph):
    # used to create the path to get to every node
    path = {}
    # stores shortest distance to reach each node from start node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    # priority queue to find smallest path
    queue = [(0, start)]
    # shortest path to reach end node from start node
    response = []

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor_distance, neighbor_node in graph[current_node]:
            # Calculate the new distance to the neighbor node
            new_distance = current_distance + neighbor_distance

            # Update the distances of the neighbors if a shorter path is found
            if new_distance < distances[neighbor_node]:
                distances[neighbor_node] = new_distance
                # Add the neighbor to the priority queue if it's not visited yet
                heapq.heappush(queue, (new_distance, neighbor_node))
                # Update the path
                path[neighbor_node] = current_node

    # Build response using path
    if end not in path:
        return []
    current_node = end
    while current_node != start:
        response.insert(0, current_node)
        current_node = path[current_node]
    response.insert(0, start)

    return response

graph = {}

total_nodes = int(input("How many nodes has your graph: "))
for i in range(total_nodes):
    node = input("node: ")
    graph[node] = []
    nodes = input("cost and neighbors: ")
    nodes = nodes.split(", ")
    for tuple in nodes:
        cost, neighbor = tuple.split(" ")
        graph[node].append((int(cost), neighbor))

initial_node = input("Initial node: ")
final_node = input("Final node: ")

print()

route = dijkstra(initial_node, final_node, graph)

if not route:
    print('No path was found')
else:
    print('Route found:')
    print(' -> '.join(route))

"""
sample input:
10
Z
1 I
F
5 Z
C
7 Z
D
6 F, 1 E
G
3 Z
A
5 D, 2 B
B
3 C, 2 E
I
1 Z
E
2 G, 5 H
H
4 I
A
Z

"""