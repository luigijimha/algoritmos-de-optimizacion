"""
perform floyd warshall iteration to update matrix path
@param{Object} matrix    problem matrix
@param{Object} path      path matrix
@param{int} pivot        pivot index for the iteration
@return {Object}         updated problem matrix
"""
def updatePath(matrix, path, pivot):
    for i in range(len(matrix[0])):
        if i == pivot: continue
        for j in range(len(matrix)):
            if j == pivot: continue
            alt_path = matrix[i][pivot] + matrix[pivot][j]

            if alt_path < matrix[i][j]:
                matrix[i][j] = alt_path
                path[i][j] = pivot
    printPathMatrix(path)
    printCostMatrix(matrix)
    return matrix

"""
prints cost matrix in table format
@param {Object} matrix    cost matrix
"""
def printCostMatrix(matrix):
    global node_names
    
    print("cost matrix")
    # Print column names
    print("  ", end="")
    for col in range(len(matrix)):
        print(f" {node_names[col]:^3}", end="")
    print()
    # Print matrix
    for row in range(len(matrix)):
        print(f"{node_names[row]:<3}", end="")
        for col in range(len(matrix[row])):
            if matrix[row][col] == float('inf'):
                print("INF", end=" ")
            else:
                print(f"{matrix[row][col]:^3}", end=" ")
        print()
    print()

"""
prints path matrix in table format
@param {Object} matrix    path matrix
"""
def printPathMatrix(matrix):
    global node_names

    print("path matrix")
    # Print column names
    print("  ", end="")
    for col in range(len(matrix)):
        print(f" {node_names[col]:^3}", end="")
    print()
    # Print matrix
    for row in range(len(matrix)):
        print(f"{node_names[row]:<3}", end="")
        for col in range(len(matrix[row])):
            if matrix[row][col] == -1:
                print("   ", end=" ")
            else:
                print(f"{node_names[matrix[row][col]]:^3}", end=" ")
        print()
    print()

# dictionary used to translate matrix indexes to node names
node_names = {}

names_input = input("input node names: ").split(" ")
nodes = len(names_input)

# initialize matrix with n rows of n infinite values
FW_matrix = [[float('inf')] * nodes for _ in range(nodes)]
# initialize path with n rows of -1 values
path = [[-1] * nodes for _ in range(nodes)]

print("input node connections in order:")
for i in range(nodes):
    # update node name in list
    node_names[i] = names_input[i]
    # set self path to 0
    FW_matrix[i][i] = 0
    # read node connections
    conn_input = input()
    # in no input was received, node has no connections. skip
    if conn_input == "": continue

    conns = conn_input.split(", ")

    # update node connections cost value in matrix
    for conn in conns:
        node, cost = conn.split()
        FW_matrix[i][int(node)] = int(cost)
        path[i][int(node)] = i

printCostMatrix(FW_matrix)

for i in range(len(FW_matrix)):
    updatePath(FW_matrix, path, i)

printPathMatrix(path)

# sample input
"""
A B C D E
1 4, 2 8
0 4, 2 1, 3 2
0 8, 3 4, 4 2
1 2, 2 4, 4 7
2 2, 3 7

"""


"""
N1 N2 N3 N4 N5
1 7, 2 2
4 1
1 4, 3 2
1 1, 4 1


"""


"""
N1 N2 N3 N4
1 3, 3 7
0 8, 2 2
0 5, 3 1
0 2

"""

"""
A B C D E
1 9, 3 5
0 9, 2 5, 4 8
1 5, 3 5, 4 7
0 5, 2 5, 4 7
1 8, 2 7, 3 7

"""