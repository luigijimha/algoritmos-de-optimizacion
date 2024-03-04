import numpy as np

vector1 = [
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6]
]

# create an identity matrix of 3x3
vector2 = np.eye(6)

print("eye:")
print(vector2, end="\n\n")

# shape helps you determine the dimentions of a matrix
print("shape:")
shape = np.shape(vector1)
print(shape, end="\n\n")
print("rows: " + str (shape[0]))
print("columns: " + str (shape[1]))

# reshape redo a vector into a specified shape
# you need to input a np array to use it.
vector3 = np.array(
    [4, 430, 420]
)
print("reshape:")
print(vector3.reshape(-1, 1), end="\n\n")

# zeros genrates an array full of zeroes with specified size
vector4 = np.zeros((3, 4))
print("zeros:")
print(vector4, end="\n\n")

# returns the position to the smallest number in array
print("argmin:")
print(np.argmin(vector3), end="\n\n")

# stack binds rows and columns of two matrix of n size, this function has its vertical and horizontal versions.
# stack works just like its name says, it stacks matrix a over matrix b
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print("hstack:")
print(np.hstack((a, b)), end="\n\n")
print(np.vstack((a, b)), end="\n\n")
a = np.array([[1], [2], [3]])
b = np.array([[4], [5], [6]])
print("vstack:")
print(np.hstack((a, b)), end="\n\n")
print(np.vstack((a, b)), end="\n\n")