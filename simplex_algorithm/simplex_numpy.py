import numpy as np
from fractions import Fraction

"""
perform one gauss jordan iteration over the matrix with the speficied pivot tuple
@param {Object} matrix    matrix where you want to perform gauss operation
@param {int} row          pivot row index
@param {int} column       pivot column index
"""
def gauss_iteration(matrix, row, column):
    m_inverse = 1 / matrix[row][column]
    matrix[row] *= m_inverse

    for i in range(len(matrix)):
        if i == row:
            continue
        a_inverse = -1 * matrix[i][column] / matrix[row][column]
        matrix[i] += a_inverse * matrix[row]

"""
print matrix in a table format
@param {Object} matrix       matrix you want to print
@param {int} variables       total variables the problem has (matrix effective columns)
@param {int} equations       total equations the problem has (matrix effective rows)
@param {Object} var_found    map to determine which variable has been with which equation
"""
def print_matrix(matrix, variables, equations, var_found):
    headers = [""] + ["var" + str(i+1) for i in range(variables)] + ["eq" + str(i+1) for i in range(equations)] + ["solution"]
    print(" ".join([f"{header:<8}" for header in headers]))

    for i in range(equations + 1):
        row_values = (["Z"] if i == 0 else ["var" + str(var_found[i])] if var_found[i] != 0 else ["eq" + str(i)]) + [str(Fraction(value).limit_denominator()) for value in matrix[i]]
        print(" ".join([f"{value:<8}" for value in row_values]))

    print()

""" --------------------------------------------------------------------------------- """
""" -------------------------- input and matrix generation -------------------------- """
""" --------------------------------------------------------------------------------- """

# input values
variables: int = int(input("insert number of variables: "))
equations: int = int(input("insert number of equations: "))
z_list = list(map(Fraction, input("insert z coefficients: ").split()))
print("insert your equations row by row:")
A_list = []
for i in range(equations):
    A_list.append(list(map(Fraction, input().split())))
B_list = list(map(Fraction, input("insert matrix solutions in one row: ").split()))
print("", end="\n\n")

# create numpy arrays
z = np.array( z_list )
A = np.array( A_list )
B = np.array( B_list )

# create simplex matrix
vector1 = np.vstack((-z, A))
vector2 = np.vstack((np.zeros((1, len(A))), np.eye(len(A))))
vector3 = B.reshape(-1, 1)
simplex_matrix = np.hstack((np.hstack((vector1, vector2)), vector3))

""" --------------------------------------------------------------------------------- """
""" ------------------------------- simplex algorithm ------------------------------- """
""" --------------------------------------------------------------------------------- """

# var found is used to track which rows have been elected as pibot and which variable was used
var_found = {key: 0 for key in range(1, equations + 1)}

print_matrix(simplex_matrix, variables, equations, var_found)

# initialize pibot row and column
pivot_column = np.argmin(simplex_matrix[0])
pivot_row = 0

while simplex_matrix[0][pivot_column] < 0:
    # find pivot row
    min_ratios_list = []
    for i in range(1, np.shape(simplex_matrix)[0]):
        if simplex_matrix[i][pivot_column] == 0 or simplex_matrix[i][-1] / simplex_matrix[i][pivot_column] < 0:
            min_ratios_list.append(float('inf'))
        else:
            min_ratios_list.append(simplex_matrix[i][-1] / simplex_matrix[i][pivot_column])
    
    min_ratios = np.array(min_ratios_list)

    pivot_row = np.argmin(min_ratios) + 1

    # map variable with equation
    var_found[pivot_row] = pivot_column

    # perform gauss iteration
    gauss_iteration(simplex_matrix, pivot_row, pivot_column)
    print_matrix(simplex_matrix, variables, equations, var_found)

    # update pivot column
    pivot_column = np.argmin(simplex_matrix[0])

"""
3
3
3 2 5
1 2 1
3 0 2
1 4 0
0 430 460 420
"""