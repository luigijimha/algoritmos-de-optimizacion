from random import uniform
from sympy import symbols, sympify, diff, solve

"""
generates random coords inside problem area
@return     tuple with (x, y) coodinates
"""
def randomizeCoords():
    x = uniform(A, B)
    limit = MAX if FX.subs(X, x) >= 0 else MIN
    y = uniform(0, limit)
    return (x, y)

"""
determines if coordinates are below the curve
@param {Tuple} coords     coordinates to evaluate
@return                   returns 1 or -1 if coords are inside circle, else 0
"""
def targetHit(coords):
    x, y = coords
    ty = FX.subs(X, x)
    if ty >= 0:
        return 1 if y <= ty else 0
    else:
        return -1 if y >= ty else 0

def main():

    success = 0
    for _ in range(N):
        coords = randomizeCoords()
        success += targetHit(coords)

    print('integral: ', success/N * abs(FX.subs(X, B)) * (B-A))

# N sample
N = 5000

# A to B interval
A = -2
B = 3

# function
X = symbols('x')
FX = sympify('-x^2')
DFX = diff(FX, X)

# find local maximum and minimum
critical_points = solve(DFX, X)
extrema = [(point, FX.subs(X, point)) for point in critical_points + [A, B]]
MAX = max(point[1] for point in extrema)
MIN = min(point[1] for point in extrema)

main()