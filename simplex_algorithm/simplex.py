from fractions import Fraction

"""
perform one gauss jordan iteration over the matrix with the speficied pivot tuple
@param {Object} matrix    matrix where you want to perform gauss operation
@param {int} row          pivot row index
@param {int} column       pivot column index
"""
def gauss_iteration(matrix, row, column):
    # apply multiplier inverse to pivot row
    m_inverse = 1 / matrix[row][column]
    for j in range(len(matrix[row])):
        matrix[row][j] *= m_inverse

    # apply additive inverse to non pivot rows
    for i in range(len(matrix)):
        if i == row:
            continue
        a_inverse = -1 * matrix[i][column] / matrix[row][column]
        for j in range(len(matrix[i])):
            matrix[i][j] += a_inverse * matrix[row][j]
    
"""
print matrix in a table format
@param {Object} matrix       matrix you want to print
@param {int} variables       total variables the problem has (matrix effective columns)
@param {int} equations       total equations the problem has (matrix effective rows)
@param {Object} var_found    map to determine which variable has been with which equation
"""
def print_matrix(matrix, variables, equations, var_found):
    # print table headers
    headers = ["", "Z"] + ["var" + str(i+1) for i in range(variables)] + ["eq" + str(i+1) for i in range(equations)] + ["solution"]
    print(" ".join([f"{header:<8}" for header in headers]))

    # print table content
    for i in range(equations + 1):
        row_values = (["Z"] if i == 0 else ["var" + str(var_found[i])] if var_found[i] != 0 else ["eq" + str(i)]) + [str(Fraction(value).limit_denominator()) for value in matrix[i]]
        print(" ".join([f"{value:<8}" for value in row_values]))

    # add endl at the end
    print()

"""
find the pivot column of matrix
@param {Object} matrix    problem matrix
@param {int} variables    total variables the problem has (matrix effective columns)
"""
def find_pivot_column(matrix, variables):
    min_ratio = float('inf')
    column = 0
    for i in range(1, variables + 1):
        # pivot must be negative
        if matrix[0][i] >= 0:
            continue
        # new pivot column found
        if matrix[0][i] < min_ratio:
            column = i
            min_ratio = matrix[0][i]
    return column

"""
find the pivot row of matrix
@param {Object} matrix    problem matrix
@param {int} column       pivot column index
@param {int} equations    total equations the problem has (matrix effective row columns)
"""
def find_pivot_row(matrix, column, equations):
    min_ratio = float('inf')
    for j in range(1, equations + 1):
        # pivot cannot be infinite
        if matrix[j][column] == 0:
            continue
        ratio = matrix[j][variables + equations + 1] / matrix[j][column]
        # pivot must be minimum positive value
        if ratio > 0 and ratio < min_ratio:
            min_ratio = ratio
            row = j
    return row

"""
solve maxZ problem using simplex algorithm
@param {int} variables    total variables problem has
@param {int} equations    total equations problem has
"""
def simplex(variables, equations):
    matrix = []
    
    # initialize map to relate equation with variable
    var_found = {key: 0 for key in range(1, equations + 1)}
    
    # initialize matrix Z row with 0s
    for i in range(equations + 1):
        matrix.append([0] * (variables + equations + 2))

    # get matrix values
    print("input matrix values:")
    for i in range(equations + 1):
        row_values = list(map(Fraction, input().split()))
        matrix[i][:len(row_values)] = row_values
    
    print()

    # start simplex iterations
    for i in range(variables):
        column = find_pivot_column(matrix, variables)

        # no pivot column found, simplex ended
        if column == 0:
            break

        # find pivot row
        row = find_pivot_row(matrix, column, equations)
                    
        var_found[row] = column
        gauss_iteration(matrix, row, column)
        print_matrix(matrix, variables, equations, var_found)




variables = int(input("Enter the number of variables: "))
equations = int(input("Enter the number of equations: "))

simplex(variables, equations)

# sample inputs
"""
2
4
1 -5 -4 0 0 0 0 0
0  6  4 1 0 0 0 24
0  1  2 0 1 0 0 6
0 -1  1 0 0 1 0 1
0  0  1 0 0 0 1 2


3
3
1 -3 -2 -5 0 0 0 0
0  1  2  1 1 0 0 430
0  3  0  2 0 1 0 460
0  1  4  0 0 0 1 420
"""